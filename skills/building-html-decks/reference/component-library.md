# Component Library — Phalanx Slide Engine

> Reference file for `building-html-decks`. Load when building slides to select the right component for each content shape.

---

## Typography

| Class | Usage |
|-------|-------|
| `.hero-title` | Large presentation title (slide 0) |
| `.hero-subtitle` | Brand name or category above hero title |
| `.hero-desc` | 1-2 sentence description below hero title |
| `.section-eyebrow` | Small uppercase label above slide title |
| `.slide-title` | Main heading on content slides (`h2`) |
| `.slide-subtitle` | Supporting line below slide title |

---

## Layout

| Class | Usage |
|-------|-------|
| `.two-col` | CSS Grid 2-column layout |
| `.two-col-header` | Column header label |
| `.stat-grid` | 3-column metrics grid |
| `.stat-item` / `.stat-value` / `.stat-label` | Individual metric |
| `.card-grid` | Auto-fit card layout |
| `.card` / `.card-body` | Content card |
| `.highlight-grid` / `.highlight-box` | Feature highlight cards |
| `.pillar-grid` / `.pillar` | Centred value pillars |

---

## Data & Callouts

| Class | Usage |
|-------|-------|
| `.data-table` | Full-width table with styled header |
| `.callout` / `.callout-label` | Left-border callout box |
| `.code-block` | Monospace code display |
| `.badge` / `.badge-accent` | Pill-shaped tag |

---

## Grid Helpers

| Class | Usage |
|-------|-------|
| `.grid-2` | 2-column grid |
| `.grid-3` | 3-column grid |
| `.grid-4` | 4-column grid |

---

## Visual Variety Patterns

Match the visual shape to the content shape — sequences get flows, comparisons get before/after, cycles get loops, hierarchies get radials.

### Flow & Sequence

| Class | Usage |
|-------|-------|
| `.step-flow` | Horizontal numbered nodes connected by arrows. 3-5 steps. Children: `.step-node` (`.step-node-number`, `.step-node-title`, `.step-node-desc`), `.step-arrow` (`.step-arrow-line`). |
| `.funnel` | Decaying horizontal bars. Children: `.funnel-bar` with `--bar-width` and `--bar-color` CSS vars. |
| `.ascend-timeline` | Ascending columns (short→tall). Children: `.ascend-node` (`.ascend-node-title`, `.ascend-node-desc`, `.ascend-node-stat`). |

### Structure & Hierarchy

| Class | Usage |
|-------|-------|
| `.layer-stack` | Stacked horizontal rows for tiered architecture. Children: `.layer-row` → `.layer-item`. |
| `.hub-spoke` | Radial layout with centre + satellites (max 8). Children: `.hub-center`, `.hub-spoke-node`, `.hub-spoke-lines` SVG. |
| `.annotated-stack` | Vertical layer stack with side annotations. Children: `.annotated-stack-layers` (`.annotated-stack-layer` with `--layer-color`) and `.annotated-stack-annotations` (`.annotated-stack-note`). |

### Comparison & Data

| Class | Usage |
|-------|-------|
| `.before-after` | Side-by-side panels with arrow separator. Children: `.before-panel`, `.ba-arrow`, `.after-panel`. |
| `.metric-strip` | Compact single-row dashboard of 3-5 figures. Children: `.metric-strip-item` (`.metric-strip-value`, `.metric-strip-label`). |

### Process & Cycle

| Class | Usage |
|-------|-------|
| `.process-loop` | Circular SVG ring with nodes around a centre icon. 4-6 nodes. Children: `.loop-ring` SVG, `.loop-center`, `.loop-node`. |

---

## Pattern Variety Rule

No more than **2 consecutive slides** may use the same component category:

- **Box grids**: `card-grid`, `highlight-grid`, `stat-grid`, `pillar-grid`, `two-col`
- **Flows**: `step-flow`, `funnel`, `ascend-timeline`
- **Structure**: `layer-stack`, `hub-spoke`, `annotated-stack`
- **Comparison/Data**: `before-after`, `metric-strip`, `data-table`
- **Process**: `process-loop`, `timeline`

When building a deck, plan the component sequence during outlining. If 3 slides default to box grids, swap one for a flow, structure, or comparison pattern.

---

## Navigation Anatomy

```html
<ul class="nav-menu">
    <li class="nav-section-label">Group Label</li>
    <li class="nav-item"><a class="nav-link active" data-slide="0">Slide Name</a></li>
    <li class="nav-item"><a class="nav-link" data-slide="1">Slide Name</a></li>
    <li class="nav-divider"></li>
    <li class="nav-section-label">Next Group</li>
    <li class="nav-item"><a class="nav-link" data-slide="2">Slide Name</a></li>
</ul>
```

---

## Theme-Specific Components

### Credera

Extended consulting-oriented components. Read: `context/templates/presentations/themes/credera-components.md`

Key additions: cover slides, horizontal timelines with dot states, question items, program elements, equation layouts, quote blocks/cards, capabilities bands, materials grids, participant grids.

### Quanta

Infrastructure/energy branding. Read: `context/templates/presentations/themes/quanta-components.md`

Key additions: diagonal-hatched pattern overlays, Bolt/Infrared dual-accent system, runbook phase cards, badge variants (`.badge-bolt`, `.badge-infrared`).

---

## Adding Brand Themes

Brand themes are CSS files satisfying the contract (`context/templates/presentations/themes/_contract.md`):

1. Create a `.css` file implementing all required selectors and custom properties
2. Place in `context/templates/presentations/themes/`
3. Document brand-specific components in a companion `*-components.md`

### Theme Variants

Override `:root` via `data-variant` on `<html>`:

```css
html[data-variant="alt"] {
    --primary: #173E2F;
    --accent:  #C8D630;
}
```
