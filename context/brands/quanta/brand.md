# Quanta Services — Brand Theme Reference

> Brand-specific tokens, typography, patterns, badges, and extended components for the Quanta Services HTML slide theme. All shared components from the [component library](../component-library.md) work with this theme — this file covers only what is unique to Quanta, see `theme.css` for the complete CSS.

---

## Color Tokens

| Token | Value | Role | Contract Alias |
|---|---|---|---|
| `--bolt` | `#F0941C` | Primary brand orange | `--accent` |
| `--bolt-light` | `#FFAE4D` | Hover / light accent | `--accent-light` |
| `--infrared` | `#CD0A1B` | Danger / emphasis red | `--accent-dark` |
| `--carbon` | `#221F1F` | Primary dark | `--primary` |
| `--carbon-light` | `#3A3535` | Dark panels | `--primary-light` |
| `--carbon-lighter` | `#575454` | Muted text | `--primary-lighter` |
| `--carbon-lightest` | `#8B8A8A` | Disabled / labels | `--primary-lightest` |

---

## Typography

| Role | Font | Weight | Style |
|---|---|---|---|
| Headings | Oswald | 600 / 700 | Uppercase, letter-spacing 0.04em |
| Body | Source Sans 3 | 300 / 400 / 600 | Normal case, line-height 1.6 |
| Code | Courier New | — | Monospace fallback |

Fonts load from Google Fonts CDN — requires internet.

---

## Pattern Overlays

Quanta uses diagonal hatch patterns on dark / accent slides to add texture:

- `.slide-dark::before` — subtle white 45° hatch lines (`rgba(255,255,255,0.015)`)
- `.slide-accent::before` — bolt-orange 45° hatch lines (`rgba(240,148,28,0.06)`)

These are pure CSS; no image assets required.

---

## Badge Variants

| Class | Color | Use |
|---|---|---|
| `.badge-bolt` | Bolt orange on transparent | Default brand tag |
| `.badge-infrared` | Infrared red | Warning / critical / risk |
| `.badge-neutral` | Carbon gray | De-emphasized / info |
| `.badge-success` | Green | Positive / complete |

---

## Quanta-Only Extended Components

These components are **only available** with the Quanta theme:

| Component | Classes | Purpose |
|---|---|---|
| Comparison card | `.comparison-card`, `.comparison-panel`, `.comparison-vs` | A vs B / Before → After split |
| Horizontal timeline | `.h-timeline`, `.timeline-item`, `.timeline-dot` | Phase milestones (horizontal) |
| Quote block | `.quote-block`, `.quote-text`, `.quote-attribution` | Attributed quotes with decorative mark |
| Maturity scale | `.maturity-scale`, `.maturity-track`, `.maturity-level` | 1–5 progress gauge |
| Step list | `.step-list`, `.step-item`, `.step-num` | Numbered vertical steps |
| Icon grid | `.icon-grid`, `.icon-item`, `.icon-glyph` | Tiled icon + label + description |
| Split stat | `.split-stat`, `.split-stat-value` | Hero metric with context |
| Tag cluster | `.tag-cluster`, `.tag-group`, `.tag` | Grouped keyword tags |
| Process flow | `.process-flow`, `.process-step` | Horizontal pipeline with arrows |
| KPI card grid | `.kpi-grid`, `.kpi-card`, `.kpi-trend` | Dashboard KPI tiles |
| Runbook phases | `.runbook-phases`, `.runbook-phase` | Multi-phase operational playbook |

---

## Logo Usage

- Reference the Quanta Services logo SVG; never rasterize
- Nav sidebar: place inside `.nav-brand` — will inherit `--bolt` color
- No cover-slide watermark pattern (unlike Credera)

---

## Photography Guidelines

- Industrial / infrastructure imagery preferred
- High-contrast, bold compositions
- Never use stock office photos

---

## Sub-Branding

When presenting as a Quanta subsidiary (e.g., Cupertino Electric, PAR Western):
- Keep Quanta nav brand
- Add subsidiary name in `.nav-brand-sub`
- May adjust `--accent` color via CSS custom property override

---

## Section Color Strategy

| Section | Slide class | Notes |
|---|---|---|
| Title / closing | `.slide-dark` | Carbon background, Bolt headline |
| Section divider | `.slide-accent` | Carbon gradient + orange hatch |
| Core content | `.slide-light` or `.slide-gray` | Legibility first |
| Data-heavy | `.slide-dark` | Tables, KPIs pop on dark bg |
