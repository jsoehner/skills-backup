#!/usr/bin/env python3
"""
Unit tests for analyze_cbom.py
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from analyze_cbom import analyze_cbom, QUANTUM_VULNERABLE_PATTERNS, POST_QUANTUM_PATTERNS


class TestCBOMAnalysis(unittest.TestCase):
    def setUp(self):
        self.fixture_path = SKILL_DIR / "tests" / "fixtures" / "sample_cbom.json"
        self.assertTrue(self.fixture_path.exists(), "Sample CBOM fixture missing")

    def test_cbom_parsing(self):
        result = analyze_cbom(self.fixture_path)
        self.assertEqual(result["bomFormat"], "CycloneDX")
        self.assertEqual(result["specVersion"], "1.6")
        self.assertEqual(result["total_components"], 7)
        self.assertEqual(result["total_crypto_assets"], 7)

    def test_pqc_classification(self):
        result = analyze_cbom(self.fixture_path)
        # RSA and ECDSA are quantum-vulnerable
        self.assertEqual(result["quantum_vulnerable_count"], 2)
        # ML-KEM and ML-DSA are post-quantum ready
        self.assertEqual(result["pqc_ready_count"], 2)

        vulnerable_names = [a["name"] for a in result["vulnerable_assets"]]
        self.assertIn("RSA-2048", vulnerable_names)
        self.assertIn("ECDSA-P256", vulnerable_names)

        pqc_names = [a["name"] for a in result["pqc_assets"]]
        self.assertIn("ML-KEM-768", pqc_names)
        self.assertIn("ML-DSA-65", pqc_names)

    def test_asset_types_and_certificates(self):
        result = analyze_cbom(self.fixture_path)
        asset_types = result["asset_types"]
        self.assertEqual(asset_types.get("algorithm"), 5)
        self.assertEqual(asset_types.get("certificate"), 1)
        self.assertEqual(asset_types.get("protocol"), 1)


if __name__ == "__main__":
    unittest.main()
