"""
Parse a PPTX outline (YAML) into a structured list of slide dicts.

Usage:
    python tools/presentations/parse_outline.py outline.yaml [-o output.json]
    python -c "from tools.presentations.parse_outline import parse; slides = parse('outline.yaml')"

Input:  YAML file matching hardprompts/presentations/pptx-outline-spec.md
Output: JSON list of normalised slide dicts ready for render_pptx.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Inline markdown → runs
# ---------------------------------------------------------------------------

_INLINE_RE = re.compile(
    r"\*\*(.+?)\*\*"       # bold
    r"|\*(.+?)\*"          # italic
    r"|~~(.+?)~~"          # strikethrough
    r"|`(.+?)`"            # code
    r"|([^*~`]+)"          # plain text
)


def _parse_inline(text: str) -> list[dict]:
    """Convert inline markdown to a list of text runs.

    Each run: {"text": str, "bold": bool, "italic": bool, "strike": bool, "code": bool}
    """
    runs: list[dict] = []
    for m in _INLINE_RE.finditer(text):
        bold, italic, strike, code, plain = m.groups()
        if bold is not None:
            runs.append({"text": bold, "bold": True})
        elif italic is not None:
            runs.append({"text": italic, "italic": True})
        elif strike is not None:
            runs.append({"text": strike, "strike": True})
        elif code is not None:
            runs.append({"text": code, "code": True})
        elif plain is not None:
            runs.append({"text": plain})
    return runs


# ---------------------------------------------------------------------------
# Body text parser  (markdown → paragraphs)
# ---------------------------------------------------------------------------

def _parse_body(raw: str) -> list[dict]:
    """Parse body markdown into a list of paragraph dicts.

    Each paragraph: {"level": int, "runs": [...]}
    level 0 = normal paragraph, 1 = bullet, 2 = sub-bullet, etc.
    """
    paragraphs: list[dict] = []
    for line in raw.split("\n"):
        stripped = line.rstrip()
        if not stripped:
            continue

        # Detect bullet level
        indent_match = re.match(r"^(\s*)-\s+(.+)$", stripped)
        if indent_match:
            indent = len(indent_match.group(1))
            level = (indent // 2) + 1  # 0-spaces=1, 2-spaces=2, 4-spaces=3
            content = indent_match.group(2)
        else:
            level = 0
            content = stripped

        paragraphs.append({
            "level": level,
            "runs": _parse_inline(content),
        })
    return paragraphs


# ---------------------------------------------------------------------------
# Slide normalisation
# ---------------------------------------------------------------------------

VALID_LAYOUTS = {
    # structural
    "title", "section", "end", "blank",
    # content
    "content", "two-col", "stat", "quote", "comparison",
    # data
    "stat-grid", "card-grid", "data-table", "highlight-grid",
    # flow
    "step-flow", "funnel", "timeline", "ascend",
    # structure
    "layer-stack", "hub-spoke",
    # process
    "process-loop",
}


def _normalise_slide(raw: dict, index: int) -> dict:
    """Validate and normalise a single slide dict."""
    layout = raw.get("layout", "content")
    if layout not in VALID_LAYOUTS:
        raise ValueError(f"Slide {index}: unknown layout '{layout}'. Valid: {sorted(VALID_LAYOUTS)}")

    slide: dict[str, Any] = {
        "index": index,
        "layout": layout,
    }

    # Copy common text fields
    for key in ("title", "subtitle", "eyebrow", "notes", "style"):
        if key in raw:
            slide[key] = str(raw[key])

    # Parse body text
    if "body" in raw:
        slide["body"] = _parse_body(str(raw["body"]))

    # --- Layout-specific fields ---

    # stat (single big number)
    if layout == "stat":
        for key in ("value", "label"):
            if key in raw:
                slide[key] = str(raw[key])

    # stat-grid
    if layout == "stat-grid" and "stats" in raw:
        slide["stats"] = [
            {"value": str(s.get("value", "")), "label": str(s.get("label", ""))}
            for s in raw["stats"]
        ]

    # card-grid / highlight-grid
    if layout in ("card-grid", "highlight-grid") and ("cards" in raw or "items" in raw):
        items_key = "cards" if "cards" in raw else "items"
        slide["cards"] = [
            {
                "title": str(c.get("title", "")),
                "body": str(c.get("body", c.get("desc", ""))),
                "icon": str(c.get("icon", "")),
            }
            for c in raw[items_key]
        ]
        if "columns" in raw:
            slide["columns"] = int(raw["columns"])

    # data-table
    if layout == "data-table":
        slide["headers"] = [str(h) for h in raw.get("headers", [])]
        slide["rows"] = [[str(cell) for cell in row] for row in raw.get("rows", [])]

    # step-flow
    if layout == "step-flow" and "steps" in raw:
        slide["steps"] = []
        for i, s in enumerate(raw["steps"], 1):
            slide["steps"].append({
                "number": s.get("number", i),
                "title": str(s.get("title", "")),
                "desc": str(s.get("desc", "")),
            })

    # funnel
    if layout == "funnel" and "bars" in raw:
        max_val = max((b.get("value", 0) for b in raw["bars"]), default=1)
        slide["bars"] = []
        for b in raw["bars"]:
            val = b.get("value", 0)
            slide["bars"].append({
                "label": str(b.get("label", "")),
                "value": val,
                "pct": b.get("pct", round(val / max_val * 100, 1) if max_val else 0),
            })

    # timeline
    if layout == "timeline" and "events" in raw:
        slide["events"] = [
            {
                "date": str(e.get("date", "")),
                "title": str(e.get("title", "")),
                "desc": str(e.get("desc", "")),
                "status": str(e.get("status", "upcoming")),
            }
            for e in raw["events"]
        ]

    # ascend
    if layout == "ascend" and "nodes" in raw:
        slide["nodes"] = [
            {
                "title": str(n.get("title", "")),
                "desc": str(n.get("desc", "")),
                "stat": str(n.get("stat", "")),
            }
            for n in raw["nodes"]
        ]

    # layer-stack
    if layout == "layer-stack" and "layers" in raw:
        slide["layers"] = [
            {
                "label": str(la.get("label", "")),
                "items": [str(i) for i in la.get("items", [])],
            }
            for la in raw["layers"]
        ]

    # hub-spoke
    if layout == "hub-spoke":
        if "center" in raw:
            slide["center"] = str(raw["center"])
        if "spokes" in raw:
            slide["spokes"] = [str(s) for s in raw["spokes"]]

    # process-loop
    if layout == "process-loop":
        if "center_label" in raw:
            slide["center_label"] = str(raw["center_label"])
        if "nodes" in raw:
            slide["nodes"] = [str(n) for n in raw["nodes"]]

    # comparison
    if layout == "comparison":
        for side in ("before", "after"):
            if side in raw:
                block = raw[side]
                slide[side] = {
                    "title": str(block.get("title", side.title())),
                    "items": [str(i) for i in block.get("items", [])],
                }

    # quote
    if layout == "quote":
        for key in ("quote", "author", "role", "photo"):
            if key in raw:
                slide[key] = str(raw[key])

    # two-col
    if layout == "two-col":
        for col in ("left", "right"):
            if col in raw:
                val = raw[col]
                if isinstance(val, str):
                    slide[col] = _parse_body(val)
                elif isinstance(val, list):
                    slide[col] = _parse_body("\n".join(f"- {item}" for item in val))

    # title layout extras
    if layout == "title" and "client_logo" in raw:
        slide["client_logo"] = str(raw["client_logo"])

    return slide


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse(source: str | Path) -> dict:
    """Parse an outline YAML file and return a normalised deck dict.

    Returns:
        {
            "meta": {"title": str, "theme": str, "variant": str, ...},
            "slides": [slide_dict, ...]
        }
    """
    path = Path(source)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Outline must be a YAML mapping with 'meta' and 'slides' keys")

    meta = raw.get("meta", {})
    meta.setdefault("title", "Untitled Presentation")
    meta.setdefault("theme", "credera")
    meta.setdefault("variant", "default")
    meta.setdefault("author", "")
    meta.setdefault("date", "")

    raw_slides = raw.get("slides", [])
    if not raw_slides:
        raise ValueError("Outline contains no slides")

    slides = [_normalise_slide(s, i) for i, s in enumerate(raw_slides)]

    return {"meta": meta, "slides": slides}


def parse_string(yaml_text: str) -> dict:
    """Parse outline from a YAML string (for programmatic use)."""
    import tempfile
    tmp = Path(tempfile.mktemp(suffix=".yaml"))
    try:
        tmp.write_text(yaml_text, encoding="utf-8")
        return parse(tmp)
    finally:
        tmp.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Parse PPTX outline YAML → JSON")
    ap.add_argument("outline", help="Path to outline YAML file")
    ap.add_argument("-o", "--output", help="Output JSON file (default: stdout)")
    args = ap.parse_args()

    deck = parse(args.outline)

    out = json.dumps(deck, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"Wrote {len(deck['slides'])} slides → {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
