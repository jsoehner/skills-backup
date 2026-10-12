import os
import shutil
import sys
import argparse
import re
from datetime import datetime

def is_safe_subpath(base_dir: str, target_path: str) -> bool:
    """Verify that target_path resides strictly within base_dir."""
    real_base = os.path.realpath(base_dir)
    real_target = os.path.realpath(target_path)
    try:
        return os.path.commonpath([real_base, real_target]) == real_base
    except ValueError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Restore skills to the correct directory based on the AI client.")
    parser.add_argument("source_root", help="The directory containing the skill backups.")
    parser.add_argument("--client", choices=["opencode", "pi", "gemini", "claude", "hermes"], default="pi", help="The AI client to restore skills for (default: pi).")
    args = parser.parse_args()

    source_root = os.path.realpath(os.path.abspath(args.source_root))
    if not os.path.exists(source_root):
        print(f"Error: Source root '{source_root}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    if args.client == "opencode":
        target_root = os.path.expanduser('~/.opencode')
        skills_dir = os.path.join(target_root, 'skills')
    elif args.client == "gemini":
        target_root = os.path.expanduser('~/.gemini/config')
        skills_dir = os.path.join(target_root, 'skills')
    elif args.client == "claude":
        target_root = os.path.expanduser('~/.claude')
        skills_dir = os.path.join(target_root, 'skills')
    elif args.client == "hermes":
        skills_dir = "C:/Users/jsoehner/AppData/Local/hermes/skills"
    else:
        target_root = os.path.expanduser('~/.pi/agent')
        skills_dir = os.path.join(target_root, 'skills')

    skills_dir = os.path.realpath(os.path.abspath(skills_dir))
    os.makedirs(skills_dir, exist_ok=True)

    seen_skills = set()
    count = 0
    # Walk through the backup directory
    for root, dirs, files in os.walk(source_root, followlinks=False):
        rel = os.path.relpath(root, source_root)
        parts = rel.split(os.sep)
        if '.git' in parts or '__pycache__' in parts:
            continue
        # Skip nested subdirectories inside skills
        if ('skills' in parts or 'config-skills' in parts) and len(parts) > 2:
            continue

        if 'SKILL.md' in files:
            skill_name = os.path.basename(root)
            # Validate skill name format against path injection
            if not re.match(r'^[a-zA-Z0-9_\-\.]+$', skill_name):
                print(f"Warning: Skipping invalid skill directory name '{skill_name}'", file=sys.stderr)
                continue

            if skill_name in seen_skills:
                continue
            seen_skills.add(skill_name)
            
            dest_path = os.path.abspath(os.path.join(skills_dir, skill_name))
            if not is_safe_subpath(skills_dir, dest_path):
                print(f"Security Alert: Blocked traversal attempt for '{skill_name}' -> '{dest_path}'", file=sys.stderr)
                continue

            os.makedirs(dest_path, exist_ok=True)
            
            # Copy directory content defensively
            for item in os.listdir(root):
                s = os.path.join(root, item)
                d = os.path.join(dest_path, item)
                
                # Check for symlink escaping source root
                if os.path.islink(s):
                    link_target = os.path.realpath(s)
                    if not is_safe_subpath(source_root, link_target):
                        print(f"Warning: Skipping unsafe symlink {s} -> {link_target}", file=sys.stderr)
                        continue

                if os.path.isdir(s):
                    if item != 'skills' and item != '__pycache__':
                        shutil.copytree(s, d, symlinks=False, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d, follow_symlinks=False)
            
            skill_md_path = os.path.join(root, 'SKILL.md')
            try:
                mtime = os.path.getmtime(skill_md_path)
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"[{date_str}] Restored skill [{skill_name}] -> {dest_path}")
            count += 1

    print(f"Total unique skills restored to {args.client}: {count}")

    # Synchronize governance rules and memory system tools across AI client harnesses
    if 'target_root' in locals():
        sync_client_governance(args.client, target_root, source_root)

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

        elif client in ("pi", "opencode"):
            agents_md = os.path.join(target_root, "AGENTS.md")
            with open(agents_md, "w", encoding="utf-8") as f:
                f.write(governance_text)
            print(f"Synchronized governance rules to {client} -> {agents_md}")
    except Exception as e:
        print(f"Warning: Failed to synchronize client governance rules: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
