import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SANITIZER = REPO_ROOT / "scripts" / "verify" / "sanitize-transcript.py"
ARCHIVE_DIR = (
    REPO_ROOT / "docs" / "measurements" / "logs" / "runtime-codex-2026-08-06"
)
VALIDATOR = REPO_ROOT / "scripts" / "learning" / "validate-candidate.py"


def make_transcript(final_message):
    events = [
        {
            "type": "item.completed",
            "item": {"type": "agent_message", "text": "an earlier message"},
        },
        {
            "type": "item.completed",
            "item": {"type": "agent_message", "text": final_message},
        },
        {"type": "turn.completed", "usage": {"input_tokens": 1}},
    ]
    return "".join(json.dumps(event) + "\n" for event in events)


def run_sanitizer(transcript_path, output_dir):
    return subprocess.run(
        [
            sys.executable,
            str(SANITIZER),
            str(transcript_path),
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


class SanitizeTranscriptTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write_transcript(self, final_message):
        path = self.root / "run.jsonl"
        path.write_text(make_transcript(final_message), encoding="utf-8")
        return path

    def test_extracts_the_final_agent_message(self):
        path = self.write_transcript("VERDICT: VERIFIED\nNEXT ACTION: none\n")
        output = self.root / "out"
        result = run_sanitizer(path, output)

        self.assertEqual(result.returncode, 0, result.stderr)
        written = (output / "run.txt").read_text(encoding="utf-8")
        self.assertIn("VERDICT: VERIFIED", written)
        self.assertNotIn("an earlier message", written)

    def test_redacts_repo_and_codex_home_paths(self):
        message = (
            "EVIDENCE: [fixture](\n"
            f"{REPO_ROOT}/tests/fixtures/correct-proof-step.json:1),\n"
            "[memory](</Users/example/.codex/memories/MEMORY.md:5>),\n"
            "[home](/Users/example/.ssh/known_hosts).\n"
        )
        path = self.write_transcript(message)
        output = self.root / "out"
        result = run_sanitizer(path, output)

        self.assertEqual(result.returncode, 0, result.stderr)
        written = (output / "run.txt").read_text(encoding="utf-8")
        self.assertIn("<repo>/tests/fixtures/correct-proof-step.json", written)
        self.assertIn("<codex-home>/memories/MEMORY.md", written)
        self.assertIn("<home>/.ssh/known_hosts", written)
        self.assertNotIn("/Users/", written)

    def test_refuses_secret_like_content(self):
        path = self.write_transcript("VERDICT: VERIFIED\nKEY: sk-0123456789abcdef\n")
        output = self.root / "out"
        result = run_sanitizer(path, output)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("secret-like", result.stderr)

    def test_refuses_a_remaining_absolute_home_path(self):
        path = self.write_transcript("VERDICT: VERIFIED\nPATH: /Users/edge\n")
        output = self.root / "out"
        result = run_sanitizer(path, output)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("absolute home path", result.stderr)


class ArchivedLogGateTests(unittest.TestCase):
    def test_archived_excerpts_are_clean_and_verdict_shaped(self):
        import importlib.util
        import re

        spec = importlib.util.spec_from_file_location("candidate_validator", VALIDATOR)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        verdict_line = re.compile(
            r"^(?:VERDICT: )?(?:VERIFIED|PARTIALLY_VERIFIED|FAILED|UNVERIFIED)$"
        )

        files = sorted(ARCHIVE_DIR.glob("*.txt"))
        self.assertEqual(len(files), 6)
        for path in files:
            with self.subTest(log=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertRegex(text.lstrip().splitlines()[0], verdict_line)
                self.assertNotIn("/Users/", text)
                for pattern in module.SECRET_PATTERNS:
                    self.assertIsNone(pattern.search(text), path.name)


if __name__ == "__main__":
    unittest.main()
