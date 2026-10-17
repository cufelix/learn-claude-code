---
name: kviz
description: Rychlé procvičení — 5 kvízů zaměřených na nejslabší místa (tagy chyb) a splatná opakování.
disable-model-invocation: true
---
Aktuální statistiky:
!`python3 .claude/learn/quiz.py stats`

Splatná opakování:
!`python3 .claude/learn/quiz.py due 5`

Polož 5 kvízů (postup `quiz` ze skillu `teach`, jeden po druhém, každý přizpůsob předchozí odpovědi): nejdřív splatná opakování přes `quiz.py replay <id>`, zbytek nové varianty na nejčastější tagy chyb. Nové varianty ověř sympy dřív, než je položíš. Na konci jednou větou shrň, co sedí a co ne, a aktualizuj `.claude/learn/learner.md`.
