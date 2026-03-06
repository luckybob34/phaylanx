# Credera — Brand Theme Reference

> Brand-specific tokens, typography, logo, variants, and extended components for the Credera HTML slide theme. All shared components from the [component library](../component-library.md) work with this theme — this file covers only what is unique to Credera, see `theme.css` for the complete CSS, `pptx-config.yaml` for PPTX configuration.

---

## Color Tokens

Colors extracted from the 2024 Credera Global PowerPoint Accelerator PPTX theme.

| Token | Value | Role |
|---|---|---|
| `--credera-red` | `#E55F4C` | Brand mark, logo, bookend backgrounds |
| `--accent` | `#E55F4C` | Interactive accent (borders, highlights, badges) |
| `--accent-light` | `#F08878` | Hover states, light accents |
| `--accent-dark` | `#C94A38` | Pressed states, emphasis |
| `--navy` | `#3A3A3A` | Primary dark / text |
| `--slate-blue` | `#496986` | Extended palette |
| `--sky-blue` | `#5CA2D1` | Charts, secondary highlights |
| `--warm-gold` | `#E9A867` | Callouts, Sage variant accent |
| `--sage` | `#6A9E98` | Subtle accents, Sage variant |
| `--light-gray` | `#F8F5F2` | Page backgrounds, covers |
| `--ice-blue` | `#D7ECF3` | Light info backgrounds |

---

## Theme Variants

| Variant | `data-variant` | Dark Tone | Accent | Usage |
|---|---|---|---|---|
| Coral + Charcoal | *(default)* | `#3A3A3A` | `#E55F4C` | Default, most versatile |
| Sage + Gold | `"sage"` | `#2A3D36` | `#E9A867` | Sustainability, growth, advisory |
| Warm + Slate | `"warm"` | `#4A3728` | `#496986` | Understated, enterprise, finance |

Apply via `data-variant="sage"` or `data-variant="warm"` on `<html>`. CSS-only swap — no HTML or JS changes needed.

---

## Typography

- **Headlines**: Source Serif Pro SemiBold, uppercase, letter-spacing +2px
- **Subheadlines**: Source Serif Pro, regular, uppercase, letter-spacing +1px
- **Labels**: Lato Bold, all-caps, character spacing +0.5
- **Body**: Lato, line height 1.6
- **Icons**: Font Awesome 6 — never emojis

Fonts load from CDN — requires internet.

---

## Logo (SVG)

Nav sidebar — place inside `.nav-brand`:
```html
<div class="nav-brand">
  <svg class="nav-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 32" fill="none">
    <!-- 8 path elements: brand mark + "Credera" letterforms -->
    <!-- Use fill="currentColor" to inherit text color -->
  </svg>
</div>
```

Cover/bookend — place inside `.cover-logo` with `opacity: 0.12` for watermark:
```html
<div class="cover-logo">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 32" fill="none">
    <!-- Same paths, fill="var(--accent)" -->
  </svg>
</div>
```

---

## Credera-Only Components

These components are **only available** with the Credera theme:

| Component | Classes | Purpose |
|---|---|---|
| Cover slide | `.slide-cover`, `.cover-date`, `.cover-title`, `.cover-logo` | Branded cover with logo watermark |
| Callout accent | `.callout-accent` | Red-branded callout (uses `--credera-red`) |
| Success highlight | `.success-highlight`, `.highlight-text` | Large gradient callout with accent heading |
| Question items | `.question-item`, `.question-number`, `.question-text` | Discussion prompt rows |
| Program elements | `.program-elements`, `.program-element` | Horizontal dark-slide panels |
| Capabilities band | `.capabilities-band`, `.capabilities-grid` | Full-width dark capability showcase |
| Equation layout | `.equation-layout`, `.equation-column`, `.equation-operator` | Visual A + B = C equations |
| Materials grid | `.materials-grid`, `.material-section`, `.material-thumbs` | Thumbnail sections for deliverables |
| Participants grid | `.participants-grid`, `.participant-group` | Stakeholder group cards |
| Card variants | `.card-dark`, `.card-clickable`, `.card-arrow`, `.card-icon`, `.card-type`, `.card-img` | Extended card styles |
| Status badge | `.status-badge` | Accent-bg inline badge |

---

## Section Color Strategy

- **Title/closing**: Bookend with `.slide-dark` or Credera Red backgrounds (sparingly)
- **Dark sections**: `.slide-dark`, `.slide-accent` for high-impact
- **Content**: `.slide-light` or `.slide-gray` for text-heavy slides
- **Never mix** accent colors within the same section
