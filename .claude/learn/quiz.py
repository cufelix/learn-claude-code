#!/usr/bin/env python3
"""Graded quiz for Claude Code — port of the pi `quiz` extension, plus spaced review.

Flow (the correct answer is committed BEFORE the learner sees the question):
  1. quiz.py new < quiz.json
       {"question", "options": [{"label", "value"?, "description"?}] (2–4), "correct": value | [values],
        "explanation", "details"?, "multiSelect"?, "shuffle"?, "header"?, "tag"?}
     Validates + shuffles, stores it as pending, prints the exact AskUserQuestion input.
  2. Claude calls AskUserQuestion with that input, unchanged (PreToolUse `guard` enforces it).
  3. PostToolUse `grade`: ✓/✗ + correct answer + explanation to the learner (systemMessage),
     a summary to Claude (additionalContext), one row in state/quiz-log.jsonl.

Other commands:
  quiz.py cancel        drop a pending quiz (e.g. the learner escaped the question)
  quiz.py stats         score + error tags (wrong / don't know) — for /pokrok
  quiz.py due [N]       quizzes due for spaced review (Leitner boxes 1/3/7/21 days)
  quiz.py replay <id>   re-ask a logged quiz (re-shuffled) — same flow as `new`
  quiz.py status        one-line score for the statusline
"""
import hashlib
import json
import os
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

STATE = Path(__file__).resolve().parent / "state"
PENDING = STATE / "pending-quiz.json"
LOG = STATE / "quiz-log.jsonl"
DONT_KNOW = re.compile(r"^\s*(nevím|nevim|nevi|idk|i don'?t know|don'?t know|\?)\s*\.?$", re.I)
JUSTIFY = re.compile(r"\b(protože|neboť|jelikož|because|since)\b", re.I)
BOX_DAYS = {1: 1, 2: 3, 3: 7, 4: 21}
DAY = 86400


def fail(msg):
    print(f"QUIZ REJECTED: {msg}\nFix the quiz JSON and run `quiz.py new` again.", file=sys.stderr)
    sys.exit(1)


def write_atomic(path, text):
    STATE.mkdir(exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def read_log():
    if not LOG.exists():
        return []
    return [json.loads(l) for l in LOG.read_text().splitlines() if l.strip()]


def validate(q):
    for key in ("question", "options", "correct", "explanation"):
        if not q.get(key):
            fail(f"missing `{key}`")
    opts = q["options"]
    if not 2 <= len(opts) <= 4:
        fail("AskUserQuestion allows 2–4 options; 'Other' (free text / 'nevím') is added automatically")
    labels = [squash(o["label"]) for o in opts]
    if len(set(labels)) != len(labels):
        fail("option labels must be unique")
    for a in labels:
        if q.get("multiSelect") and ", " in a:
            fail(f"multi-select label {a!r} contains ', ' — that is the answer separator")
        if JUSTIFY.search(a):
            fail(f"option {a!r} carries a justification — options are bare claims, reasoning goes in `explanation`")
        if DONT_KNOW.match(a):
            fail("don't add your own 'nevím' option — the learner types it via Other")
    values = [o.get("value", o["label"]) for o in opts]
    correct = q["correct"] if isinstance(q["correct"], list) else [q["correct"]]
    missing = [c for c in correct if c not in values]
    if missing:
        fail(f"correct value(s) {missing} not among option values {values}")
    if len(correct) > 1 and not q.get("multiSelect"):
        fail("several correct values but multiSelect is not true")
    right = [len(o["label"]) for o in opts if o.get("value", o["label"]) in correct]
    wrong = [len(o["label"]) for o in opts if o.get("value", o["label"]) not in correct]
    if wrong and max(right) > 1.5 * (sum(wrong) / len(wrong)) and max(right) - min(wrong) > 15:
        fail("the correct option is visibly longer than the distractors — that gives it away; "
             "rewrite so all options share one skeleton")
    return values, correct


def quiz_id(q):
    return hashlib.sha1(q["question"].split("\n\n")[0].encode()).hexdigest()[:8]


def cmd_new(q=None):
    q = q or json.load(sys.stdin)
    values, correct = validate(q)
    opts = [{"label": squash(o["label"]), "value": v, "description": o.get("description", "")}
            for o, v in zip(q["options"], values)]
    if q.get("shuffle", True):
        random.shuffle(opts)
    question = q["question"] + (f"\n\n{q['details'].strip()}" if q.get("details") else "")
    spec = {k: q[k] for k in ("question", "details", "multiSelect", "shuffle", "header", "tag", "explanation")
            if k in q}
    spec["options"] = [{"label": o["label"], "value": v, **({"description": o["description"]} if o.get("description") else {})}
                       for o, v in zip(q["options"], values)]
    spec["correct"] = correct
    write_atomic(PENDING, json.dumps({"id": quiz_id(q), "spec": spec, "question": question, "options": opts,
                                      "correct": correct, "explanation": q["explanation"],
                                      "tag": q.get("tag", ""), "ts": time.time()}, ensure_ascii=False))
    ask = {"questions": [{
        "question": question,
        "header": (q.get("header") or "Kvíz")[:12],
        "multiSelect": bool(q.get("multiSelect")),
        "options": [{"label": o["label"], "description": o["description"] or f"Možnost {'ABCD'[i]}"}
                    for i, o in enumerate(opts)],
    }]}
    print("Call AskUserQuestion with EXACTLY this input (do not reorder or reword):")
    print(json.dumps(ask, ensure_ascii=False))


def find_answer(resp, question):
    if isinstance(resp, dict):
        answers = resp.get("answers")
        if isinstance(answers, dict):
            return answers.get(question) or next(iter(answers.values()), "")
        return next((a for a in (find_answer(v, question) for v in resp.values()) if a), "")
    if isinstance(resp, list):
        return next((a for a in (find_answer(v, question) for v in resp) if a), "")
    if isinstance(resp, str):
        m = re.search(re.escape(f'"{question}"="') + r'(.*?)"(?:\.|,)', resp, re.S)
        return m.group(1) if m else ""
    return ""


def find_note(resp):
    """Notes the learner attached to their selection (AskUserQuestion annotations)."""
    if isinstance(resp, dict):
        ann = resp.get("annotations")
        if isinstance(ann, dict):
            return " ".join(a.get("notes", "") for a in ann.values() if isinstance(a, dict)).strip()
        return next((n for n in map(find_note, resp.values()) if n), "")
    return ""


def squash(s):
    """The answer UI collapses runs of whitespace, so labels are compared whitespace-normalized."""
    return " ".join(s.split())


def chosen_options(quiz, answer):
    """Exact match only — a free-text answer that merely contains a label is NOT that choice."""
    by_label = {squash(o["label"]): o for o in quiz["options"]}
    answer = squash(answer)
    if answer in by_label:
        return [by_label[answer]]
    parts = [squash(p) for p in answer.split(", ")]
    if quiz["spec"].get("multiSelect") and parts and all(p in by_label for p in parts):
        return [by_label[p] for p in parts]
    return []


def cmd_guard():
    """PreToolUse: a pending quiz must be asked verbatim, otherwise grading would silently break."""
    event = json.load(sys.stdin)
    if not PENDING.exists():
        return
    quiz = json.loads(PENDING.read_text())
    qs = event.get("tool_input", {}).get("questions", [])
    ok = (len(qs) == 1 and qs[0].get("question") == quiz["question"]
          and [o.get("label") for o in qs[0].get("options", [])] == [o["label"] for o in quiz["options"]])
    if not ok:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": "A quiz is pending. Pass the `quiz.py new` output to AskUserQuestion "
                                        "verbatim (same question, same option order, one question), or run "
                                        "`python3 .claude/learn/quiz.py cancel` first."}}))


def cmd_grade():
    event = json.load(sys.stdin)
    if event.get("tool_name") != "AskUserQuestion" or not PENDING.exists():
        return
    quiz = json.loads(PENDING.read_text())
    if not any(q.get("question") == quiz["question"] for q in event.get("tool_input", {}).get("questions", [])):
        return
    PENDING.unlink()
    answer = find_answer(event.get("tool_response"), quiz["question"]).strip()
    note = find_note(event.get("tool_response"))
    chosen = chosen_options(quiz, answer)
    by_value = {o["value"]: o["label"] for o in quiz["options"]}
    correct_labels = [by_value[c] for c in quiz["correct"]]
    if not answer or DONT_KNOW.match(answer):
        status, mark = "dont_know", "∅ Nevíš — v pořádku, to je užitečná informace."
    elif not chosen:
        status, mark = "free_text", f"✎ Vlastní odpověď: „{answer}“"
    elif sorted(o["value"] for o in chosen) == sorted(quiz["correct"]):
        status, mark = "correct", "✓ Správně!"
    else:
        status, mark = "wrong", "✗ Špatně."
    STATE.mkdir(exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps({"ts": time.time(), "session": event.get("session_id", ""), "id": quiz["id"],
                            "tag": quiz["tag"], "question": quiz["question"], "answer": answer,
                            "correct": correct_labels, "status": status, "explanation": quiz["explanation"],
                            "note": note, "spec": quiz["spec"]}, ensure_ascii=False) + "\n")
    context = (f"QUIZ GRADED [{quiz['id']}{' #' + quiz['tag'] if quiz['tag'] else ''}]: status={status}. "
               f"Learner answered {answer!r}; correct: {correct_labels}. The learner already saw ✓/✗, the correct "
               "answer and the explanation — don't repeat them; react to what this answer reveals"
               + (" (interpret the free-text answer yourself)." if status == "free_text" else ".")
               + (" dont_know = an honest gap, NOT a wrong guess: teach into it." if status == "dont_know" else "")
               + (f" Learner's note: {note!r} — let it steer your follow-up." if note else ""))
    print(json.dumps({"systemMessage": f"{mark}\nSprávná odpověď: {' + '.join(correct_labels)}\n{quiz['explanation']}",
                      "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": context}},
                     ensure_ascii=False))


def leitner():
    """id -> (box, last_ts, last_row). Correct moves up a box; anything else drops to box 1."""
    items = {}
    for row in read_log():
        prev = items.get(row["id"], (1,))[0]
        box = min(prev + 1, 4) if row["status"] == "correct" else 1
        items[row["id"]] = (box, row["ts"], row)
    return items


def cmd_due(n="5"):
    now = time.time()
    due = sorted(((ts + BOX_DAYS[box] * DAY, box, row) for box, ts, row in leitner().values()
                  if ts + BOX_DAYS[box] * DAY <= now and row.get("spec")), key=lambda d: (d[1], d[0]))
    if not due:
        print("Nothing due for review.")
    for _, box, row in due[:int(n)]:
        print(f"{row['id']}  box {box}  #{row.get('tag') or '-'}  {row['question'].splitlines()[0][:80]}")


def cmd_replay(qid):
    row = leitner().get(qid)
    if not row or not row[2].get("spec"):
        fail(f"no logged quiz with id {qid}")
    cmd_new(dict(row[2]["spec"]))


def cmd_stats():
    rows = read_log()
    if not rows:
        print("Zatím žádné kvízy.")
        return
    c = Counter(r["status"] for r in rows)
    print(f"Celkem {len(rows)}: ✓ {c['correct']}  ✗ {c['wrong']}  ∅ {c['dont_know']}  ✎ {c['free_text']}")
    gaps = Counter(r.get("tag") or "(bez tagu)" for r in rows if r["status"] in ("wrong", "dont_know"))
    if gaps:
        print("Nejčastější mezery: " + ", ".join(f"#{t} ×{k}" for t, k in gaps.most_common(5)))
    boxes = Counter(b for b, _, _ in leitner().values())
    print("Leitner boxy: " + "  ".join(f"{b}:{boxes[b]}" for b in sorted(BOX_DAYS)))
    recent = [r for r in rows[-10:] if r["status"] in ("wrong", "dont_know")]
    for r in recent:
        print(f"  ✗ [{r['id']}] {r['question'].splitlines()[0][:70]} → {r['answer'] or 'nevím'}")


def cmd_status():
    rows = read_log()
    c = Counter(r["status"] for r in rows)
    streak = 0
    for r in reversed(rows):
        if r["status"] != "correct":
            break
        streak += 1
    due = sum(1 for box, ts, row in leitner().values() if ts + BOX_DAYS[box] * DAY <= time.time())
    print(f"📚 ✓{c['correct']} ✗{c['wrong']} ∅{c['dont_know']} · série {streak}" + (f" · k opakování {due}" if due else ""))


def cmd_cancel():
    PENDING.unlink(missing_ok=True)
    print("Pending quiz cancelled.")


if __name__ == "__main__":
    commands = {"new": cmd_new, "grade": cmd_grade, "guard": cmd_guard, "cancel": cmd_cancel, "stats": cmd_stats,
                "due": cmd_due, "replay": cmd_replay, "status": cmd_status}
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        fail(f"usage: quiz.py {'|'.join(commands)}")
    commands[sys.argv[1]](*sys.argv[2:])
