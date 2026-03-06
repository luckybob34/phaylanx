"""
Analyze images using OpenRouter API with vision-capable models.

Sends an image to a vision model via OpenRouter for analysis: technical accuracy
checks, content description, quality assessment, and improvement suggestions.

Usage:
    python tools/media/analyze_image.py --image workspace/my-project/visuals/arch.png --task describe
    python tools/media/analyze_image.py --image arch.png --task review --context "AWS 3-tier web app architecture"
    python tools/media/analyze_image.py --image diagram.png --task custom --prompt "List every AWS service shown"

Environment:
    OPENROUTER_API_KEY - Required. Set in .credentials/.env
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CREDENTIALS_PATH = Path(__file__).resolve().parent.parent.parent / ".credentials" / ".env"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.0-flash-001"
SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}

ANALYSIS_TASKS = {
    "describe": (
        "Describe this image in detail. Identify all components, labels, relationships, "
        "and any text visible in the image. Provide a structured breakdown."
    ),
    "review": (
        "Review this technical diagram or visual asset for:\n"
        "1. **Technical accuracy** - Are components and relationships correctly represented?\n"
        "2. **Completeness** - Are any expected components, labels, or connections missing?\n"
        "3. **Clarity** - Can the target audience understand this without additional context?\n"
        "4. **Readability** - Are labels legible? Is text appropriately sized?\n"
        "5. **Improvements** - List specific, actionable suggestions for the next iteration.\n"
        "Provide a structured assessment with ratings (Good / Needs Work / Poor) per category."
    ),
    "extract": (
        "Extract all text, labels, annotations, and data visible in this image. "
        "Return the content in a structured format, preserving hierarchy and relationships."
    ),
    "compare": (
        "Analyze this image and describe what it shows. Focus on elements that could be "
        "compared against a reference design or specification. List all identifiable components."
    ),
    "custom": None,  # Uses --prompt argument
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_env() -> None:
    """Load credentials from .credentials/.env into environment."""
    if CREDENTIALS_PATH.exists():
        with open(CREDENTIALS_PATH, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())


def _read_image_as_data_uri(image_path: Path) -> str:
    """Read an image file and return a data URI string."""
    mime_type, _ = mimetypes.guess_type(str(image_path))
    if mime_type is None:
        mime_type = "image/png"
    raw = image_path.read_bytes()
    b64 = base64.b64encode(raw).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------


def analyze_image(
    image_path: str,
    task: str = "describe",
    custom_prompt: str | None = None,
    context: str | None = None,
    model: str = DEFAULT_MODEL,
) -> dict:
    """
    Analyze an image using a vision model via OpenRouter.

    Args:
        image_path: Path to the image file.
        task: Analysis task - one of: describe, review, extract, compare, custom.
        custom_prompt: Custom analysis prompt (required when task='custom').
        context: Optional additional context about the image to guide analysis.
        model: OpenRouter vision model ID (default: google/gemini-2.0-flash-001).

    Returns:
        dict with success status, analysis text, and metadata.
    """
    try:
        import requests
    except ImportError:
        return {
            "success": False,
            "error": "requests package not installed. Run: pip install requests",
        }

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return {"success": False, "error": "OPENROUTER_API_KEY not set in environment or .credentials/.env"}

    img = Path(image_path)
    if not img.exists():
        return {"success": False, "error": f"Image file not found: {image_path}"}

    if img.suffix.lower() not in SUPPORTED_FORMATS:
        return {
            "success": False,
            "error": f"Unsupported image format '{img.suffix}'. Supported: {sorted(SUPPORTED_FORMATS)}",
        }

    if task not in ANALYSIS_TASKS:
        return {
            "success": False,
            "error": f"Unknown task '{task}'. Must be one of: {list(ANALYSIS_TASKS.keys())}",
        }

    # Build instruction text
    if task == "custom":
        if not custom_prompt:
            return {"success": False, "error": "Custom task requires --prompt argument"}
        instruction = custom_prompt
    else:
        instruction = ANALYSIS_TASKS[task]

    if context:
        instruction = f"Context about this image: {context}\n\n{instruction}"

    # Read image as data URI
    data_uri = _read_image_as_data_uri(img)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            }
        ],
    }

    try:
        response = requests.post(
            OPENROUTER_BASE_URL,
            headers=headers,
            json=payload,
            timeout=120,
        )
    except Exception as exc:
        return {"success": False, "error": f"API call failed: {exc}"}

    if response.status_code != 200:
        return {"success": False, "error": f"API returned {response.status_code}: {response.text[:500]}"}

    data = response.json()

    try:
        analysis_text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return {"success": False, "error": f"Unexpected response format: {json.dumps(data)[:500]}"}

    if not analysis_text:
        return {"success": False, "error": "No analysis returned. The image may have been blocked by safety filters."}

    return {
        "success": True,
        "data": {
            "analysis": analysis_text,
            "task": task,
            "model": model,
            "image_path": str(img),
            "image_size_bytes": img.stat().st_size,
        },
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze images using OpenRouter vision models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--image", required=True, help="Path to the image file to analyze")
    parser.add_argument(
        "--task",
        default="describe",
        choices=list(ANALYSIS_TASKS.keys()),
        help="Analysis task to perform (default: describe)",
    )
    parser.add_argument(
        "--prompt",
        default=None,
        help="Custom analysis prompt (required when --task custom)",
    )
    parser.add_argument(
        "--context",
        default=None,
        help="Additional context about the image to guide analysis",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenRouter vision model ID (default: {DEFAULT_MODEL})",
    )

    args = parser.parse_args()

    _load_env()

    result = analyze_image(
        image_path=args.image,
        task=args.task,
        custom_prompt=args.prompt,
        context=args.context,
        model=args.model,
    )

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
