import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SYMBOLIC_CHECK = REPO_ROOT / "scripts" / "verify" / "symbolic-check.py"
STATUS_CONTRACT = (
    REPO_ROOT / "openai" / "portable" / "contracts" / "verification-status.md"
)
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures"

VALID_STATUSES = {"PASS", "FAIL", "UNVERIFIED"}
VERDICT_STATUSES = {"VERIFIED", "PARTIALLY_VERIFIED", "FAILED", "UNVERIFIED"}


def run_check(*args):
    return subprocess.run(
        [sys.executable, str(SYMBOLIC_CHECK), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def parse_text_output(result):
    fields = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


class SymbolicCheckTests(unittest.TestCase):
    def test_reports_pass_for_a_zero_residual(self):
        result = run_check("log(exp(x)) - x", "--positive", "x")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(parse_text_output(result)["STATUS"], "PASS")

    def test_reports_fail_for_a_nonzero_residual(self):
        result = run_check("sqrt(x**2) - x")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(parse_text_output(result)["STATUS"], "FAIL")

    def test_reports_unverified_for_an_invalid_expression(self):
        result = run_check("log((")

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(parse_text_output(result)["STATUS"], "UNVERIFIED")

    def test_positive_fixture_verifies_through_the_committed_script(self):
        fixture = json.loads(
            (FIXTURE_DIR / "correct-proof-step.json").read_text(encoding="utf-8")
        )
        result = run_check(
            fixture["residual"],
            "--positive",
            ",".join(fixture.get("positive_symbols", [])),
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(parse_text_output(result)["STATUS"], "PASS")
        self.assertIn("DOMAIN: positive x", result.stdout)

    def test_negative_fixture_fails_through_the_committed_script(self):
        fixture = json.loads(
            (FIXTURE_DIR / "planted-proof-error.json").read_text(encoding="utf-8")
        )
        result = run_check(fixture["residual"])

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(parse_text_output(result)["STATUS"], "FAIL")

    def test_output_reports_backend_name_and_version(self):
        result = run_check("log(exp(x)) - x", "--positive", "x")

        fields = parse_text_output(result)
        self.assertIn("sympy", fields["BACKEND"])
        self.assertRegex(fields["BACKEND"], r"^sympy \d+\.\d+")

    def test_output_shape_matches_the_status_contract(self):
        contract = STATUS_CONTRACT.read_text(encoding="utf-8")
        for residual in ("log(exp(x)) - x", "sqrt(x**2) - x", "log(("):
            with self.subTest(residual=residual):
                result = run_check(residual)
                fields = parse_text_output(result)
                self.assertIn(fields["STATUS"], VALID_STATUSES)
                self.assertEqual(
                    fields["STATUS"] in {"PASS", "FAIL"},
                    "SIMPLIFIED" in fields,
                )
                self.assertIn(fields["STATUS"], contract)

    def test_json_mode_emits_a_structured_check(self):
        result = run_check("--json", "log(exp(x)) - x", "--positive", "x")

        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["backend"], "sympy")
        self.assertEqual(payload["simplified"], "0")
        self.assertEqual(payload["positive_symbols"], ["x"])
        self.assertIn("backend_version", payload)


class RuntimeFixtureTests(unittest.TestCase):
    def test_runtime_fixtures_have_valid_modes_and_verdicts(self):
        for path in sorted(FIXTURE_DIR.glob("*.json")):
            with self.subTest(fixture=path.name):
                fixture = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn(
                    fixture["mode"],
                    {"proof", "statistics", "simulation", "reproducibility"},
                )
                self.assertIn(fixture["expected_verdict"], VERDICT_STATUSES)

    def test_domain_assumption_fixture_omits_a_residual(self):
        fixture = json.loads(
            (FIXTURE_DIR / "cancellation-without-assumption.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertNotIn("residual", fixture)
        self.assertEqual(fixture["expected_verdict"], "FAILED")


if __name__ == "__main__":
    unittest.main()
