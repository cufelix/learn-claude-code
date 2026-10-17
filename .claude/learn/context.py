#!/usr/bin/env python3
"""SessionStart hook: hand Claude the learner model + recent quiz misses + due reviews, so every
session resumes where the last one ended (Claude Code sessions don't remember each other)."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
learner = HERE / "learner.md"
parts = [f"## learner.md\n{learner.read_text()}" if learner.exists()
         else "No learner.md yet — this is the first session: start with Phase 1 (probe) of the teach skill."]
for cmd, title in (("stats", "Quiz stats"), ("due", "Due for spaced review (replay these first)")):
    out = subprocess.run([sys.executable, str(HERE / "quiz.py"), cmd], capture_output=True, text=True).stdout.strip()
    if out and not out.startswith(("Zatím", "Nothing")):
        parts.append(f"## {title}\n{out}")
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                         "additionalContext": "# Learning state\n\n" + "\n\n".join(parts)}},
                 ensure_ascii=False))
