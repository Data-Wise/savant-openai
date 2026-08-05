import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MEASURER = REPO_ROOT / "scripts" / "learning" / "measure-lesson.py"


def lesson(lesson_id="lesson-proof-001", **overrides):
    value = {
        "schema_version": "1.0",
        "id": lesson_id,
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
        "lifecycle_status": "approved",
        "created_at": "2026-08-04T12:00:00Z",
        "reviewed_at": "2026-08-04T13:00:00Z",
    }
    value.update(overrides)
    return value


def run_measurement(fixture, lesson_path, assisted_verdict, output=None):
    command = [
        sys.executable,
        str(MEASURER),
        str(fixture),
        str(lesson_path),
        "--with-lesson-verdict",
        assisted_verdict,
    ]
    if output:
        command.extend(["--output", str(output)])
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )


class LessonMeasurementTests(unittest.TestCase):
    def test_reports_review_only_overhead_and_preserves_verdict(self):
        fixture = REPO_ROOT / "tests" / "fixtures" / "planted-proof-error.json"
        with tempfile.TemporaryDirectory() as directory:
            lesson_path = Path(directory) / "lesson.json"
            lesson_path.write_text(json.dumps(lesson()), encoding="utf-8")

            result = run_measurement(fixture, lesson_path, "FAILED")

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["baseline"]["verdict"], "FAILED")
            self.assertEqual(report["with_lesson"]["verdict"], "FAILED")
            self.assertTrue(report["verdict_preserved"])
            self.assertFalse(report["normal_verification"]["learning_context_loaded"])
            self.assertEqual(
                report["normal_verification"]["estimated_tokens"],
                report["baseline"]["estimated_tokens"],
            )
            self.assertGreater(report["review_only"]["added_tokens"], 0)

    def test_writes_the_measurement_report_when_requested(self):
        fixture = REPO_ROOT / "tests" / "fixtures" / "planted-proof-error.json"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lesson_path = root / "lesson.json"
            report_path = root / "reports" / "measurement.json"
            lesson_path.write_text(json.dumps(lesson()), encoding="utf-8")

            result = run_measurement(fixture, lesson_path, "FAILED", report_path)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(report_path.exists())
            self.assertTrue(json.loads(report_path.read_text())["verdict_preserved"])

    def test_rejects_an_unsupported_upgrade_to_verified(self):
        fixture = REPO_ROOT / "tests" / "fixtures" / "planted-proof-error.json"
        with tempfile.TemporaryDirectory() as directory:
            lesson_path = Path(directory) / "lesson.json"
            lesson_path.write_text(json.dumps(lesson()), encoding="utf-8")

            result = run_measurement(fixture, lesson_path, "VERIFIED")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsupported", result.stderr.lower())

    def test_rejects_a_lesson_outside_the_fixture_scope(self):
        fixture = REPO_ROOT / "tests" / "fixtures" / "planted-proof-error.json"
        with tempfile.TemporaryDirectory() as directory:
            lesson_path = Path(directory) / "lesson.json"
            lesson_path.write_text(
                json.dumps(lesson(task_class="statistics")), encoding="utf-8"
            )

            result = run_measurement(fixture, lesson_path, "FAILED")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("scope", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
