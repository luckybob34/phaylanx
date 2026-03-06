# Agent Manifest

> Registry of all specialist agents. Check this before invoking an agent.

## Available Agents

| Agent | Model | Expertise | Linked Skills |
|-------|-------|-----------|---------------|
| `aws-architect` | claude-opus-4 | AWS cloud architecture, Well-Architected Framework | designing-architecture, planning-cloud-migration |
| `azure-architect` | claude-opus-4 | Azure cloud architecture, WAF + CAF | designing-architecture, planning-cloud-migration |
| `creative-director` | seedream-4.5 | Visual assets, diagrams, proposal graphics | creating-visuals |
| `devops-engineer` | claude-opus-4 | CI/CD pipelines, GitHub Actions, Azure DevOps | deploying-infrastructure |
| `iac-engineer` | claude-opus-4 | Terraform, Bicep, infrastructure as code | deploying-infrastructure, designing-architecture |
| `proposal-writer` | claude-opus-4 | RFP responses, SOWs, compliance matrices | responding-to-rfps, building-sow |
| `researcher` | claude-opus-4-6 | Multi-source research, synthesis, validation | building-apps |
| `technical-writer` | claude-sonnet-4-6 | SOPs, architecture docs, executive summaries | building-apps |

## Agent Structure

Each agent directory contains:
- `role.md` — system prompt defining identity, expertise, principles
- `config.yaml` — model, linked skills, linked agents, context files, MCPs

## Invocation

See the `invoking-agents` skill for the full protocol.
