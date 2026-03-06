---
name: generating-architecture-diagrams
description: Generates professional cloud architecture diagram images using structured prompt templates for image generation models. Produces clean, flat-design diagrams with tiered layouts, labeled components, and styled connections. Used by the creating-visuals and designing-architecture skills.
allowed-tools: Terminal
---

# Architecture Diagram Prompt Builder

Construct image generation prompts that produce clean, professional cloud architecture diagrams.

---

## Prompt Template

```
Create a clean, professional, flat-design cloud architecture diagram on a white background.

Layout: The diagram is organized in [NUMBER] horizontal tiers flowing from top to bottom:
- [TIER 1 NAME]: [Components in this tier]
- [TIER 2 NAME]: [Components in this tier]
- [TIER 3 NAME]: [Components in this tier]

Components:
[For each component, specify:]
- [COMPONENT NAME] - shown as a [shape/icon description] labeled "[LABEL TEXT]", positioned [POSITION]

Connections:
[For each connection, specify:]
- [SOURCE] connects to [TARGET] via a [solid/dashed] arrow labeled "[PROTOCOL/LABEL]"

Visual Style:
- Color palette: [PRIMARY COLOR] for compute/processing, [SECONDARY COLOR] for storage/data, [ACCENT COLOR] for networking/security, [NEUTRAL COLOR] for backgrounds and borders
- Each component has a subtle drop shadow and rounded corners
- Arrows are [COLOR] with labeled connection descriptions
- All text uses a clean sans-serif font
- The diagram includes a light gray dashed-line boundary around each tier/zone labeled with the tier name

Title: "[DIAGRAM TITLE]" displayed prominently at the top in [COLOR] text

This diagram illustrates [PURPOSE].
```

---

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[NUMBER]` | Number of tiers/zones | 3 |
| `[TIER N NAME]` | Architectural tier name | Presentation, Application, Data |
| `[COMPONENT NAME]` | Service or component | EC2 Auto Scaling Group |
| `[LABEL TEXT]` | Text shown on component | "ALB" |
| `[POSITION]` | Spatial location | top center, bottom left |
| `[SOURCE]` / `[TARGET]` | Connection endpoints | CloudFront → ALB |
| `[PROTOCOL/LABEL]` | Connection description | "HTTPS", "PostgreSQL :5432" |
| `[PRIMARY/SECONDARY/ACCENT COLOR]` | Hex codes | #FF9900, #3B48CC |
| `[DIAGRAM TITLE]` | Top title | "AWS 3-Tier Architecture" |
| `[PURPOSE]` | What the diagram shows | "a migration target-state architecture" |

---

## Color Conventions

| Platform | Compute | Networking | Storage | Security |
|----------|---------|------------|---------|----------|
| AWS | #FF9900 (orange) | #3B48CC (blue) | #3ECF8E (green) | #DD344C (red) |
| Azure | #0078D4 (blue) | #50E6FF (cyan) | #773ADC (purple) | #E74856 (red) |
| GCP | #4285F4 (blue) | #34A853 (green) | #EA4335 (red) | #FBBC04 (yellow) |

---

## Tips

- Keep to 8-12 components maximum per diagram for readability
- If the architecture is complex, split into multiple diagrams (network view, application view, data flow view)
- Always include a title and tier/zone boundaries
- Name every component explicitly — never use vague terms like "several services"
- Specify spatial relationships: top-left, center, connected by, flows from

---

## Tool

```bash
python tools/media/generate_image.py \
  --prompt "<composed prompt>" \
  --output "workspace/<project-slug>/visuals/<name>.png" \
  --aspect-ratio 16:9
```
