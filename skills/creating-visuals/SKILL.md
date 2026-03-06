---
name: creating-visuals
description: Generates professional visual assets — architecture diagrams, proposal graphics, infographics, technical illustrations — using the RENDER workflow. Composes structured image generation prompts, generates via API, evaluates output, and iterates. Invokes the creative-director agent for visual direction.
allowed-tools: Terminal
agent: creative-director
---

# Visual Asset Generation — RENDER Workflow

Generate professional visual assets for consulting deliverables.

| Phase | What You Do |
|-------|-------------|
| **R** — Receive | Understand what's needed, audience, placement |
| **E** — Examine | Extract technical details from source material |
| **N** — Narrate | Compose image generation prompt |
| **D** — Draw | Generate image via API |
| **E** — Evaluate | Assess quality and accuracy |
| **R** — Refine | Iterate or deliver final assets |

---

## R — Receive

Gather: asset type (diagram, infographic, org chart, timeline), target audience, placement context (slide, document, standalone), aspect ratio, style preferences, brand constraints.

---

## E — Examine

1. Read source architecture doc, proposal section, or spec
2. List every component that must appear
3. Map relationships and data flows
4. Identify labels and annotations
5. Check `context/` for brand guidelines

---

## N — Narrate

Follow this prompt structure:

```
[Style]: "Clean, professional [style] diagram..."
[Layout]: "Organized as [layout description]..."
[Components]: "The following components: [each with position]..."
[Relationships]: "Arrows connect [A] to [B] labeled '[label]'..."
[Color palette]: "[hex codes]..."
[Text/Labels]: "[font description]..."
[Background]: "White/light gray..."
```

Rules:
- 3-4 sentences minimum for simple, 8-12+ for complex
- Name every component explicitly
- Specify spatial relationships
- Include purpose in the prompt

For architecture diagrams, use the `generating-architecture-diagrams` skill templates.
For proposal graphics, use the `generating-proposal-visuals` skill templates.

---

## D — Draw

```bash
python tools/media/generate_image.py \
  --prompt "<prompt>" \
  --output "workspace/<project-slug>/visuals/<name>.png" \
  --aspect-ratio <ratio> \
  --count 1
```

| Use Case | Ratio |
|----------|-------|
| Slides | `16:9` |
| Documents | `4:3` |
| Square | `1:1` |
| Portrait | `9:16` |

Use `--count 2` for options. Use `--negative-prompt` to exclude unwanted elements.

---

## E — Evaluate

```bash
python tools/media/analyze_image.py \
  --image "workspace/<project-slug>/visuals/<name>.png" \
  --task review \
  --context "Should show <expected content>"
```

Criteria: technical accuracy, completeness, clarity, readability, style consistency.

- All Good → deliver
- Needs Work → return to Narrate with adjustments
- Poor → re-examine source, major rewrite
- Maximum 3 iteration cycles

---

## R — Refine

Save finals to `workspace/<project-slug>/visuals/`. If multiple assets, create a manifest:

```markdown
## Visual Assets
| File | Type | Section | Description |
|------|------|---------|-------------|
| arch-overview.png | Architecture | 3.1 | AWS 3-tier architecture |
```

---

## Edge Cases

- **Safety filter blocks** — Rephrase generic ("professionals" → "organizational hierarchy")
- **Poor text rendering** — Note labels may need post-processing
- **API rate limits** — Check OpenRouter for current limits
- **Brand logos** — Leave as placeholders, note for manual insertion

---

## Tools

| Tool | Purpose |
|------|---------|
| `tools/media/generate_image.py` | Generate via OpenRouter |
| `tools/media/analyze_image.py` | Analyze via Gemini Flash |

---

## Workspace Structure

```
workspace/<project-slug>/
└── visuals/
    ├── <name>.png
    └── visuals-manifest.md (if multiple)
```
