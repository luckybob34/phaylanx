---
name: reviewing-architecture
description: Conducts architecture reviews and assessments for existing cloud environments using the AUDIT workflow — gather documentation, analyze against Well-Architected pillars, discover findings with severity ratings, produce a structured report, and create a prioritized remediation roadmap.
allowed-tools: Terminal
agent: aws-architect azure-architect
---

# Architecture Review — AUDIT Workflow

Conduct architecture reviews producing findings, recommendations, and remediation plans.

| Step | Phase | What You Do |
|------|-------|-------------|
| **A** | Assess | Gather current-state documentation and access |
| **U** | Understand | Analyze against Well-Architected pillars |
| **D** | Discover | Identify gaps, risks, optimization opportunities |
| **I** | Inform | Produce structured findings report |
| **T** | Track | Create prioritized remediation roadmap |

---

## A — Assess

Gather: architecture docs, infrastructure inventory, cost data, incident history, compliance requirements.

```bash
python tools/architecture/generate_architecture_doc.py --type current-state \
  --output workspace/<project-slug>/review/current_state.md
```

---

## U — Understand

### AWS Well-Architected (6 Pillars)

| Pillar | Key Questions |
|--------|--------------|
| Operational Excellence | IaC? Automated ops? Observability? |
| Security | Least privilege? Encryption? Segmentation? |
| Reliability | Multi-AZ? Auto-healing? DR tested? |
| Performance | Right-sized? Caching? CDN? |
| Cost Optimization | Right-sizing? Reserved/Spot? Tagging? |
| Sustainability | Efficient usage? Managed services? |

### Azure Well-Architected (5 Pillars)

| Pillar | Key Questions |
|--------|--------------|
| Reliability | Availability zones? Health monitoring? DR? |
| Security | Identity? Encryption? Network isolation? |
| Cost Optimization | Right-sizing? Reserved? Hybrid Benefit? |
| Operational Excellence | IaC? Monitoring? Automation? |
| Performance | Scaling? Caching? Geographic distribution? |

Agents: **aws-architect**, **azure-architect**, **iac-engineer**, **devops-engineer**.

---

## D — Discover

Each finding must include:

- **Category**: Security / Reliability / Cost / Performance / Operations
- **Severity**: Critical / High / Medium / Low / Informational
- **Current State**: What exists today (specific, factual)
- **Risk**: What could go wrong (business impact)
- **Recommendation**: Specific remediation action
- **Effort**: Low / Medium / High
- **Estimated Impact**: Cost savings, risk reduction, performance improvement

### Common Finding Areas

**Security**: permissive IAM, unencrypted data, public access, missing MFA, no segmentation, no monitoring.

**Reliability**: single-AZ, no auto-scaling, untested backups, no DR plan, single points of failure.

**Cost**: over-provisioned (<20% utilization), no reserved coverage, unused resources, missing tags.

**Operations**: no IaC, manual deployments, missing monitoring/alerting, no runbooks.

---

## I — Inform

Report structure:
1. Executive Summary (1-page)
2. Scope and Methodology
3. Current State Summary
4. Findings Summary (table by severity)
5. Detailed Findings
6. Cost Optimization Summary
7. Remediation Roadmap

Agents: **technical-writer** for polish, **proposal-writer** if feeding into a remediation proposal.

Save to `workspace/<project-slug>/review/architecture_review_report.md`.

---

## T — Track

Score each finding: business impact (1-5) + risk (1-5) / effort (1-5) = priority.

### Roadmap

- **Phase 1 — Quick Wins** (Weeks 1-2)
- **Phase 2 — Short-Term** (Weeks 3-6)
- **Phase 3 — Medium-Term** (Months 2-3)
- **Phase 4 — Long-Term** (Months 3-6)

Save to `workspace/<project-slug>/review/remediation_roadmap.md`.

Record: `python tools/memory/memory_write.py --content "Review complete: <project-slug> - X findings" --type event --importance 7`

---

## Edge Cases

- **No documentation** — Build from interviews/questionnaire, note documentation gap as finding
- **Multi-cloud** — Review each separately, then cross-cloud integration points
- **Feeds into proposal** — Cross-reference `responding-to-rfps` or `building-sow`
- **Sensitive environment** — Recommend penetration testing for security-specific reviews

---

## Workspace Structure

```
workspace/<project-slug>/
└── review/
    ├── current_state.md
    ├── architecture_review_report.md
    └── remediation_roadmap.md
```
