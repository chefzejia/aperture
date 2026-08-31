# AGENTS.md

[中文](AGENTS.md) | English

Scope: the entire `agentic-work-infra` repository.

## Project Boundary

This project studies how people and agents can organize long-running work so that intent, context, sources of truth, results, and feedback survive across sessions, tools, and teams.

"Applicable to every domain and industry" is a research hypothesis that must remain open to refutation. It is not a project slogan or a default assumption.

## Reading Order

Read these files first for every task:

1. `README.en.md`
2. `docs/handoffs/current.en.md`

For validation against a real project, then read `docs/validation-protocol.en.md`. For work on a specific track, read only that track's `README.en.md` and the method documents it links directly.

## Sources of Truth

- `README.md` owns the project's long-term question, boundary, candidate hypotheses, and validation approach.
- `docs/handoffs/current.md` is the sole source of truth for the current research question, accepted baseline, and next action. It does not accumulate full history.
- `docs/validation-protocol.md` is the shared protocol for local validation, public evidence, and rule promotion.
- Each `tracks/*/README.md` owns that track's question, boundary, candidate methods, and validation criteria. Method documents within the track own the corresponding professional rules.
- Real cases retain raw facts and failure history. Method documents retain only candidate judgments that still hold after comparison.
- Current code, files, task results, and real-world feedback override prior methods and memory.

The Chinese files named above are normative. Their English counterparts are translations.

## Research Discipline

- Define the real work problem before discussing products, interfaces, protocols, skills, or directory structures.
- Observe the complete work process. Do not invent a general classification from one file, field, or local failure.
- Separate cross-domain constraints, domain strategy, and carrier-specific implementation. A common problem does not imply one common implementation.
- One reproducible counterexample caused by the rule itself is enough to narrow or remove a candidate.
- Support from several independent domains increases confidence. It cannot prove that a rule holds in every domain.
- Only real tasks can show that a method works. Consistent documentation, generated files, and demos are not business validation.
- The same physical object can play different roles in different tasks. State the task and purpose before classifying it.
- Evidence from one track can change only that track. A constraint needs support from real tasks in at least two independent tracks before it can enter the cross-track core.
- Every conclusion must state its disposition: enter the core candidates, remain in the track, continue under observation, or be rejected by a counterexample.

## Minimality

- Create only the files required by current research or validation.
- Do not create empty templates, permanent status dashboards, content calendars, or structures meant to be filled later.
- Do not copy private paths, business processes, account state, or tool configuration from an existing project into a general method.
- Store local source mappings and unredacted temporary analysis only in the ignored `.local/` directory. External projects continue to own the original material. Do not create a second source of truth here.
- Let evidence determine the final artifact. Do not build a visual dashboard or general platform before the core model holds.

## Bilingual Management

- Chinese documents without a language suffix are normative. A sibling `*.en.md` file is an English mirror and does not own facts or rules independently.
- Update both languages in the same commit whenever an active project entry, protocol, handoff, core candidate, track method, or validation record changes. If both versions cannot be updated, do not change public semantics.
- Chinese documents link to Chinese versions first. English documents link to English versions first. Historical notes and archives without a translation must be labeled as Chinese-only.
- If the two languages conflict, follow the Chinese source and fix the English drift in the current change. Do not let the versions evolve separately.
- Fixed terms: `当前执行面` is `current execution surface`; `真源` is `source of truth`; `线路` is `track`; `验证记录` is `validation record`; `规则去向` is `rule disposition`.

## Safety and Git

- Do not commit credentials, cookies, tokens, API keys, private customer data, or unredacted material.
- External projects are read-only by default. Modifying a case repository requires explicit authorization for the current task.
- Before committing, run `git status --short` and `git diff --check`, and confirm that no accidental files are present.
- Do not revert unrelated user changes.
