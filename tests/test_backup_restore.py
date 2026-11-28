#!/usr/bin/env python3
"""Unit tests for backup & restore scripts (restore_skills.py, sync.py, catalog.py)."""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import restore_skills
import sync as sync_mod
import catalog as catalog_mod


def _write_skill(base: Path, rel_dir: str, content: str = "---\nname: test\ndescription: test\n---\n# Skill\n"):
    skill_dir = base / rel_dir
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
    return skill_dir


class TestRestoreSkills(unittest.TestCase):
    def test_valid_skill_name_blocks_dot_and_traversal(self):
        self.assertTrue(restore_skills.is_valid_skill_name("my-skill_1.0"))
        self.assertFalse(restore_skills.is_valid_skill_name("."))
        self.assertFalse(restore_skills.is_valid_skill_name(".."))
        self.assertFalse(restore_skills.is_valid_skill_name("../escape"))
        self.assertFalse(restore_skills.is_valid_skill_name("bad name"))
        self.assertFalse(restore_skills.is_valid_skill_name(""))

    def test_is_safe_subpath_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "base"
            child = base / "skill-a"
            outside = Path(tmp) / "outside"
            base.mkdir()
            child.mkdir()
            outside.mkdir()
            self.assertTrue(restore_skills.is_safe_subpath(str(base), str(child), allow_equal=False))
            self.assertFalse(restore_skills.is_safe_subpath(str(base), str(base), allow_equal=False))
            self.assertFalse(restore_skills.is_safe_subpath(str(base), str(outside), allow_equal=True))

    def test_root_precedence_over_config_skills_and_clean_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            src_repo = Path(tmp) / "repo"
            target_root = Path(tmp) / "client_home"
            skills_dir = target_root / "skills"

            _write_skill(src_repo, "pdf", "---\nname: pdf\ndescription: root version\n---\nROOT")
            _write_skill(src_repo, "config-skills/pdf", "---\nname: pdf\ndescription: config version\n---\nCONFIG")
            _write_skill(src_repo, "config-skills/only-config", "---\nname: only-config\ndescription: cfg\n---\nCFG")

            # Add an ignored directory inside root skill
            ignored = src_repo / "pdf" / "__pycache__"
            ignored.mkdir(parents=True)
            (ignored / "junk.pyc").write_text("x", encoding="utf-8")

            # Seed stale file in destination to verify --clean removes it
            stale = skills_dir / "pdf" / "stale.txt"
            stale.parent.mkdir(parents=True, exist_ok=True)
            stale.write_text("stale", encoding="utf-8")

            with mock.patch.object(restore_skills, "get_client_paths", return_value=(str(target_root), str(skills_dir))), \
                 mock.patch.object(restore_skills, "sync_client_governance"):
                # Dry-run should not remove stale file or create only-config
                dry_count = restore_skills.restore_skills(str(src_repo), client="pi", dry_run=True, clean=True)
                self.assertEqual(dry_count, 2)
                self.assertTrue(stale.exists())
                self.assertFalse((skills_dir / "only-config").exists())

                # Real clean restore
                count = restore_skills.restore_skills(str(src_repo), client="pi", dry_run=False, clean=True)
                self.assertEqual(count, 2)
                self.assertIn("ROOT", (skills_dir / "pdf" / "SKILL.md").read_text(encoding="utf-8"))
                self.assertFalse(stale.exists())
                self.assertFalse((skills_dir / "pdf" / "__pycache__").exists())
                self.assertTrue((skills_dir / "only-config" / "SKILL.md").is_file())

    def test_hermes_path_is_portable(self):
        with mock.patch.dict(os.environ, {"LOCALAPPDATA": r"C:\Temp\LocalAppData"}):
            target_root, skills_dir = restore_skills.get_client_paths("hermes")
            self.assertTrue(target_root.lower().endswith(os.path.join("localappdata", "hermes")))
            self.assertTrue(skills_dir.lower().endswith(os.path.join("hermes", "skills")))


class TestSyncSkills(unittest.TestCase):
    def test_deploy_precedence_and_save_backs_up_new_local_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            local_dir = Path(tmp) / "client_skills"
            local_dir.mkdir(parents=True)

            _write_skill(repo, "pdf", "---\nname: pdf\ndescription: root\n---\nROOT")
            _write_skill(repo, "config-skills/pdf", "---\nname: pdf\ndescription: cfg\n---\nCFG")
            _write_skill(repo, "config-skills/cfg-only", "---\nname: cfg-only\ndescription: cfg\n---\nCFG_ONLY")

            # Deploy: root pdf must win over config-skills/pdf
            res_deploy = sync_mod.sync_skills(
                "deploy", client="pi", base_repo_dir=str(repo), local_dir_override=str(local_dir)
            )
            self.assertEqual(res_deploy["unique"], 2)
            self.assertIn("ROOT", (local_dir / "pdf" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertIn("CFG_ONLY", (local_dir / "cfg-only" / "SKILL.md").read_text(encoding="utf-8"))

            # Modify an existing skill locally and add a brand new client-only skill
            (local_dir / "pdf" / "SKILL.md").write_text("---\nname: pdf\ndescription: root\n---\nUPDATED", encoding="utf-8")
            _write_skill(local_dir, "brand-new-skill", "---\nname: brand-new-skill\ndescription: new\n---\nNEW")

            # Dry-run save should not modify repo
            res_dry = sync_mod.sync_skills(
                "save", client="pi", dry_run=True, base_repo_dir=str(repo), local_dir_override=str(local_dir)
            )
            self.assertEqual(res_dry["new_backed_up"], 1)
            self.assertFalse((repo / "brand-new-skill").exists())
            self.assertIn("ROOT", (repo / "pdf" / "SKILL.md").read_text(encoding="utf-8"))

            # Real save should update root pdf (NOT config-skills/pdf) and back up brand-new-skill to root
            res_save = sync_mod.sync_skills(
                "save", client="pi", dry_run=False, base_repo_dir=str(repo), local_dir_override=str(local_dir)
            )
            self.assertEqual(res_save["new_backed_up"], 1)
            self.assertIn("UPDATED", (repo / "pdf" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertIn("CFG", (repo / "config-skills" / "pdf" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertIn("NEW", (repo / "brand-new-skill" / "SKILL.md").read_text(encoding="utf-8"))

    def test_client_dir_supports_opencode_and_hermes(self):
        self.assertIn(".opencode", sync_mod.get_client_skills_dir("opencode"))
        self.assertIn("hermes", sync_mod.get_client_skills_dir("hermes").lower())
        self.assertIn("hermes", catalog_mod.get_client_skills_dir("hermes").lower())


if __name__ == "__main__":
    unittest.main()
