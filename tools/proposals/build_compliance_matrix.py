"""
Tool: Compliance Matrix Builder
Purpose: Map RFP requirements to capability responses and generate a compliance matrix

Takes parsed RFP requirements (from parse_rfp.py output) and capability/response
descriptions, then generates a compliance matrix showing compliant/partial/non-compliant
status per requirement.

Usage:
    python tools/proposals/build_compliance_matrix.py --requirements parsed_rfp.json --capabilities capabilities.json
    python tools/proposals/build_compliance_matrix.py --requirements parsed_rfp.json --capabilities capabilities.json --format markdown
    python tools/proposals/build_compliance_matrix.py --requirements parsed_rfp.json --output compliance_matrix.md --format markdown

Dependencies:
    - json (stdlib)
    - argparse (stdlib)

Output:
    JSON or Markdown compliance matrix with requirement-to-response mapping
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


COMPLIANCE_LEVELS = {
    "compliant": "Compliant",
    "partial": "Partial",
    "non-compliant": "Non-Compliant",
    "not-applicable": "N/A",
}


def build_matrix(requirements: list, capabilities: dict) -> dict:
    """
    Build a compliance matrix from requirements and capabilities.

    Args:
        requirements: List of requirement dicts with 'id', 'text', 'type', 'mandatory'
        capabilities: Dict mapping requirement IDs to response info:
            {
                "3.1.1": {
                    "compliance": "compliant|partial|non-compliant|not-applicable",
                    "response_section": "Section 3.1",
                    "evidence": "Description of how we meet this",
                    "notes": "Optional additional context"
                }
            }
            OR a list of general capabilities for auto-matching.

    Returns:
        Structured compliance matrix dict
    """
    matrix = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_requirements": len(requirements),
            "mapped": 0,
            "unmapped": 0,
            "compliant": 0,
            "partial": 0,
            "non_compliant": 0,
            "not_applicable": 0,
        },
        "entries": [],
        "unmapped_requirements": [],
        "summary": {},
    }

    for req in requirements:
        req_id = req.get("id", "unknown")
        req_text = req.get("text", "")
        req_type = req.get("type", "general")
        mandatory = req.get("mandatory", False)

        # Look for a capability mapping
        cap = capabilities.get(req_id) if isinstance(capabilities, dict) else None

        if cap:
            compliance = cap.get("compliance", "non-compliant").lower()
            entry = {
                "requirement_id": req_id,
                "requirement_text": req_text,
                "requirement_type": req_type,
                "mandatory": mandatory,
                "compliance": COMPLIANCE_LEVELS.get(compliance, compliance),
                "response_section": cap.get("response_section", ""),
                "evidence": cap.get("evidence", ""),
                "notes": cap.get("notes", ""),
            }
            matrix["entries"].append(entry)
            matrix["metadata"]["mapped"] += 1

            # Count by compliance level
            if compliance == "compliant":
                matrix["metadata"]["compliant"] += 1
            elif compliance == "partial":
                matrix["metadata"]["partial"] += 1
            elif compliance == "non-compliant":
                matrix["metadata"]["non_compliant"] += 1
            elif compliance == "not-applicable":
                matrix["metadata"]["not_applicable"] += 1
        else:
            # No mapping - add as unmapped
            entry = {
                "requirement_id": req_id,
                "requirement_text": req_text,
                "requirement_type": req_type,
                "mandatory": mandatory,
                "compliance": "UNMAPPED",
                "response_section": "",
                "evidence": "",
                "notes": "Requires response - no mapping provided",
            }
            matrix["entries"].append(entry)
            matrix["unmapped_requirements"].append(req_id)
            matrix["metadata"]["unmapped"] += 1

    # Summary by type
    type_counts = {}
    for entry in matrix["entries"]:
        rtype = entry["requirement_type"]
        if rtype not in type_counts:
            type_counts[rtype] = {"total": 0, "compliant": 0, "partial": 0, "non_compliant": 0, "unmapped": 0}
        type_counts[rtype]["total"] += 1
        if entry["compliance"] == "Compliant":
            type_counts[rtype]["compliant"] += 1
        elif entry["compliance"] == "Partial":
            type_counts[rtype]["partial"] += 1
        elif entry["compliance"] == "Non-Compliant":
            type_counts[rtype]["non_compliant"] += 1
        elif entry["compliance"] == "UNMAPPED":
            type_counts[rtype]["unmapped"] += 1
    matrix["summary"]["by_type"] = type_counts

    # Compliance percentage (excluding N/A and unmapped)
    scoreable = matrix["metadata"]["compliant"] + matrix["metadata"]["partial"] + matrix["metadata"]["non_compliant"]
    if scoreable > 0:
        matrix["summary"]["compliance_rate"] = round(
            (matrix["metadata"]["compliant"] + matrix["metadata"]["partial"] * 0.5) / scoreable * 100, 1
        )
    else:
        matrix["summary"]["compliance_rate"] = 0

    # Risk flag: mandatory requirements that are non-compliant or unmapped
    matrix["summary"]["critical_gaps"] = [
        e for e in matrix["entries"]
        if e["mandatory"] and e["compliance"] in ("Non-Compliant", "UNMAPPED")
    ]

    return matrix


def format_as_markdown(matrix: dict) -> str:
    """Convert compliance matrix to readable markdown."""
    lines = []
    meta = matrix["metadata"]
    summary = matrix.get("summary", {})

    lines.append("# Compliance Matrix")
    lines.append("")
    lines.append(f"**Generated:** {meta['generated_at']}")
    lines.append(f"**Total Requirements:** {meta['total_requirements']}")
    lines.append(f"**Compliance Rate:** {summary.get('compliance_rate', 0)}%")
    lines.append("")
    lines.append(f"| Status | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Compliant | {meta['compliant']} |")
    lines.append(f"| Partial | {meta['partial']} |")
    lines.append(f"| Non-Compliant | {meta['non_compliant']} |")
    lines.append(f"| N/A | {meta['not_applicable']} |")
    lines.append(f"| Unmapped | {meta['unmapped']} |")
    lines.append("")

    # Critical gaps
    critical = summary.get("critical_gaps", [])
    if critical:
        lines.append("## Critical Gaps (Mandatory + Non-Compliant/Unmapped)")
        lines.append("")
        for gap in critical:
            lines.append(f"- **{gap['requirement_id']}**: {gap['requirement_text'][:100]}")
        lines.append("")

    # Full matrix
    lines.append("## Full Matrix")
    lines.append("")
    lines.append("| Req # | Requirement | Type | Mandatory | Compliance | Response Section | Evidence |")
    lines.append("|-------|------------|------|-----------|------------|-----------------|----------|")
    for e in matrix["entries"]:
        mandatory = "Yes" if e["mandatory"] else "No"
        text = e["requirement_text"][:60] + ("..." if len(e["requirement_text"]) > 60 else "")
        evidence = e["evidence"][:50] + ("..." if len(e["evidence"]) > 50 else "")
        lines.append(
            f"| {e['requirement_id']} | {text} | {e['requirement_type']} | "
            f"{mandatory} | {e['compliance']} | {e['response_section']} | {evidence} |"
        )
    lines.append("")

    # Unmapped
    if matrix["unmapped_requirements"]:
        lines.append("## Unmapped Requirements (Need Response)")
        lines.append("")
        for req_id in matrix["unmapped_requirements"]:
            entry = next((e for e in matrix["entries"] if e["requirement_id"] == req_id), None)
            if entry:
                mandatory = " **(MANDATORY)**" if entry["mandatory"] else ""
                lines.append(f"- **{req_id}**: {entry['requirement_text'][:100]}{mandatory}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Build a compliance matrix from parsed RFP requirements and capability mappings"
    )
    parser.add_argument(
        "--requirements", "-r", required=True,
        help="Path to parsed RFP JSON (output of parse_rfp.py) or a JSON file with a 'requirements' list"
    )
    parser.add_argument(
        "--capabilities", "-c",
        help="Path to capabilities JSON mapping requirement IDs to responses"
    )
    parser.add_argument("--output", "-o", help="Path to write output (default: stdout)")
    parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown"],
        default="json",
        help="Output format (default: json)"
    )

    args = parser.parse_args()

    # Load requirements
    req_path = Path(args.requirements)
    if not req_path.exists():
        print(json.dumps({"success": False, "error": f"File not found: {args.requirements}"}))
        sys.exit(1)

    req_data = json.loads(req_path.read_text(encoding="utf-8"))

    # Handle parse_rfp.py output format (nested under "data")
    if "data" in req_data and "requirements" in req_data["data"]:
        requirements = req_data["data"]["requirements"]
    elif "requirements" in req_data:
        requirements = req_data["requirements"]
    else:
        print(json.dumps({"success": False, "error": "No 'requirements' found in input JSON"}))
        sys.exit(1)

    # Load capabilities (optional)
    capabilities = {}
    if args.capabilities:
        cap_path = Path(args.capabilities)
        if not cap_path.exists():
            print(json.dumps({"success": False, "error": f"File not found: {args.capabilities}"}))
            sys.exit(1)
        capabilities = json.loads(cap_path.read_text(encoding="utf-8"))

    # Build matrix
    matrix = build_matrix(requirements, capabilities)

    # Format output
    if args.format == "markdown":
        output = format_as_markdown(matrix)
    else:
        output = json.dumps({"success": True, "data": matrix}, indent=2)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(json.dumps({"success": True, "message": f"Written to {args.output}"}))
    else:
        print(output)


if __name__ == "__main__":
    main()
