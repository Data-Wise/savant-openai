import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "learning" / "validate-candidate.py"


def candidate(**overrides):
    value = {
        "schema_version": "1.0",
        "id": "lesson-proof-001",
        "task_class": "proof",
        "observed_failure": "A cancellation step omitted a nonzero denominator assumption.",
        "desired_behavior": "State the denominator assumption before cancelling.",
        "scope": "savant-research-verify/proof",
        "evidence": {
            "type": "fixture",
            "ref": "tests/fixtures/planted-proof-error.json",
        },
        "confidence": "high",
        "provenance": {
            "source_type": "verification",
            "content_hash": "sha256:abc123",
        },
        "redaction_status": "passed",
        "lifecycle_status": "candidate",
        "created_at": "2026-08-04T12:00:00Z",
    }
    value.update(overrides)
    return value


def run_validator(value):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "candidate.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            capture_output=True,
            text=True,
            check=False,
        )


class CandidateValidationTests(unittest.TestCase):
    def test_accepts_a_well_formed_candidate(self):
        result = run_validator(candidate())

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID", result.stdout)

    def test_rejects_a_missing_required_field(self):
        value = candidate()
        del value["desired_behavior"]

        result = run_validator(value)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("desired_behavior", result.stderr)

    def test_rejects_an_unknown_task_class(self):
        result = run_validator(candidate(task_class="manuscript"))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("task_class", result.stderr)

    def test_requires_review_timestamp_before_approval(self):
        result = run_validator(candidate(lifecycle_status="approved"))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("reviewed_at", result.stderr)

    def test_rejects_a_date_only_created_timestamp(self):
        result = run_validator(candidate(created_at="2026-08-04"))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("date-time", result.stderr)

    def test_rejects_a_timezone_less_created_timestamp(self):
        result = run_validator(candidate(created_at="2026-08-04T12:00:00"))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("timezone", result.stderr)

    def test_rejects_a_missing_file_evidence_reference(self):
        result = run_validator(
            candidate(
                evidence={
                    "type": "fixture",
                    "ref": "tests/fixtures/does-not-exist.json",
                }
            )
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence.ref", result.stderr)

    def test_rejects_an_evidence_reference_outside_the_repository(self):
        result = run_validator(
            candidate(
                evidence={
                    "type": "fixture",
                    "ref": "../outside-repository.json",
                }
            )
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence.ref", result.stderr)

    def test_rejects_an_evidence_reference_to_a_directory(self):
        result = run_validator(
            candidate(
                evidence={
                    "type": "fixture",
                    "ref": "tests",
                }
            )
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence.ref", result.stderr)

    def test_rejects_secret_like_content(self):
        value = candidate(
            observed_failure="The API key was sk-1234567890abcdefghijklmnop.",
        )

        result = run_validator(value)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("secret", result.stderr.lower())

    def test_rejects_an_oversized_candidate(self):
        value = candidate(observed_failure="x" * 9000)

        result = run_validator(value)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("size", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
