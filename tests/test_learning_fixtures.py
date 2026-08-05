import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "learning" / "fixtures"
VALIDATOR = REPO_ROOT / "scripts" / "learning" / "validate-candidate.py"


EXPECTED_FIXTURES = {
    "positive-lesson.json": (True, None),
    "negative-overgeneralization.json": (True, None),
    "unavailable-backend.json": (True, None),
    "prompt-injection.json": (False, "prompt-injection"),
    "secret-redaction.json": (False, "secret"),
    "rollback-supersession.json": (True, None),
}


def run_fixture(path):
    fixture = json.loads(path.read_text(encoding="utf-8"))
    candidate_path = path.with_suffix(".candidate.json")
    candidate_path.write_text(
        json.dumps(fixture["candidate"]), encoding="utf-8"
    )
    try:
        return fixture, subprocess.run(
            [sys.executable, str(VALIDATOR), str(candidate_path)],
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        candidate_path.unlink(missing_ok=True)


class LearningFixtureTests(unittest.TestCase):
    def test_phase_two_fixture_matrix_has_expected_validation_results(self):
        for filename, (should_pass, error_fragment) in EXPECTED_FIXTURES.items():
            with self.subTest(fixture=filename):
                path = FIXTURE_DIR / filename
                fixture, result = run_fixture(path)
                if should_pass:
                    self.assertEqual(result.returncode, 0, result.stderr)
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(error_fragment, result.stderr.lower())
                self.assertIn("expected_verdict", fixture)

    def test_negative_and_unavailable_lessons_cannot_claim_verified(self):
        for filename in (
            "negative-overgeneralization.json",
            "unavailable-backend.json",
        ):
            with self.subTest(fixture=filename):
                fixture = json.loads(
                    (FIXTURE_DIR / filename).read_text(encoding="utf-8")
                )
                self.assertNotEqual(fixture["expected_verdict"], "VERIFIED")


if __name__ == "__main__":
    unittest.main()
