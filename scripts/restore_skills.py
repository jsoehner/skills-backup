#!/usr/bin/env python3
import os
import shutil
import sys
import argparse
import re
from datetime import datetime

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

VALID_SKILL_NAME_RE = re.compile(r"^[a-zA-Z0-9_\-\.]+$")
IGNORED_DIR_NAMES = {".git", "__pycache__", ".venv", "node_modules"}


def is_valid_skill_name(skill_name: str) -> bool:
    """Validate skill directory name against traversal and special names."""
    if not skill_name or skill_name in (".", ".."):
        return False
    return bool(VALID_SKILL_NAME_RE.match(skill_name))


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


def get_client_paths(client: str):
    """Resolve (target_root, skills_dir) for a supported AI client."""
    client = client.lower()
    if client == "opencode":
        target_root = os.path.expanduser("~/.opencode")
    elif client == "gemini":
        target_root = os.path.expanduser("~/.gemini/config")
    elif client == "claude":
        target_root = os.path.expanduser("~/.claude")
    elif client == "hermes":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            target_root = os.path.join(local_app_data, "hermes")
        else:
            target_root = os.path.expanduser("~/.local/share/hermes")
    else:
        target_root = os.path.expanduser("~/.pi/agent")

    skills_dir = os.path.realpath(os.path.abspath(os.path.join(target_root, "skills")))
    return os.path.realpath(os.path.abspath(target_root)), skills_dir


def copy_skill_contents(src_dir: str, dest_dir: str, allowed_src_root: str) -> None:
    """Defensively copy skill directory contents while blocking symlink escapes and ignored dirs."""
    os.makedirs(dest_dir, exist_ok=True)

    for item in sorted(os.listdir(src_dir)):
        if item in IGNORED_DIR_NAMES or item == "skills":
            continue

        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)

        if os.path.islink(s):
            link_target = os.path.realpath(s)
            if not os.path.exists(link_target) or not is_safe_subpath(allowed_src_root, link_target):
                print(f"Warning: Skipping unsafe or broken symlink {s} -> {link_target}", file=sys.stderr)
                continue
            s = link_target

        if os.path.isdir(s):
            copy_skill_contents(s, d, allowed_src_root)
        elif os.path.isfile(s):
            shutil.copy2(s, d)


def discover_candidate_skills(source_root: str):
    """
    Discover skills in deterministic precedence order:
    1. Top-level root skill directories (highest priority)
    2. Mirrored / nested skill directories (e.g., config-skills/)
    """
    candidate_roots = []

    for entry in sorted(os.listdir(source_root)):
        full_entry = os.path.join(source_root, entry)
        if (
            os.path.isdir(full_entry)
            and not entry.startswith(".")
            and entry not in ("skills", "config-skills", "__pycache__", "node_modules")
            and os.path.isfile(os.path.join(full_entry, "SKILL.md"))
        ):
            candidate_roots.append((full_entry, ["SKILL.md"]))

    for root, dirs, files in os.walk(source_root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIR_NAMES and not d.startswith("."))
        rel = os.path.relpath(root, source_root)
        parts = rel.split(os.sep)
        if ("skills" in parts or "config-skills" in parts) and len(parts) > 2:
            dirs[:] = []
            continue
        if "SKILL.md" in files and rel != ".":
            candidate_roots.append((root, files))
            # Do not descend into a skill directory looking for nested skills
            dirs[:] = []

    return candidate_roots


def restore_skills(source_root: str, client: str = "pi", dry_run: bool = False, clean: bool = False) -> int:
    """Restore all unique skills from source_root into the target client's skills directory."""
    source_root = os.path.realpath(os.path.abspath(source_root))
    if not os.path.exists(source_root):
        print(f"Error: Source root '{source_root}' does not exist.", file=sys.stderr)
        sys.exit(1)

    target_root, skills_dir = get_client_paths(client)
    if not dry_run:
        os.makedirs(skills_dir, exist_ok=True)

    seen_skills = set()
    count = 0
    candidate_roots = discover_candidate_skills(source_root)

    for root, files in candidate_roots:
        if "SKILL.md" not in files:
            continue

        skill_name = os.path.basename(root)
        if not is_valid_skill_name(skill_name):
            print(f"Warning: Skipping invalid skill directory name '{skill_name}'", file=sys.stderr)
            continue

        if skill_name in seen_skills:
            continue
        seen_skills.add(skill_name)

        dest_path = os.path.abspath(os.path.join(skills_dir, skill_name))
        if not is_safe_subpath(skills_dir, dest_path, allow_equal=False):
            print(f"Security Alert: Blocked traversal attempt for '{skill_name}' -> '{dest_path}'", file=sys.stderr)
            continue

        skill_md_path = os.path.join(root, "SKILL.md")
        try:
            mtime = os.path.getmtime(skill_md_path)
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if dry_run:
            action_label = "Would restore (clean)" if clean else "Would restore"
            print(f"[{date_str}] [DRY-RUN] {action_label} skill [{skill_name}] -> {dest_path}")
            count += 1
            continue

        if clean and os.path.exists(dest_path):
            if os.path.isdir(dest_path) and not os.path.islink(dest_path):
                shutil.rmtree(dest_path)
            else:
                os.remove(dest_path)

        copy_skill_contents(root, dest_path, source_root)
        print(f"[{date_str}] Restored skill [{skill_name}] -> {dest_path}")
        count += 1

    prefix = "[DRY-RUN] Total unique skills that would be restored" if dry_run else "Total unique skills restored"
    print(f"{prefix} to {client}: {count}")

    if not dry_run:
        sync_client_governance(client, target_root, source_root)
    else:
        print(f"[DRY-RUN] Would synchronize governance rules for client '{client}' under {target_root}")

    return count


def main():
    parser = argparse.ArgumentParser(description="Restore skills to the correct directory based on the AI client.")
    parser.add_argument("source_root", help="The directory containing the skill backups.")
    parser.add_argument(
        "--client",
        choices=["opencode", "pi", "gemini", "claude", "hermes"],
        default="pi",
        help="The AI client to restore skills for (default: pi).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview restore operations without writing files.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing destination skill directory contents before copying to avoid stale files.",
    )
    args = parser.parse_args()

    restore_skills(args.source_root, client=args.client, dry_run=args.dry_run, clean=args.clean)


def sync_client_governance(client: str, target_root: str, source_root: str):
    """
    Ensure the target AI harness receives global governance rules,
    fork guardrail policies, and memory pre-flight tools.
    """
    # 1. Keep shared memory system utilities synchronized
    mem_dir = os.path.expanduser("~/memory_system")
    if os.path.isdir(mem_dir):
        for script_name in ["check_fork_guardrail.py", "inspect_memory.py"]:
            src_script = os.path.join(source_root, "scripts", script_name)
            if os.path.isfile(src_script):
                dest_script = os.path.join(mem_dir, script_name)
                try:
                    shutil.copy2(src_script, dest_script)
                    os.chmod(dest_script, 0o755)
                except Exception as e:
                    print(f"Warning: Could not sync {script_name} to ~/memory_system: {e}", file=sys.stderr)

    governance_text = """# Global Repository Governance & Memory Pre-Flight Guardrails

## 1. Forked Repository & Upstream Guardrail
- **Never unilaterally update a forked repository**: Forked repositories have an upstream source of truth. Skills and agents must avoid updating, modifying dependencies, or creating pull requests on a forked repository unless it is verified abandoned.
- **Refresh before deciding**: Always consider refreshing the fork against its upstream source first:
  ```bash
  gh repo sync --branch <default-branch>
  ```
- **Abandonment Test**: Upstream is abandoned ONLY if archived (`isArchived: true`), returns 404/deleted, or has had zero commits/releases for >18 consecutive months.
- **Automated Verification**: Before modifying any repository, execute:
  ```bash
  python3 ~/memory_system/check_fork_guardrail.py .
  ```
  If this returns exit code 1 (BLOCKED), halt unilateral updates immediately. Submit proposed changes upstream via PR or sync the fork.

## 2. Mandatory Memory Pre-Flight Protocol
- **Retrieve Lessons Learned Before Acting**: Before planning, refactoring, or modifying code, query the local memory system:
  ```bash
  python3 ~/memory_system/inspect_memory.py --preflight .
  # Or query by topic:
  python3 ~/memory_system/inspect_memory.py -q "<topic>"
  ```
- **Adhere to OKF Architectural Decisions**: Check and obey policies located in `~/memory_system/knowledge/okf/` (including Fork Governance, GitHub Actions SHA pinning, Dependabot cooldown, and Security Governance).
"""

    try:
        os.makedirs(target_root, exist_ok=True)
        if client == "gemini":
            rules_dir = os.path.join(target_root, "rules")
            os.makedirs(rules_dir, exist_ok=True)
            rule_file = os.path.join(rules_dir, "fork-and-memory-governance.md")
            with open(rule_file, "w", encoding="utf-8") as f:
                f.write(governance_text)
            src_agents = os.path.join(source_root, "AGENTS.md")
            if os.path.isfile(src_agents):
                shutil.copy2(src_agents, os.path.join(target_root, "AGENTS.md"))
            print(f"Synchronized governance rules to Gemini -> {rule_file}")

        elif client == "claude":
            claude_md = os.path.join(target_root, "CLAUDE.md")
            with open(claude_md, "w", encoding="utf-8") as f:
                f.write(governance_text)
            print(f"Synchronized governance rules to Claude -> {claude_md}")

        elif client in ("pi", "opencode", "hermes"):
            agents_md = os.path.join(target_root, "AGENTS.md")
            with open(agents_md, "w", encoding="utf-8") as f:
                f.write(governance_text)
            print(f"Synchronized governance rules to {client} -> {agents_md}")
    except Exception as e:
        print(f"Warning: Failed to synchronize client governance rules: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
