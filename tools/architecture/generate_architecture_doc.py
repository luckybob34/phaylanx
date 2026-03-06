"""
Tool: Architecture Document Generator
Purpose: Generate structured architecture documentation templates and scaffolds

Produces architecture documents in markdown format following consistent
structure. Supports multiple document types: current-state, target-state,
migration-inventory, and ADR.

Usage:
    python tools/architecture/generate_architecture_doc.py --type target-state --output arch.md
    python tools/architecture/generate_architecture_doc.py --type current-state --input brief.md --output current.md
    python tools/architecture/generate_architecture_doc.py --type adr --title "Use Aurora over RDS" --output adr-001.md
    python tools/architecture/generate_architecture_doc.py --type migration-inventory --output inventory.md

Dependencies:
    - json (stdlib)
    - argparse (stdlib)

Output:
    Markdown architecture document (scaffold or populated template)
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


TEMPLATES = {
    "target-state": """# Target-State Architecture: {title}

**Date:** {date}
**Author:** {author}
**Version:** {version}
**Platform:** {platform}

---

## 1. Architecture Overview

[High-level narrative describing the target architecture, its purpose, and key design decisions.]

## 2. Component Architecture

### Service Inventory

| Component | Service | Purpose | Tier |
|-----------|---------|---------|------|
| [Name] | [Cloud service] | [What it does] | [Web/App/Data/Security] |

### Component Interactions

[Describe how components communicate: synchronous APIs, async messaging, event-driven, etc.]

## 3. Network Design

### Topology

| Network | CIDR | Purpose | AZs |
|---------|------|---------|-----|
| [VPC/VNet] | [10.0.0.0/16] | [Production] | [2-3] |

### Subnets

| Subnet | CIDR | Type | Purpose |
|--------|------|------|---------|
| [Name] | [10.0.1.0/24] | [Public/Private] | [Load balancers] |

### Connectivity

- Internet egress: [NAT Gateway / Azure Firewall]
- On-premises: [VPN / Direct Connect / ExpressRoute]
- Cross-region: [Peering / Transit Gateway / Virtual WAN]

## 4. Data Architecture

### Storage

| Data Store | Service | Size | Encryption | Backup |
|-----------|---------|------|------------|--------|
| [Name] | [Service] | [Estimate] | [KMS/Key Vault] | [Schedule] |

### Data Flow

[Describe how data moves through the system: ingestion → processing → storage → consumption]

## 5. Security Architecture

### Identity and Access

- Authentication: [Cognito / Entra ID / etc.]
- Authorization: [IAM roles / RBAC / etc.]
- Service-to-service: [IAM roles / Managed Identity / mTLS]

### Network Security

- Perimeter: [WAF / Shield / DDoS Protection]
- Segmentation: [Security Groups / NSGs / Private subnets]
- Inspection: [Flow logs / Firewall rules]

### Encryption

- At rest: [KMS keys / Key Vault / SSE]
- In transit: [TLS 1.2+ / Certificate management]
- Key management: [Rotation policy]

### Compliance Mapping

| Requirement | Control | Implementation |
|-------------|---------|----------------|
| [e.g., Data encryption at rest] | [e.g., AES-256] | [e.g., KMS with annual rotation] |

## 6. Scalability

### Auto-Scaling Configuration

| Component | Min | Max | Metric | Target |
|-----------|-----|-----|--------|--------|
| [Service] | [N] | [N] | [CPU/Requests] | [Target %] |

### Capacity Planning

- Current load: [estimate]
- Expected growth: [%/year]
- Scale ceiling: [architectural limits]

## 7. Disaster Recovery

- **RPO:** [target]
- **RTO:** [target]
- **Backup strategy:** [description]
- **Failover strategy:** [active-passive / active-active / pilot light]
- **DR region:** [region]

## 8. Architecture Decision Records

[Reference ADR files in the `adrs/` directory]

| ADR | Decision | Status |
|-----|----------|--------|
| ADR-001 | [Title] | [Proposed/Accepted] |

## 9. Cost Estimate

[Reference cost estimate document]

See `cost_estimate.md` for detailed breakdown.

---

*Generated: {date}*
""",

    "current-state": """# Current-State Assessment: {title}

**Date:** {date}
**Author:** {author}

---

## 1. Infrastructure Overview

[High-level description of the current environment]

## 2. Compute

| Asset | Type | OS | CPU | RAM | Storage | Location |
|-------|------|----|-----|-----|---------|----------|
| [Name] | [VM/Physical/Container] | [OS] | [cores] | [GB] | [GB] | [DC/Cloud/Region] |

## 3. Applications

| Application | Version | Language/Framework | Dependencies | Owner | Criticality |
|-------------|---------|-------------------|--------------|-------|-------------|
| [Name] | [ver] | [stack] | [deps] | [team] | [High/Med/Low] |

## 4. Databases

| Database | Engine | Version | Size | Growth Rate | Backup |
|----------|--------|---------|------|-------------|--------|
| [Name] | [MySQL/PostgreSQL/etc.] | [ver] | [GB] | [GB/month] | [Schedule] |

## 5. Network

| Network | Type | CIDR/Range | Purpose |
|---------|------|------------|---------|
| [Name] | [LAN/VLAN/VPC] | [CIDR] | [Purpose] |

### Connectivity

- Internet: [ISP / Direct Connect / ExpressRoute]
- Inter-site: [VPN / MPLS / Peering]
- DNS: [Provider / Self-hosted]

## 6. Security Posture

- Authentication: [AD / LDAP / SSO / etc.]
- Network security: [Firewalls / Segmentation]
- Encryption: [At rest / In transit - current state]
- Compliance: [Current certifications / gaps]

## 7. Pain Points

1. [Pain point with impact description]
2. [Pain point with impact description]
3. [Pain point with impact description]

## 8. Dependencies Map

[Describe critical dependencies between applications, databases, and external systems]

---

*Generated: {date}*
""",

    "migration-inventory": """# Migration Workload Inventory: {title}

**Date:** {date}
**Author:** {author}

---

## Workload Catalog

| # | Workload | Type | Current Platform | Size | Dependencies | Strategy | Priority | Wave |
|---|----------|------|-----------------|------|--------------|----------|----------|------|
| 1 | [Name] | [App/DB/Service] | [Platform] | [CPU/RAM/Storage] | [List] | [7R] | [1-5] | [#] |

## Dependency Matrix

| Workload | Depends On | Depended On By | Notes |
|----------|-----------|----------------|-------|
| [Name] | [List] | [List] | [Migration order implications] |

## Data Volume Summary

| Data Store | Size (GB) | Growth (GB/mo) | Sensitivity | Migration Method |
|-----------|-----------|----------------|-------------|-----------------|
| [Name] | [GB] | [GB] | [PII/HIPAA/Public] | [Online/Offline/Replication] |

## License Portability

| Software | License Type | Cloud-Portable | Notes |
|----------|-------------|---------------|-------|
| [Name] | [Per-core/Per-user/Subscription] | [Yes/No/BYOL] | [Hybrid Benefit applicable?] |

---

*Generated: {date}*
""",

    "adr": """# ADR-{adr_number}: {title}

**Date:** {date}
**Status:** Proposed
**Author:** {author}

## Context

[What is the issue or decision that needs to be made? What forces are at play?]

## Options Considered

### Option A: [Name]
- **Description:** [Approach]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Cost:** [Estimate]

### Option B: [Name]
- **Description:** [Approach]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Cost:** [Estimate]

### Option C: [Name]
- **Description:** [Approach]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Cost:** [Estimate]

## Decision

[Which option was selected and why. Reference the deciding factors.]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Trade-off 1]
- [Trade-off 2]

### Cost Impact

- **One-time:** [Amount]
- **Monthly:** [Amount]
- **Annual:** [Amount]

---

*Created: {date}*
""",
}


def generate_document(doc_type: str, title: str = "", author: str = "",
                      platform: str = "", version: str = "1.0",
                      adr_number: str = "001") -> str:
    """Generate an architecture document from template."""
    template = TEMPLATES.get(doc_type)
    if not template:
        return f"Unknown document type: {doc_type}. Available: {', '.join(TEMPLATES.keys())}"

    return template.format(
        title=title or "Untitled",
        date=datetime.now().strftime("%Y-%m-%d"),
        author=author or "AI Architecture Assistant",
        platform=platform or "TBD",
        version=version,
        adr_number=adr_number,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate architecture document templates and scaffolds"
    )
    parser.add_argument(
        "--type", "-t", required=True,
        choices=["target-state", "current-state", "migration-inventory", "adr"],
        help="Type of architecture document to generate"
    )
    parser.add_argument("--title", default="", help="Document title")
    parser.add_argument("--author", default="", help="Author name")
    parser.add_argument("--platform", default="", help="Cloud platform (AWS/Azure/Multi-cloud)")
    parser.add_argument("--version", default="1.0", help="Document version")
    parser.add_argument("--adr-number", default="001", help="ADR number (for ADR type)")
    parser.add_argument("--input", "-i", help="Path to input file for context (e.g., brief.md)")
    parser.add_argument("--output", "-o", help="Path to write output (default: stdout)")

    args = parser.parse_args()

    # Generate document
    doc = generate_document(
        doc_type=args.type,
        title=args.title,
        author=args.author,
        platform=args.platform,
        version=args.version,
        adr_number=args.adr_number,
    )

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(doc, encoding="utf-8")
        print(json.dumps({"success": True, "message": f"Written to {args.output}", "type": args.type}))
    else:
        print(doc)


if __name__ == "__main__":
    main()
