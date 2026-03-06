"""
Generate images using OpenRouter API with image generation models.

Uses the OpenRouter chat completions API with models that support image output
(e.g., bytedance-seed/seedream-4.5). Saves generated images to disk.

Usage:
    python tools/media/generate_image.py --prompt "A clean architecture diagram..." --output workspace/my-project/visuals/arch.png
    python tools/media/generate_image.py --prompt "..." --output out.png --model bytedance-seed/seedream-4.5

Environment:
    OPENROUTER_API_KEY - Required. Set in .credentials/.env
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CREDENTIALS_PATH = Path(__file__).resolve().parent.parent.parent / ".credentials" / ".env"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "bytedance-seed/seedream-4.5"
MAX_IMAGES = 4

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


def _ensure_output_dir(output_path: Path) -> None:
    """Create parent directories for the output file if they don't exist."""
    output_path.parent.mkdir(parents=True, exist_ok=True)


def _save_image_from_data_uri(data_uri: str, save_path: Path) -> str:
    """Decode a data URI and save the image bytes to disk. Returns the final path."""
    if "," in data_uri:
        header, b64_data = data_uri.split(",", 1)
    else:
        b64_data = data_uri
        header = ""

    image_bytes = base64.b64decode(b64_data)

    # Determine extension from header if not already set appropriately
    if save_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        if "jpeg" in header or "jpg" in header:
            save_path = save_path.with_suffix(".jpg")
        elif "png" in header:
            save_path = save_path.with_suffix(".png")
        elif "webp" in header:
            save_path = save_path.with_suffix(".webp")
        else:
            save_path = save_path.with_suffix(".jpg")

    save_path.write_bytes(image_bytes)
    return str(save_path)


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------


def generate_image(
    prompt: str,
    output_path: str,
    model: str = DEFAULT_MODEL,
    number_of_images: int = 1,
) -> dict:
    """
    Generate images via OpenRouter and save to disk.

    Args:
        prompt: Text description of the desired image.
        output_path: File path for the output image.
        model: OpenRouter model ID (default: bytedance-seed/seedream-4.5).
        number_of_images: Number of images to generate (1-4). Each is a separate API call.

    Returns:
        dict with success status, saved file paths, and metadata.
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

    number_of_images = max(1, min(number_of_images, MAX_IMAGES))
    out = Path(output_path)
    _ensure_output_dir(out)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    saved_files: list[str] = []
    errors: list[str] = []

    for i in range(number_of_images):
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=headers,
                json=payload,
                timeout=180,
            )
        except Exception as exc:
            errors.append(f"Request {i + 1} failed: {exc}")
            continue

        if response.status_code != 200:
            errors.append(f"Request {i + 1} returned {response.status_code}: {response.text[:300]}")
            continue

        data = response.json()

        # Extract image from response
        try:
            message = data["choices"][0]["message"]
            images_list = message.get("images", [])
            if images_list:
                data_uri = images_list[0]["image_url"]["url"]
            else:
                content = message.get("content", "")
                if content.startswith("data:image"):
                    data_uri = content
                else:
                    errors.append(f"Request {i + 1}: No image in response. Content: {content[:200]}")
                    continue
        except (KeyError, IndexError) as exc:
            errors.append(f"Request {i + 1}: Could not parse image from response: {exc}")
            continue

        if number_of_images == 1:
            save_path = out
        else:
            save_path = out.with_stem(f"{out.stem}_{i + 1}")

        try:
            saved = _save_image_from_data_uri(data_uri, save_path)
            saved_files.append(saved)
        except Exception as exc:
            errors.append(f"Request {i + 1}: Failed to save image: {exc}")

    if not saved_files:
        return {
            "success": False,
            "error": f"No images generated. Errors: {'; '.join(errors)}",
        }

    result = {
        "success": True,
        "data": {
            "files": saved_files,
            "model": model,
            "prompt_length": len(prompt),
            "images_generated": len(saved_files),
        },
    }
    if errors:
        result["data"]["warnings"] = errors

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate images using OpenRouter API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--prompt", required=True, help="Text prompt describing the desired image")
    parser.add_argument("--output", required=True, help="Output file path (PNG/JPG)")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenRouter model ID (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of images to generate, 1-4 (default: 1)",
    )

    args = parser.parse_args()

    _load_env()

    result = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        model=args.model,
        number_of_images=args.count,
    )

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
