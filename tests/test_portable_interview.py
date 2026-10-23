"""Interview checkpoint boundaries; installed-host behavior is evaluated separately."""

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "plugins/careerground-portable/references"
sys.path.insert(0, str(REFERENCES))
SPEC = importlib.util.spec_from_file_location("portable_interview", REFERENCES / "interview.py")
interview = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(interview)
sys.path.pop(0)


def fixture():
    return json.loads((ROOT / "fixtures/portable/interview-session-v1.json").read_text())


class PortableInterviewTests(unittest.TestCase):
    def test_roundtrip_preserves_original_and_renders_pending_without_promotion(self):
        data = fixture()
        before = copy.deepcopy(data)
        self.assertEqual(interview.validate_session(data), [])
        text = interview.render_session(data)
        self.assertIn("Pending candidate", text)
        self.assertIn("Unanswered", text)
        self.assertEqual(data, before)
        self.assertNotIn("profile", data)

    def test_materials_and_constraints_cannot_silently_change(self):
        for change in ("materials", "constraints"):
            data = fixture()
            if change == "materials":
                data[change][0]["text"] += " changed"
            else:
                data[change].append("new restriction")
            self.assertIn("MATERIAL_CONFLICT", interview.validate_session(data))

    def test_unconfirmed_voice_answer_cannot_be_assessed_or_promoted(self):
        for field in ("feedback", "candidates"):
            data = fixture()
            turn = data["turns"][0]
            turn["answers"][0].update(input_mode="voice", confirmed=False)
            other = "candidates" if field == "feedback" else "feedback"
            turn[other] = []
            self.assertIn("ANSWER_UNCONFIRMED", interview.validate_session(data))

    def test_correction_keeps_history_but_excludes_old_feedback_and_candidates(self):
        data = fixture()
        turn = data["turns"][0]
        turn["answers"].append(
            {
                "revision": 2,
                "text": "배포는 동료가 했습니다.",
                "input_mode": "text",
                "confirmed": True,
            }
        )
        self.assertEqual(interview.validate_session(data), [])
        self.assertEqual(interview.current_records(turn), {"feedback": [], "candidates": []})
        self.assertIn("stale / excluded", interview.render_session(data))
        turn["feedback"].append({"answer_revision": 2, "text": "기여 경계를 분명히 했습니다."})
        self.assertEqual(len(interview.current_records(turn)["feedback"]), 1)

    def test_pending_voice_correction_excludes_all_current_records(self):
        data = fixture()
        turn = data["turns"][0]
        turn["answers"].append(
            {"revision": 2, "text": "검토 중 전사", "input_mode": "voice", "confirmed": False}
        )
        self.assertEqual(interview.validate_session(data), [])
        self.assertEqual(interview.current_records(turn), {"feedback": [], "candidates": []})

    def test_missing_answer_or_material_references_are_rejected(self):
        for field in ("material_ids", "feedback", "candidates"):
            data = fixture()
            turn = data["turns"][0]
            if field == "material_ids":
                turn[field] = ["missing"]
            else:
                turn[field][0]["answer_revision"] = 99
            self.assertIn("MISSING_REFERENCE", interview.validate_session(data))

    def test_duplicate_ids_and_noncontiguous_answer_revisions_are_rejected(self):
        for field in ("materials", "turns"):
            data = fixture()
            data[field].append(copy.deepcopy(data[field][0]))
            self.assertIn("DUPLICATE_ID", interview.validate_session(data))
        data = fixture()
        turn = data["turns"][0]
        turn["answers"].append(copy.deepcopy(turn["answers"][0]))
        self.assertIn("ANSWER_REVISION_CONFLICT", interview.validate_session(data))

    def test_general_practice_requires_no_materials_or_handoff(self):
        data = fixture()
        data["materials"] = []
        data["constraints"] = []
        data["material_digest"] = interview.material_digest([], [])
        for turn in data["turns"]:
            turn["material_ids"] = []
        self.assertEqual(interview.validate_session(data), [])

    def test_gap_question_cannot_claim_selected_evidence(self):
        data = fixture()
        data["turns"][0]["gap"] = True
        self.assertIn("GAP_EVIDENCE_CONFLICT", interview.validate_session(data))

    def test_candidate_cannot_be_approved_in_session(self):
        data = fixture()
        data["turns"][0]["candidates"][0]["status"] = "approved"
        self.assertIn("SCHEMA", interview.validate_session(data))

    def test_invalid_or_oversized_payloads_are_rejected(self):
        self.assertEqual(interview.validate_session([]), ["UNSUPPORTED_VERSION"])
        data = fixture()
        data["turns"][0]["answers"][0]["text"] = "x" * (3 * 1024 * 1024)
        self.assertEqual(interview.validate_session(data), ["SIZE_LIMIT"])

    def test_cli_saves_readable_checkpoint_once_and_leaves_input_untouched(self):
        with tempfile.TemporaryDirectory() as folder:
            source, review = Path(folder) / "session.json", Path(folder) / "review.md"
            source.write_text(json.dumps(fixture(), ensure_ascii=False))
            before = source.read_bytes()
            cmd = [
                sys.executable,
                str(REFERENCES / "interview.py"),
                str(source),
                "--review",
                str(review),
            ]
            run = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertFalse(json.loads(run.stdout)["profile_modified"])
            self.assertEqual(source.read_bytes(), before)
            saved = review.read_bytes()
            self.assertNotEqual(subprocess.run(cmd, capture_output=True, check=False).returncode, 0)
            self.assertEqual(review.read_bytes(), saved)
