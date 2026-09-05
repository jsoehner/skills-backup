#!/usr/bin/env python3
"""
Skills Catalog and Status Inspector

Provides functions and CLI commands to:
1. Browse and search the skills catalog organized by category.
2. Show new vs. existing (installed) skills for a target AI client runtime.
"""

import os
import sys
import argparse
import re
from typing import Dict, List, Set, Tuple

# Ensure scripts directory is in sys.path
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

try:
    from update_readme import (
        USER_CATEGORIES,
        CONFIG_CATEGORIES,
        extract_frontmatter,
        determine_category,
        scan_skills_dir,
        repo_dir
    )
except ImportError:
    repo_dir = os.path.dirname(_script_dir)
    USER_CATEGORIES = {}
    CONFIG_CATEGORIES = {}
    def extract_frontmatter(path): return None
    def determine_category(path, is_config=False): return "other"
    def scan_skills_dir(directory, is_config=False): return []

def get_client_skills_dir(client: str) -> str:
    """Resolve target client skills directory path."""
    client_map = {
        "pi": "~/.pi/agent/skills",
        "gemini": "~/.gemini/config/skills",
        "claude": "~/.claude/skills",
        "opencode": "~/.opencode/skills"
    }
    path_str = client_map.get(client.lower(), "~/.pi/agent/skills")
    return os.path.realpath(os.path.abspath(os.path.expanduser(path_str)))

def get_installed_skills(client: str) -> Dict[str, str]:
    """Scan local AI client directory for installed skills."""
    skills_dir = get_client_skills_dir(client)
    installed = {}
    if not os.path.exists(skills_dir):
        return installed

    for item in sorted(os.listdir(skills_dir)):
        item_path = os.path.join(skills_dir, item)
        if os.path.isdir(item_path):
            skill_md = os.path.join(item_path, "SKILL.md")
            if os.path.isfile(skill_md):
                installed[item] = item_path
    return installed

def get_repo_skills() -> Tuple[List[dict], List[dict]]:
    """Scan repository for all user skills and config skills."""
    user_skills = scan_skills_dir(repo_dir, is_config=False)
    config_skills_path = os.path.join(repo_dir, "config-skills")
    config_skills = scan_skills_dir(config_skills_path, is_config=True) if os.path.exists(config_skills_path) else []
    return user_skills, config_skills

def show_catalog(category_filter: str = None, search_query: str = None, include_config: bool = True):
    """Print the formatted skill catalog."""
    user_skills, config_skills = get_repo_skills()
    all_skills = list(user_skills)
    if include_config:
        all_skills.extend(config_skills)

    # Filter by search query if provided
    if search_query:
        query_lower = search_query.lower()
        all_skills = [
            s for s in all_skills
            if query_lower in s.get("name", "").lower() or query_lower in s.get("description", "").lower()
        ]

    # Filter by category if provided
    if category_filter:
        cat_lower = category_filter.lower()
        all_skills = [s for s in all_skills if cat_lower in s.get("group_key", "").lower()]

    if not all_skills:
        print(f"No skills found matching filter (category='{category_filter}', search='{search_query}').")
        return

    # Group skills by category
    by_category: Dict[str, List[dict]] = {}
    for s in all_skills:
        cat = s.get("group_key", "other")
        by_category.setdefault(cat, []).append(s)

    print("=" * 80)
    print(f"SKILLS CATALOG ({len(all_skills)} skills found)")
    print("=" * 80)

    for cat_key in sorted(by_category.keys()):
        skills_in_cat = by_category[cat_key]
        cat_title = (
            USER_CATEGORIES.get(cat_key, {}).get("title")
            or CONFIG_CATEGORIES.get(cat_key, {}).get("title")
            or f"📁 {cat_key.replace('_', ' ').title()}"
        )
        print(f"\n{cat_title} ({len(skills_in_cat)} skills)")
        print("-" * 80)
        for s in sorted(skills_in_cat, key=lambda x: x.get("name", "")):
            name = s.get("name", "unnamed")
            desc = s.get("description", "").strip()
            # Truncate description for clean catalog listing
            if len(desc) > 85:
                desc = desc[:82] + "..."
            print(f"  • {name:<35} {desc}")

    print("\n" + "=" * 80)

def show_categories():
    """List all available categories and skill counts."""
    user_skills, config_skills = get_repo_skills()
    all_skills = user_skills + config_skills
    counts: Dict[str, int] = {}
    for s in all_skills:
        cat = s.get("group_key", "other")
        counts[cat] = counts.get(cat, 0) + 1

    print("=" * 80)
    print("AVAILABLE SKILL CATEGORIES")
    print("=" * 80)
    print(f"{'Category Key':<30} {'Title':<40} {'Count':<5}")
    print("-" * 80)
    for cat_key in sorted(counts.keys()):
        title = (
            USER_CATEGORIES.get(cat_key, {}).get("title")
            or CONFIG_CATEGORIES.get(cat_key, {}).get("title")
            or cat_key.replace('_', ' ').title()
        )
        print(f"{cat_key:<30} {title:<40} {counts[cat_key]:<5}")
    print("=" * 80)
    print(f"Total skills across all categories: {len(all_skills)}")

def show_status(client: str = "pi", filter_mode: str = "all", search_query: str = None):
    """
    Compare repository skills against local client installation.
    filter_mode: 'all', 'new', 'existing' / 'installed', 'orphaned'
    """
    client_dir = get_client_skills_dir(client)
    installed = get_installed_skills(client)
    user_skills, config_skills = get_repo_skills()
    all_repo_skills = {s["name"]: s for s in (user_skills + config_skills)}

    installed_names = set(installed.keys())
    repo_names = set(all_repo_skills.keys())

    existing_names = sorted(installed_names.intersection(repo_names))
    new_names = sorted(repo_names - installed_names)
    client_only_names = sorted(installed_names - repo_names)

    # Optional search filtering
    if search_query:
        sq = search_query.lower()
        existing_names = [n for n in existing_names if sq in n]
        new_names = [n for n in new_names if sq in n]
        client_only_names = [n for n in client_only_names if sq in n]

    print("=" * 80)
    print(f"SKILLS STATUS FOR CLIENT: {client.upper()}")
    print(f"Target Directory: {client_dir}")
    print("=" * 80)
    print(f"Summary:")
    print(f"  • Existing (Installed) in {client} : {len(existing_names)}")
    print(f"  • New (Uninstalled) from repo    : {len(new_names)}")
    if client_only_names:
        print(f"  • Client-only (Not in repo)       : {len(client_only_names)}")
    print(f"  • Total Repository Skills         : {len(repo_names)}")
    print("=" * 80)

    # Show new / uninstalled skills
    if filter_mode in ("all", "new") and new_names:
        print(f"\n🆕 NEW / UNINSTALLED SKILLS ({len(new_names)} available to restore):")
        print("-" * 80)
        for name in new_names:
            skill = all_repo_skills.get(name, {})
            cat = skill.get("group_key", "other")
            desc = skill.get("description", "")
            if len(desc) > 60:
                desc = desc[:57] + "..."
            print(f"  [+] {name:<35} [{cat:<20}] {desc}")

    # Show existing / installed skills
    if filter_mode in ("all", "existing", "installed") and existing_names:
        print(f"\n✅ EXISTING / INSTALLED SKILLS ({len(existing_names)} active in {client}):")
        print("-" * 80)
        for name in existing_names:
            skill = all_repo_skills.get(name, {})
            cat = skill.get("group_key", "other")
            desc = skill.get("description", "")
            if len(desc) > 60:
                desc = desc[:57] + "..."
            print(f"  [✓] {name:<35} [{cat:<20}] {desc}")

    # Show client only skills
    if filter_mode in ("all", "orphaned") and client_only_names:
        print(f"\n⚠️  CLIENT-ONLY SKILLS ({len(client_only_names)} not found in repo):")
        print("-" * 80)
        for name in client_only_names:
            print(f"  [?] {name:<35} (Installed in {client} but not tracked in repository)")

    print("\n" + "=" * 80)

def show_memory_info():
    """Display information about the local memory system and associated skills."""
    mem_root = os.path.realpath(os.path.abspath(os.path.expanduser("~/memory_system")))
    mem_db = os.path.join(mem_root, "db")
    mem_okf = os.path.join(mem_root, "knowledge", "okf")
    mem_inbox = os.path.join(mem_root, "inbox")

    def status_label(path):
        return "✅ Present" if os.path.exists(path) else "❌ Not found"

    print("=" * 80)
    print("🧠 LOCAL AGENT MEMORY & RAG ARCHITECTURE")
    print("=" * 80)
    print("This repository provides a multi-tiered local memory architecture designed to")
    print("capture, persist, and retrieve agent learnings without consuming frontier LLM tokens.\n")

    print("📁 Storage Layout & Local Host Status:")
    print("-" * 80)
    print(f"  • Root Directory  : {mem_root:<40} [{status_label(mem_root)}]")
    print(f"  • ChromaDB Vector : {mem_db:<40} [{status_label(mem_db)}]")
    print(f"  • OKF Policies    : {mem_okf:<40} [{status_label(mem_okf)}]")
    print(f"  • Ingest Inbox    : {mem_inbox:<40} [{status_label(mem_inbox)}]")
    print("-" * 80)

    print("\n🧩 Key Memory & Context Skills:")
    print("-" * 80)
    print("  1. memory-capture")
    print("     - Routes architectural rules into OKF (regex / deterministic matching).")
    print("     - Routes troubleshooting logs and snippets into local ChromaDB vector store.")
    print("     - Ingestion script: python3 ~/memory_system/capture_knowledge.py <file.md>")
    print("  2. context-manager")
    print("     - Context assembly, working/long-term memory tiers, and token budget control.")
    print("  3. session-handoff")
    print("     - Transfers working memory, active decisions, and pending tasks between sessions.")
    print("  4. rag-implementation & similarity-search-patterns")
    print("     - Patterns for custom retrieval-augmented generation and vector index tuning.")

    print("\n🚀 Initialization & Ingestion Commands:")
    print("-" * 80)
    print("  Initialize storage:  python3 ~/memory_system/init_storage.py")
    print("  Ingest knowledge:    python3 ~/memory_system/capture_knowledge.py <summary.md>")
    print("  Or drop Markdown:    cp <notes.md> ~/memory_system/inbox/")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="View skills catalog and installation status across AI clients.")
    parser.add_argument("--client", choices=["pi", "gemini", "claude", "opencode"], default="pi",
                        help="Target AI client to inspect (default: pi)")
    parser.add_argument("-c", "--catalog", action="store_true",
                        help="Show the full skills catalog grouped by category")
    parser.add_argument("-s", "--status", action="store_true",
                        help="Show installation status (existing vs new skills) for the target client")
    parser.add_argument("--new", action="store_true",
                        help="Show only new/uninstalled skills for the target client")
    parser.add_argument("--installed", "--existing", dest="installed", action="store_true",
                        help="Show only installed/existing skills for the target client")
    parser.add_argument("--categories", action="store_true",
                        help="List all categories with skill counts")
    parser.add_argument("-m", "--memory", "--memory-info", dest="memory", action="store_true",
                        help="Show information and host status for the local memory system (OKF + ChromaDB)")
    parser.add_argument("-g", "--group", "--category", dest="category",
                        help="Filter catalog by category name")
    parser.add_argument("-q", "--search",
                        help="Search skills by name or description keyword")

    args = parser.parse_args()

    # Default action if none specified: show status
    if not (args.catalog or args.status or args.new or args.installed or args.categories or args.memory):
        # If group or search is specified without flags, default to catalog view
        if args.category or args.search:
            show_catalog(category_filter=args.category, search_query=args.search)
        else:
            show_status(client=args.client, filter_mode="all")
        return

    if args.memory:
        show_memory_info()
    elif args.categories:
        show_categories()
    elif args.catalog:
        show_catalog(category_filter=args.category, search_query=args.search)
    elif args.new:
        show_status(client=args.client, filter_mode="new", search_query=args.search)
    elif args.installed:
        show_status(client=args.client, filter_mode="existing", search_query=args.search)
    elif args.status:
        show_status(client=args.client, filter_mode="all", search_query=args.search)

if __name__ == "__main__":
    main()
