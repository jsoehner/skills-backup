#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import re
import yaml

# Imports categories mapping from update_readme.py dynamically
from update_readme import USER_CATEGORIES, CONFIG_CATEGORIES, extract_frontmatter, determine_category, repo_dir

def get_client_skills_dir(client):
    if client == "opencode":
        return os.path.expanduser("~/.opencode/skills")
    elif client == "gemini":
        return os.path.expanduser("~/.gemini/config/skills")
    elif client == "claude":
        return os.path.expanduser("~/.claude/skills")
    else:
        return os.path.expanduser("~/.pi/agent/skills")

def get_all_skills_in_repo(local_dir):
    skills = []
    seen = set()
    
    # 1. Walk root for user skills
    for root, dirs, files in os.walk(repo_dir):
        parts = os.path.relpath(root, repo_dir).split(os.sep)
        if '.git' in parts or '__pycache__' in parts:
            continue
        # Skip nested skills subdirectories inside skills
        if 'skills' in parts[1:] and parts[0] != 'config-skills':
            continue
            
        if "SKILL.md" in files:
            rel_path = os.path.relpath(root, repo_dir)
            if rel_path == "." or rel_path == "":
                continue
            if "config-skills" in rel_path.split(os.sep):
                continue
                
            name = os.path.basename(root)
            if name in seen:
                continue
            seen.add(name)
            skill_md = os.path.join(root, "SKILL.md")
            info = extract_frontmatter(skill_md) or {}
            group_key = info.get("group") or determine_category(rel_path, is_config=False)
            skills.append({
                "name": name,
                "repo_path": root,
                "local_path": os.path.join(local_dir, name),
                "is_config": False,
                "group": group_key
            })
            
    # 2. Walk config-skills folder
    config_skills_repo = os.path.join(repo_dir, "skills", "config-skills")
    if not os.path.exists(config_skills_repo):
        config_skills_repo = os.path.join(repo_dir, "config-skills")
    if os.path.exists(config_skills_repo):
        for root, dirs, files in os.walk(config_skills_repo):
            parts = os.path.relpath(root, config_skills_repo).split(os.sep)
            if '.git' in parts or '__pycache__' in parts:
                continue
            if "SKILL.md" in files:
                name = os.path.basename(root)
                if name in seen:
                    continue
                seen.add(name)
                skill_md = os.path.join(root, "SKILL.md")
                rel_path = os.path.relpath(root, repo_dir)
                info = extract_frontmatter(skill_md) or {}
                group_key = info.get("group") or determine_category(rel_path, is_config=True)
                skills.append({
                    "name": name,
                    "repo_path": root,
                    "local_path": os.path.join(local_dir, name),
                    "is_config": True,
                    "group": group_key
                })
    return skills

def list_groups():
    print("Available Custom User Skill Groups:")
    for key, info in USER_CATEGORIES.items():
        print(f"  - {key:<30} ({info['title']})")
    print("\nAvailable System Config Skill Groups:")
    for key, info in CONFIG_CATEGORIES.items():
        print(f"  - {key:<30} ({info['title']})")
    print("  - other                          (Uncategorized)")

def sync_skills(direction, client="pi", filter_group=None):
    local_dir = get_client_skills_dir(client)
    skills = get_all_skills_in_repo(local_dir)
    
    if filter_group:
        skills = [s for s in skills if s["group"] == filter_group]
        if not skills:
            print(f"No skills found matching group '{filter_group}'.")
            return
            
    print(f"Starting sync ({direction}) for client '{client}' [{local_dir}]...")
    
    success_count = 0
    synced_names = set()
    for s in skills:
        src = s["repo_path"] if direction == "deploy" else s["local_path"]
        dst = s["local_path"] if direction == "deploy" else s["repo_path"]
        
        # Ensure parent directory of destination exists
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        if not os.path.exists(src):
            if direction == "save":
                continue
            print(f"Warning: Source path {src} does not exist. Skipping.")
            continue
            
        try:
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
                    
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns('skills', '__pycache__', '.git'))
            synced_names.add(s['name'])
            success_count += 1
        except Exception as e:
            print(f"  Error syncing {s['name']}: {e}")
            
    print(f"Sync complete. Successfully processed {success_count} location updates for {len(synced_names)} unique skills.")

def main():
    parser = argparse.ArgumentParser(description="Synchronize skills between repo and local AI client directories.")
    parser.add_argument("action", choices=["deploy", "save"], help="deploy: repo -> local; save: local -> repo")
    parser.add_argument("--client", choices=["opencode", "pi", "gemini", "claude"], default="pi", help="Target AI client (default: pi)")
    parser.add_argument("-g", "--group", help="Filter by skill category/group name")
    parser.add_argument("-l", "--list-groups", action="store_true", help="List all available group names")
    
    if "-l" in sys.argv or "--list-groups" in sys.argv:
        list_groups()
        sys.exit(0)
        
    args = parser.parse_args()
    sync_skills(args.action, args.client, args.group)

if __name__ == "__main__":
    main()
