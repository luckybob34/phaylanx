# PPTX Theme Contract

> Every PPTX theme directory must contain these files and satisfy this contract.
> This mirrors `_contract.md` for HTML themes.

---

## Required Files

```
themes/pptx/<theme-name>/
├── template.pptx          # Source PPTX with slide masters, layouts, colour scheme
├── config.yaml            # Layout mapping, colour tokens, font config
└── components.md          # Docs for available component renderers
```

## config.yaml Structure

```yaml
name: theme-name
display_name: "Theme Display Name"

# Map outline layout keys → template layout indices
layouts:
  title: 3
  section_gradient: 8
  section_photo: 7
  content: 21                # workhorse: title + subtitle + body area
  content_titled: 19         # title only (for custom-drawn body)
  blank: 0
  stat: 17
  quote: 23
  two_qualities: 22
  end: 33

# Colour tokens (hex, no #)
colors:
  primary: "3A3A3A"
  primary_light: "9B9B9B"
  accent: "E55F4C"
  accent_light: "F08878"
  accent_dark: "C94A38"
  background: "FFFFFF"
  background_warm: "F8F5F2"
  text_on_dark: "FFFFFF"
  text_on_light: "3A3A3A"
  text_muted: "9B9B9B"

# Extended palette for components
palette:
  blue: "496986"
  light_blue: "5CA2D1"
  gold: "E9A867"
  sage: "6A9E98"
  ice: "D7ECF3"

# Colour variants (override colors above)
variants:
  sage:
    accent: "6A9E98"
    accent_light: "8FBFB3"
    accent_dark: "4F7A70"
  warm:
    accent: "496986"
    accent_light: "6A8BA5"
    accent_dark: "364F65"

# Font configuration
fonts:
  heading:
    name: "Source Serif Pro SemiBold"
    size_title: 28            # pt
    size_section: 24
    size_slide: 20
    bold: true
  body:
    name: "Lato"
    size: 12
    size_small: 10
    bold: false
  mono:
    name: "Consolas"
    size: 10

# Slide dimensions (auto-detected from template, here for reference)
slide:
  width_in: 13.333
  height_in: 7.5

# Content area margins (inches from edge)
margins:
  left: 0.66
  right: 0.66
  top: 0.67
  bottom: 0.75
  content_top: 1.8           # below title area
```

## Layout Mapping Rules

- Every outline `layout` key must map to either a template layout index OR the string `"draw"` (meaning: use a blank layout and render everything programmatically)
- Template layouts are used for their background treatment, colour blocks, and decorative elements
- Content is always placed programmatically (placeholders in custom templates are unreliable across editors)

## Colour Token Rules

- All hex values without `#` prefix (python-pptx `RGBColor` expects this)
- `primary` = main text colour
- `accent` = brand highlight colour
- `background` = slide background
- `background_warm` = alternate warm background
- Variants override only the keys listed (others fall through to defaults)
