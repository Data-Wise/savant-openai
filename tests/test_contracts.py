import importlib.util
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "learning" / "validate-candidate.py"
EVIDENCE_SCHEMA = REPO_ROOT / "openai" / "portable" / "contracts" / "evidence-report.schema.json"
RUNTIME_SCHEMA = REPO_ROOT / "openai" / "portable" / "contracts" / "runtime-measurement.schema.json"
RUNTIME_MEASUREMENT = REPO_ROOT / "docs" / "measurements" / "MEASUREMENT-runtime-codex-2026-08-06.json"


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

    def _runtime_measurement(self, **overrides):
        measurement = json.loads(RUNTIME_MEASUREMENT.read_text(encoding="utf-8"))
        measurement.update(overrides)
        return measurement

    def test_runtime_measurement_schema_accepts_the_committed_measurement(self):
        validator = load_validator()
        errors = validator.validate_schema(
            self._runtime_measurement(),
            json.loads(RUNTIME_SCHEMA.read_text(encoding="utf-8")),
        )
        self.assertEqual(errors, [])

    def test_runtime_measurement_schema_rejects_an_unknown_evidence_path(self):
        measurement = self._runtime_measurement()
        measurement["runs"][0]["evidence_path"] = "guessing"
        validator = load_validator()
        errors = validator.validate_schema(
            measurement, json.loads(RUNTIME_SCHEMA.read_text(encoding="utf-8"))
        )
        self.assertTrue(any("evidence_path" in error for error in errors))

    def test_runtime_measurement_schema_rejects_an_unknown_verdict(self):
        measurement = self._runtime_measurement()
        measurement["runs"][0]["verdict"] = "MAYBE"
        validator = load_validator()
        errors = validator.validate_schema(
            measurement, json.loads(RUNTIME_SCHEMA.read_text(encoding="utf-8"))
        )
        self.assertTrue(any("verdict" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
