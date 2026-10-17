---
description: Zrcadli lekci do zvoleného markdown souboru (bez argumentu = výchozí lekce/<datum>-<session>.md)
argument-hint: "[cesta/k/souboru.md]"
allowed-tools: Bash(python3 .claude/learn/md_log.py:*)
---
!`python3 .claude/learn/md_log.py link $ARGUMENTS 2>&1 || true; [ -z "$ARGUMENTS" ] && rm -f .claude/learn/state/md-log.json && echo "md-log → výchozí lekce/"`

Potvrď jednou větou, kam se lekce teď zapisuje (celá session se při dalším kroku zapíše zpětně).
