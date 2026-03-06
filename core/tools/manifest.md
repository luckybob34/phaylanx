# Tools Manifest

> Master list of available tools. Check here before creating a new script.

## Architecture Tools

| Tool | Description |
|------|-------------|
| `tools/architecture/generate_architecture_doc.py` | Generate architecture documentation from brief inputs |
| `tools/architecture/estimate_costs.py` | Estimate monthly cloud costs from architecture specifications |

## IaC Tools

| Tool | Description |
|------|-------------|
| `tools/iac/scaffold_terraform.py` | Generate Terraform module scaffolding from module list |
| `tools/iac/validate_terraform.py` | Format, validate, lint, and security scan Terraform code |

## Media Tools

| Tool | Description |
|------|-------------|
| `tools/media/generate_image.py` | Generate images via OpenRouter (seedream-4.5) |
| `tools/media/analyze_image.py` | Analyze images via OpenRouter (Gemini Flash) |

## Memory Tools

| Tool | Description |
|------|-------------|
| `tools/memory/memory_read.py` | Read memory entries with formatted output |
| `tools/memory/memory_write.py` | Write facts, events, preferences to memory |
| `tools/memory/memory_db.py` | Direct database operations (search, list, delete) |
| `tools/memory/semantic_search.py` | Semantic search across memory entries |
| `tools/memory/hybrid_search.py` | Combined keyword + semantic memory search |
| `tools/memory/embed_memory.py` | Generate embeddings for memory entries |

## Presentation Tools

| Tool | Description |
|------|-------------|
| `tools/presentations/render_pptx.py` | Render PowerPoint from YAML outline |
| `tools/presentations/parse_outline.py` | Parse and validate YAML slide outlines |
| `tools/presentations/inspect_template.py` | Inspect PPTX template layouts and placeholders |

## Proposal Tools

| Tool | Description |
|------|-------------|
| `tools/proposals/parse_rfp.py` | Extract requirements from RFP documents |
| `tools/proposals/build_compliance_matrix.py` | Build compliance matrix from parsed requirements |
| `tools/proposals/generate_sow.py` | Generate SOW document from structured input |

## Platform Tools

| Tool | Description |
|------|-------------|
| `tools/platform/generate_instructions.py` | Generate Copilot and Codex instruction files from skill definitions |

---

> **Note:** Tools are inherited from the source GOTCHA framework. Copy `tools/` from `bootstrap-0/tools/` when deploying this workspace.
