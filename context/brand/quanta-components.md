# Quanta Theme — Component Reference

> Components available when using `quanta.css`. All classes work on `.slide-dark`, `.slide-light`, `.slide-gray`, and `.slide-accent` backgrounds unless noted.

---

## Brand System

### Color Tokens

| CSS Variable | Value | Name |
|---|---|---|
| `--bolt` | `#F0941C` | Bolt Orange — primary brand color |
| `--bolt-light` | `#FFAE4D` | Bolt tint |
| `--infrared` | `#CD0A1B` | Infrared Red — accent / danger |
| `--carbon` | `#221F1F` | Carbon Black — primary dark |
| `--carbon-light` | `#3A3535` | Carbon +1 |
| `--carbon-lighter` | `#575454` | Carbon +2 |
| `--carbon-lightest` | `#8B8A8A` | Carbon +3, muted text |
| `--white` | `#FFFFFF` | White |
| `--light-gray` | `#F4F4F4` | Light background |

Contract token aliases: `--primary` → carbon, `--accent` → bolt, `--accent-dark` → infrared.

### Typography

| Role | CSS Variable | Web Font | Fallback | Notes |
|---|---|---|---|---|
| Headings | `--font-heading` | Oswald | Arial, sans-serif | Always uppercase, letter-spacing 0.04em |
| Body | `--font-body` | Source Sans 3 | Arial, sans-serif | Weight 300/400/600 |

> Web substitutes for the official Quanta typefaces: Alternate Gothic Extra Condensed ATF (headings) and Proxima Nova (body). See `context/quanta-brand.md` for full typography hierarchy.

### Pattern Overlays

`.slide-dark` and `.slide-accent` include an automatic diagonal-hatched overlay (`repeating-linear-gradient` at 45°) matching the Quanta brand pattern system. No extra markup needed.

---

## Slide Types

| Class | Background | Use For |
|---|---|---|
| `.slide-dark` | Carbon `#221F1F` + diagonal grid | Hero/title, stats, key metrics, section covers |
| `.slide-light` | White | Tables, dense content, runbooks, light-bg-only components |
| `.slide-gray` | `#F4F4F4` | Two-column layouts, supporting/body slides |
| `.slide-accent` | Carbon gradient + bolt diagonal overlay | Section divider transitions, chapter breaks |

Slide footer: all slides get a 3px `bolt → infrared` gradient bar at the bottom automatically via `.slide-footer`.

---

## Component Library

### Layout

#### `.two-col`
Two-column 1:1 grid layout. Wrap columns in a container inside `.slide-inner`.
```html
<div class="two-col">
  <div>
    <div class="two-col-header">Left Column</div>
    <!-- content -->
  </div>
  <div>
    <div class="two-col-header">Right Column</div>
    <!-- content -->
  </div>
</div>
```
- `.two-col-header` — uppercase bolt-colored column label with bottom border

---

### Metrics

#### `.stat-grid` / `.stat-item` / `.stat-value` / `.stat-label`
Large-number KPI grid. Auto-fits columns with `minmax(140px, 1fr)`.
```html
<div class="stat-grid">
  <div class="stat-item">
    <div class="stat-value">98%</div>
    <div class="stat-label">Uptime SLA</div>
  </div>
</div>
```
- On `.slide-light` / `.slide-gray`: white card with drop shadow
- On dark slides: semi-transparent with bolt top border

---

### Callouts & Highlights

#### `.callout` / `.callout-label`
Left-border quote or note box. Bolt orange 3px left border.
```html
<div class="callout">
  <div class="callout-label">Key Insight</div>
  <p>Supporting text here.</p>
</div>
```

#### `.highlight-grid` / `.highlight-box`
Auto-fit grid of fact/callout boxes with bolt border and background tint.
```html
<div class="highlight-grid">
  <div class="highlight-box">
    <strong>Capability</strong>
    <p>Description of the capability.</p>
  </div>
</div>
```

---

### Cards

#### `.card-grid` / `.card`
Auto-fit card grid (`minmax(200px, 1fr)`). White cards with bolt top border.
```html
<div class="card-grid">
  <div class="card">
    <div class="card-body">
      <h4>Card Title</h4>
      <p>Card body text.</p>
    </div>
  </div>
</div>
```
- On `.slide-dark`: semi-transparent dark card, bolt-light title

---

### Lists

#### `.program-element-list`
Icon-prefixed feature/principle list. Auto-fit grid, bolt `▸` prefix.
```html
<ul class="program-element-list">
  <li>
    <div>
      <strong>Feature Name</strong>
      <p>Brief description of this feature or principle.</p>
    </div>
  </li>
</ul>
```

#### `.pillar-grid` / `.pillar`
Icon + label + text pillar columns. Centered, bolt top border.
```html
<div class="pillar-grid">
  <div class="pillar">
    <div class="pillar-icon">⚡</div>
    <h3>Pillar Name</h3>
    <p>Supporting description.</p>
  </div>
</div>
```

---

### Tables

#### `.data-table`
Full-width bordered table. Bolt-colored headers on carbon background.
```html
<table class="data-table">
  <thead>
    <tr><th>Column A</th><th>Column B</th></tr>
  </thead>
  <tbody>
    <tr><td>Value</td><td>Value</td></tr>
  </tbody>
</table>
```
- Row hover: subtle bolt tint
- On `.slide-dark`: headers use translucent white background

---

### Operational

#### `.runbook-phases` / `.runbook-phase`
Numbered operational step phase cards. Bolt top border, arrow-prefixed list items.
```html
<div class="runbook-phases">
  <div class="runbook-phase">
    <div class="runbook-phase-header">
      <span class="phase-num">01</span>
      <span class="phase-title">Assess</span>
    </div>
    <ul>
      <li>Step one</li>
      <li>Step two</li>
    </ul>
  </div>
</div>
```

#### `.code-block`
Dark monospace code snippet with bolt left border.
```html
<div class="code-block">
  terraform apply -var-file="prod.tfvars"
</div>
```
- On `.slide-light` / `.slide-gray`: light background variant

---

### Badges

#### `.badge` + modifier
Small inline label chips. Add one modifier class.

| Class | Color | Use |
|---|---|---|
| `.badge-bolt` | Bolt orange | Active, primary, featured |
| `.badge-infrared` | Infrared red | Risk, critical, required |
| `.badge-neutral` | Gray | Informational, secondary |
| `.badge-success` | Green | Complete, approved, healthy |

```html
<span class="badge badge-bolt">Active</span>
<span class="badge badge-infrared">Critical</span>
```

---

## Nav & JS Conventions

- Each `.nav-link` that navigates must have `data-slide="N"` (0-indexed from 0)
- Section labels that group links (non-clickable) use `.nav-section-label`
- Visual separators use `.nav-divider`
- `const TOTAL_SLIDES = N` at the top of `<script>` must match actual slide count
- `goToSlide(index)` is the only navigation function
- Keyboard: Arrow keys, Space/PageDown, Home/End work automatically
- Touch swipe threshold: 50px. Wheel debounce: 50ms

---

## Creating a New Quanta Presentation

1. Copy `context/templates/presentations/base-template.html` → `workspace/<project-slug>/presentation/index.html`
2. Change the `<link>` theme reference to `quanta.css`
3. Update `<title>`, `.nav-brand` text, and `TOTAL_SLIDES`
4. Replace placeholder slides — keep `data-index` values sequential from 0
5. Update `.nav-list` items — one `.nav-link[data-slide]` per navigable slide
6. Update `progress-fill` initial width: `(1 / TOTAL_SLIDES * 100)%`

### Background selection guide

- **Start** with `.slide-dark` (hero/title)
- **Alternate** `.slide-gray` and `.slide-dark` for body slides
- **Use** `.slide-light` for dense tables and runbooks
- **Use** `.slide-accent` sparingly — section dividers only
- **Avoid** using the same background 3+ times in a row

---

## Known Limitations

- Font sizes use fixed `rem` units (contract recommends `clamp()` for full viewport responsiveness). Works correctly at standard desktop resolutions. Flagged for future responsive pass.
- Fonts (Oswald, Source Sans 3) load from Google Fonts — requires internet access to render correctly.

---

## Extended Components — v2

> Added in the quanta-style-guide visual library expansion. Preview all 10 in `workspace/quanta-style-guide/sample-visuals.html`.

### 1. Comparison Card

Side-by-side two-panel layout with center VS divider. Use for Before/After, Option A vs B, Current vs Target.

```html
<div class="comparison-card">
    <div class="comparison-panel">
        <div class="comparison-panel-label">Option A</div>
        <ul>
            <li>Point one</li>
            <li>Point two</li>
        </ul>
    </div>
    <div class="comparison-divider">
        <span class="comparison-vs">VS</span>
    </div>
    <div class="comparison-panel">
        <div class="comparison-panel-label">Option B</div>
        <ul>
            <li>Point one</li>
            <li>Point two</li>
        </ul>
    </div>
</div>
```

Works on all slide backgrounds. Panel background auto-adjusts for light/gray slides.

---

### 2. Horizontal Timeline

Left-to-right timeline with dot markers and date labels. Dot states: `complete` (past), `active` (current, bolt orange), `future` (hollow).

```html
<div class="h-timeline">
    <div class="timeline-item">
        <div class="timeline-dot complete"></div>
        <div class="timeline-date">Q1 2026</div>
        <div class="timeline-label">Phase Name</div>
        <div class="timeline-desc">Description of what happened or will happen.</div>
    </div>
    <!-- Repeat for each milestone -->
</div>
```

Note: Add `margin-top: 2.5rem` (already built in) — the dot sits above the top line so the element needs that breathing room.

---

### 3. Quote Block

Oversized decorative pull quote with attribution and role line. The `"` glyph renders as a large background decoration automatically.

```html
<div class="quote-block">
    <p class="quote-text">The quote text goes here.</p>
    <div class="quote-attribution">Person Name</div>
    <div class="quote-role">Title · Organization</div>
</div>
```

Best on `.slide-dark` for maximum contrast. Also works on `.slide-light` and `.slide-gray` with auto color swap.

---

### 4. Maturity Scale

5-level horizontal capability scale. Apply `complete`, `active`, or `future` to each `.maturity-level`. Add a `.maturity-desc` block below the track for the current level description.

```html
<div class="maturity-scale">
    <div class="maturity-track">
        <div class="maturity-level complete">
            <div class="maturity-num">1</div>
            <div class="maturity-label">Aware</div>
        </div>
        <div class="maturity-level active">
            <div class="maturity-num">2</div>
            <div class="maturity-label">Building</div>
        </div>
        <div class="maturity-level future">
            <div class="maturity-num">3</div>
            <div class="maturity-label">Scaling</div>
        </div>
    </div>
    <div class="maturity-desc">Current state description here.</div>
</div>
```

Scale can have 3–6 levels — `auto-fit` handles the column widths automatically.

---

### 5. Step List

Numbered steps with large ghost numerals. Vertical flow, more text-dense than runbook phases. Best for 3–6 sequential steps.

```html
<div class="step-list">
    <div class="step-item">
        <div class="step-num">1</div>
        <div class="step-content">
            <strong>Step Title</strong>
            <p>Step description with supporting detail.</p>
        </div>
    </div>
    <!-- Repeat -->
</div>
```

---

### 6. Icon Grid

Grid items with prominent emoji/icon prefix. Use for tool stacks, capabilities, feature lists. Works on dark and light slides.

```html
<div class="icon-grid">
    <div class="icon-item">
        <span class="icon-glyph">🤖</span>
        <div class="icon-label">Tool Name</div>
        <div class="icon-desc">Short description of what this tool does.</div>
    </div>
    <!-- Repeat -->
</div>
```

Use actual emoji or Unicode symbols for `.icon-glyph`. Icon grid auto-fits at `minmax(160px, 1fr)`.

---

### 7. Split Stat

Single large primary metric left-aligned with explanatory text right. Use for one headline number with a supporting narrative.

```html
<div class="split-stat">
    <div class="split-stat-figure">
        <span class="split-stat-value">40+</span>
        <span class="split-stat-unit">OpCos</span>
    </div>
    <div class="split-stat-divider"></div>
    <div class="split-stat-body">
        <span class="split-stat-label">Metric label</span>
        <p class="split-stat-desc">Supporting context and explanation for the metric.</p>
    </div>
</div>
```

`.split-stat-unit` is optional. The component flexes to fill available height.

---

### 8. Tag Cluster

Flexible pill tags in multiple colour variants. Group with `.tag-group` and `.tag-group-label`. Mix variants within a cluster.

```html
<div class="tag-cluster">
    <div class="tag-group">
        <div class="tag-group-label">Category</div>
        <span class="tag tag-primary">Primary Tag</span>
        <span class="tag tag-accent">Alert Tag</span>
        <span class="tag tag-success">Certified ✓</span>
        <span class="tag">Neutral Tag</span>
    </div>
</div>
```

| Variant | Colour | Use for |
|---------|--------|---------|
| `tag-primary` | Bolt orange | Key skills, confirmed items |
| `tag-accent` | Infrared red | Required, critical, blockers |
| `tag-success` | Green | Completed, certified, passed |
| *(no modifier)* | Gray | Baseline, neutral, pending |

---

### 9. Process Flow

Horizontal arrow-connected steps. More compact than runbook phases — suited for 4–6 quick steps. Arrow decoration is CSS-only via `.process-step-arrow`.

```html
<div class="process-flow">
    <div class="process-step">
        <div class="process-step-arrow"></div>
        <div class="process-step-num">Step 01</div>
        <div class="process-step-title">Step Name</div>
        <p>Short description.</p>
    </div>
    <!-- Repeat; last step omits .process-step-arrow -->
</div>
```

The last `.process-step` should omit `.process-step-arrow` (or it will show — the CSS hides the arrow on `:last-child` automatically).

---

### 10. KPI Card Grid

Metric cards with trend indicators. Use `kpi-trend-up` (green), `kpi-trend-down` (red), or `kpi-trend-flat` (gray) on the `.kpi-trend` element.

```html
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-value">94%</div>
        <div class="kpi-trend kpi-trend-up">↑ +6pts</div>
        <span class="kpi-label">Metric Name</span>
        <div class="kpi-context">Supporting context or baseline comparison.</div>
    </div>
    <!-- Repeat -->
</div>
```

Grid auto-fits at `minmax(180px, 1fr)`. Works on all slide backgrounds — light/gray slide overrides automatically applied.
