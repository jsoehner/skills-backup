#!/usr/bin/env python3
"""
validate_skill.py - Self-contained Skill Validator
Checks SKILL.md frontmatter, naming conventions, and structure.
"""

import sys
import re
from pathlib import Path


def validate_skill(skill_path):
    skill_path = Path(skill_path).resolve()
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return False, f"SKILL.md not found in {skill_path}"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found (must start with ---)"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format (missing closing ---)"

    frontmatter = match.group(1)

    if "name:" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description:" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name_match = re.search(r"name:\s*(.+)", frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        if not re.match(r"^[a-z0-9-]+$", name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"

    desc_match = re.search(r"description:\s*(.+)", frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"

    return True, "Skill structure and frontmatter are valid!"


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    valid, message = validate_skill(target)
    print(message)
    sys.exit(0 if valid else 1)
