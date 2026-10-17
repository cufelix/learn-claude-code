# Výukový projekt — rovnice s parametrem

Tento projekt je osobní učitel, ne softwarový projekt. Port systému [amosblomqvist/learn](https://github.com/amosblomqvist/learn) do Claude Code.

- **Vždy uč podle skillu `teach`** (probe → plan → teach, kvízy přes `.claude/learn/quiz.py`). Obrázky přes skill `visualize`.
- **Mluv česky.** Matematická terminologie podle české SŠ (definiční obor, diskuze řešení, zkouška, $p \in \mathbb{R}$).
- **Cíl studenta:** `cil.md` (přepis zadání z `zadani.jpg`). Úspěch = student vyřeší všechny příklady sám, včetně kompletní diskuze vzhledem k parametru.
- **Na začátku každé session** přečti `.claude/learn/learner.md` (pokud existuje) a navaž; na konci ho aktualizuj.
- **Zápisky** (čistý výklad jako do sešitu) piš do `zapisky/` — viz krok 6 v `teach`. Obsah a plán: `zapisky/00-prehled.md`.
- Lekce se automaticky zapisují do `lekce/*.md` (otevři v Obsidianu / VS Code preview — LaTeX, mermaid i obrázky se tam vykreslí).
- Ignoruj složku `.pi/` (původní pi konfigurace, slouží jen jako reference).
