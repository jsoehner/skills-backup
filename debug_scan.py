import os

root_dir = "."
tools_path = os.path.join(root_dir, "tools")
print(f"Tools path: {tools_path}")

if os.path.exists(tools_path):
    print(f"Tools path exists.")
    for root, dirs, files in os.walk(tools_path):
        if "SKILL.md" in files:
            print(f"Found SKILL.md in: {root}")
            print(f"Skill name: {os.path.basename(root)}")
else:
    print("Tools path does not exist.")

print("\nScanning root for composite skills...")
for root, dirs, files in os.walk(root_dir):
    if any(part.startswith('.') for part in root.split(os.sep)):
        continue
    if "tools" in root.split(os.sep):
        continue
    
    if "SKILL.md" in files:
        manifest_path = os.path.join(root, "manifest.json")
        if os.path.exists(manifest_path):
            print(f"Found manifest in: {root}")
            print(f"Skill name: {os.path.basename(root)}")
