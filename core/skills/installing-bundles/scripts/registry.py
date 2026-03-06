#!/usr/bin/env python3
"""
Phalanx Registry Tool
======================
Searches, installs, updates, and removes skill bundles from a remote
git-hosted registry.  Designed to be invoked by the installing-bundles
skill.

Fetch Strategy:
  1. git sparse-checkout (preferred — fast, works with large repos)
  2. GitHub REST API tree/blob endpoints (fallback when git CLI unavailable)

Usage:
  python registry.py --search "cloud architecture"
  python registry.py --list
  python registry.py --installed
  python registry.py --install cloud-architecture
  python registry.py --update cloud-architecture
  python registry.py --update-all
  python registry.py --remove cloud-architecture
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_REGISTRY_URL = "https://github.com/td-project-ai/phalanx"
DEFAULT_BRANCH = "main"
CATALOG_PATH = "catalog.yaml"          # path inside the registry repo
INSTALLED_MARKER = ".phalanx-installed.json"

# ---------------------------------------------------------------------------
# Helpers — project root discovery
# ---------------------------------------------------------------------------

def find_project_root(start: Path | None = None) -> Path:
    """Walk up from *start* looking for CLAUDE.md or config.yaml."""
    cwd = start or Path.cwd()
    for d in [cwd, *cwd.parents]:
        if (d / "CLAUDE.md").exists() or (d / "config.yaml").exists():
            return d
    return cwd


def load_registry_config(root: Path) -> dict[str, Any]:
    """Read registry settings from config.yaml."""
    cfg_path = root / "config.yaml"
    if not cfg_path.exists():
        return {}
    try:
        import yaml  # type: ignore
        with open(cfg_path) as f:
            cfg = yaml.safe_load(f) or {}
        return cfg.get("registry", {})
    except ImportError:
        # Fallback: crude YAML parse for flat keys under registry:
        in_registry = False
        result: dict[str, str] = {}
        for line in cfg_path.read_text().splitlines():
            stripped = line.strip()
            if stripped.startswith("registry:"):
                in_registry = True
                continue
            if in_registry:
                if line and not line[0].isspace():
                    break
                m = re.match(r"\s+(\w+):\s*(.+)", line)
                if m:
                    result[m.group(1)] = m.group(2).strip().strip('"').strip("'")
        return result


# ---------------------------------------------------------------------------
# Helpers — catalog loading
# ---------------------------------------------------------------------------

def _github_api_url(repo_url: str) -> str:
    """Convert https://github.com/owner/repo to API base."""
    m = re.match(r"https?://github\.com/([^/]+/[^/]+?)(?:\.git)?$", repo_url)
    if not m:
        raise ValueError(f"Cannot parse GitHub URL: {repo_url}")
    return f"https://api.github.com/repos/{m.group(1)}"


def _api_headers(token: str | None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "phalanx-registry"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def _fetch_url(url: str, headers: dict[str, str] | None = None) -> bytes:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def _resolve_token(cfg: dict[str, Any]) -> str | None:
    """Resolve a GitHub PAT from env var name in config."""
    env_name = cfg.get("auth_env", "GITHUB_PAT")
    # Check .credentials/.env if not in env
    token = os.environ.get(env_name)
    if token:
        return token
    for env_file in [".credentials/.env", ".env"]:
        p = find_project_root() / env_file
        if p.exists():
            for line in p.read_text().splitlines():
                line = line.strip()
                if line.startswith(f"{env_name}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def load_catalog(cfg: dict[str, Any], root: Path) -> dict[str, Any]:
    """Fetch and parse catalog.yaml from the registry."""
    cache_dir = root / cfg.get("cache_dir", ".tmp/registry-cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / "catalog.yaml"
    cache_meta = cache_dir / "catalog.meta.json"
    ttl = int(cfg.get("cache_ttl", 3600))

    # Check cache freshness
    if cache_file.exists() and cache_meta.exists():
        meta = json.loads(cache_meta.read_text())
        if time.time() - meta.get("fetched_at", 0) < ttl:
            return _parse_catalog(cache_file.read_text())

    repo_url = cfg.get("url", DEFAULT_REGISTRY_URL)
    branch = cfg.get("branch", DEFAULT_BRANCH)
    token = _resolve_token(cfg)
    raw = None

    # Try raw GitHub URL first
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + f"/{branch}/{CATALOG_PATH}"
    try:
        raw = _fetch_url(raw_url, _api_headers(token)).decode()
    except Exception:
        pass

    # Fallback: GitHub API
    if raw is None:
        try:
            api_base = _github_api_url(repo_url)
            url = f"{api_base}/contents/{CATALOG_PATH}?ref={branch}"
            data = json.loads(_fetch_url(url, _api_headers(token)))
            import base64
            raw = base64.b64decode(data["content"]).decode()
        except Exception as e:
            if cache_file.exists():
                print(f"⚠ Could not refresh catalog ({e}), using cached version.", file=sys.stderr)
                return _parse_catalog(cache_file.read_text())
            raise RuntimeError(f"Cannot fetch catalog from {repo_url}: {e}")

    cache_file.write_text(raw)
    cache_meta.write_text(json.dumps({"fetched_at": time.time()}))
    return _parse_catalog(raw)


def _parse_catalog(text: str) -> dict[str, Any]:
    """Parse catalog YAML. Falls back to simple parser if PyYAML missing."""
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except ImportError:
        # Minimal YAML parse: good enough for flat catalog structure
        # This won't handle nested lists perfectly but covers basic use
        result: dict[str, Any] = {"bundles": []}
        current: dict[str, Any] | None = None
        in_list_key: str | None = None
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("- name:"):
                if current:
                    result["bundles"].append(current)
                current = {"name": stripped.split(":", 1)[1].strip()}
                in_list_key = None
            elif current and ":" in stripped and not stripped.startswith("-"):
                k, v = stripped.split(":", 1)
                k = k.strip()
                v = v.strip()
                if v:
                    current[k] = v
                else:
                    current[k] = []
                    in_list_key = k
            elif current and stripped.startswith("- ") and in_list_key:
                current[in_list_key].append(stripped[2:].strip())
        if current:
            result["bundles"].append(current)
        return result


# ---------------------------------------------------------------------------
# Installed state tracking
# ---------------------------------------------------------------------------

def _installed_path(root: Path) -> Path:
    return root / INSTALLED_MARKER


def load_installed(root: Path) -> dict[str, Any]:
    p = _installed_path(root)
    if p.exists():
        return json.loads(p.read_text())
    return {"bundles": {}}


def save_installed(root: Path, data: dict[str, Any]) -> None:
    _installed_path(root).write_text(json.dumps(data, indent=2))


# ---------------------------------------------------------------------------
# Git operations
# ---------------------------------------------------------------------------

def _has_git() -> bool:
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def _git_sparse_checkout(repo_url: str, branch: str, paths: list[str],
                          dest: Path, token: str | None = None) -> bool:
    """Clone only specific paths using sparse-checkout."""
    if not _has_git():
        return False

    # Build authenticated URL if token provided
    clone_url = repo_url
    if token and "github.com" in repo_url:
        clone_url = repo_url.replace("https://", f"https://x-access-token:{token}@")

    try:
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            ["git", "clone", "--filter=blob:none", "--no-checkout", "--depth=1",
             "-b", branch, clone_url, str(dest)],
            capture_output=True, check=True, timeout=60
        )
        subprocess.run(
            ["git", "sparse-checkout", "init", "--cone"],
            cwd=str(dest), capture_output=True, check=True, timeout=15
        )
        subprocess.run(
            ["git", "sparse-checkout", "set"] + paths,
            cwd=str(dest), capture_output=True, check=True, timeout=15
        )
        subprocess.run(
            ["git", "checkout"],
            cwd=str(dest), capture_output=True, check=True, timeout=30
        )
        return True
    except Exception:
        return False


def _api_download_tree(repo_url: str, branch: str, path: str,
                        token: str | None = None) -> list[dict[str, str]]:
    """Recursively list files under a path via GitHub API."""
    api_base = _github_api_url(repo_url)
    headers = _api_headers(token)
    url = f"{api_base}/git/trees/{branch}?recursive=1"
    data = json.loads(_fetch_url(url, headers))
    files = []
    for item in data.get("tree", []):
        if item["type"] == "blob" and item["path"].startswith(path):
            files.append({"path": item["path"], "sha": item["sha"]})
    return files


def _api_download_blob(repo_url: str, sha: str, token: str | None = None) -> bytes:
    api_base = _github_api_url(repo_url)
    headers = _api_headers(token)
    headers["Accept"] = "application/vnd.github.v3.raw"
    url = f"{api_base}/git/blobs/{sha}"
    return _fetch_url(url, headers)


# ---------------------------------------------------------------------------
# Bundle resolution — map bundle YAML to file paths
# ---------------------------------------------------------------------------

def resolve_bundle_paths(bundle: dict[str, Any]) -> list[str]:
    """Given a bundle entry from the catalog, return registry paths to fetch."""
    paths = []
    name = bundle["name"]

    # Skills
    for skill in bundle.get("skills", []):
        paths.append(f"skills/{skill}")

    # Agents
    for agent in bundle.get("agents", []):
        paths.append(f"agents/{agent}")

    # Tools
    for tool in bundle.get("tools", []):
        paths.append(f"tools/{tool}")

    # Themes
    for theme in bundle.get("themes", []):
        paths.append(f"themes/{theme}")

    # Context
    for ctx in bundle.get("context", []):
        paths.append(f"context/{ctx}")

    # Bundle manifest itself
    paths.append(f"bundles/{name}.yaml")

    return paths


def resolve_local_mappings(bundle: dict[str, Any]) -> dict[str, str]:
    """Map registry paths → local install paths."""
    mappings: dict[str, str] = {}
    for skill in bundle.get("skills", []):
        mappings[f"skills/{skill}"] = f".claude/skills/{skill}"
    for agent in bundle.get("agents", []):
        mappings[f"agents/{agent}"] = f".claude/agents/{agent}"
    for tool in bundle.get("tools", []):
        mappings[f"tools/{tool}"] = f"tools/{tool}"
    for theme in bundle.get("themes", []):
        # themes/html/foo.css → context/brands/foo/theme.css (legacy HTML theme)
        # themes/pptx/foo/    → context/brands/foo/
        if theme.startswith("html/"):
            name = theme.removeprefix("html/").removesuffix(".css")
            mappings[f"themes/{theme}"] = f"context/brands/{name}/theme.css"
        elif theme.startswith("pptx/"):
            mappings[f"themes/{theme}"] = f"context/brands/{theme.removeprefix('pptx/')}"
        else:
            mappings[f"themes/{theme}"] = f"context/brands/{theme}"
    for ctx in bundle.get("context", []):
        mappings[f"context/{ctx}"] = f"context/{ctx}"
    return mappings


# ---------------------------------------------------------------------------
# Core actions
# ---------------------------------------------------------------------------

def action_list(catalog: dict[str, Any], **_: Any) -> None:
    """List all available bundles."""
    bundles = catalog.get("bundles", [])
    if not bundles:
        print("No bundles found in the catalog.")
        return
    print(f"{'Bundle':<28} {'Description'}")
    print(f"{'─' * 28} {'─' * 50}")
    for b in bundles:
        name = b.get("name", "?")
        desc = b.get("description", "")[:50]
        print(f"{name:<28} {desc}")
    print(f"\n{len(bundles)} bundles available. Use --install <name> to install.")


def action_search(catalog: dict[str, Any], query: str, **_: Any) -> None:
    """Search bundles by keyword matching against name, description, tags."""
    terms = query.lower().split()
    results = []
    for b in catalog.get("bundles", []):
        blob = " ".join([
            b.get("name", ""),
            b.get("description", ""),
            " ".join(b.get("tags", [])),
            " ".join(b.get("skills", [])),
        ]).lower()
        score = sum(1 for t in terms if t in blob)
        if score > 0:
            results.append((score, b))
    results.sort(key=lambda x: -x[0])
    if not results:
        print(f"No bundles match '{query}'. Try different keywords or --list to see all.")
        return
    print(f"Search results for '{query}':\n")
    for score, b in results:
        name = b.get("name", "?")
        desc = b.get("description", "")
        skills = ", ".join(b.get("skills", []))
        print(f"  {name}")
        print(f"    {desc}")
        if skills:
            print(f"    Skills: {skills}")
        print()


def action_installed(root: Path, **_: Any) -> None:
    """Show installed bundles."""
    data = load_installed(root)
    bundles = data.get("bundles", {})
    if not bundles:
        print("No bundles installed. Use --list to see available bundles.")
        return
    print(f"{'Bundle':<28} {'Installed At'}")
    print(f"{'─' * 28} {'─' * 30}")
    for name, info in bundles.items():
        ts = info.get("installed_at", "unknown")
        print(f"{name:<28} {ts}")
    print(f"\n{len(bundles)} bundles installed.")


def action_install(catalog: dict[str, Any], bundle_name: str, root: Path,
                    cfg: dict[str, Any], force: bool = False, **_: Any) -> None:
    """Install a bundle from the registry."""
    # Find in catalog
    bundle = None
    for b in catalog.get("bundles", []):
        if b.get("name") == bundle_name:
            bundle = b
            break
    if not bundle:
        print(f"✗ Bundle '{bundle_name}' not found in catalog.")
        _suggest_similar(catalog, bundle_name)
        return

    installed = load_installed(root)
    if bundle_name in installed.get("bundles", {}) and not force:
        print(f"Bundle '{bundle_name}' is already installed. Use --update or --install --force to reinstall.")
        return

    print(f"Installing bundle: {bundle_name}")
    repo_url = cfg.get("url", DEFAULT_REGISTRY_URL)
    branch = cfg.get("branch", DEFAULT_BRANCH)
    token = _resolve_token(cfg)
    registry_paths = resolve_bundle_paths(bundle)
    local_map = resolve_local_mappings(bundle)

    cache_dir = root / cfg.get("cache_dir", ".tmp/registry-cache") / "checkout"

    # Try git sparse-checkout first
    success = _git_sparse_checkout(repo_url, branch, registry_paths, cache_dir, token)

    if success:
        _copy_from_checkout(cache_dir, root, local_map, registry_paths)
    else:
        print("  Git unavailable, falling back to API download...")
        _api_install(repo_url, branch, token, root, local_map, registry_paths)

    # Record installation
    installed.setdefault("bundles", {})[bundle_name] = {
        "installed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": bundle.get("version", "latest"),
        "skills": bundle.get("skills", []),
        "agents": bundle.get("agents", []),
        "tools": bundle.get("tools", []),
    }
    save_installed(root, installed)
    print(f"✓ Bundle '{bundle_name}' installed successfully.")
    _print_bundle_summary(bundle)


def action_update(catalog: dict[str, Any], bundle_name: str, root: Path,
                   cfg: dict[str, Any], **_: Any) -> None:
    """Update an installed bundle."""
    installed = load_installed(root)
    if bundle_name not in installed.get("bundles", {}):
        print(f"Bundle '{bundle_name}' is not installed. Use --install to install it.")
        return
    print(f"Updating bundle: {bundle_name}")
    action_install(catalog, bundle_name, root, cfg, force=True)


def action_update_all(catalog: dict[str, Any], root: Path, cfg: dict[str, Any], **_: Any) -> None:
    """Update all installed bundles."""
    installed = load_installed(root)
    bundles = list(installed.get("bundles", {}).keys())
    if not bundles:
        print("No bundles installed.")
        return
    print(f"Updating {len(bundles)} installed bundle(s)...\n")
    for name in bundles:
        action_update(catalog, name, root, cfg)
        print()


def action_remove(bundle_name: str, root: Path, **_: Any) -> None:
    """Remove an installed bundle."""
    installed = load_installed(root)
    info = installed.get("bundles", {}).get(bundle_name)
    if not info:
        print(f"Bundle '{bundle_name}' is not installed.")
        return

    print(f"Removing bundle: {bundle_name}")

    # Remove skills
    for skill in info.get("skills", []):
        p = root / ".claude" / "skills" / skill
        if p.exists():
            shutil.rmtree(p)
            print(f"  Removed skill: {skill}")

    # Remove agents (only if not used by other installed bundles)
    other_agents = set()
    for name, other in installed.get("bundles", {}).items():
        if name != bundle_name:
            other_agents.update(other.get("agents", []))
    for agent in info.get("agents", []):
        if agent not in other_agents:
            p = root / ".claude" / "agents" / agent
            if p.exists():
                shutil.rmtree(p)
                print(f"  Removed agent: {agent}")
        else:
            print(f"  Kept agent: {agent} (used by another bundle)")

    # Remove tools (only if not used by other installed bundles)
    other_tools = set()
    for name, other in installed.get("bundles", {}).items():
        if name != bundle_name:
            other_tools.update(other.get("tools", []))
    for tool in info.get("tools", []):
        if tool not in other_tools:
            p = root / "tools" / tool
            if p.is_dir():
                shutil.rmtree(p)
            elif p.exists():
                p.unlink()
            print(f"  Removed tool: {tool}")

    del installed["bundles"][bundle_name]
    save_installed(root, installed)
    print(f"✓ Bundle '{bundle_name}' removed.")


# ---------------------------------------------------------------------------
# Helpers — file operations
# ---------------------------------------------------------------------------

def _copy_from_checkout(checkout: Path, root: Path, local_map: dict[str, str],
                         registry_paths: list[str]) -> None:
    """Copy files from git sparse-checkout to their local destinations."""
    for reg_path in registry_paths:
        src = checkout / reg_path
        if not src.exists():
            continue
        # Find the best matching local destination
        dest_rel = None
        for prefix, local_prefix in local_map.items():
            if reg_path.startswith(prefix) or reg_path == prefix:
                remainder = reg_path[len(prefix):].lstrip("/")
                dest_rel = f"{local_prefix}/{remainder}" if remainder else local_prefix
                break
        if not dest_rel:
            continue
        dest = root / dest_rel
        if src.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


def _api_install(repo_url: str, branch: str, token: str | None,
                  root: Path, local_map: dict[str, str],
                  registry_paths: list[str]) -> None:
    """Download files via GitHub API when git is unavailable."""
    api_base = _github_api_url(repo_url)
    headers = _api_headers(token)

    for reg_path in registry_paths:
        # Find local destination
        dest_rel = None
        for prefix, local_prefix in local_map.items():
            if reg_path.startswith(prefix):
                remainder = reg_path[len(prefix):].lstrip("/")
                dest_rel = f"{local_prefix}/{remainder}" if remainder else local_prefix
                break
        if not dest_rel:
            continue

        # Fetch file list for this path
        try:
            tree_data = json.loads(_fetch_url(
                f"{api_base}/git/trees/{branch}?recursive=1", headers
            ))
        except Exception as e:
            print(f"  ⚠ Failed to fetch tree: {e}")
            continue

        for item in tree_data.get("tree", []):
            if item["type"] != "blob":
                continue
            if not item["path"].startswith(reg_path):
                continue
            # Download this blob
            try:
                blob_headers = dict(headers)
                blob_headers["Accept"] = "application/vnd.github.v3.raw"
                content = _fetch_url(f"{api_base}/git/blobs/{item['sha']}", blob_headers)
                rel_in_prefix = item["path"][len(reg_path):].lstrip("/")
                if rel_in_prefix:
                    dest = root / dest_rel / rel_in_prefix
                else:
                    dest = root / dest_rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(content)
                print(f"  ↓ {item['path']}")
            except Exception as e:
                print(f"  ⚠ Failed to download {item['path']}: {e}")


def _suggest_similar(catalog: dict[str, Any], query: str) -> None:
    """Suggest bundles with similar names."""
    names = [b["name"] for b in catalog.get("bundles", []) if "name" in b]
    matches = [n for n in names if any(w in n for w in query.lower().split("-"))]
    if matches:
        print(f"  Did you mean: {', '.join(matches)}?")


def _print_bundle_summary(bundle: dict[str, Any]) -> None:
    """Print what was installed."""
    parts = []
    if bundle.get("skills"):
        parts.append(f"  Skills: {', '.join(bundle['skills'])}")
    if bundle.get("agents"):
        parts.append(f"  Agents: {', '.join(bundle['agents'])}")
    if bundle.get("tools"):
        parts.append(f"  Tools: {', '.join(bundle['tools'])}")
    if bundle.get("themes"):
        parts.append(f"  Themes: {', '.join(bundle['themes'])}")
    if parts:
        print("\n".join(parts))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Phalanx Registry — bundle management")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="List all available bundles")
    group.add_argument("--search", type=str, metavar="QUERY", help="Search bundles by keyword")
    group.add_argument("--installed", action="store_true", help="Show installed bundles")
    group.add_argument("--install", type=str, metavar="BUNDLE", help="Install a bundle")
    group.add_argument("--update", type=str, metavar="BUNDLE", help="Update an installed bundle")
    group.add_argument("--update-all", action="store_true", help="Update all installed bundles")
    group.add_argument("--remove", type=str, metavar="BUNDLE", help="Remove a bundle")
    parser.add_argument("--force", action="store_true", help="Force reinstall on --install")
    parser.add_argument("--root", type=str, help="Project root directory")

    args = parser.parse_args()
    root = Path(args.root) if args.root else find_project_root()
    cfg = load_registry_config(root)

    if args.installed:
        action_installed(root)
        return

    if args.remove:
        action_remove(args.remove, root)
        return

    # All other actions need the catalog
    catalog = load_catalog(cfg, root)

    if args.list:
        action_list(catalog)
    elif args.search:
        action_search(catalog, args.search)
    elif args.install:
        action_install(catalog, args.install, root, cfg, force=args.force)
    elif args.update:
        action_update(catalog, args.update, root, cfg)
    elif args.update_all:
        action_update_all(catalog, root, cfg)


if __name__ == "__main__":
    main()
