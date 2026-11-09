#!/usr/bin/env python3
"""
enrich_sbom_gradle.py - Enrich CycloneDX SBOM with Gradle Runtime Dependencies

Resolves the project's runtimeClasspath dependencies and merges them into
the CycloneDX SBOM (oss/sbom.cyclonedx.json) to ensure third-party libraries
and binaries are captured for supply chain CBOM assimilation and confidence scoring.
"""

import sys
import os
import json
import re
import subprocess
from pathlib import Path


def get_gradle_dependencies() -> list:
    """Run Gradle to get resolved runtimeClasspath dependencies."""
    cmd = ["./gradlew", "-q", "dependencies", "--configuration", "runtimeClasspath"]
    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Warning: Could not query Gradle runtimeClasspath: {e}", file=sys.stderr)
        return []

    components = []
    seen = set()

    for line in output.splitlines():
        # Match pattern: group:artifact:version (with optional -> resolved_version)
        m = re.search(r"([a-zA-Z0-9.\-_]+):([a-zA-Z0-9.\-_]+):([a-zA-Z0-9.\-_]+)", line)
        if not m:
            continue
        group, artifact, version = m.group(1), m.group(2), m.group(3)
        if "->" in line:
            parts = line.split("->")
            version = parts[1].strip().split()[0]

        # Ignore local project coordinates if any
        if group == "com.example":
            continue

        key = (group, artifact)
        if key in seen:
            continue
        seen.add(key)

        purl = f"pkg:maven/{group}/{artifact}@{version}"
        components.append({
            "name": artifact,
            "group": group,
            "version": version,
            "purl": purl,
            "type": "library",
            "bom-ref": purl
        })

    return components


def enrich_sbom(sbom_path: Path):
    gradle_deps = get_gradle_dependencies()
    if not gradle_deps:
        print("No Gradle dependencies resolved or Gradle not present.")
        return

    sbom_path.parent.mkdir(parents=True, exist_ok=True)

    if sbom_path.exists():
        try:
            with open(sbom_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"bomFormat": "CycloneDX", "specVersion": "1.6", "components": []}
    else:
        data = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.6",
            "serialNumber": "urn:uuid:gradle-runtime-dependencies",
            "version": 1,
            "metadata": {
                "component": {
                    "name": "spring-ai-blog-agent",
                    "type": "application"
                }
            },
            "components": []
        }

    existing_components = data.setdefault("components", [])
    existing_purls = {c.get("purl") for c in existing_components if c.get("purl")}
    existing_names = {c.get("name") for c in existing_components if c.get("name")}

    added = 0
    for dep in gradle_deps:
        if dep["purl"] not in existing_purls and dep["name"] not in existing_names:
            existing_components.append(dep)
            existing_purls.add(dep["purl"])
            existing_names.add(dep["name"])
            added += 1

    with open(sbom_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Enriched SBOM ({sbom_path}) with {added} Gradle runtime dependencies (Total: {len(existing_components)})")


def main():
    target_path = Path("oss/sbom.cyclonedx.json")
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
    enrich_sbom(target_path)


if __name__ == "__main__":
    main()
