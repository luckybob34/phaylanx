"""
Tool: Terraform Validator
Purpose: Run validation, linting, and security scanning on Terraform configurations

Orchestrates multiple validation tools against a Terraform directory:
format check, validate, tflint, and security scanning (tfsec/checkov).

Requires external tools to be installed for full functionality.
Falls back gracefully when tools are not available.

Usage:
    python tools/iac/validate_terraform.py --path ./infrastructure
    python tools/iac/validate_terraform.py --path ./infrastructure --checks format,validate,lint,security
    python tools/iac/validate_terraform.py --path ./infrastructure --checks validate --fix

Dependencies:
    - json (stdlib)
    - subprocess (stdlib)
    - External: terraform, tflint, tfsec or checkov (optional)

Output:
    JSON report with results per check, issues found, and recommendations
"""

import sys
import json
import argparse
import subprocess
import shutil
from datetime import datetime
from pathlib import Path


AVAILABLE_CHECKS = ["format", "validate", "lint", "security"]


def check_tool_available(tool_name: str) -> bool:
    """Check if an external tool is available on PATH."""
    return shutil.which(tool_name) is not None


def run_command(cmd: list, cwd: str = None) -> dict:
    """Run a command and capture output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=120,
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": "Command timed out (120s)", "success": False}
    except FileNotFoundError:
        return {"returncode": -1, "stdout": "", "stderr": f"Tool not found: {cmd[0]}", "success": False}


def check_format(path: str, fix: bool = False) -> dict:
    """Run terraform fmt check."""
    if not check_tool_available("terraform"):
        return {"check": "format", "status": "skipped", "reason": "terraform not found on PATH"}

    if fix:
        result = run_command(["terraform", "fmt", "-recursive"], cwd=path)
        return {
            "check": "format",
            "status": "fixed" if result["success"] else "error",
            "output": result["stdout"],
            "errors": result["stderr"] if not result["success"] else "",
        }
    else:
        result = run_command(["terraform", "fmt", "-check", "-recursive", "-diff"], cwd=path)
        return {
            "check": "format",
            "status": "pass" if result["success"] else "fail",
            "files_needing_format": result["stdout"].strip().split("\n") if result["stdout"].strip() else [],
            "errors": result["stderr"] if not result["success"] else "",
        }


def check_validate(path: str) -> dict:
    """Run terraform validate."""
    if not check_tool_available("terraform"):
        return {"check": "validate", "status": "skipped", "reason": "terraform not found on PATH"}

    # Init first (required for validate)
    init_result = run_command(["terraform", "init", "-backend=false"], cwd=path)
    if not init_result["success"]:
        return {
            "check": "validate",
            "status": "error",
            "errors": f"Init failed: {init_result['stderr']}",
        }

    result = run_command(["terraform", "validate", "-json"], cwd=path)
    try:
        validation = json.loads(result["stdout"])
    except (json.JSONDecodeError, TypeError):
        validation = {"valid": result["success"]}

    return {
        "check": "validate",
        "status": "pass" if validation.get("valid") else "fail",
        "diagnostics": validation.get("diagnostics", []),
        "error_count": validation.get("error_count", 0),
        "warning_count": validation.get("warning_count", 0),
    }


def check_lint(path: str) -> dict:
    """Run tflint."""
    if not check_tool_available("tflint"):
        return {"check": "lint", "status": "skipped", "reason": "tflint not found on PATH"}

    result = run_command(["tflint", "--recursive", "--format", "json"], cwd=path)
    try:
        lint_output = json.loads(result["stdout"])
    except (json.JSONDecodeError, TypeError):
        lint_output = {}

    issues = lint_output.get("issues", [])
    return {
        "check": "lint",
        "status": "pass" if not issues else "fail",
        "issues_count": len(issues),
        "issues": issues[:20],  # Cap at 20 for readability
    }


def check_security(path: str) -> dict:
    """Run tfsec or checkov for security scanning."""
    # Try tfsec first
    if check_tool_available("tfsec"):
        result = run_command(["tfsec", path, "--format", "json", "--soft-fail"], cwd=path)
        try:
            scan_output = json.loads(result["stdout"])
        except (json.JSONDecodeError, TypeError):
            scan_output = {}

        results_list = scan_output.get("results", [])
        return {
            "check": "security",
            "tool": "tfsec",
            "status": "pass" if not results_list else "warning",
            "findings_count": len(results_list) if isinstance(results_list, list) else 0,
            "findings": results_list[:20] if isinstance(results_list, list) else [],
        }

    # Fall back to checkov
    if check_tool_available("checkov"):
        result = run_command(["checkov", "-d", path, "--output", "json", "--soft-fail"], cwd=path)
        try:
            scan_output = json.loads(result["stdout"])
        except (json.JSONDecodeError, TypeError):
            scan_output = {}

        return {
            "check": "security",
            "tool": "checkov",
            "status": "pass" if result["success"] else "warning",
            "output": scan_output,
        }

    return {
        "check": "security",
        "status": "skipped",
        "reason": "Neither tfsec nor checkov found on PATH. Install one: `brew install tfsec` or `pip install checkov`",
    }


def run_checks(path: str, checks: list, fix: bool = False) -> dict:
    """Run selected validation checks."""
    report = {
        "metadata": {
            "path": path,
            "timestamp": datetime.now().isoformat(),
            "checks_requested": checks,
        },
        "results": [],
        "summary": {
            "total": len(checks),
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "warnings": 0,
        },
    }

    check_functions = {
        "format": lambda: check_format(path, fix=fix),
        "validate": lambda: check_validate(path),
        "lint": lambda: check_lint(path),
        "security": lambda: check_security(path),
    }

    for check in checks:
        if check in check_functions:
            result = check_functions[check]()
            report["results"].append(result)

            status = result.get("status", "unknown")
            if status == "pass":
                report["summary"]["passed"] += 1
            elif status == "fail":
                report["summary"]["failed"] += 1
            elif status == "skipped":
                report["summary"]["skipped"] += 1
            elif status in ("warning", "fixed"):
                report["summary"]["warnings"] += 1

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Validate, lint, and security-scan Terraform configurations"
    )
    parser.add_argument(
        "--path", "-p", required=True,
        help="Path to Terraform configuration directory"
    )
    parser.add_argument(
        "--checks", "-c",
        default="format,validate,lint,security",
        help="Comma-separated checks to run (default: all)"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix format issues (terraform fmt)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to write report (default: stdout)"
    )

    args = parser.parse_args()

    target_path = Path(args.path)
    if not target_path.exists():
        print(json.dumps({"success": False, "error": f"Path not found: {args.path}"}))
        sys.exit(1)

    checks = [c.strip() for c in args.checks.split(",") if c.strip() in AVAILABLE_CHECKS]

    report = run_checks(str(target_path), checks, fix=args.fix)

    output = json.dumps({"success": True, "data": report}, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(json.dumps({"success": True, "message": f"Report written to {args.output}"}))
    else:
        print(output)


if __name__ == "__main__":
    main()
