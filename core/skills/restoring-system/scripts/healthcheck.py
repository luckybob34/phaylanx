#!/usr/bin/env python3
"""
Health check for the GOTCHA framework (Skills Edition).

Usage:
    python healthcheck.py           # Check and report
    python healthcheck.py --repair  # Check and fix what's possible

Checks:
    - Required directories exist
    - Key files exist (CLAUDE.md, manifests, MEMORY.md)
    - SQLite databases exist and have correct schema
    - All skill directories have SKILL.md
    - Agent files exist
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime


def find_project_root() -> Path:
    """Walk up from script location to find CLAUDE.md."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    # Fallback: assume cwd
    return Path.cwd()


def check_directories(root: Path) -> list[tuple[str, bool, str]]:
    """Check required directories exist."""
    required = [
        ".claude/skills",
        ".claude/agents",
        "tools",
        "context",
        "context/templates/presentations",
        "context/templates/presentations/themes",
        "memory",
        "memory/logs",
        "data",
        "workspace",
    ]
    results = []
    for d in required:
        path = root / d
        exists = path.is_dir()
        results.append((d, exists, "directory"))
    return results


def check_files(root: Path) -> list[tuple[str, bool, str]]:
    """Check required files exist."""
    required = [
        ("CLAUDE.md", "System prompt"),
        (".claude/skills/manifest.md", "Skills manifest"),
        ("tools/manifest.md", "Tools manifest"),
        ("config.yaml", "Global config"),
        ("memory/MEMORY.md", "Persistent memory"),
        ("context/style-guide.md", "Writing style guide"),
        ("context/templates/presentations/base-template.html", "HTML slide engine"),
        ("context/templates/presentations/themes/_contract.md", "CSS theme contract"),
    ]
    results = []
    for filepath, desc in required:
        path = root / filepath
        exists = path.is_file()
        results.append((filepath, exists, desc))
    return results


def check_databases(root: Path) -> list[tuple[str, bool, str]]:
    """Check SQLite databases exist and have correct tables."""
    results = []

    # Memory database
    mem_db = root / "data" / "memory.db"
    if mem_db.is_file():
        try:
            conn = sqlite3.connect(str(mem_db))
            tables = [r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()]
            conn.close()
            has_table = "memory_entries" in tables
            results.append(("data/memory.db", has_table,
                          "memory_entries table" if has_table else "MISSING memory_entries table"))
        except Exception as e:
            results.append(("data/memory.db", False, f"corrupt: {e}"))
    else:
        results.append(("data/memory.db", False, "database file"))

    # Activity database
    act_db = root / "data" / "activity.db"
    if act_db.is_file():
        try:
            conn = sqlite3.connect(str(act_db))
            tables = [r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()]
            conn.close()
            has_table = "tasks" in tables
            results.append(("data/activity.db", has_table,
                          "tasks table" if has_table else "MISSING tasks table"))
        except Exception as e:
            results.append(("data/activity.db", False, f"corrupt: {e}"))
    else:
        results.append(("data/activity.db", False, "database file"))

    return results


def check_themes(root: Path) -> list[tuple[str, bool, str]]:
    """Check that theme CSS files exist for configured themes."""
    results = []
    # Check HTML theme CSS files in context/brands/
    brands_dir = root / "context" / "brands"
    if not brands_dir.is_dir():
        results.append(("context/brands/", False, "brands directory missing"))
        return results

    brand_css_found = False
    for brand_folder in sorted(brands_dir.iterdir()):
        if brand_folder.is_dir():
            css_file = brand_folder / "theme.css"
            if css_file.is_file():
                results.append((f"context/brands/{brand_folder.name}/theme.css", True, "theme CSS"))
                brand_css_found = True
    if not brand_css_found:
        results.append(("context/brands/*/theme.css", False, "no CSS theme files found"))

    # Check PPTX themes
    pptx_templates = list(brands_dir.rglob("*.pptx"))
    if pptx_templates:
        for t in pptx_templates:
            rel = t.relative_to(root)
            results.append((str(rel).replace("\\", "/"), True, "PPTX template"))
    else:
        results.append(("context/brands/*/*.pptx", False, "no PPTX templates found"))

    return results


def check_skills(root: Path) -> list[tuple[str, bool, str]]:
    """Check all skill directories have SKILL.md."""
    results = []
    skills_dir = root / ".claude" / "skills"
    if not skills_dir.is_dir():
        return [(".claude/skills/", False, "skills directory missing")]

    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            skill_file = item / "SKILL.md"
            exists = skill_file.is_file()
            results.append((f".claude/skills/{item.name}/SKILL.md", exists, "skill file"))

    return results


def repair(root: Path, all_results: list[tuple[str, bool, str]]):
    """Attempt to repair missing components."""
    repaired = []

    for path_str, exists, desc in all_results:
        if exists:
            continue

        full_path = root / path_str

        if desc == "directory":
            full_path.mkdir(parents=True, exist_ok=True)
            repaired.append(f"Created directory: {path_str}")

        elif path_str == "memory/MEMORY.md":
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(
                "# Persistent Memory\n\n"
                "> Curated long-term facts and context. Read at session start.\n\n"
                "## User Preferences\n\n- (Add preferences)\n\n"
                "## Key Facts\n\n- (Add facts)\n\n"
                "## Learned Behaviors\n\n"
                "- Always check .claude/skills/manifest.md before starting a task\n"
                "- Always check tools/manifest.md before creating new scripts\n\n"
                "## Current Projects\n\n- (List projects)\n\n"
                f"---\n\n*Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n",
                encoding="utf-8"
            )
            repaired.append("Created memory/MEMORY.md")

        elif path_str == "data/memory.db":
            (root / "data").mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(full_path))
            conn.execute("""CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL DEFAULT 'fact',
                content TEXT NOT NULL,
                content_hash TEXT UNIQUE,
                source TEXT DEFAULT 'session',
                confidence REAL DEFAULT 1.0,
                importance INTEGER DEFAULT 5,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_accessed DATETIME,
                access_count INTEGER DEFAULT 0,
                embedding BLOB,
                embedding_model TEXT,
                tags TEXT,
                context TEXT,
                expires_at DATETIME,
                is_active INTEGER DEFAULT 1
            )""")
            conn.commit()
            conn.close()
            repaired.append("Created data/memory.db with memory_entries table")

        elif path_str == "data/activity.db":
            (root / "data").mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(full_path))
            conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                source TEXT,
                request TEXT,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                summary TEXT
            )""")
            conn.commit()
            conn.close()
            repaired.append("Created data/activity.db with tasks table")

    # Create today's log if missing
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = root / "memory" / "logs" / f"{today}.md"
    if not log_file.exists() and (root / "memory" / "logs").is_dir():
        log_file.write_text(
            f"# Daily Log: {today}\n\n"
            f"> Session log for {datetime.now().strftime('%A, %B %d, %Y')}\n\n"
            "---\n\n## Events & Notes\n\n",
            encoding="utf-8"
        )
        repaired.append(f"Created daily log: memory/logs/{today}.md")

    return repaired


def main():
    do_repair = "--repair" in sys.argv
    root = find_project_root()

    print(f"\nGOTCHA Health Check")
    print(f"Root: {root}")
    print(f"{'='*60}\n")

    all_results = []

    # Run all checks
    sections = [
        ("Directories", check_directories(root)),
        ("Files", check_files(root)),
        ("Databases", check_databases(root)),
        ("Themes", check_themes(root)),
        ("Skills", check_skills(root)),
    ]

    total_pass = 0
    total_fail = 0

    for section_name, results in sections:
        print(f"## {section_name}")
        for path_str, ok, desc in results:
            status = "PASS" if ok else "FAIL"
            icon = "+" if ok else "-"
            print(f"  [{icon}] {path_str} — {desc}")
            if ok:
                total_pass += 1
            else:
                total_fail += 1
            all_results.append((path_str, ok, desc))
        print()

    # Summary
    print(f"{'='*60}")
    print(f"Results: {total_pass} pass, {total_fail} fail")

    if total_fail > 0 and do_repair:
        print(f"\nRepairing...\n")
        repaired = repair(root, all_results)
        for msg in repaired:
            print(f"  [*] {msg}")
        print(f"\nRepaired {len(repaired)} items. Run again to verify.")

    elif total_fail > 0:
        print(f"\nRun with --repair to fix issues.")
        sys.exit(1)
    else:
        print(f"\nAll systems healthy.")
        sys.exit(0)


if __name__ == "__main__":
    main()
