import os
import shutil
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Restore skills to the correct directory based on the AI client.")
    parser.add_argument("source_root", help="The directory containing the skill backups.")
    parser.add_argument("--client", choices=["opencode", "pi"], default="opencode", help="The AI client to restore skills for (default: opencode).")
    args = parser.parse_args()

    source_root = os.path.abspath(args.source_root)
    
    if args.client == "opencode":
        target_root = os.path.expanduser('~/.opencode')
        skills_dir = os.path.join(target_root, 'skills')
    else:
        target_root = os.path.expanduser('~/.pi/agent')
        skills_dir = os.path.join(target_root, 'skills')

    # Ensure target directory exists and is clean
    if os.path.exists(skills_dir):
        shutil.rmtree(skills_dir, ignore_errors=True)
    os.makedirs(skills_dir, exist_ok=True)

    seen_skills = set()
    count = 0
    # Walk through the backup directory
    for root, dirs, files in os.walk(source_root):
        rel = os.path.relpath(root, source_root)
        parts = rel.split(os.sep)
        if '.git' in parts or '__pycache__' in parts:
            continue
        # Skip nested skills subdirectories inside skills
        if 'skills' in parts and len(parts) > 1 and parts[0] != 'config-skills':
            continue

        if 'SKILL.md' in files:
            skill_name = os.path.basename(root)
            if skill_name in seen_skills:
                continue
            seen_skills.add(skill_name)
            
            dest_path = os.path.join(skills_dir, skill_name)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path, exist_ok=True)
            
            # Copy the directory content
            for item in os.listdir(root):
                s = os.path.join(root, item)
                d = os.path.join(dest_path, item)
                if os.path.isdir(s):
                    if item != 'skills' and item != '__pycache__':
                        shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            
            print(f"Restored skill [{skill_name}] -> {dest_path}")
            count += 1

    print(f"Total unique skills restored to {args.client}: {count}")

if __name__ == "__main__":
    main()