#!/usr/bin/env python3
"""
Validate skill directories against the agentskills.io specification.

Usage:
    python validate-skill.py <skill-directory>
    python validate-skill.py --all [<skills-root>]

Checks:
    - SKILL.md exists
    - Frontmatter has required fields (name, description)
    - Name matches directory name
    - Name format (kebab-case, 1-64 chars, no leading/trailing hyphens)
    - Description length (1-1024 chars)
    - Body under 500 lines
    - Reference depth max 1 level
    - No Windows-style paths
    - No XML tags in name/description
    - allowed-tools uses space-delimited string (not YAML list)
"""

import sys
import re
from pathlib import Path


def _strip_code_fence(content: str) -> str:
    """Strip ```skill or ````skill code-fence wrapper if present."""
    lines = content.splitlines()
    if not lines:
        return content
    first = lines[0].strip()
    # Match ```skill, ````skill, ```Skill, etc.
    if re.match(r'^`{3,}\s*skill\b', first, re.IGNORECASE):
        lines = lines[1:]
        # Strip matching closing fence
        if lines and re.match(r'^`{3,}\s*$', lines[-1].strip()):
            lines = lines[:-1]
    return "\n".join(lines)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from SKILL.md content.

    Handles both plain --- fenced and ```skill wrapped formats.
    """
    content = _strip_code_fence(content)

    # Find the opening ---
    stripped = content.lstrip("\n")
    if not stripped.startswith("---"):
        return {}, content

    # Find the closing ---
    end = stripped.find("\n---", 3)
    if end == -1:
        return {}, content

    fm_text = stripped[3:end].strip()
    body = stripped[end + 4:].strip()

    # Simple YAML parsing (scalars, multi-line >, simple lists)
    fm = {}
    current_key = None
    current_value = []
    in_list = False

    for line in fm_text.split("\n"):
        line_stripped = line.strip()

        # List item continuation
        if in_list and line_stripped.startswith("- "):
            fm[current_key].append(line_stripped[2:].strip())
            continue
        elif in_list and line_stripped and not line_stripped.startswith("-"):
            in_list = False

        # Check for new key
        match = re.match(r'^(\w[\w-]*)\s*:\s*(.*)', line)
        if match:
            # Flush previous key
            if current_key and current_key not in fm:
                val = "\n".join(current_value).strip()
                # Clean multi-line > style
                if val.startswith(">"):
                    val = val[1:].strip()
                fm[current_key] = val
            elif current_key and isinstance(fm.get(current_key), str) and not fm[current_key]:
                val = "\n".join(current_value).strip()
                if val.startswith(">"):
                    val = val[1:].strip()
                fm[current_key] = val

            current_key = match.group(1)
            value = match.group(2).strip()

            if value == ">":
                current_value = []
                in_list = False
            elif value == "":
                # Might be a list or empty
                fm[current_key] = []
                current_value = []
                in_list = True
            elif value.lower() == "true":
                fm[current_key] = True
                current_value = []
                in_list = False
            elif value.lower() == "false":
                fm[current_key] = False
                current_value = []
                in_list = False
            elif value.startswith('"') and value.endswith('"'):
                fm[current_key] = value[1:-1]
                current_value = []
                in_list = False
            else:
                fm[current_key] = value
                current_value = []
                in_list = False
        elif current_key:
            current_value.append(line)

    # Flush last key
    if current_key and current_key not in fm:
        val = "\n".join(current_value).strip()
        if val.startswith(">"):
            val = val[1:].strip()
        fm[current_key] = val

    return fm, body


def validate_name(name: str) -> list[str]:
    """Validate skill name against spec rules."""
    errors = []

    if not name:
        errors.append("FAIL: name is empty")
        return errors

    if len(name) > 64:
        errors.append(f"FAIL: name exceeds 64 chars ({len(name)})")

    if name.startswith("-") or name.endswith("-"):
        errors.append("FAIL: name must not start or end with hyphen")

    if "--" in name:
        errors.append("FAIL: name must not contain consecutive hyphens")

    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', name) and len(name) > 1:
        errors.append("FAIL: name must be lowercase alphanumeric + hyphens only")

    reserved = ["anthropic", "claude"]
    for word in reserved:
        if word in name.lower():
            errors.append(f"FAIL: name contains reserved word '{word}'")

    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    """Validate a single skill directory. Returns list of issues."""
    issues = []
    dir_name = skill_dir.name

    # Check SKILL.md exists
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        issues.append(f"FAIL: {dir_name}/ — SKILL.md not found")
        return issues

    content = skill_file.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    # Required fields
    if "name" not in fm:
        issues.append(f"FAIL: {dir_name}/ — missing 'name' in frontmatter")
    else:
        name = fm["name"]
        # Name matches directory
        if name != dir_name:
            issues.append(f"FAIL: {dir_name}/ — name '{name}' doesn't match directory '{dir_name}'")
        # Name format
        issues.extend([f"  {dir_name}/: {e}" for e in validate_name(name)])

    if "description" not in fm:
        issues.append(f"FAIL: {dir_name}/ — missing 'description' in frontmatter")
    else:
        desc = str(fm["description"])
        if len(desc) > 1024:
            issues.append(f"FAIL: {dir_name}/ — description exceeds 1024 chars ({len(desc)})")
        if len(desc) == 0:
            issues.append(f"FAIL: {dir_name}/ — description is empty")
        if re.search(r'<\/?[a-zA-Z][a-zA-Z0-9]*[^>]*>', desc):
            issues.append(f"WARN: {dir_name}/ — description may contain XML tags")

    # Body length
    body_lines = body.split("\n")
    if len(body_lines) > 500:
        issues.append(f"FAIL: {dir_name}/ — body exceeds 500 lines ({len(body_lines)})")

    # Windows paths (skip code blocks and anti-pattern documentation lines)
    in_code_block = False
    for line in content.split("\n"):
        if line.strip().startswith("```") or line.strip().startswith("````"):
            in_code_block = not in_code_block
            continue
        if not in_code_block and "\\" in line:
            # Skip lines documenting anti-patterns
            if any(kw in line for kw in ["Windows path", "Don't", "don't"]):
                continue
            issues.append(f"WARN: {dir_name}/ — contains backslash outside code block: {line.strip()[:60]}")
            break

    # Reference depth check
    ref_dir = skill_dir / "reference"
    if ref_dir.exists():
        for item in ref_dir.rglob("*"):
            if item.is_dir():
                rel = item.relative_to(ref_dir)
                if len(rel.parts) > 1:
                    issues.append(f"FAIL: {dir_name}/ — nested reference directory: {rel}")

    # allowed-tools format check
    allowed_tools = fm.get("allowed-tools")
    if isinstance(allowed_tools, list):
        tools_str = ", ".join(str(t) for t in allowed_tools)
        issues.append(
            f"WARN: {dir_name}/ — allowed-tools uses YAML list format; "
            f"spec recommends space-delimited string. Current: [{tools_str}]"
        )

    return issues


def find_project_root() -> Path:
    """Walk up from script location to find CLAUDE.md."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return Path.cwd()


def main():
    if len(sys.argv) < 2:
        print("Usage: validate-skill.py <skill-dir>")
        print("       validate-skill.py --all [<skills-root>]")
        sys.exit(1)

    if sys.argv[1] == "--all":
        if len(sys.argv) > 2:
            root = Path(sys.argv[2])
        else:
            root = find_project_root() / ".claude" / "skills"

        if not root.is_dir():
            print(f"Error: skills directory not found: {root}")
            sys.exit(1)

        all_issues = []
        skill_count = 0

        for skill_dir in sorted(root.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_count += 1
                issues = validate_skill(skill_dir)
                all_issues.extend(issues)

        if all_issues:
            fails = [i for i in all_issues if "FAIL" in i]
            warns = [i for i in all_issues if "WARN" in i]
            print(f"\n{'='*60}")
            print(f"Validation: {skill_count} skills, {len(fails)} errors, {len(warns)} warnings")
            print(f"{'='*60}\n")
            for issue in all_issues:
                print(f"  {issue}")
            sys.exit(1 if fails else 0)
        else:
            print(f"\nAll {skill_count} skills pass validation.")
            sys.exit(0)
    else:
        skill_dir = Path(sys.argv[1])
        if not skill_dir.is_dir():
            print(f"Error: {skill_dir} is not a directory")
            sys.exit(1)

        issues = validate_skill(skill_dir)
        if issues:
            print(f"\nValidation issues for {skill_dir.name}/:")
            for issue in issues:
                print(f"  {issue}")
            sys.exit(1)
        else:
            print(f"{skill_dir.name}/ — PASS")
            sys.exit(0)


if __name__ == "__main__":
    main()
