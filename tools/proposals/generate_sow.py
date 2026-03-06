"""
Tool: SOW Generator
Purpose: Assemble a Statement of Work document from structured inputs

Takes structured project data (scope, deliverables, timeline, assumptions,
pricing, risks) and generates a formatted SOW document. Uses a template-driven
approach - the hardprompt defines the structure, this tool assembles the content.

Usage:
    python tools/proposals/generate_sow.py --input sow_data.json --output sow_draft.md
    python tools/proposals/generate_sow.py --input sow_data.json --format markdown
    python tools/proposals/generate_sow.py --scaffold --output sow_data.json

Dependencies:
    - json (stdlib)
    - argparse (stdlib)

Output:
    Markdown SOW document or JSON scaffold for data entry
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


SOW_SCAFFOLD = {
    "project_title": "",
    "client_name": "",
    "prepared_by": "",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "version": "1.0",
    "background": {
        "context": "",
        "business_need": "",
        "current_state": "",
    },
    "scope": {
        "description": "",
        "in_scope": [],
        "out_of_scope": [],
    },
    "deliverables": [
        {
            "id": "D1",
            "name": "",
            "description": "",
            "acceptance_criteria": "",
            "due": "",
        }
    ],
    "timeline": {
        "start_date": "",
        "end_date": "",
        "milestones": [
            {
                "id": "M1",
                "name": "",
                "deliverables": ["D1"],
                "target_date": "",
            }
        ],
    },
    "assumptions": [],
    "dependencies": [],
    "staffing": [
        {
            "role": "",
            "responsibility": "",
            "allocation": "",
        }
    ],
    "pricing": {
        "type": "fixed-price|time-and-materials|hybrid",
        "total": "",
        "breakdown": [],
        "payment_schedule": [],
        "expenses": "",
    },
    "risks": [
        {
            "id": "R1",
            "risk": "",
            "probability": "high|medium|low",
            "impact": "high|medium|low",
            "mitigation": "",
        }
    ],
    "change_management": {
        "process": "Change requests must be submitted in writing and approved by both parties before work begins.",
        "impact_assessment": "Each change request will include scope, timeline, and cost impact analysis.",
    },
    "acceptance": {
        "review_period_days": 5,
        "process": "",
    },
}


def generate_sow_markdown(data: dict) -> str:
    """Generate a formatted SOW document from structured data."""
    lines = []

    # Header
    lines.append(f"# Statement of Work: {data.get('project_title', 'Untitled Project')}")
    lines.append("")
    lines.append(f"**Client:** {data.get('client_name', 'TBD')}")
    lines.append(f"**Prepared by:** {data.get('prepared_by', 'TBD')}")
    lines.append(f"**Date:** {data.get('date', datetime.now().strftime('%Y-%m-%d'))}")
    lines.append(f"**Version:** {data.get('version', '1.0')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Background and Purpose
    bg = data.get("background", {})
    lines.append("## 1. Background and Purpose")
    lines.append("")
    if bg.get("context"):
        lines.append(bg["context"])
        lines.append("")
    if bg.get("business_need"):
        lines.append(f"**Business Need:** {bg['business_need']}")
        lines.append("")
    if bg.get("current_state"):
        lines.append(f"**Current State:** {bg['current_state']}")
        lines.append("")

    # 2. Scope of Work
    scope = data.get("scope", {})
    lines.append("## 2. Scope of Work")
    lines.append("")
    if scope.get("description"):
        lines.append(scope["description"])
        lines.append("")
    if scope.get("in_scope"):
        lines.append("### In Scope")
        lines.append("")
        for item in scope["in_scope"]:
            lines.append(f"- {item}")
        lines.append("")
    if scope.get("out_of_scope"):
        lines.append("### Out of Scope")
        lines.append("")
        for item in scope["out_of_scope"]:
            lines.append(f"- {item}")
        lines.append("")

    # 3. Deliverables
    deliverables = data.get("deliverables", [])
    lines.append("## 3. Deliverables")
    lines.append("")
    if deliverables:
        lines.append("| ID | Deliverable | Description | Acceptance Criteria | Due |")
        lines.append("|----|------------|-------------|---------------------|-----|")
        for d in deliverables:
            desc = d.get("description", "")[:60]
            criteria = d.get("acceptance_criteria", "")[:60]
            lines.append(
                f"| {d.get('id', '')} | {d.get('name', '')} | {desc} | {criteria} | {d.get('due', 'TBD')} |"
            )
        lines.append("")

    # 4. Timeline and Milestones
    timeline = data.get("timeline", {})
    lines.append("## 4. Timeline and Milestones")
    lines.append("")
    if timeline.get("start_date") or timeline.get("end_date"):
        lines.append(f"**Start Date:** {timeline.get('start_date', 'TBD')}")
        lines.append(f"**End Date:** {timeline.get('end_date', 'TBD')}")
        lines.append("")
    milestones = timeline.get("milestones", [])
    if milestones:
        lines.append("| ID | Milestone | Deliverables | Target Date |")
        lines.append("|----|-----------|-------------|-------------|")
        for m in milestones:
            delivs = ", ".join(m.get("deliverables", []))
            lines.append(
                f"| {m.get('id', '')} | {m.get('name', '')} | {delivs} | {m.get('target_date', 'TBD')} |"
            )
        lines.append("")

    # 5. Assumptions and Dependencies
    lines.append("## 5. Assumptions and Dependencies")
    lines.append("")
    assumptions = data.get("assumptions", [])
    if assumptions:
        lines.append("### Assumptions")
        lines.append("")
        for i, a in enumerate(assumptions, 1):
            lines.append(f"{i}. {a}")
        lines.append("")
    dependencies = data.get("dependencies", [])
    if dependencies:
        lines.append("### Dependencies")
        lines.append("")
        for i, d in enumerate(dependencies, 1):
            lines.append(f"{i}. {d}")
        lines.append("")

    # 6. Staffing and Roles
    staffing = data.get("staffing", [])
    if staffing:
        lines.append("## 6. Staffing and Roles")
        lines.append("")
        lines.append("| Role | Responsibility | Allocation |")
        lines.append("|------|---------------|------------|")
        for s in staffing:
            lines.append(
                f"| {s.get('role', '')} | {s.get('responsibility', '')} | {s.get('allocation', '')} |"
            )
        lines.append("")

    # 7. Pricing
    pricing = data.get("pricing", {})
    lines.append("## 7. Pricing")
    lines.append("")
    if pricing.get("type"):
        lines.append(f"**Pricing Model:** {pricing['type']}")
    if pricing.get("total"):
        lines.append(f"**Total:** {pricing['total']}")
    lines.append("")
    breakdown = pricing.get("breakdown", [])
    if breakdown:
        lines.append("### Cost Breakdown")
        lines.append("")
        lines.append("| Item | Amount |")
        lines.append("|------|--------|")
        for b in breakdown:
            if isinstance(b, dict):
                lines.append(f"| {b.get('item', '')} | {b.get('amount', '')} |")
            else:
                lines.append(f"| {b} | |")
        lines.append("")
    payment = pricing.get("payment_schedule", [])
    if payment:
        lines.append("### Payment Schedule")
        lines.append("")
        for p in payment:
            if isinstance(p, dict):
                lines.append(f"- **{p.get('milestone', '')}**: {p.get('amount', '')} - {p.get('trigger', '')}")
            else:
                lines.append(f"- {p}")
        lines.append("")
    if pricing.get("expenses"):
        lines.append(f"**Expenses:** {pricing['expenses']}")
        lines.append("")

    # 8. Risk Register
    risks = data.get("risks", [])
    if risks:
        lines.append("## 8. Risk Register")
        lines.append("")
        lines.append("| ID | Risk | Probability | Impact | Mitigation |")
        lines.append("|----|------|------------|--------|------------|")
        for r in risks:
            lines.append(
                f"| {r.get('id', '')} | {r.get('risk', '')} | "
                f"{r.get('probability', '')} | {r.get('impact', '')} | {r.get('mitigation', '')} |"
            )
        lines.append("")

    # 9. Change Management
    cm = data.get("change_management", {})
    lines.append("## 9. Change Management")
    lines.append("")
    if cm.get("process"):
        lines.append(cm["process"])
        lines.append("")
    if cm.get("impact_assessment"):
        lines.append(cm["impact_assessment"])
        lines.append("")

    # 10. Acceptance
    acceptance = data.get("acceptance", {})
    lines.append("## 10. Acceptance Criteria and Process")
    lines.append("")
    if acceptance.get("review_period_days"):
        lines.append(
            f"The client will have **{acceptance['review_period_days']} business days** "
            f"to review each deliverable upon submission."
        )
    if acceptance.get("process"):
        lines.append("")
        lines.append(acceptance["process"])
    lines.append("")

    # Signature block
    lines.append("---")
    lines.append("")
    lines.append("## Signatures")
    lines.append("")
    lines.append(f"**{data.get('prepared_by', 'Provider')}**")
    lines.append("")
    lines.append("Signature: _________________________ Date: ___________")
    lines.append("")
    lines.append(f"**{data.get('client_name', 'Client')}**")
    lines.append("")
    lines.append("Signature: _________________________ Date: ___________")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Statement of Work document from structured data"
    )
    parser.add_argument("--input", "-i", help="Path to SOW data JSON file")
    parser.add_argument("--output", "-o", help="Path to write output (default: stdout)")
    parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Output a blank SOW data scaffold for filling in"
    )

    args = parser.parse_args()

    if args.scaffold:
        output = json.dumps(SOW_SCAFFOLD, indent=2)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(output, encoding="utf-8")
            print(json.dumps({"success": True, "message": f"Scaffold written to {args.output}"}))
        else:
            print(output)
        return

    if not args.input:
        print(json.dumps({"success": False, "error": "Provide --input <file> or --scaffold"}))
        sys.exit(1)

    # Load data
    input_path = Path(args.input)
    if not input_path.exists():
        print(json.dumps({"success": False, "error": f"File not found: {args.input}"}))
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))

    # Generate
    if args.format == "markdown":
        output = generate_sow_markdown(data)
    else:
        output = json.dumps({"success": True, "data": data}, indent=2)

    # Write
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(json.dumps({"success": True, "message": f"Written to {args.output}"}))
    else:
        print(output)


if __name__ == "__main__":
    main()
