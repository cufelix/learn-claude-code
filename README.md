# learn-claude-code

AI učitel pro [Claude Code](https://claude.com/claude-code), postavený jako port systému
**[amosblomqvist/learn](https://github.com/amosblomqvist/learn)** (pi konfigurace z videa
[How I Use AI to Learn Things](https://www.youtube.com/watch?v=kzcI5F4tGiU)). Výuková filozofie
(skill `teach`) je převzatá od autora; tento repo ji přenáší do Claude Code a rozšiřuje.
Ukázkový obsah: české SŠ **rovnice s parametrem** (`cil.md`).

## Spuštění

```bash
git clone https://github.com/cufelix/learn-claude-code && cd learn-claude-code
(cd .claude/learn && npm install)   # mermaid-cli + puppeteer pro obrázky
pip install sympy                   # ověřování výsledků (klic.py)
claude "začni mě učit"              # potvrď "trust this folder" — jinak neběží hooky
```

Vedle terminálu otevři složku v **Obsidianu** (nebo VS Code preview): lekce se živě zapisují do
`lekce/*.md` i s LaTeXem, mermaid diagramy a obrázky.

Vlastní téma: přepiš `cil.md` a `CLAUDE.md`, smaž `.claude/learn/reseni.md` + `klic.py` (klíč k ukázce).

## Co v tom je

| Původní pi | Tady (Claude Code) |
|---|---|
| `skills/teach` — probe → plan → teach | `.claude/skills/teach/` (+ návod k nástrojům, paměť, produkce, mastery gate) |
| `skills/visualize` + `mermaid-maker`, `svg-maker` | `.claude/skills/visualize/`, `.claude/agents/` — subagent vykreslí, **podívá se** na PNG, opraví, publikuje do `viz/` |
| `researcher` (web_search) | `.claude/agents/researcher.md` (WebSearch/WebFetch) |
| `extensions/quiz.ts` | `.claude/learn/quiz.py` + hooky: správná odpověď se uloží **před** otázkou, náhodné pořadí, okamžité ✓/✗ + vysvětlení, „nevím“, poznámka k odpovědi, kontrola férovosti možností |
| `extensions/ask-user-question.ts` | vestavěný `AskUserQuestion` |
| `extensions/md-log.ts` (+ `/md-log`, `/md-unlog`) | `.claude/learn/md_log.py` (hooky Pre/PostToolUse + Stop) + příkazy `/md-log`, `/md-unlog` |
| `extensions/visual-tools` | `.claude/learn/render.mjs` (Mermaid přes mmdc, SVG přes headless Chrome) |

### Navíc oproti originálu
- **Paměť mezi sessions** — `learner.md` (hranice znalostí, chyby, plán) se automaticky vkládá na začátku každé session (SessionStart hook).
- **Spaced repetition** — Leitnerovy boxy (1/3/7/21 dní) nad historií kvízů: `quiz.py due` / `replay`.
- **Tagy chyb** — každý kvíz nese typ chyby; `/pokrok` ukáže nejčastější mezery.
- **Produkce, ne jen rozpoznání** — student píše celá řešení, hodnotí se podle rubriky; mastery gate + závěrečná zkouška.
- **Ověřený klíč** — `klic.py` (sympy) zkontroluje řešení studenta pro libovolnou hodnotu parametru.
- **Guard hook** — kvíz nejde položit jinak, než jak byl zaregistrován (jinak by hodnocení tiše selhalo).
- **Statusline** — `📚 ✓12 ✗3 ∅1 · série 4 · k opakování 2`.
- Příkazy `/lekce`, `/kviz`, `/pokrok`.

## Omezení
- `AskUserQuestion` má max. 4 možnosti a zobrazuje prostý text (matematika v možnostech jako Unicode, LaTeX až ve vysvětlení a v logu).
- „Nevím“ se zadává přes *Other*.

## Licence
Originální repo [amosblomqvist/learn](https://github.com/amosblomqvist/learn) nemá uvedenou licenci; texty skillů a agentů jsou
odvozené z něj a patří autorovi. Vlastní kód tohoto portu (`.claude/learn/*`, hooky, příkazy) je MIT.
