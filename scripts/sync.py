#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import re
import tempfile

# Reconfigure stdout/stderr for Unicode support on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure scripts directory is in sys.path for reliable imports
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

# Imports categories mapping from update_readme.py dynamically
from update_readme import USER_CATEGORIES, CONFIG_CATEGORIES, extract_frontmatter, determine_category, repo_dir

VALID_SKILL_NAME_RE = re.compile(r"^[a-zA-Z0-9_\-\.]+$")
IGNORED_DIR_NAMES = {".git", "__pycache__", ".venv", "node_modules"}
NON_SKILL_TOP_DIRS = {"skills", "config-skills", "scripts", "categories", "docs", "oss", "tests", "__pycache__", "node_modules"}


def is_valid_skill_name(skill_name: str) -> bool:
    """Validate skill directory name against traversal and special names."""
    if not skill_name or skill_name in (".", ".."):
        return False
    return bool(VALID_SKILL_NAME_RE.match(skill_name))


def get_client_skills_dir(client: str) -> str:
    client = client.lower()
    if client == "pi":
        return os.path.expanduser("~/.pi/agent/skills")
    elif client == "gemini":
        return os.path.expanduser("~/.gemini/config/skills")
    elif client == "claude":
        return os.path.expanduser("~/.claude/skills")
    elif client == "opencode":
        return os.path.expanduser("~/.opencode/skills")
    elif client == "hermes":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return os.path.join(local_app_data, "hermes", "skills")
        return os.path.expanduser("~/.local/share/hermes/skills")
    else:
        return os.path.expanduser("~/.pi/agent/skills")


def is_safe_subpath(base_dir: str, target_path: str, allow_equal: bool = True) -> bool:
    """Verify that target_path resides strictly within base_dir."""
    real_base = os.path.realpath(base_dir)
    real_target = os.path.realpath(target_path)
    try:
        if os.path.commonpath([real_base, real_target]) != real_base:
            return False
        if not allow_equal and real_target == real_base:
            return False
        return True
    except ValueError:
        return False


def _copy_tree_safe(src_dir: str, dst_dir: str, allowed_src_root: str) -> None:
    """Copy a skill directory while blocking symlinks escaping allowed_src_root and ignored folders."""
    os.makedirs(dst_dir, exist_ok=True)
    for item in sorted(os.listdir(src_dir)):
        if item in IGNORED_DIR_NAMES or item == "skills":
            continue
        s = os.path.join(src_dir, item)
        d = os.path.join(dst_dir, item)
        if os.path.islink(s):
            link_target = os.path.realpath(s)
            if not os.path.exists(link_target) or not is_safe_subpath(allowed_src_root, link_target):
                print(f"Warning: Skipping unsafe or broken symlink {s} -> {link_target}", file=sys.stderr)
                continue
            s = link_target
        if os.path.isdir(s):
            _copy_tree_safe(s, d, allowed_src_root)
        elif os.path.isfile(s):
            shutil.copy2(s, d)


def _atomic_replace_dir(src_dir: str, dst_dir: str, allowed_src_root: str) -> None:
    """Stage copy into a temp directory alongside dst_dir and swap atomically to avoid data loss on error."""
    parent_dir = os.path.dirname(dst_dir)
    os.makedirs(parent_dir, exist_ok=True)
    staging_dir = tempfile.mkdtemp(prefix=f".sync_tmp_{os.path.basename(dst_dir)}_", dir=parent_dir)
    backup_dir = None
    try:
        _copy_tree_safe(src_dir, staging_dir, allowed_src_root)
        if os.path.exists(dst_dir):
            backup_dir = tempfile.mkdtemp(prefix=f".sync_bak_{os.path.basename(dst_dir)}_", dir=parent_dir)
            os.rmdir(backup_dir)
            os.replace(dst_dir, backup_dir)
        os.replace(staging_dir, dst_dir)
        if backup_dir and os.path.exists(backup_dir):
            if os.path.isdir(backup_dir) and not os.path.islink(backup_dir):
                shutil.rmtree(backup_dir)
            else:
                os.remove(backup_dir)
    except Exception:
        # Rollback if dst_dir was moved aside
        if backup_dir and os.path.exists(backup_dir) and not os.path.exists(dst_dir):
            try:
                os.replace(backup_dir, dst_dir)
            except Exception:
                pass
        if os.path.exists(staging_dir):
            shutil.rmtree(staging_dir, ignore_errors=True)
        raise


def get_all_skills_in_repo(local_dir: str, base_repo_dir: str = None):
    """
    Discover unique skills in the repository with deterministic precedence:
    1. Top-level root user skills take precedence over config-skills/
    2. Legacy skills/ mirror directory is excluded
    """
    root_repo = os.path.realpath(base_repo_dir or repo_dir)
    skills = []
    seen = set()

    # 1. Walk root for user skills (top-level directories first)
    for entry in sorted(os.listdir(root_repo)):
        if entry.startswith(".") or entry in NON_SKILL_TOP_DIRS:
            continue
        entry_path = os.path.join(root_repo, entry)
        if not os.path.isdir(entry_path):
            continue
        skill_md = os.path.join(entry_path, "SKILL.md")
        if os.path.isfile(skill_md) and is_valid_skill_name(entry):
            seen.add(entry)
            info = extract_frontmatter(skill_md) or {}
            group_key = info.get("group") or determine_category(entry, is_config=False)
            skills.append({
                "name": entry,
                "repo_path": entry_path,
                "local_path": os.path.join(local_dir, entry),
                "is_config": False,
                "group": group_key,
                "is_new_local": False,
            })

    # 2. Walk config-skills folder (skip duplicates already present at root)
    config_skills_repo = os.path.join(root_repo, "config-skills")
    if os.path.isdir(config_skills_repo):
        for root, dirs, files in os.walk(config_skills_repo, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIR_NAMES and not d.startswith("."))
            if "SKILL.md" in files:
                name = os.path.basename(root)
                if not is_valid_skill_name(name) or name in seen:
                    dirs[:] = []
                    continue
                seen.add(name)
                skill_md = os.path.join(root, "SKILL.md")
                rel_path = os.path.relpath(root, root_repo)
                info = extract_frontmatter(skill_md) or {}
                group_key = info.get("group") or determine_category(rel_path, is_config=True)
                skills.append({
                    "name": name,
                    "repo_path": root,
                    "local_path": os.path.join(local_dir, name),
                    "is_config": True,
                    "group": group_key,
                    "is_new_local": False,
                })
                dirs[:] = []

    return skills


def get_client_only_skills(local_dir: str, existing_names: set, base_repo_dir: str = None):
    """Discover newly created local skills in the client directory not yet tracked in the repository."""
    root_repo = os.path.realpath(base_repo_dir or repo_dir)
    new_skills = []
    if not os.path.isdir(local_dir):
        return new_skills

    for entry in sorted(os.listdir(local_dir)):
        if entry in existing_names or entry.startswith(".") or entry in NON_SKILL_TOP_DIRS:
            continue
        if not is_valid_skill_name(entry):
            continue
        local_path = os.path.join(local_dir, entry)
        if os.path.islink(local_path) or not os.path.isdir(local_path):
            continue
        skill_md = os.path.join(local_path, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        info = extract_frontmatter(skill_md) or {}
        group_key = info.get("group") or determine_category(entry, is_config=False)
        new_skills.append({
            "name": entry,
            "repo_path": os.path.join(root_repo, entry),
            "local_path": local_path,
            "is_config": False,
            "group": group_key,
            "is_new_local": True,
        })

    return new_skills


def list_groups():
    print("Available Custom User Skill Groups:")
    for key, info in USER_CATEGORIES.items():
        print(f"  - {key:<30} ({info['title']})")
    print("\nAvailable System Config Skill Groups:")
    for key, info in CONFIG_CATEGORIES.items():
        print(f"  - {key:<30} ({info['title']})")
    print("  - other                          (Uncategorized)")


def sync_skills(
    direction: str,
    client: str = "pi",
    filter_group: str = None,
    dry_run: bool = False,
    include_new: bool = True,
    base_repo_dir: str = None,
    local_dir_override: str = None,
):
    local_dir = os.path.realpath(local_dir_override or get_client_skills_dir(client))
    real_repo_dir = os.path.realpath(base_repo_dir or repo_dir)
    skills = get_all_skills_in_repo(local_dir, base_repo_dir=real_repo_dir)

    if direction == "save" and include_new:
        existing_names = {s["name"] for s in skills}
        skills.extend(get_client_only_skills(local_dir, existing_names, base_repo_dir=real_repo_dir))

    if filter_group:
        skills = [s for s in skills if s["group"] == filter_group]
        if not skills:
            print(f"No skills found matching group '{filter_group}'.")
            return {"processed": 0, "unique": 0, "new_backed_up": 0}

    mode_prefix = "[DRY-RUN] " if dry_run else ""
    print(f"{mode_prefix}Starting sync ({direction}) for client '{client}' [{local_dir}]...")

    success_count = 0
    new_backed_up = 0
    synced_names = set()

    for s in skills:
        if not is_valid_skill_name(s["name"]):
            print(f"Warning: Skipping invalid skill name '{s['name']}'.", file=sys.stderr)
            continue

        src = s["repo_path"] if direction == "deploy" else s["local_path"]
        dst = s["local_path"] if direction == "deploy" else s["repo_path"]

        allowed_dst_base = local_dir if direction == "deploy" else real_repo_dir
        allowed_src_base = real_repo_dir if direction == "deploy" else local_dir

        if not os.path.exists(src):
            if direction == "save":
                continue
            print(f"Warning: Source path {src} does not exist. Skipping.")
            continue

        if not is_safe_subpath(allowed_src_base, src, allow_equal=False):
            print(f"Security Alert: Source '{src}' is outside allowed base '{allowed_src_base}'. Skipping.", file=sys.stderr)
            continue

        if not is_safe_subpath(allowed_dst_base, dst, allow_equal=False):
            print(f"Security Alert: Destination '{dst}' is outside allowed base '{allowed_dst_base}'. Skipping.", file=sys.stderr)
            continue

        if dry_run:
            tag = " [NEW]" if s.get("is_new_local") else ""
            print(f"  [DRY-RUN] Would {direction}{tag}: {s['name']} ({src} -> {dst})")
            synced_names.add(s["name"])
            success_count += 1
            if s.get("is_new_local"):
                new_backed_up += 1
            continue

        try:
            _atomic_replace_dir(src, dst, allowed_src_base)
            synced_names.add(s["name"])
            success_count += 1
            if s.get("is_new_local"):
                new_backed_up += 1
                print(f"  [NEW] Backed up client-only skill '{s['name']}' -> {dst}")
        except Exception as e:
            print(f"  Error syncing {s['name']}: {e}", file=sys.stderr)

    extra_note = f" (including {new_backed_up} newly backed up client-only skills)" if new_backed_up else ""
    print(
        f"{mode_prefix}Sync complete. Successfully processed {success_count} location updates "
        f"for {len(synced_names)} unique skills{extra_note}."
    )
    return {"processed": success_count, "unique": len(synced_names), "new_backed_up": new_backed_up}


def main():
    parser = argparse.ArgumentParser(description="Synchronize skills between repo and local AI client directories.")
    parser.add_argument("action", choices=["deploy", "save"], help="deploy: repo -> local; save: local -> repo")
    parser.add_argument(
        "--client",
        choices=["pi", "gemini", "claude", "opencode", "hermes"],
        default="pi",
        help="Target AI client (default: pi)",
    )
    parser.add_argument("-g", "--group", help="Filter by skill category/group name")
    parser.add_argument("-l", "--list-groups", action="store_true", help="List all available group names")
    parser.add_argument("--dry-run", action="store_true", help="Preview sync operations without modifying files")
    parser.add_argument(
        "--no-new",
        action="store_true",
        help="During 'save', only update skills already tracked in the repository (skip client-only skills)",
    )

    if "-l" in sys.argv or "--list-groups" in sys.argv:
        list_groups()
        sys.exit(0)

    args = parser.parse_args()
    sync_skills(
        args.action,
        client=args.client,
        filter_group=args.group,
        dry_run=args.dry_run,
        include_new=not args.no_new,
    )


if __name__ == "__main__":
    main()
