"""
Tool: Cloud Cost Estimator
Purpose: Generate structured cost estimates for cloud architectures

Takes architecture specifications and produces cost breakdowns by category,
with baseline/expected/peak projections and optimization recommendations.

This tool generates the STRUCTURE for cost estimates. Actual pricing data
should be validated against current cloud provider pricing calculators.

Usage:
    python tools/architecture/estimate_costs.py --platform aws --output cost_estimate.md
    python tools/architecture/estimate_costs.py --platform azure --input architecture.md --output cost_estimate.md
    python tools/architecture/estimate_costs.py --scaffold --output cost_data.json

Dependencies:
    - json (stdlib)
    - argparse (stdlib)

Output:
    Markdown cost estimate document or JSON scaffold
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


COST_SCAFFOLD = {
    "project": "",
    "platform": "aws|azure",
    "region": "",
    "currency": "USD",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "categories": {
        "compute": {
            "items": [
                {
                    "service": "",
                    "description": "",
                    "configuration": "",
                    "quantity": 1,
                    "monthly_cost": 0.0,
                    "notes": "",
                }
            ],
            "subtotal": 0.0,
        },
        "storage": {
            "items": [],
            "subtotal": 0.0,
        },
        "database": {
            "items": [],
            "subtotal": 0.0,
        },
        "networking": {
            "items": [],
            "subtotal": 0.0,
        },
        "security": {
            "items": [],
            "subtotal": 0.0,
        },
        "monitoring": {
            "items": [],
            "subtotal": 0.0,
        },
        "other": {
            "items": [],
            "subtotal": 0.0,
        },
    },
    "projections": {
        "baseline_monthly": 0.0,
        "expected_monthly": 0.0,
        "peak_monthly": 0.0,
        "annual_expected": 0.0,
    },
    "optimizations": [
        {
            "recommendation": "",
            "estimated_savings_monthly": 0.0,
            "effort": "low|medium|high",
        }
    ],
    "assumptions": [],
}


def generate_cost_markdown(data: dict) -> str:
    """Generate a formatted cost estimate document from structured data."""
    lines = []

    lines.append(f"# Cost Estimate: {data.get('project', 'Untitled')}")
    lines.append("")
    lines.append(f"**Platform:** {data.get('platform', 'TBD')}")
    lines.append(f"**Region:** {data.get('region', 'TBD')}")
    lines.append(f"**Date:** {data.get('date', datetime.now().strftime('%Y-%m-%d'))}")
    lines.append(f"**Currency:** {data.get('currency', 'USD')}")
    lines.append("")

    # Disclaimer
    lines.append("> **Note:** These are estimates based on expected usage patterns.")
    lines.append("> Validate against the [AWS Pricing Calculator](https://calculator.aws/) or")
    lines.append("> [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) for accuracy.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Summary
    proj = data.get("projections", {})
    lines.append("## Cost Summary")
    lines.append("")
    lines.append("| Scenario | Monthly | Annual |")
    lines.append("|----------|---------|--------|")
    baseline = proj.get("baseline_monthly", 0)
    expected = proj.get("expected_monthly", 0)
    peak = proj.get("peak_monthly", 0)
    lines.append(f"| Baseline (minimum) | ${baseline:,.2f} | ${baseline * 12:,.2f} |")
    lines.append(f"| Expected (normal load) | ${expected:,.2f} | ${expected * 12:,.2f} |")
    lines.append(f"| Peak (maximum load) | ${peak:,.2f} | ${peak * 12:,.2f} |")
    lines.append("")

    # Category breakdown
    categories = data.get("categories", {})
    total = 0.0

    for cat_name, cat_data in categories.items():
        items = cat_data.get("items", [])
        if not items:
            continue

        subtotal = cat_data.get("subtotal", sum(i.get("monthly_cost", 0) for i in items))
        total += subtotal

        lines.append(f"## {cat_name.title()}")
        lines.append("")
        lines.append("| Service | Description | Configuration | Qty | Monthly |")
        lines.append("|---------|-------------|--------------|-----|---------|")
        for item in items:
            cost = item.get("monthly_cost", 0)
            lines.append(
                f"| {item.get('service', '')} | {item.get('description', '')} | "
                f"{item.get('configuration', '')} | {item.get('quantity', 1)} | ${cost:,.2f} |"
            )
        lines.append(f"| | | | **Subtotal** | **${subtotal:,.2f}** |")
        lines.append("")

    lines.append(f"### Total Estimated Monthly Cost: **${total:,.2f}**")
    lines.append(f"### Total Estimated Annual Cost: **${total * 12:,.2f}**")
    lines.append("")

    # Optimizations
    optimizations = data.get("optimizations", [])
    if optimizations and any(o.get("recommendation") for o in optimizations):
        lines.append("## Optimization Recommendations")
        lines.append("")
        lines.append("| Recommendation | Est. Monthly Savings | Effort |")
        lines.append("|---------------|---------------------|--------|")
        total_savings = 0.0
        for opt in optimizations:
            if opt.get("recommendation"):
                savings = opt.get("estimated_savings_monthly", 0)
                total_savings += savings
                lines.append(
                    f"| {opt['recommendation']} | ${savings:,.2f} | {opt.get('effort', '')} |"
                )
        lines.append(f"| **Total Potential Savings** | **${total_savings:,.2f}/mo** | |")
        lines.append("")

    # Assumptions
    assumptions = data.get("assumptions", [])
    if assumptions:
        lines.append("## Assumptions")
        lines.append("")
        for a in assumptions:
            lines.append(f"- {a}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d')}*")
    lines.append("")

    return "\n".join(lines)


def generate_empty_estimate(platform: str) -> str:
    """Generate an empty cost estimate template for a platform."""
    if platform.lower() == "aws":
        services = {
            "compute": ["EC2", "ECS/Fargate", "Lambda"],
            "storage": ["S3", "EBS"],
            "database": ["RDS/Aurora", "DynamoDB"],
            "networking": ["Data Transfer", "ALB/NLB", "CloudFront", "Route 53"],
            "security": ["WAF", "KMS", "Secrets Manager", "GuardDuty"],
            "monitoring": ["CloudWatch", "X-Ray"],
        }
    elif platform.lower() == "azure":
        services = {
            "compute": ["Virtual Machines", "App Service", "Azure Functions"],
            "storage": ["Blob Storage", "Managed Disks"],
            "database": ["Azure SQL", "Cosmos DB"],
            "networking": ["Data Transfer", "Application Gateway", "Front Door", "Azure DNS"],
            "security": ["Azure Firewall", "Key Vault", "Defender for Cloud"],
            "monitoring": ["Azure Monitor", "Log Analytics", "Application Insights"],
        }
    else:
        services = {
            "compute": ["Compute Service 1"],
            "storage": ["Storage Service 1"],
            "database": ["Database Service 1"],
            "networking": ["Networking Service 1"],
            "security": ["Security Service 1"],
            "monitoring": ["Monitoring Service 1"],
        }

    lines = []
    lines.append(f"# Cost Estimate Template ({platform.upper()})")
    lines.append("")
    lines.append(f"**Platform:** {platform.upper()}")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append("> Fill in the cost columns after checking the pricing calculator.")
    lines.append("")

    for category, svc_list in services.items():
        lines.append(f"## {category.title()}")
        lines.append("")
        lines.append("| Service | Description | Configuration | Qty | Monthly |")
        lines.append("|---------|-------------|--------------|-----|---------|")
        for svc in svc_list:
            lines.append(f"| {svc} | | | | $ |")
        lines.append("")

    lines.append("## Projections")
    lines.append("")
    lines.append("| Scenario | Monthly | Annual |")
    lines.append("|----------|---------|--------|")
    lines.append("| Baseline | $ | $ |")
    lines.append("| Expected | $ | $ |")
    lines.append("| Peak | $ | $ |")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate cloud cost estimate documents and scaffolds"
    )
    parser.add_argument(
        "--platform", "-p",
        choices=["aws", "azure", "multi-cloud"],
        default="aws",
        help="Cloud platform (default: aws)"
    )
    parser.add_argument("--input", "-i", help="Path to cost data JSON or architecture doc")
    parser.add_argument("--output", "-o", help="Path to write output (default: stdout)")
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Output a blank cost data scaffold (JSON)"
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Output an empty cost estimate template (Markdown)"
    )

    args = parser.parse_args()

    if args.scaffold:
        scaffold = COST_SCAFFOLD.copy()
        scaffold["platform"] = args.platform
        output = json.dumps(scaffold, indent=2)
    elif args.template:
        output = generate_empty_estimate(args.platform)
    elif args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(json.dumps({"success": False, "error": f"File not found: {args.input}"}))
            sys.exit(1)
        data = json.loads(input_path.read_text(encoding="utf-8"))
        output = generate_cost_markdown(data)
    else:
        output = generate_empty_estimate(args.platform)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(json.dumps({"success": True, "message": f"Written to {args.output}"}))
    else:
        print(output)


if __name__ == "__main__":
    main()
