---
name: lekce
description: Začni nebo navaž lekci — opakování splatných kvízů, pak další uzel plánu z learner.md (skill teach).
disable-model-invocation: true
---
Navaž výuku podle skillu `teach`:
1. Stav studenta máš z SessionStart kontextu (learner.md, statistiky, splatná opakování). Pokud learner.md chybí, začni fází 1 (probe) a cíl ber z `cil.md`.
2. Nejdřív odehraj splatná opakování (`quiz.py due` → `quiz.py replay <id>`), max 5.
3. Pak pokračuj dalším nedokončeným uzlem plánu. Pokud plán ještě není schválený, ukaž ho a počkej na souhlas.
