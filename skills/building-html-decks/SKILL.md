---
name: building-html-decks
description: Creates interactive, single-file HTML slide deck presentations using the Phalanx slide engine with pluggable CSS themes. Follows the PRESENT workflow — prepare content, select theme, build deck, style, evaluate, deliver. Triggers for requests like "create a presentation", "build a slide deck", or "deckify this content".
allowed-tools: Terminal
---

# HTML Slide Deck Builder — PRESENT Workflow

Create interactive, single-file HTML slide presentations using the **Phalanx slide engine**.

**PRESENT** is a 7-step process:

| Step | Phase | What You Do |
|------|-------|-------------|
| **P** | Prepare | Gather content, confirm audience, scope |
| **R** | Resolve | Select theme, read engine references, plan structure |
| **E** | Engineer | Build the deck following structural rules |
| **S** | Style | Visual polish — background variety, component balance |
| **E** | Evaluate | Review against checklist, fix issues |
| **N** | Notify | Save to workspace, record in memory |
| **T** | Transfer | Deliver to user |

---

## P — Prepare

Answer before building:

1. **Content?** — Source material. If nothing provided, ask.
2. **Audience?** — Determines tone (see `context/style-guide.md`)
3. **Goal?** — Inform, persuade, teach, status update, sales pitch
4. **Slide count?** — Default: 8-15
5. **Brand?** — Check `config.yaml` for `default_theme`. Default: Minimal.

Output a brief and confirm with user before proceeding.

---

## R — Resolve

### Theme Selection

Ask the user:

> **Which theme?**
> 1. **Minimal** — System fonts, slate/blue (brand-agnostic default)
> 2. **Credera** — Source Serif Pro + Lato, coral/charcoal (3 variants)
> 3. **Quanta** — Oswald + Source Sans 3, bolt orange/carbon
> 4. **Custom** — User provides CSS

For **Credera** variants: Navy+Purple (default), Green+Yellow (`data-variant="green"`), Maroon+Pink (`data-variant="maroon"`).

For **Quanta**: see `context/quanta-brand.md` for brand guidelines.

### Read Engine References

| File | Purpose |
|------|---------|
| `context/templates/presentations/base-template.html` | Canonical HTML + JS engine |
| `context/templates/presentations/themes/_contract.md` | CSS contract |
| Selected theme `.css` file | Visual tokens |
| `reference/component-library.md` (this skill) | Full component reference |
| Theme companion `*-components.md` (if brand theme) | Extended components |

### Plan Slide Structure

Map content to slides. Assign background types (dark, light, gray, accent). Choose components per slide — match visual shape to content shape. **No more than 2 consecutive slides may use the same component category.**

---

## E — Engineer

### Structural Rules

| Rule | Detail |
|------|--------|
| Template | Start from `base-template.html`. Replace `<link>` with chosen theme. |
| Slide indexing | Every `.slide` has `data-index="N"` starting at 0, sequential, no gaps. |
| First slide | Must include `class="visible"`. |
| Nav links | Each `.nav-link` has `data-slide="N"` matching a slide. |
| Slide number | `.slide-number` text reads `N / TOTAL` (1-indexed). |
| Progress | `totalSlides` auto-calculates from DOM. No manual constants. |
| Background types | One per slide: `.slide-dark`, `.slide-light`, `.slide-gray`, `.slide-accent`. |
| Inline delivery | Single `.html` file — inline theme CSS, move `@import` to `<link>` tags. |
| Responsive | Content typography uses `clamp()`. `.slide-inner` uses `max-width: 90%`. |

### Slide Anatomy

```html
<div class="slide slide-light" data-index="N">
    <div class="slide-inner">
        <p class="section-eyebrow">SECTION LABEL</p>
        <h2 class="slide-title">Slide Title</h2>
        <!-- Components from reference/component-library.md -->
    </div>
    <div class="slide-footer"></div>
    <div class="slide-number">N+1 / TOTAL</div>
</div>
```

### Agent Delegation

- **technical-writer** for content drafting
- **creative-director** for custom visuals

---

## S — Style

Checklist:

- [ ] Background types alternate (no 3 consecutive same-type)
- [ ] Component variety (no 3+ consecutive box-grid slides)
- [ ] Stat grids use meaningful, quantified data
- [ ] Section eyebrows used consistently
- [ ] Nav section labels group slides logically
- [ ] Slide 0 hero title is impactful

---

## E — Evaluate

- [ ] All `data-index` values sequential
- [ ] All `.nav-link[data-slide]` match slide indices
- [ ] First slide has `class="visible"`
- [ ] Theme CSS fully inlined
- [ ] `@import` URLs in `<link>` tags
- [ ] All 4 slide types render correctly
- [ ] Navigation (keyboard, wheel, touch, nav clicks) works
- [ ] No placeholder text (search `{{`, `TODO`, `TBD`)

---

## N — Notify

Save to `workspace/<project-slug>/presentations/<deck-name>.html`.

Record: `python tools/memory/memory_write.py --content "Presentation delivered: <deck-name>" --type event --importance 5`

---

## T — Transfer

Confirm file location. Note gaps or follow-ups. Theme changes only require CSS swap.

---

## Content Rules

1. Do not invent content — use only what the user provides
2. Headlines are punchy, bold, action-oriented, no periods
3. Bullets never have periods, are verb-driven when possible
4. Details on the page must support the headline
5. Include a legend if data elements have colours
6. Use footnotes for sources, assumptions, or pertinent details

---

## Edge Cases

- **No content** — Ask for source material. Don't generate placeholders.
- **Brand theme unavailable** — Offer to build custom CSS satisfying the contract.
- **Very long content** — Split into multiple decks. Max ~25 slides per deck.
- **Content update** — Read existing `.html`, modify in place, preserve `data-index` sequencing.
- **Custom components** — Build inline in `<style>`. If reusable, add to theme CSS.

---

## Workspace Structure

```
workspace/<project-slug>/
├── presentations/
│   └── <deck-name>.html
└── notes/
    └── slide-plan.md (optional)
```
