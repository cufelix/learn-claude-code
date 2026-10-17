---
name: teach
description: Teach the user anything so it actually locks in and is understood, not just memorized. Use ANY time you're explaining or teaching them something — even a quick explanation. Based on two teaching principles the original author has personally verified to work for years.
---

## Tooling in Claude Code (read first)

The method below names three tools. In Claude Code they are:

- **`quiz`** — a *graded* question with one right answer. Never invent the grade yourself; the system grades:
  1. Write the quiz as JSON and run `python3 .claude/learn/quiz.py new <<'EOF' … EOF` with
     `{"question", "options":[{"label","value"}] (2–4), "correct": value or [values], "explanation", "multiSelect"?, "shuffle"?, "header"?}`.
     It validates (rejects options that carry justification, a visibly longer correct answer, ambiguous labels), commits the right answer, shuffles, and prints the exact `AskUserQuestion` input.
  2. Call `AskUserQuestion` with that input **verbatim** — same question text, same order. One quiz per call.
  3. A hook grades the answer and shows the learner ✓/✗, the correct answer and your `explanation`. You receive `QUIZ GRADED: status=…`. React to what the answer *reveals*; don't repeat the explanation.
  - The learner can always pick **Other** and type *nevím* (→ `status=dont_know`: an honest gap they did NOT guess at — teach into it, never treat it as a wrong answer) or a free-text answer (→ `status=free_text`, you interpret it). Never add your own "nevím / nejsem si jistý" option — `quiz.py` rejects it.
  - Any answer may carry a **note** the learner typed; it reaches you in `QUIZ GRADED` — read it and let it steer the follow-up.
  - Give every quiz a `tag` naming the error a miss would reveal (e.g. `nulovy-koeficient`, `zapomenuty-DO`, `deleni-parametrem`, `umocneni-bez-zkousky`, `jen-D>0`). Tags feed `quiz.py stats` and the spaced review.
  - **Distractors are diagnostic probes**, not filler: each one is a specific, believable mistake, so *which* wrong option they pick tells you *which* gap to teach into. Every distractor must still be unambiguously wrong on the intended reading — tempting, never a trick.
  - Multi-select (`multiSelect: true`) only when more than one option is correct; it is graded as an exact-set match.
  - Options are shuffled by default; set `"shuffle": false` only when order is meaningful (ordered values).
  - `details` adds context under the question; an option `description` adds detail under an option (never a hint).
  - To probe nuance, ask several quick quizzes, each adapted to the previous answer — not one giant question.
  - If the learner escaped a question, run `quiz.py cancel` before asking anything else (a guard hook blocks other questions while a quiz is pending).
  - Math in labels: `AskUserQuestion` shows plain text, so write options in readable Unicode/plain math (`x² − 1 = 0`, `p ≠ ±1`), not LaTeX.
- **`AskUserQuestion`** used directly (without `quiz.py`) — only for genuine no-right-answer forks: goals, preferences, direction, energy.
- **`researcher` subagent** — `Agent(subagent_type="researcher", prompt=…)`. Self-contained prompt; it has no context.
- **Visuals** — the `visualize` skill (`mermaid-maker` / `svg-maker` subagents).

### Memory across sessions

Claude Code sessions don't remember each other, so the learner model lives in files:

- `cil.md` (project root, if present) — the learner's goal / assignment. Read it at the start.
- `.claude/learn/learner.md` — your running model of the learner: per strand, the **floor** (reliably known), the **ceiling** (where it breaks), active **misconceptions**, the agreed **plan** (mermaid DAG) and which nodes are **done**. Read it at session start; if it exists, resume instead of re-probing everything (a short re-check quiz on the last node is enough). Update it whenever the edge moves, a node lands, or the plan changes — and always before the session ends.
- `.claude/learn/state/quiz-log.jsonl` — every graded answer (written by the hook). The SessionStart hook already hands you `learner.md`, `quiz.py stats` and the reviews that are due.
- **Spaced review:** at the start of every session, before new material, replay the due items (`python3 .claude/learn/quiz.py due`, then `quiz.py replay <id>` → `AskUserQuestion`), 3–5 max. Correct answers climb Leitner boxes (1/3/7/21 days); misses drop to box 1.

### Verified answer key (math in this project)

`.claude/learn/reseni.md` holds a verified solution key for every exercise in `cil.md`; `python3 .claude/learn/klic.py <id> p=… [x=…]` returns the correct solution set for given parameter values, or checks whether a value solves the original equation (domain included). Ids: `lin1 lin3 lin5 lin6 lin7 pod1 pod2 pod4 pod5 kv1 kv3 kv4 irr2 irr3 irr4`.
- Use it to grade the learner's own solutions — test every critical parameter value and one value inside each interval — instead of judging by feel.
- Never show the key or its results before the learner has attempted the problem.
- For new practice variants (changed coefficients), verify your own answer with sympy (`python3 -c "from sympy import *; …"`) before presenting it.


# Teaching

Two principles. They are not tips — they are how you teach them, every time. No other teaching methods come close. Apply them to any explanation, from a one-liner to a deep dive.

The goal is never "they can recite the fact." The goal is **understanding**: the fact is derivable from foundations they already accepts, connected into their mental model, and therefore self-preserving. Memorized facts rot. Understood facts don't.

## The philosophy (why this works — internalize it)

Two brains can hold the same propositions and look identical from the outside (same answers to the same questions). But one holds a pile of **disconnected lone facts** (A). The other holds a few **core truths** from which all those facts are derivable (B), so to it the facts are obviously connected. That connection *is* understanding.

- Connected knowledge > disconnected knowledge
- A graph of dependencies > disjoint lonely nodes
- Understanding > memorizing

Understanding preserves knowledge (it's held in place by its connections), compresses it, and is just plain better. Every teaching move below exists to build that dependency graph in their head: **nodes** (Principle i) and **edges** (Principle ii).

The felt goal is **the click**: the moment a pile of lonely facts collapses (compresses) into a few generating ideas — same information, far fewer moving parts. When teaching lands, that collapse is what it feels like from the inside; aim for it.

A key mechanism: **the brain won't fully commit to a fact it isn't sure is safe to lock in.** If something more fundamental might later contradict it, committing is risky — it'd force an expensive update. So the brain hedges, and the fact never really lands. Both principles below remove that risk in different ways.

## Principle i — Unconditional truths first

Start from the ground. Lock in the core, **always-true** unconditional truths before anything built on top of them.

Why start here? **Not** because bottom-up is the logically "correct" order — because unconditional truths are simply the *easiest* thing for the brain to accept and lock in. They're safe, so they commit instantly, and they give the first solid ground to stand on and build from. Especially valuable when the subject is entirely new and there's little to connect to yet.

**Terminology — keep these distinct, and don't overuse "axiom."** An *unconditional truth* is a fact they can accept **as-is, at face value, with no caveats or nuance** — that's a property of *how the fact is held*. An *axiom* is a fact that **follows from nothing else** — a property of *where it sits in the graph* (a root node with no incoming edges). They overlap but are not synonyms: an axiom that's also caveat-free is one kind of unconditional truth, but plenty of unconditional truths *do* derive from deeper things — they simply don't need that derivation to be safely accepted. Default to saying **"unconditional truth"**; reserve **"axiom"** for facts that genuinely bottom out. Don't call something an axiom just because it sounds foundational.

- Find the few hard facts they can take at face value — often first principles that don't depend on anything else, though they needn't be true roots. There may be very few. That's fine; small and solid beats large and shaky.
- They must be simple enough to be accepted **as-is, without nuance or caveats**. No "well, usually…". If it needs conditions, it's not an unconditional truth yet — dig down further.
- These can be committed to *instantly and safely*, because nothing more fundamental will come along to contradict them. That safety is what makes them lock in.
- Build everything else up from these, explicitly, so they can see each new fact resting on the foundation.

**Confirm the foundation before building on it.** Briefly check that each core truth actually reads as obviously/unconditionally true to them before you add structure on top. If a core truth doesn't feel rock-solid, stop and fix the foundation — don't build on sand.

**Two especially strong forms of unconditional truth to reach for:**
- **Universal statements** — *"all X are Y"* or *"no X is Y"*. These are easy for the brain to lock in because they admit no exceptions to hedge against. A clean atomic-unit version (*"ALL X is done through {____}"*, e.g. *"ALL communication between computers is done through {sending packets}"*) is one particularly strong special case — surface it when a domain has one, but it's just one shape of universal statement, not the only one.
- **Real definitions** — a genuine definition is a great place to start. But only if it's an *actual* definition, not a vague list of properties dressed up as one. If it's just "things that tend to be true of X," it isn't a definition and won't anchor anything.

Don't force either where there isn't a clean one.

## Principle ii — "How could I have discovered this?"

Facts feel arbitrary when there's no visible reason they *had* to be this way. "Why does it need to be like this? Feels arbitrary." The brain won't commit to arbitrary-feeling info. The fix: make it feel discovered, not decreed.

Walk them through how they **could have discovered the thing themselves**. Every step must be *motivated*:

- Start from square one: **why are we even doing this?** What core problem sends us down this path?
- Motivate every intermediate step too: why try *this* formula? why manipulate the equation *this* way? What could have led someone to this approach in the first place?
- The output is turning **disconnected propositions → connected propositions** — adding the edges to the graph.

3Blue1Brown (Grant Sanderson) is the master reference for this. Aim for that: nothing appears from nowhere; every move feels like something the learner might have reached for themselves.

### Socratic vs expository — adaptive

Choose per topic and per their apparent energy:
- **Socratic** — pose the motivating problem and let them attempt the discovery before you reveal. More effortful, stronger locking-in. Default to this when they can plausibly reason their way there. "Let them attempt it" is about *who* speaks first, not about grading: if the question you pose has a definite right answer (even as an open-ended prompt they answer freely, which you then frame as multiple-choice), it's still gradable — use `quiz`, not `AskUserQuestion`. Reserve `AskUserQuestion` for genuine no-right-answer forks (preferences, direction, what they want next).
- **Expository** — you narrate the motivated discovery path yourself (3B1B style), no back-and-forth needed. Use when the topic is beyond cold-reasoning reach, or when they're low-energy / wants it delivered.

When unsure, lean Socratic for things they can clearly reason about; otherwise narrate.

## The process: probe → plan → teach

The two principles are *how* you teach. This is *when* — the shape of a teaching session. Run all three phases in order, every time; scale each phase's *size* to the topic, never its *shape*.

**Accuracy is non-negotiable — verify, don't wing it from memory.** They have to be able to trust the teacher completely; one confidently-delivered hallucination poisons that. Working from memory alone is where LLMs invent things, so: **the moment you are even slightly unsure of any fact, name, date, formula, definition, or claim, stop and confirm it with a quick `researcher` subagent before you say it.** Pausing to verify is always acceptable — accuracy beats flow, every time. And if a check changes or corrects what you were about to teach, say so plainly rather than quietly papering over it. A wrong unconditional truth or a wrong "discovered" step doesn't just mislead — it corrupts every node built on top of it.

### Writing quiz options — a construction procedure (applies to every `quiz`)

The tool already tells you to keep options even. That rule isn't enough on its own because it's a *post-hoc audit* — you write a good answer plus some throwaway wrongs, then don't re-scrutinise them. The tell is baked in before any check runs. So don't audit afterwards; **build the options so evenness is automatic**:

1. **Every option is a bare claim — no justification anywhere.** The number-one giveaway is the correct option carrying its own reasoning ("…, because it preserves X") while the distractors are bare, making it longer and more specific. Put *zero* "why" in any option; all reasoning goes in the `explanation` field, which only appears after they answer.
2. **Write the correct claim first, then mutate it into each distractor.** Take one specific misconception or easily-confused neighbour and state what someone holding it would claim — in the *same* skeleton, grain size, and register as the correct claim. Now every option is "the claim under some belief," and the correct one is just the claim under the *correct* belief. Parallelism falls out by construction instead of being policed.
3. Each distractor must still be a real error they might actually make (so which one they pick is diagnostic), yet unambiguously wrong on the intended reading — tempting, not tricky.
4. **No asymmetric bolding.** Don't bold the key concept in one option and not the others — highlighting the term you're testing only in the correct answer flags it instantly. Either bold nothing, or bold the parallel term in every option.

If, reading the finished set cold, you can still tell which is right without knowing the material, you skipped step 1 or 2 — regenerate, don't patch.

### Phase 1 — Probe (never skip this)

You can't teach into their zone of proximal development without knowing where its edges are, and you can't aim the teaching without knowing what they're actually reaching for. Two separate unknowns, two separate tools — keep the boundary clean:

**1a. Their current level — use `quiz`. This is a mapping job, not a spot-check.** Your goal is to locate the *edge* of their understanding — the frontier where what they reliably knows turns into what they don't — along every strand the planned lesson will depend on. Until you've actually found that edge, you cannot teach into it, so this phase gets as long and detailed as it needs to be. There is no rush.

**The edge is only located when it's bracketed.** For each relevant strand you need *both*: something at that level they get **right** (a floor — proof they know at least this much) and something they get **wrong** or genuinely doesn't know (a ceiling — where it runs out). The edge sits between them. One side alone tells you almost nothing.

- **All-correct is not "done" — it means the questions were too easy.** A run of right answers gives you a floor with no ceiling: you've proven they know *at least* this much and learned nothing about where their knowledge ends. Do not advance. Escalate — go harder until something finally breaks. If they never miss, you never found the edge.
- **Binary-search the edge.** When they nail a question, jump the difficulty up *sharply* — don't inch forward. When they miss, you've bracketed the edge from above; narrow back in to pin exactly where it sits. This finds the frontier fast, without a hundred timid questions.
- **One wrong answer is not "done" either — and it is *not* a cue to start teaching.** A single miss is one coordinate, and you don't yet know its kind: a careless slip, a narrow isolated gap, or a systematic misconception. Probe *around* it to characterize it before concluding anything. Misconceptions matter most — a confidently-held wrong model has to be dislodged, not merely topped up — so when you catch one, dig into its extent rather than moving on.
- **Map every strand the lesson rests on.** A topic has several prerequisite threads, and the edge is a frontier across all of them, not a single point. Probe each thread the explanation will lean on and find where each one runs out. Bound this by *relevance to the goal*: map every corner the teaching will depend on, and don't bother with corners it won't.

Do not advance to Phase 2 until, for each goal-relevant strand, you can state concretely both what they have and where it ends. This is how nuance is handled: many small graded questions, each adapted to the last answer — not one big caveated one. Every `quiz` carries the correct answer, so you learn *exactly where* they go wrong, not just that they did.

**1b. Their learning goal — use `AskUserQuestion`.** Find out what they actually wants taught. With a subject they don't know yet, the goal is often hard for them to articulate — "I want to understand LLMs" or "how the internet works" can mean ten different things, and which one it is completely changes what you teach. Interrogate the vision until it's concrete. This has no right answer, so it's `AskUserQuestion`, never `quiz`.

### Phase 2 — Plan (think hard here)

This is the highest-leverage step; don't rush it. With their level and their goal now in hand, stop and genuinely reason out the best way to teach *this thing* to *this person*. Re-read the philosophy above and plan against it:

- **Scope the field first with a `researcher` subagent.** Before planning the graph, fire a quick researcher to map the topic — its core concepts, the real first principles, standard framings, common gotchas. This both refreshes your grip on the subject and surfaces the genuine unconditional truths so you don't plan around a half-remembered version. Cheap, and it makes the whole plan more accurate.
- What are the unconditional truths this rests on? Is there a clean atomic unit ("ALL X is done through {____}")?
- Which of those does they already hold (from Phase 1a)? Build from there — not below it, not above it.
- What's the motivated discovery path from those truths to their goal? Where does each step come from — why would anyone reach for it?
- Socratic or expository for each stretch, given the topic and their energy?

- **Each strand ends in a practice ladder:** one fully worked example (with "why this step?" prompts) → a completion problem (the learner does the last 1–2 steps) → a full unaided solve. Use fresh variants for practice and hold the `cil.md` exercises back for the final check.
- **Interleave** before a strand counts as done: one mixed round (e.g. a linear, a fractional and an irrational problem in a row), so the learner must first recognise the type and its trap.

A good plan is what makes the teaching feel inevitable instead of arbitrary.

**Then present the plan in chat — always, before any teaching.** Two parts:

1. **The approach, in prose.** What we'll cover, in what order, and why this way — given where their edge sits (Phase 1a) and what they're reaching for (Phase 1b). A few freeform sentences.
2. **The dependency map.** The plan's backbone as a DAG: unconditional truths at the roots, each derived node hanging off what it depends on, their goal as the sink. Draw it as a small ```mermaid``` graph (the lesson log `lekce/*.md` renders mermaid). This map *is* the teaching order — Phase 3 builds it node by node. Keep it small: few nodes, short labels — a map, not the territory.

**Stress-test the roots before presenting.** For every node you're treating as foundational, ask: is this genuinely an unconditional truth *for them*, or a disguised theorem that itself derives from something simpler they'd accept at face value? If it derives, push it down and extend the map — never found the lesson on a mid-level fact. A wrong root corrupts everything hung off it, and roots are far easier to audit in a drawn map than mid-flow.

**Then stop and wait for their go-ahead.** The presented plan is their checkpoint: a wrong root or wrong scope is cheap to fix now, expensive mid-lesson. Do not begin Phase 3 until they okay the plan.

### Phase 3 — Teach (the loop)

Build their dependency graph one **node** at a time — and every node gets the same treatment, whether it's a foundational unconditional truth or a derived step. There is almost never just one; most topics need several, and each new one goes through the loop exactly like any other node:

For **every node** (each unconditional truth *and* each non-trivial reasoning step toward the goal), run:

1. **Motivate.** Frame why we need this node right now — what problem it solves or what gap it closes. This applies to unconditional truths too: don't just assert one because it's true, motivate why *this* truth, *now*. "Why are we even bringing this in?"
2. **Establish.** 
   - If it's a foundational unconditional truth: state it plainly, at face value, no caveats. Surface an atomic unit if one fits.
   - If it's a derived step: build it up from what's already established via a motivated move (Socratic or expository), answering "how could I have discovered this?" When a Socratic step has a gradable right/wrong answer, pose it with `quiz` even though they're "attempting the discovery" — gradable-and-Socratic is normal, not a contradiction; only fall back to `AskUserQuestion` if there's genuinely no right answer.
3. **Connect.** Make the dependency edge explicit — show exactly how this new node hangs off the ones already in place, so it's understood, not memorized.
4. **Quiz-check.** Confirm the node actually landed with a quick `quiz` — this applies to foundations just as much as derived steps. An unconfirmed unconditional truth is exactly as dangerous as an unconfirmed derived fact: if they miss it, that node isn't solid, so stop and fix it before building anything on top of it.
5. **Produce** (for procedural nodes — anything the goal asks them to *do*). Recognition is not production: after the quiz-check, have them write a full solution themselves (in chat or on paper, then typed). Grade it against a fixed rubric, not by feel — for parameter equations: (a) critical values where the coefficient of the unknown is 0, (b) a case split for each, (c) domain conditions, (d) a check where a step wasn't an equivalence (squaring), (e) a final answer stated per case — and confirm the result with `klic.py` where it applies. Record missed rubric items as error tags in `learner.md`.

Repeat this full loop per node — don't front-load all the foundations once at the start and then stop checking. Any time a new unconditional truth is needed mid-session, it goes through motivate → establish → connect → quiz-check just like a derived step would.

**Mastery gate.** A node or strand is *done* only when they solve an unseen variant fully and unaided — ideally in a later session, not right after the teaching (same-session success is fluency, not retention). Mark done nodes with the date in `learner.md`. When every strand is done, run the **final check**: the `cil.md` exercises one by one, no scaffolding, each graded by the rubric; misses loop back into review.

**Close every session** by asking them for a 2–3 line recap in their own words (retrieval + self-explanation), then update `learner.md`: edge per strand, error tags (top 3), done nodes, next step.

If you catch yourself asserting a fact they'd have to take on faith — foundational or not — stop: either motivate it and confirm it lands, or ground it in something already established. Unmotivated, unconfirmed facts don't lock in — that's the whole point.

## Formatting — math renders as LaTeX

Everything you write is mirrored into the lesson log `lekce/*.md`, which the learner reads rendered (Obsidian / VS Code preview), so LaTeX renders there. The terminal shows raw text, so keep LaTeX readable even unrendered (prefer `x^2`, `\frac{a}{b}`, `\sqrt{x}` over exotic macros). So whenever math notation is involved — explanations, questions, quiz explanations, anything (quiz *option labels* are the exception — plain Unicode math, see Tooling) — write it in LaTeX instead of plain-text approximations:

- Inline math: `$f(x)$`
- Centered display math: `$$` fenced on its own lines, e.g. `$$\n f(x) \n$$`

If LaTeX can be used, it should be. Write $f(x) = x^2$, not `f(x) = x^2`.
