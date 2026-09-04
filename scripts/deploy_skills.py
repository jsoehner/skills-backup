#!/usr/bin/env python3
import os
import json
import argparse
import sys
from typing import Set, List, Dict

# Configuration
# The script is located in yuv-skills-backup/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = SCRIPT_DIR
MANIFEST_FILENAME = "manifest.json"

class SkillDeployer:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.skills_map: Dict[str, dict] = {}
        self.atomic_skills: Set[str] = set()

    def scan_skills(self):
        """Scan the backup directory to map all skills and identify atomic ones."""
        print(f"Scanning directory: {self.root_dir}")
        
        # 1. Scan the tools directory for atomic skills
        tools_path = os.path.join(self.root_dir, "tools")
        if os.path.exists(tools_path):
            print(f"Scanning tools path: {tools_path}")
            for root, dirs, files in os.walk(tools_path):
                if "SKILL.md" in files:
                    # The skill name is the folder name containing SKILL.md
                    skill_name = os.path.basename(root)
                    self.atomic_skills.add(skill_name)

        # 2. Scan the root directory for composite skills (those with manifest.json)
        for root, dirs, files in os.walk(self.root_dir):
            # Skip hidden directories
            if any(part.startswith('.') for part in root.split(os.sep)):
                continue
            
            # Skip the tools directory here as we handled it above
            if "tools" in root.split(os.sep):
                continue

            # Check if this directory is a skill (has a SKILL.md)
            if "SKILL.md" in files:
                skill_name = os.path.basename(root)
                
                # Skip the root directory itself if it has a SKILL.md
                if root == self.root_dir:
                    continue

                manifest_path = os.path.join(root, MANIFEST_FILENAME)
                
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            manifest = json.load(f)
                            if isinstance(manifest, dict):
                                self.skills_map[skill_name] = {
                                    "path": root,
                                    "manifest": manifest
                                }
                            else:
                                self.atomic_skills.add(skill_name)
                    except Exception as e:
                        print(f"Warning: Failed to parse manifest at {manifest_path}: {e}", file=sys.stderr)
                        self.atomic_skills.add(skill_name)
                else:
                    # If it has SKILL.md but no manifest, it's an atomic skill
                    self.atomic_skills.add(skill_name)

    def get_all_dependencies(self, skill_name: str, visited: Set[str] = None) -> Set[str]:
        """Recursively collect all dependencies for a skill."""
        if visited is None:
            visited = set()
        
        if skill_name in visited:
            return set()
        
        visited.add(skill_name)
        
        if skill_name not in self.skills_map:
            # If it's not in our manifest map, it's a leaf/atomic skill
            return {skill_name}
        
        manifest = self.skills_map[skill_name]["manifest"]
        # Use a temporary set to avoid "Set changed size during iteration"
        direct_deps = set(manifest.get("dependencies", []))
        
        all_deps = set()
        for dep in list(direct_deps):
            all_deps.update(self.get_all_dependencies(dep, visited))
            
        return all_deps

    def plan_deployment(self, harness: str):
        """Plan the skills to include for a specific harness."""
        print(f"--- Planning Deployment for Harness: {harness} ---")
        
        to_include = set()
        
        # Identify all composite skills
        composites = [name for name, info in self.skills_map.items() 
                      if info["manifest"].get("type") == "composite"]
        
        # Collect dependencies for all composites
        for comp in composites:
            print(f"Resolving dependencies for Composite: {comp}...")
            deps = self.get_all_dependencies(comp)
            to_include.update(deps)
        
        # Also include all atomic skills from the tools folder
        for atomic in self.atomic_skills:
            to_include.add(atomic)
            
        print(f"\nTotal skills to include ({len(to_include)}):")
        for skill in sorted(list(to_include)):
            print(f" - {skill}")
            
        return to_include

def main():
    parser = argparse.ArgumentParser(description="Deploy skills to specific AI harnesses.")
    parser.add_argument("--harness", choices=["pi", "gemini", "claude"], required=True, 
                        help="The target AI harness for deployment.")
    parser.add_argument("--dry-run", action="store_true", help="Only plan the deployment without creating files.")
    args = parser.parse_args()

    deployer = SkillDeployer(SCRIPT_DIR)
    deployer.scan_skills()
    
    plan = deployer.plan_deployment(args.harness)
    
    if not args.dry_run:
        print(f"\nCreating deployment package for {args.harness}...")
        # Here we would create the actual directory structure or zip file
        # For now, we'll just print the success message
        print(f"SUCCESS: Deployment plan for {args.harness} finalized.")

if __name__ == "__main__":
    main()
