---
name: building-pptx-decks
description: Creates branded PowerPoint (.pptx) presentations from structured YAML outlines using the PPTX rendering engine with pluggable themes. Follows the PRESENT workflow — prepare, resolve theme, write outline, style, render, deliver. Triggers for "create a PowerPoint", "build a pptx deck", or "deckify for PowerPoint".
allowed-tools: Terminal
---

# PPTX Slide Deck Builder — PRESENT Workflow

Create branded PowerPoint presentations from structured YAML outlines.

**PRESENT** is a 7-step process:

| Step | Phase | What You Do |
|------|-------|-------------|
| **P** | Prepare | Gather content, confirm audience, scope |
| **R** | Resolve | Select theme + variant, plan structure |
| **E** | Engineer | Write YAML outline per spec |
| **S** | Style | Visual polish — component variety, colour balance |
| **E** | Evaluate | Render, validate output |
| **N** | Notify | Save to workspace, record in memory |
| **T** | Transfer | Deliver to user |

---

## P — Prepare

1. **Content?** — Source material. Ask if nothing provided.
2. **Audience?** — Determines tone and depth.
3. **Goal?** — Inform, persuade, teach, update.
4. **Slide count?** — Default: 8-15.
5. **Format?** — If user says "presentation", ask: HTML or PPTX?
6. **Brand?** — Check themes in `context/templates/presentations/themes/pptx/`.

---

## R — Resolve

### Theme Selection

Available themes are directories in `context/templates/presentations/themes/pptx/`.

**Credera** variants:
1. **Default** — Coral Red `#E55F4C` accent
2. **Sage** — Sage Green `#6A9E98` — set `variant: sage`
3. **Warm** — Slate Blue `#496986` — set `variant: warm`

### Read References

| File | Purpose |
|------|---------|
| `reference/outline-spec.md` (this skill) | Full YAML outline format |
| Theme `config.yaml` | Layout mapping, colours, fonts |
| Theme `components.md` | Available renderers |

### Plan Slides

Map content to slides. Choose layout per slide. Verify component variety — no 3+ from same category.

---

## E — Engineer

Write a YAML outline following `reference/outline-spec.md` exactly.

```yaml
meta:
  title: "Deck Title"
  theme: credera
  variant: default
  author: "Author Name"
  date: ""

slides:
  - layout: title
    title: "..."
    subtitle: "..."
  - layout: section
    title: "..."
    style: gradient
```

### Layout Quick Reference

| Category | Layouts |
|----------|---------|
| Structural | `title`, `section`, `end`, `blank` |
| Content | `content`, `two-col` |
| Data | `stat-grid`, `card-grid`, `data-table`, `highlight-grid` |
| Flow | `step-flow`, `funnel`, `timeline`, `ascend` |
| Structure | `layer-stack`, `hub-spoke` |
| Process | `process-loop` |
| Comparison | `comparison` |
| Feature | `stat`, `quote` |

### Agent Delegation

- **technical-writer** for slide copy
- **creative-director** for custom visuals

---

## S — Style

- [ ] Alternate layout types (no 3 consecutive same-category)
- [ ] Stat values are short (1-4 chars)
- [ ] Eyebrows used consistently
- [ ] Section breaks between logical groups
- [ ] First slide: impactful title. Last slide: `end` layout.

---

## E — Evaluate

### Render

```bash
python tools/presentations/render_pptx.py workspace/<project-slug>/notes/outline.yaml -o workspace/<project-slug>/presentations/<deck-name>.pptx
```

### Validate

- [ ] Correct slide count
- [ ] Each slide uses expected layout
- [ ] Content slides have reasonable shape counts (not 0)
- [ ] File opens in PowerPoint/Google Slides
- [ ] Speaker notes populated
- [ ] No placeholder text remaining

---

## N — Notify

Save: `workspace/<project-slug>/presentations/<deck-name>.pptx`

Record: `python tools/memory/memory_write.py --content "PPTX deck delivered: <deck-name>" --type event --importance 5`

---

## T — Transfer

Confirm file location. To change variant, re-render with `-v <variant>`. For HTML version, use `building-html-decks`.

---

## Content Rules

1. Do not invent content
2. Headlines: punchy, bold, no periods
3. Bullets: no periods, verb-driven
4. Stat values: 1-4 chars ("98%", "$4M", "3x")
5. Speaker notes on every content slide
6. 10-20 slides is the sweet spot

---

## Edge Cases

- **No content** — Ask for source material
- **Theme unavailable** — Offer to create per `themes/pptx/_contract.md`
- **Very long content** — Split into multiple decks, max ~20 slides
- **Content update** — Edit YAML and re-render (idempotent)
- **Both formats** — Same outline, render to both HTML and PPTX

---

## Tools

| Tool | Purpose |
|------|---------|
| `tools/presentations/parse_outline.py` | Parse YAML → normalised JSON |
| `tools/presentations/render_pptx.py` | Render outline + theme → .pptx |
| `tools/presentations/inspect_template.py` | Inspect PPTX template |

---

## Workspace Structure

```
workspace/<project-slug>/
├── notes/
│   └── outline.yaml
└── presentations/
    └── <deck-name>.pptx
```
