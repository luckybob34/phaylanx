---
name: deploying-infrastructure
description: Deploys cloud infrastructure using Infrastructure as Code (Terraform or Bicep) following the DEPLOY workflow — translate architecture to modules, write IaC code, configure environments, validate and lint, deploy through pipeline, and hand off to operations. Invokes the iac-engineer agent for code generation.
allowed-tools: Terminal
agent: iac-engineer
---

# Infrastructure Deployment — DEPLOY Workflow

Deploy cloud infrastructure using IaC (Terraform or Bicep).

| Step | Phase | What You Do |
|------|-------|-------------|
| **D** | Design | Translate architecture to module structure |
| **E** | Engineer | Write IaC code |
| **P** | Prepare | Configure state backend, variables, environments |
| **L** | Lint | Validate, lint, security scan |
| **O** | Operate | Plan, review, apply |
| **Y** | Yield | Hand off with documentation |

---

## D — Design

Break architecture into reusable modules: identify resource groups, define interfaces (inputs/outputs), map dependencies, choose composition pattern.

```bash
python tools/iac/scaffold_terraform.py --modules networking,compute,database,security \
  --provider aws --output workspace/<project-slug>/infrastructure/
```

---

## E — Engineer

### Terraform Standards

- Pin provider versions in `versions.tf`
- Variables with types and descriptions
- Descriptive resource names (`aws_vpc.main`)
- `for_each` over `count` for named items
- Output everything downstream needs
- Comment non-obvious decisions

### Bicep Standards

- Use modules for reusable components
- Parameter files per environment
- `@description` decorators on all parameters
- `existing` keyword for pre-existing resources

Agent: **iac-engineer** for code generation. Reference architecture from **aws-architect** / **azure-architect**.

---

## P — Prepare

### State Backend

AWS: S3 + DynamoDB lock. Azure: Storage Account container.

### Environment Configuration

```
environments/
  dev/terraform.tfvars + backend.tf
  staging/terraform.tfvars + backend.tf
  prod/terraform.tfvars + backend.tf
```

---

## L — Lint

```bash
python tools/iac/validate_terraform.py --path workspace/<project-slug>/infrastructure/ \
  --checks format,validate,lint,security
```

Common issues: unencrypted storage, public access, permissive IAM, missing tags, hardcoded values.

---

## O — Operate

### Development

```bash
terraform init
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
```

### Production

Pipeline: `plan → review → approve → apply`. Manual approval gate required.

### Rollback

Terraform: apply previous state or targeted destroy/recreate. Bicep: redeploy previous version. Always have rollback plan documented.

---

## Y — Yield

Documentation: module READMEs, environment runbook, state management guide, architecture mapping.

Agents: **technical-writer** for polish, **devops-engineer** for pipeline docs.

Record: `python tools/memory/memory_write.py --content "Infrastructure deployed: <project-slug>" --type event --importance 7`

---

## Tools

| Tool | Purpose |
|------|---------|
| `tools/iac/scaffold_terraform.py` | Generate module scaffolds |
| `tools/iac/validate_terraform.py` | Format, validate, lint, security scan |

---

## Edge Cases

- **Existing infrastructure** — Use `terraform import` before modifying
- **Multi-account** — Provider aliases and assume-role patterns
- **Shared infrastructure** — Remote state data sources
- **State corruption** — Document backup/recovery procedures up front
- **Provider bugs** — Pin versions, check changelogs before upgrading

---

## Workspace Structure

```
workspace/<project-slug>/
└── infrastructure/
    ├── modules/
    │   ├── networking/
    │   ├── compute/
    │   ├── database/
    │   └── security/
    ├── environments/
    │   ├── dev/
    │   ├── staging/
    │   └── prod/
    └── README.md
```
