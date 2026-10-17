#!/usr/bin/env python3
"""Stop hook: mirror the session into lekce/<date>-<session>.md for comfortable reading.

Port of the pi `md-log` extension. Open the file in Obsidian (or any viewer with
LaTeX + mermaid) next to the terminal. Captures only what matters for reading:
learner prompts, Claude's lesson text, and quiz / question blocks with grades.
The file is regenerated from the transcript each turn, so it is always complete.
"""
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
STATE = Path(__file__).resolve().parent / "state"
QUIZ_LOG = STATE / "quiz-log.jsonl"
LINK = STATE / "md-log.json"  # {"file": path} → log there; {"file": null} → logging off
NOISE = re.compile(r"<(system-reminder|command-[a-z]+|local-command-[a-z]+)>.*?</\1>", re.S)
MARKS = {"correct": "✓ Správně", "wrong": "✗ Špatně", "dont_know": "∅ Nevím", "free_text": "✎ Vlastní odpověď"}


def callout(kind, title, body):
    lines = [f"> [!{kind}] {title}"] + [f"> {l}" if l else ">" for l in body.strip().splitlines()]
    return "\n".join(lines)


def text_of(content):
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")


def load_grades(session):
    grades = {}
    if QUIZ_LOG.exists():
        for line in QUIZ_LOG.read_text().splitlines():
            g = json.loads(line)
            if g.get("session", session) == session:
                grades.setdefault(g["question"], []).append(g)
    return grades


def render(transcript, session):
    grades = load_grades(session)
    asks, out = {}, []
    for line in transcript.read_text().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("isSidechain") or e.get("isMeta") or e.get("type") not in ("user", "assistant"):
            continue
        content = (e.get("message") or {}).get("content")
        if e["type"] == "user":
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") in asks:
                        out.append(answer_block(asks.pop(b["tool_use_id"]), e.get("toolUseResult"), grades))
            prompt = NOISE.sub("", text_of(content or "")).strip()
            if prompt and not prompt.startswith("<"):
                out.append(callout("quote", "TY", prompt))
            continue
        for b in content if isinstance(content, list) else [{"type": "text", "text": content or ""}]:
            if b.get("type") == "text" and b["text"].strip():
                out.append(b["text"].strip())
            elif b.get("type") == "tool_use" and b.get("name") == "Skill":
                out.append(f"> [!note] SKILL loaded: {b['input'].get('skill', '?')}")
            elif b.get("type") == "tool_use" and b.get("name") == "AskUserQuestion":
                for q in b["input"].get("questions", []):
                    asks[b["id"]] = q
                    opts = "\n".join(f"{i}. {o['label']}" for i, o in enumerate(q.get("options", []), 1))
                    kind = "question" if q["question"] in grades else "info"
                    out.append(callout(kind, "KVÍZ" if kind == "question" else "OTÁZKA", f"{q['question']}\n\n{opts}"))
    return "\n\n".join(out) + "\n"


def answer_block(q, result, grades):
    answer = ""
    if isinstance(result, dict) and isinstance(result.get("answers"), dict):
        answer = result["answers"].get(q["question"], "")
    graded = grades.get(q["question"])
    if not graded:
        return callout("success", "ODPOVĚĎ", answer or "(bez odpovědi)")
    g = graded.pop(0)
    kind = "success" if g["status"] == "correct" else "failure" if g["status"] == "wrong" else "warning"
    body = f"Tvoje odpověď: {g['answer'] or '—'}\n\nSprávně: {' + '.join(g['correct'])}\n\n{g['explanation']}"
    return callout(kind, MARKS.get(g["status"], g["status"]), body)


def first_date(transcript):
    """Date of the session's first entry — stable across midnight and resumes (file ctime is not)."""
    with transcript.open() as f:
        for line in f:
            ts = json.loads(line).get("timestamp") if line.strip() else None
            if ts:
                return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone().strftime("%Y-%m-%d")
    return datetime.now().strftime("%Y-%m-%d")


def safe_target(arg):
    """Only a .md file inside the project, never through a symlink — the hook writes there unattended."""
    path = (PROJECT / arg)
    resolved = path.resolve()
    if resolved.suffix != ".md" or not resolved.is_relative_to(PROJECT) or path.is_symlink():
        return None
    return str(resolved)


def link(arg):
    """`md_log.py link <file>` / `md_log.py unlink` — port of pi's /md-log and /md-unlog."""
    STATE.mkdir(exist_ok=True)
    target = safe_target(arg) if arg else None
    if arg and not target:
        sys.exit(f"Odmítnuto: {arg!r} — log musí být .md soubor uvnitř projektu (ne symlink).")
    LINK.write_text(json.dumps({"file": target}))
    print(f"md-log → {target}" if target else "md-log off")


def main():
    if len(sys.argv) > 1:
        return link(sys.argv[2] if sys.argv[1] == "link" and len(sys.argv) > 2 else None)
    event = json.load(sys.stdin)
    transcript = Path(event.get("transcript_path", ""))
    if not transcript.is_file():
        return
    started = first_date(transcript)
    target = PROJECT / "lekce" / f"{started}-{transcript.stem[:8]}.md"
    if LINK.exists():
        linked = json.loads(LINK.read_text()).get("file")
        if not linked:
            return
        if not safe_target(linked):
            return
        target = Path(linked)
    target.parent.mkdir(parents=True, exist_ok=True)
    body = render(transcript, event.get("session_id", transcript.stem))
    if body.strip():
        tmp = target.with_suffix(".tmp")
        tmp.write_text(f"# Lekce {started}\n\n{body}")
        os.replace(tmp, target)  # a live viewer never sees a half-written file


if __name__ == "__main__":
    main()
