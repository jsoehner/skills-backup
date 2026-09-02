import os

root_dir = "."
skills_path = os.path.join(root_dir, "skills")
print(f"Skills path: {skills_path}")

if os.path.exists(skills_path):
    print(f"Skills path exists.")
    for root, dirs, files in os.walk(skills_path):
        if "SKILL.md" in files:
            print(f"Found SKILL.md in: {root}")
            print(f"Skill name: {os.path.basename(root)}")
else:
    print("Skills path does not exist.")

print("\nScanning root for composite skills...")
for root, dirs, files in os.walk(root_dir):
    if any(part.startswith('.') for part in root.split(os.sep)):
        continue
    if "skills" in root.split(os.sep):
        continue
    
    if "SKILL.md" in files:
        manifest_path = os.path.join(root, "manifest.json")
        if os.path.exists(manifest_path):
            print(f"Found manifest in: {root}")
            print(f"Skill name: {os.path.basename(root)}")
