import importlib.util
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "learning" / "validate-candidate.py"
EVIDENCE_SCHEMA = REPO_ROOT / "openai" / "portable" / "contracts" / "evidence-report.schema.json"


def load_validator():
    spec = importlib.util.spec_from_file_location("candidate_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("candidate validator unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ContractTests(unittest.TestCase):
    def test_accepts_a_valid_evidence_report(self):
        report = {
            "verdict": "PARTIALLY_VERIFIED",
            "claim": "The proof is valid under the stated assumptions.",
            "scope": "the displayed derivation",
            "checks": [
                {
                    "name": "denominator assumption",
                    "status": "PASS",
                    "evidence": "The assumption is stated before cancellation.",
                }
            ],
            "limitations": ["No formal checker was available."],
        }
        validator = load_validator()

        errors = validator.validate_schema(
            report, json.loads(EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
        )

        self.assertEqual(errors, [])

    def test_rejects_an_evidence_report_with_an_invalid_nested_check(self):
        report = {
            "verdict": "PARTIALLY_VERIFIED",
            "claim": "The proof is valid under the stated assumptions.",
            "scope": "the displayed derivation",
            "checks": [
                {
                    "name": "denominator assumption",
                    "status": "MAYBE",
                    "evidence": "The assumption is stated before cancellation.",
                }
            ],
            "limitations": [],
        }
        validator = load_validator()

        errors = validator.validate_schema(
            report, json.loads(EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
        )

        self.assertTrue(any("status" in error for error in errors))

    def test_plugin_manifest_points_to_existing_skills(self):
        manifest = json.loads(
            (REPO_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(manifest["name"], "savant-openai")
        self.assertTrue((REPO_ROOT / manifest["skills"]).is_dir())

    def test_skill_files_have_matching_frontmatter(self):
        for skill_file in sorted((REPO_ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=str(skill_file)):
                lines = skill_file.read_text(encoding="utf-8").splitlines()
                self.assertGreaterEqual(len(lines), 4)
                self.assertEqual(lines[0], "---")
                self.assertIn("---", lines[1:])
                closing = lines[1:].index("---") + 1
                frontmatter = lines[1:closing]
                fields = {
                    line.split(":", 1)[0]: line
                    for line in frontmatter
                    if ":" in line
                }
                self.assertEqual(fields["name"].split(":", 1)[1].strip(), skill_file.parent.name)
                self.assertIn("description", fields)


if __name__ == "__main__":
    unittest.main()
