# Skills Manifest

> Registry of all skills in this system. Check here before starting any task.

## Workflow Skills

| Skill | Description | Tools Referenced | Agent |
|---|---|---|---|
| `building-pptx-decks` | PowerPoint presentations from YAML outlines | `render_pptx.py`, `parse_outline.py` | — |
| `building-html-decks` | Interactive HTML slide deck presentations | — | — |
| `responding-to-rfps` | RFP response with compliance matrix | `parse_rfp.py`, `build_compliance_matrix.py` | `proposal-writer`, `researcher` |
| `building-sow` | Statement of Work generation | `generate_sow.py` | `proposal-writer` |
| `building-apps` | Full-stack application development | — | — |
| `designing-architecture` | Cloud architecture design | `generate_architecture_doc.py`, `estimate_costs.py` | `aws-architect`, `azure-architect` |
| `planning-cloud-migration` | Cloud migration planning | — | `aws-architect`, `azure-architect` |
| `deploying-infrastructure` | Infrastructure as Code deployment | `scaffold_terraform.py`, `validate_terraform.py` | `iac-engineer` |
| `reviewing-architecture` | Architecture review and audit | — | `aws-architect`, `azure-architect` |
| `creating-visuals` | Visual asset generation | `generate_image.py`, `analyze_image.py` | `creative-director` |
| `building-university-decks` | University degree program presentations | — | — |

## Atomic Skills

| Skill | Description | Tools Referenced |
|---|---|---|
| `generating-architecture-diagrams` | Architecture diagram image prompts | `generate_image.py` |
| `generating-proposal-visuals` | Proposal graphics (org charts, timelines) | `generate_image.py` |

## Protocol Skills (Background)

| Skill | Description | Activation |
|---|---|---|
| `managing-memory` | Memory read/write/search protocol | Session start, during session |
| `managing-workspaces` | Workspace creation and management | Project start |
| `invoking-agents` | Specialist agent invocation protocol | When delegation needed |
| `checking-manifests` | Check skills and tools before acting | Before any task |

## Meta Skills

| Skill | Description | Invocation |
|---|---|---|
| `creating-skills` | Build new skills to agentskills.io spec | `/creating-skills` |
| `improving-skills` | Error recovery and learning loop | Automatic on failure |
| `restoring-system` | Self-healing and system repair | `/restoring-system` |
