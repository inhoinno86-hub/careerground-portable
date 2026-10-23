"""Offline interview checkpoints. No model calls, network, or career-profile writes."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

from portable import InvalidFile, load_json, schema_errors


def material_digest(materials, constraints):
    payload = json.dumps(
        {"materials": materials, "constraints": constraints},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def validate_session(data):
    errors = set(schema_errors(data, "interview-session-1.0.schema.json"))
    if errors:
        return sorted(errors)
    if data["material_digest"] != material_digest(data["materials"], data["constraints"]):
        errors.add("MATERIAL_CONFLICT")
    materials = {m["id"] for m in data["materials"]}
    turns = {t["id"] for t in data["turns"]}
    if len(materials) != len(data["materials"]) or len(turns) != len(data["turns"]):
        errors.add("DUPLICATE_ID")
    candidates = set()
    for turn in data["turns"]:
        if not set(turn["material_ids"]) <= materials:
            errors.add("MISSING_REFERENCE")
        if turn["gap"] and turn["material_ids"]:
            errors.add("GAP_EVIDENCE_CONFLICT")
        answers = {a["revision"]: a for a in turn["answers"]}
        if list(answers) != list(range(1, len(turn["answers"]) + 1)):
            errors.add("ANSWER_REVISION_CONFLICT")
        for item in turn["feedback"] + turn["candidates"]:
            answer = answers.get(item["answer_revision"])
            if answer is None:
                errors.add("MISSING_REFERENCE")
            elif not answer["confirmed"]:
                errors.add("ANSWER_UNCONFIRMED")
        for item in turn["candidates"]:
            if item["id"] in candidates:
                errors.add("DUPLICATE_ID")
            candidates.add(item["id"])
    return sorted(errors)


def current_records(turn):
    """Only the latest confirmed revision can feed reflection or career review."""
    if not turn["answers"] or not turn["answers"][-1]["confirmed"]:
        return {"feedback": [], "candidates": []}
    revision = turn["answers"][-1]["revision"]
    return {
        field: copy.deepcopy([i for i in turn[field] if i["answer_revision"] == revision])
        for field in ("feedback", "candidates")
    }


def render_session(data):
    errors = validate_session(data)
    if errors:
        raise InvalidFile(errors[0])
    lines = [
        f"# Interview {data['session_id']} / v{data['revision']}",
        "",
        f"Mode: {data['mode']} | Status: {data['status']}",
        "",
        "User-editable checkpoint; no career certification or automatic profile updates.",
        "",
        "## Selected materials",
    ]
    for material in data["materials"]:
        lines.extend(
            [f"- {material['id']} ({material['kind']}): {material['label']}", material["text"]]
        )
    lines.extend(["", "## Constraints", *[f"- {c}" for c in data["constraints"]]])
    for turn in data["turns"]:
        lines.extend(
            [
                "",
                f"## {turn['id']}: {turn['question']}",
                f"Materials: {', '.join(turn['material_ids']) or 'none / general or gap'}",
            ]
        )
        latest = turn["answers"][-1]["revision"] if turn["answers"] else None
        if latest is None:
            lines.append("Unanswered")
        for answer in turn["answers"]:
            state = "confirmed" if answer["confirmed"] else "unconfirmed / not evaluated"
            lines.extend(
                [f"Answer r{answer['revision']} ({answer['input_mode']}, {state}):", answer["text"]]
            )
        for field, label in (("feedback", "Model feedback"), ("candidates", "Pending candidate")):
            for item in turn[field]:
                state = "current" if item["answer_revision"] == latest else "stale / excluded"
                lines.extend([f"{label} r{item['answer_revision']} ({state}):", item["text"]])
    lines.extend(["", "## Next step", data["next_step"], ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", type=Path)
    parser.add_argument("--review", type=Path)
    args = parser.parse_args()
    try:
        data = load_json(args.session)
        errors = validate_session(data)
        if not errors and args.review:
            with args.review.open("x", encoding="utf-8") as stream:
                stream.write(render_session(data))
    except (InvalidFile, OSError) as error:
        errors = [error.code if isinstance(error, InvalidFile) else "FILE_UNAVAILABLE"]
    print(json.dumps({"valid": not errors, "errors": errors, "profile_modified": False}))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
