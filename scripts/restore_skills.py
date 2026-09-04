import os
import shutil
import sys
import argparse
import re

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
    parser.add_argument("--client", choices=["opencode", "pi", "gemini", "claude"], default="pi", help="The AI client to restore skills for (default: pi).")
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
        # Skip nested skills subdirectories inside skills
        if 'skills' in parts and len(parts) > 1 and parts[0] != 'config-skills':
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
            
            print(f"Restored skill [{skill_name}] -> {dest_path}")
            count += 1

    print(f"Total unique skills restored to {args.client}: {count}")

if __name__ == "__main__":
    main()