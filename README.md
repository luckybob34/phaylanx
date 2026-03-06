<p align="center">
  <img src="phalanx-logo.jpg" alt="Phalanx Framework" width="600">
</p>

# Phalanx

**A modular AI skills framework built on the [GOTCHA architecture](https://agentskills.io/) for Claude Code, GitHub Copilot, and OpenAI Codex.**

Named after the ancient Greek and Roman military formation where interlocking shields created an unstoppable coordinated unit, **Phalanx** applies the same principle to AI: specialist agents, each with a defined role and position, working in tight formation through deterministic tools and structured workflows. No single agent fights alone. The formation is the strength.

Phalanx provides a minimal core of essential skills — memory management, workspace organization, agent invocation, manifest checking, skill creation, self-improvement, system restoration, and bundle management — then lets you install optional bundles for cloud architecture, presentations, proposals, media generation, and more.

---

## Quick Start

Create a new project directory, open your AI coding assistant, and say:

> **"Bootstrap this project using https://github.com/td-project-ai/phalanx"**

The AI will fetch [bootstrap.md](bootstrap.md), detect your platform, install the core framework, generate the correct configuration files, initialize memory, and offer optional bundles — all automatically.

This works on **Claude Code**, **GitHub Copilot**, and **OpenAI Codex**. The bootstrap handles everything:

| Step | What Happens |
|------|-------------|
| 1 | Detects your platform (Claude Code / Copilot / Codex) |
| 2 | Fetches core skills, tools, and context from this repo |
| 3 | Generates platform-specific config (`CLAUDE.md`, `.github/copilot-instructions.md`, `AGENTS.md`) |
| 4 | Initializes persistent memory (MEMORY.md + SQLite databases) |
| 5 | Offers optional bundles — pick what you need |
| 6 | Verifies the installation |

---

## What's Included

### Core (Always Installed)

| Skill | Type | Purpose |
|-------|------|---------|
| `managing-memory` | Protocol | Persistent memory across sessions |
| `managing-workspaces` | Protocol | Project directory management |
| `invoking-agents` | Protocol | Specialist agent delegation |
| `checking-manifests` | Protocol | Pre-task manifest checks |
| `creating-skills` | Meta | Build new skills to agentskills.io spec |
| `improving-skills` | Meta | Error recovery and learning loop |
| `restoring-system` | Meta | Self-healing and system repair |
| `installing-bundles` | Meta | Bundle search, install, update, remove |

Plus: memory tools, platform tools, style guide, base HTML template, minimal CSS theme.

### Optional Bundles

| Bundle | Skills | Agents | Key Tools |
|--------|--------|--------|-----------|
| `cloud-architecture` | designing-architecture | aws-architect, azure-architect | architecture/* |
| `cloud-migration` | planning-cloud-migration | aws-architect, azure-architect | — |
| `cloud-iac` | deploying-infrastructure | iac-engineer, devops-engineer | iac/* |
| `cloud-review` | reviewing-architecture | aws-architect, azure-architect | — |
| `presentations-html` | building-html-decks, building-university-decks | — | — |
| `presentations-pptx` | building-pptx-decks | — | presentations/* |
| `proposals` | responding-to-rfps, building-sow | proposal-writer, researcher | proposals/* |
| `media` | creating-visuals, generating-*-diagrams/visuals | creative-director | media/* |
| `app-development` | building-apps | researcher, technical-writer | — |

---

## Bundle Management

```bash
# Search
python tools/platform/registry.py --search "cloud"

# List all
python tools/platform/registry.py --list

# Install
python tools/platform/registry.py --install cloud-architecture

# Update
python tools/platform/registry.py --update cloud-architecture
python tools/platform/registry.py --update-all

# Remove
python tools/platform/registry.py --remove cloud-architecture

# Show installed
python tools/platform/registry.py --installed
```

Or just tell your AI: *"Install the cloud architecture bundle"* — the `installing-bundles` skill handles the rest.

---

## Repository Structure

```
phalanx/
├── bootstrap.md          # AI-readable installation playbook
├── catalog.yaml          # Searchable bundle index
├── README.md
│
├── core/                 # Required framework core
│   ├── CLAUDE.md         # System handbook
│   ├── config.yaml       # Global configuration
│   ├── skills/           # 8 core skills
│   ├── tools/            # Memory + platform tools
│   └── context/          # Style guide, base template, minimal theme
│
├── bundles/              # Bundle manifests (YAML)
│   ├── cloud-architecture.yaml
│   ├── cloud-migration.yaml
│   ├── cloud-iac.yaml
│   ├── cloud-review.yaml
│   ├── presentations-html.yaml
│   ├── presentations-pptx.yaml
│   ├── proposals.yaml
│   ├── media.yaml
│   └── app-development.yaml
│
├── skills/               # Installable workflow + atomic skills
├── agents/               # Specialist agent definitions
├── tools/                # Domain-specific tool scripts
└── context/              # Brand guides and component docs
    └── brands/
        ├── component-library.md   # Shared components (brand-agnostic)
        ├── html-contract.md       # HTML CSS theme contract
        ├── pptx-contract.md       # PPTX theme contract spec
        ├── minimal/               # Minimal theme (brand.md + theme.css)
        ├── credera/               # Credera (brand.md, theme.css, pptx-config.yaml, ...)
        └── quanta/                # Quanta (brand.md + theme.css)
```

---

## Brand Themes

Phalanx separates **shared components** from **brand-specific styling** so you can add new brands without touching the component library.

### Architecture

| Layer | File | Purpose |
|-------|------|---------|
| **Contract** | `context/brands/html-contract.md` | CSS custom properties and selectors every theme must implement |
| **Components** | `context/brands/component-library.md` | Brand-agnostic HTML components (layouts, metrics, cards, flows, timelines, etc.) |
| **Brand Folder** | `context/brands/<brand>/` | `brand.md` (color tokens, typography, logo usage, brand-only components) + `theme.css` (complete CSS) |

### Included Brand

The **Minimal** theme ships with core — system fonts, slate/blue palette, works fully offline. It serves as the brand-agnostic default and the starting point for creating custom brands.

| File | Purpose |
|------|--------|
| `context/brands/minimal/brand.md` + `theme.css` | Default brand reference + theme CSS (installed with core) |

Additional brand themes (e.g., client-specific branding) can be installed via bundles or created manually using the steps below.

### Adding a New Brand

1. **Read the contract** — `context/brands/html-contract.md` defines every CSS custom property and selector your theme must implement.

2. **Clone the minimal brand** as a starting point:
   ```bash
   cp -r context/brands/minimal context/brands/mybrand
   ```

3. **Update CSS custom properties** — at minimum, set these in `:root`:
   ```css
   :root {
       --primary: #1A1A2E;      /* Dark backgrounds, text */
       --accent: #E94560;       /* Highlights, borders, badges */
       --accent-light: #FF6B81; /* Hover states */
       --accent-dark: #C73E54;  /* Pressed states */
       --light-gray: #F5F5F5;   /* Light slide backgrounds */
       --font-heading: 'Your Heading Font', sans-serif;
       --font-body: 'Your Body Font', sans-serif;
   }
   ```

4. **Create brand documentation** at `context/brands/mybrand/brand.md` documenting:
   - Color token table (all custom property values)
   - Typography stack (heading and body fonts, weights, letter-spacing)
   - Logo usage rules (if applicable)
   - Any brand-only components added in the CSS
   - Section color strategy (which slide types to use where)

5. **Test** — verify all 4 slide types render correctly (`.slide-dark`, `.slide-light`, `.slide-gray`, `.slide-accent`) and that every shared component from the component library works with your new theme.

6. **Register** — add the theme to `bundles/presentations-html.yaml` and `catalog.yaml` so it's installable via the registry.

All shared components from `component-library.md` work automatically — brand CSS only needs to define the visual tokens and any additional brand-specific selectors.

---

## How It Works

Phalanx uses the **GOTCHA Framework** — a 6-layer architecture that separates what AI is good at (reasoning, flexibility) from what must be deterministic (tool execution, file operations):

- **Skills** define workflows as markdown process docs
- **Tools** are Python scripts that execute deterministically
- **Agents** are specialist AI personas with domain expertise
- **Context** provides brand guides, templates, and reference material
- **Config** controls behavior without editing skills

Skills follow the [agentskills.io](https://agentskills.io/) open standard for cross-platform compatibility.

---

## Configuration

After installation, `config.yaml` in your project root controls behavior:

```yaml
# Theme and style
default_theme: minimal
default_tone: professional

# Registry (added during bootstrap)
registry:
  url: https://github.com/td-project-ai/phalanx
  branch: main
  auth_env: GITHUB_PAT
  cache_dir: .tmp/registry-cache
  cache_ttl: 3600
```

---

## License

MIT
