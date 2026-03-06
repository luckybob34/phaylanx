"""
Tool: RFP Parser
Purpose: Extract structured requirements, evaluation criteria, deadlines, and compliance items from an RFP document

Takes raw RFP text (markdown, plain text, or structured input) and produces
a structured JSON output that downstream tools (compliance matrix, response
drafting) can consume.

Usage:
    python tools/proposals/parse_rfp.py --input rfp_document.md
    python tools/proposals/parse_rfp.py --input rfp_document.md --output parsed_rfp.json
    python tools/proposals/parse_rfp.py --input rfp_document.md --format markdown
    python tools/proposals/parse_rfp.py --stdin < rfp_document.md

Dependencies:
    - json (stdlib)
    - re (stdlib)
    - argparse (stdlib)

Output:
    JSON with: metadata, requirements[], evaluation_criteria[], deadlines[], submission_instructions, compliance_items[]
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path


def parse_rfp_text(text: str) -> dict:
    """
    Parse RFP text into structured sections.

    This uses heuristic pattern matching to identify common RFP sections.
    For best results, feed it clean markdown or structured text.
    The AI orchestrator should pre-process messy PDFs into clean text before calling this tool.
    """
    result = {
        "metadata": {
            "parsed_at": datetime.now().isoformat(),
            "source_length": len(text),
            "source_lines": text.count("\n") + 1,
        },
        "title": "",
        "issuing_organization": "",
        "requirements": [],
        "evaluation_criteria": [],
        "deadlines": [],
        "submission_instructions": [],
        "compliance_items": [],
        "sections_found": [],
        "warnings": [],
    }

    lines = text.split("\n")

    # --- Extract title (first heading or first non-empty line) ---
    for line in lines:
        stripped = line.strip()
        if stripped:
            if stripped.startswith("#"):
                result["title"] = stripped.lstrip("#").strip()
            else:
                result["title"] = stripped
            break

    # --- Section detection ---
    section_patterns = {
        "scope": r"(?i)\b(scope\s+of\s+work|scope|sow|statement\s+of\s+work)\b",
        "requirements": r"(?i)\b(requirements?|technical\s+requirements?|functional\s+requirements?|mandatory\s+requirements?)\b",
        "evaluation": r"(?i)\b(evaluation\s+criteria|scoring|award\s+criteria|selection\s+criteria|evaluation\s+factors?)\b",
        "deadline": r"(?i)\b(schedule|timeline|deadlines?|due\s+date|submission\s+date|key\s+dates?|important\s+dates?)\b",
        "submission": r"(?i)\b(submission\s+instructions?|proposal\s+format|format\s+requirements?|submission\s+requirements?|how\s+to\s+submit)\b",
        "compliance": r"(?i)\b(compliance|certifications?|qualifications?|mandatory\s+qualifications?|minimum\s+qualifications?|eligibility)\b",
        "pricing": r"(?i)\b(pricing|cost\s+proposal|price\s+schedule|fee\s+schedule|budget|compensation)\b",
        "background": r"(?i)\b(background|introduction|overview|purpose|about)\b",
    }

    current_section = None
    current_section_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if this line starts a new section (heading)
        is_heading = (
            stripped.startswith("#")
            or (i + 1 < len(lines) and lines[i + 1].strip().startswith("==="))
            or (i + 1 < len(lines) and lines[i + 1].strip().startswith("---") and stripped)
            or re.match(r"^\d+\.\s+[A-Z]", stripped)
        )

        if is_heading:
            # Save previous section
            if current_section and current_section_lines:
                _process_section(result, current_section, current_section_lines)

            # Detect new section type
            current_section = None
            for section_name, pattern in section_patterns.items():
                if re.search(pattern, stripped):
                    current_section = section_name
                    result["sections_found"].append({
                        "type": section_name,
                        "heading": stripped.lstrip("#").strip(),
                        "line": i + 1,
                    })
                    break
            current_section_lines = []
        elif current_section:
            current_section_lines.append(stripped)

    # Process final section
    if current_section and current_section_lines:
        _process_section(result, current_section, current_section_lines)

    # --- Extract dates from entire document ---
    date_patterns = [
        r"(?i)(due\s+(?:date|by))[:\s]+(\w+\s+\d{1,2},?\s+\d{4})",
        r"(?i)(deadline)[:\s]+(\w+\s+\d{1,2},?\s+\d{4})",
        r"(?i)(submit\s+by|submission\s+deadline)[:\s]+(\w+\s+\d{1,2},?\s+\d{4})",
        r"(?i)(questions?\s+due|questions?\s+deadline)[:\s]+(\w+\s+\d{1,2},?\s+\d{4})",
        r"(?i)(response\s+due|responses?\s+due)[:\s]+(\w+\s+\d{1,2},?\s+\d{4})",
        r"(\d{1,2}/\d{1,2}/\d{2,4})",
        r"(\d{4}-\d{2}-\d{2})",
    ]

    for pattern in date_patterns:
        for match in re.finditer(pattern, text):
            groups = match.groups()
            if len(groups) >= 2:
                result["deadlines"].append({
                    "type": groups[0].strip(),
                    "date": groups[1].strip(),
                    "source_text": match.group(0).strip(),
                })
            else:
                # Bare date - add as untyped
                if groups[0] not in [d.get("date") for d in result["deadlines"]]:
                    result["deadlines"].append({
                        "type": "date_found",
                        "date": groups[0].strip(),
                        "source_text": match.group(0).strip(),
                    })

    # Deduplicate deadlines
    seen = set()
    unique_deadlines = []
    for d in result["deadlines"]:
        key = (d["type"], d["date"])
        if key not in seen:
            seen.add(key)
            unique_deadlines.append(d)
    result["deadlines"] = unique_deadlines

    # --- Extract numbered requirements from entire doc ---
    req_pattern = re.compile(
        r"^(?:\s*)(\d+(?:\.\d+)*)[.\)]\s+(.+)", re.MULTILINE
    )
    for match in req_pattern.finditer(text):
        req_num = match.group(1)
        req_text = match.group(2).strip()
        # Only add if it looks like a requirement (not a heading or TOC entry)
        if len(req_text) > 20 and not req_text.startswith("#"):
            # Avoid duplicates
            existing_ids = [r["id"] for r in result["requirements"]]
            if req_num not in existing_ids:
                result["requirements"].append({
                    "id": req_num,
                    "text": req_text,
                    "type": _classify_requirement(req_text),
                    "mandatory": _is_mandatory(req_text),
                })

    # --- Summary stats ---
    result["metadata"]["requirements_count"] = len(result["requirements"])
    result["metadata"]["mandatory_count"] = sum(
        1 for r in result["requirements"] if r.get("mandatory")
    )
    result["metadata"]["evaluation_criteria_count"] = len(result["evaluation_criteria"])
    result["metadata"]["deadlines_count"] = len(result["deadlines"])
    result["metadata"]["sections_found_count"] = len(result["sections_found"])

    # --- Warnings ---
    if not result["requirements"]:
        result["warnings"].append("No numbered requirements found - RFP may need manual extraction")
    if not result["deadlines"]:
        result["warnings"].append("No deadlines detected - verify submission dates manually")
    if not result["evaluation_criteria"]:
        result["warnings"].append("No evaluation criteria found - check for scoring rubric in attachments")

    return result


def _process_section(result: dict, section_type: str, lines: list):
    """Process accumulated lines for a detected section."""
    content = "\n".join(line for line in lines if line)

    if section_type == "requirements":
        for line in lines:
            if line and (re.match(r"^\d+", line) or line.startswith("-") or line.startswith("*")):
                clean = re.sub(r"^[\d.\-\*\)]+\s*", "", line).strip()
                if clean and len(clean) > 10:
                    result["requirements"].append({
                        "id": f"req_{len(result['requirements']) + 1}",
                        "text": clean,
                        "type": _classify_requirement(clean),
                        "mandatory": _is_mandatory(clean),
                    })

    elif section_type == "evaluation":
        for line in lines:
            if line:
                # Look for "criteria - weight" or "criteria (XX points)" patterns
                weight_match = re.search(r"(\d+)\s*(?:%|points?|pts)", line)
                clean = re.sub(r"^[\d.\-\*\)]+\s*", "", line).strip()
                if clean and len(clean) > 5:
                    criterion = {
                        "criterion": clean,
                        "weight": weight_match.group(1) if weight_match else None,
                    }
                    result["evaluation_criteria"].append(criterion)

    elif section_type == "submission":
        for line in lines:
            if line:
                result["submission_instructions"].append(line)

    elif section_type == "compliance":
        for line in lines:
            if line and len(line) > 10:
                clean = re.sub(r"^[\d.\-\*\)]+\s*", "", line).strip()
                if clean:
                    result["compliance_items"].append({
                        "item": clean,
                        "mandatory": _is_mandatory(clean),
                    })


def _classify_requirement(text: str) -> str:
    """Classify a requirement as technical, functional, administrative, or general."""
    text_lower = text.lower()
    if any(kw in text_lower for kw in [
        "infrastructure", "server", "network", "cloud", "aws", "azure",
        "security", "encrypt", "backup", "database", "api", "integration",
        "architecture", "platform", "sla", "uptime", "availability",
        "terraform", "kubernetes", "docker", "ci/cd", "pipeline",
    ]):
        return "technical"
    elif any(kw in text_lower for kw in [
        "user", "interface", "dashboard", "report", "workflow",
        "feature", "functionality", "capability", "access",
    ]):
        return "functional"
    elif any(kw in text_lower for kw in [
        "insurance", "license", "certification", "bonding", "cleared",
        "compliance", "audit", "background check", "reference",
        "experience", "years", "qualified", "personnel",
    ]):
        return "administrative"
    return "general"


def _is_mandatory(text: str) -> bool:
    """Heuristic: does this look like a mandatory requirement?"""
    text_lower = text.lower()
    mandatory_signals = [
        "shall", "must", "required", "mandatory", "minimum",
        "will not be considered", "failure to", "prerequisite",
    ]
    optional_signals = [
        "may", "optional", "preferred", "desirable", "nice to have",
        "bonus", "should", "encouraged",
    ]
    mandatory_score = sum(1 for s in mandatory_signals if s in text_lower)
    optional_score = sum(1 for s in optional_signals if s in text_lower)
    return mandatory_score > optional_score


def format_as_markdown(parsed: dict) -> str:
    """Convert parsed RFP to readable markdown."""
    lines = []
    lines.append(f"# Parsed RFP: {parsed['title']}")
    lines.append("")
    lines.append(f"**Parsed at:** {parsed['metadata']['parsed_at']}")
    lines.append(f"**Requirements found:** {parsed['metadata']['requirements_count']}"
                 f" ({parsed['metadata']['mandatory_count']} mandatory)")
    lines.append(f"**Evaluation criteria:** {parsed['metadata']['evaluation_criteria_count']}")
    lines.append(f"**Deadlines:** {parsed['metadata']['deadlines_count']}")
    lines.append("")

    if parsed["warnings"]:
        lines.append("## Warnings")
        for w in parsed["warnings"]:
            lines.append(f"- ⚠ {w}")
        lines.append("")

    if parsed["deadlines"]:
        lines.append("## Key Dates")
        lines.append("")
        lines.append("| Type | Date |")
        lines.append("|------|------|")
        for d in parsed["deadlines"]:
            lines.append(f"| {d['type']} | {d['date']} |")
        lines.append("")

    if parsed["requirements"]:
        lines.append("## Requirements")
        lines.append("")
        lines.append("| ID | Requirement | Type | Mandatory |")
        lines.append("|----|------------|------|-----------|")
        for r in parsed["requirements"]:
            mandatory = "Yes" if r["mandatory"] else "No"
            text = r["text"][:100] + ("..." if len(r["text"]) > 100 else "")
            lines.append(f"| {r['id']} | {text} | {r['type']} | {mandatory} |")
        lines.append("")

    if parsed["evaluation_criteria"]:
        lines.append("## Evaluation Criteria")
        lines.append("")
        lines.append("| Criterion | Weight |")
        lines.append("|-----------|--------|")
        for c in parsed["evaluation_criteria"]:
            weight = c["weight"] if c["weight"] else "-"
            lines.append(f"| {c['criterion'][:80]} | {weight} |")
        lines.append("")

    if parsed["compliance_items"]:
        lines.append("## Compliance Items")
        lines.append("")
        for c in parsed["compliance_items"]:
            mandatory = " **(mandatory)**" if c["mandatory"] else ""
            lines.append(f"- {c['item']}{mandatory}")
        lines.append("")

    if parsed["submission_instructions"]:
        lines.append("## Submission Instructions")
        lines.append("")
        for s in parsed["submission_instructions"]:
            lines.append(f"- {s}")
        lines.append("")

    if parsed["sections_found"]:
        lines.append("## Sections Detected")
        lines.append("")
        for s in parsed["sections_found"]:
            lines.append(f"- **{s['type']}**: {s['heading']} (line {s['line']})")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Parse an RFP document into structured requirements, criteria, and deadlines"
    )
    parser.add_argument("--input", "-i", help="Path to RFP document (text/markdown)")
    parser.add_argument("--output", "-o", help="Path to write output (default: stdout)")
    parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read RFP text from stdin instead of --input file"
    )

    args = parser.parse_args()

    # Read input
    if args.stdin:
        text = sys.stdin.read()
    elif args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(json.dumps({"success": False, "error": f"File not found: {args.input}"}))
            sys.exit(1)
        text = input_path.read_text(encoding="utf-8")
    else:
        print(json.dumps({"success": False, "error": "Provide --input <file> or --stdin"}))
        sys.exit(1)

    # Parse
    parsed = parse_rfp_text(text)

    # Format output
    if args.format == "markdown":
        output = format_as_markdown(parsed)
    else:
        output = json.dumps({"success": True, "data": parsed}, indent=2)

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
