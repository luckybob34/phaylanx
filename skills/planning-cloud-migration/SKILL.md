---
name: planning-cloud-migration
description: Plans and executes cloud migration engagements using the MIGRATE workflow — inventory workloads, classify by the 7 Rs, assess risk, design target architecture, build migration waves with runbooks, test in landing zones, and execute cutover. Invokes aws-architect or azure-architect for platform-specific design.
allowed-tools: Terminal
agent: aws-architect azure-architect
---

# Cloud Migration — MIGRATE Workflow

Plan and execute cloud migrations from assessment through cutover.

| Step | Phase | What You Do |
|------|-------|-------------|
| **M** | Map | Inventory current infrastructure and workloads |
| **I** | Identify | Classify workloads by migration strategy (7 R's) |
| **G** | Gauge | Assess complexity, risk, dependencies |
| **R** | Redesign | Design target-state per workload |
| **A** | Arrange | Build migration plan with waves and runbooks |
| **T** | Test | Validate in landing zone before cutover |
| **E** | Execute | Cutover, verify, decommission |

---

## M — Map

Discovery: compute inventory (OS, CPU, RAM, storage), application inventory, data inventory (size, growth, sensitivity), network topology, integrations, licenses, compliance requirements.

```bash
python tools/architecture/generate_architecture_doc.py --type migration-inventory \
  --output workspace/<project-slug>/migration/workload_inventory.md
```

---

## I — Identify (7 R's)

| Strategy | When to Use |
|----------|-------------|
| **Rehost** (Lift & Shift) | Legacy apps, tight timeline, low risk |
| **Replatform** (Lift & Reshape) | Quick wins, move to managed services |
| **Refactor** (Re-architect) | Strategic apps, cloud-native needs |
| **Repurchase** | Commodity software → SaaS |
| **Retain** | Compliance, latency, or cost reasons |
| **Retire** | No longer needed |
| **Relocate** | Region/account reorg |

Output per workload: `| Workload | Strategy | Rationale | Complexity | Priority |`

Save to `workspace/<project-slug>/migration/workload_classification.md`.

---

## G — Gauge

Per workload: technical complexity, data complexity, integration risk, business criticality, team readiness, compliance impact.

Risk matrix: probability × impact → mitigation strategy.

Save to `workspace/<project-slug>/migration/risk_assessment.md`.

---

## R — Redesign

Group workloads by wave. Design target architecture per wave using `designing-architecture` workflow. Agents: **aws-architect**, **azure-architect**.

Save to `workspace/<project-slug>/migration/target_architectures/`.

---

## A — Arrange

### Wave Planning

Group by: dependencies (migrate deps first), risk (start low-risk), business windows (avoid peaks), team capacity.

### Runbook Per Wave

1. Pre-migration checklist (backups, DNS TTL, notifications)
2. Migration steps (ordered, with durations)
3. Validation steps
4. Rollback procedure
5. Post-migration steps (DNS cutover, monitoring, decommission timeline)

Save to `workspace/<project-slug>/migration/migration_plan.md` and `runbooks/`.

---

## T — Test

1. Landing zone validation (network, security, identity)
2. Pilot migration (one low-risk workload end-to-end)
3. Integration testing
4. Performance testing
5. DR testing

Save to `workspace/<project-slug>/migration/test_results.md`.

---

## E — Execute

Cutover: final data sync, DNS switch, monitoring active, health verified, rollback window defined, stakeholders notified.

Post-migration: right-size, enable auto-scaling, apply reserved pricing, update docs, schedule decommission, retrospective.

Record: `python tools/memory/memory_write.py --content "Migration complete: <project-slug>" --type event --importance 7`

---

## Workspace Structure

```
workspace/<project-slug>/
└── migration/
    ├── workload_inventory.md
    ├── workload_classification.md
    ├── risk_assessment.md
    ├── target_architectures/
    ├── migration_plan.md
    ├── runbooks/
    ├── test_results.md
    ├── cutover_log.md
    └── post_migration_optimization.md
```
