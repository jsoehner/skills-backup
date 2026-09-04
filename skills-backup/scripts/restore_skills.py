import os
import shutil
import sys
import argparse
from pathlib import Path

def detect_installed_harnesses():
    \"\"\"Detects active AI harnesses based on local directory existence.\"\"\"
    harnesses = []
    # Define common locations
    targets = {
        "pi": os.path.expanduser('~/.pi/agent/skills'),
        "gemini": os.path.expanduser('~/.gemini/config/skills'),
        "claude": os.path.expanduser('~/.claude/skills'),
        "opencode": os.path.expanduser('~/.opencode/skills'),
        "cursor": os.path.expanduser('~/.cursor/skills'),
        "codex": os.path.expanduser('~/.codex/skills'),
        "hermes": os.path.expanduser('~/.hermes/skills')
    }
    
    for name, path in targets.items():
        if os.path.exists(path):
            harnesses.append(name)
    return harnesses

def main():
    parser = argparse.ArgumentParser(description="Restore skills to the correct directory based on the AI client.")
    parser.add_argument("source_root", help="The directory containing the skill backups.")
    parser.add_argument("--client", choices=["opencode", "pi", "gemini", "claude", "cursor", "codex", "hermes"], default=None, 
                        help="The AI client to restore skills for. If omitted, the first detected harness will be used.")
    args = parser.parse_args()

    source_root = os.path.abspath(args.source_root)
    
    # Detection Logic
    detected = detect_installed_harnesses()
    
    if not args.client:
        if detected:
            print(f"No client specified. Detected active harnesses: {', '.join(detected)}")
            print(f"Defaulting to: {detected[0]}")
            args.client = detected[0]
        else:
            print("Warning: No active harnesses detected in standard locations.")
            print("Defaulting to 'pi'.")
            args.client = "pi"

    # Path resolution based on client
    if args.client == "opencode":
        target_root = os.path.expanduser('~/.opencode')
        skills_dir = os.path.join(target_root, 'skills')
    elif args.client == "gemini":
        target_root = os.path.expanduser('~/.gemini/config')
        skills_dir = os.path.join(target_root, 'skills')
    elif args.client == "claude":
        target_root = os.path.expanduser('~/.claude')
        skills_dir = os.path.join(target_root, 'skills')
    elif args.client == "cursor":
        target_root = os.path.expanduser('~/.cursor')
        skills_dir = os.path.join(target_root, 'skills')
    elif args.client == "codex":
        target_root = os.path.expanduser('~/.codex')
        skills_dir = os.path.join(target_root, 'skills')
    elif args.client == "hermes":
        target_root = os.path.expanduser('~/.hermes')
        skills_dir = os.path.join(target_root, 'skills')
    else:
        target_root = os.path.expanduser('~/.pi/agent')
        skills_dir = os.path.join(target_root, 'skills')

    # If a "skills" directory exists in the source, use it as the base for walking
    if os.path.isdir(os.path.join(source_root, "skills")):
        source_root = os.path.join(source_root, "skills")
    
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
                        shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            
            print(f"Restored skill [{skill_name}] -> {dest_path}")
            count += 1

    print(f"\nTotal unique skills restored to {args.client}: {count}")

if __name__ == "__main__":
    main()
