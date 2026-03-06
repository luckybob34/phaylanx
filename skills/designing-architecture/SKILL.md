---
name: designing-architecture
description: Designs cloud and application architectures using the BLUEPRINT workflow — gather requirements, assess current state, evaluate options, engineer target architecture with ADRs, estimate costs, and package for implementation handoff. Invokes aws-architect or azure-architect agents for platform-specific expertise.
allowed-tools: Terminal
agent: aws-architect azure-architect
---

# Architecture Design — BLUEPRINT Workflow

Design production-grade cloud architectures with documentation ready for IaC implementation.

| Step | Phase | What You Do |
|------|-------|-------------|
| **B** | Brief | Gather requirements, constraints, success criteria |
| **L** | Landscape | Assess current state, dependencies, integrations |
| **U** | Understand | Evaluate options and trade-offs |
| **E** | Engineer | Design target architecture with ADRs |
| **P** | Price | Estimate costs, optimize |
| **T** | Transfer | Package for implementation handoff |

---

## B — Brief

Gather: functional requirements, non-functional requirements (availability, performance, scalability, compliance), constraints (budget, tech mandates, timeline), team profile (who will operate this).

Save to `workspace/<project-slug>/architecture/brief.md`.

---

## L — Landscape

Assess: existing infrastructure, data flows, integrations, pain points, hard dependencies.

```bash
python tools/architecture/generate_architecture_doc.py --type current-state \
  --input workspace/<project-slug>/architecture/brief.md \
  --output workspace/<project-slug>/architecture/current_state.md
```

---

## U — Understand

For each significant decision, evaluate 2-3 options:

| Aspect | Option A | Option B | Option C |
|--------|----------|----------|----------|
| Description | | | |
| Pros | | | |
| Cons | | | |
| Cost (monthly) | | | |
| Complexity | | | |
| **Recommendation** | | **Selected** | |

Agents: **aws-architect**, **azure-architect**, **researcher**.

Save to `workspace/<project-slug>/architecture/options_analysis.md`.

---

## E — Engineer

Produce a comprehensive architecture spec:

1. Architecture overview
2. Component diagram description
3. Network design (VPC/VNet, subnets, routing)
4. Data architecture (storage, databases, encryption)
5. Security architecture (IAM, encryption, compliance mapping)
6. Scalability design (auto-scaling configuration)
7. Disaster recovery (RPO/RTO, backup, failover)
8. ADRs — one per significant decision

```bash
python tools/architecture/generate_architecture_doc.py --type target-state \
  --input workspace/<project-slug>/architecture/brief.md \
  --output workspace/<project-slug>/architecture/target_architecture.md
```

---

## P — Price

```bash
python tools/architecture/estimate_costs.py \
  --input workspace/<project-slug>/architecture/target_architecture.md \
  --output workspace/<project-slug>/architecture/cost_estimate.md
```

Categories: compute, storage, network, security, monitoring, licensing.

---

## T — Transfer

Package: architecture spec, ADRs, cost estimate, implementation notes, diagram descriptions.

Agents: **technical-writer** for polish, handoff to **iac-engineer** for Terraform/Bicep.

Record: `python tools/memory/memory_write.py --content "Architecture complete: <project-slug>" --type event --importance 6`

---

## Edge Cases

- **Multi-cloud** — Invoke both aws/azure architects, document integration points
- **Migration** — Include current-state assessment, reference `planning-cloud-migration`
- **Greenfield** — Skip current-state assessment
- **Budget-constrained** — Lead with cost optimization (reserved/spot/serverless)
- **Compliance-heavy** — Full compliance mapping section (FedRAMP, HIPAA, SOC 2, PCI-DSS)

---

## Tools

| Tool | Purpose |
|------|---------|
| `tools/architecture/generate_architecture_doc.py` | Generate architecture documents |
| `tools/architecture/estimate_costs.py` | Cost estimation |

---

## Workspace Structure

```
workspace/<project-slug>/
└── architecture/
    ├── brief.md
    ├── current_state.md
    ├── options_analysis.md
    ├── target_architecture.md
    ├── cost_estimate.md
    ├── adrs/
    └── diagrams/
```
