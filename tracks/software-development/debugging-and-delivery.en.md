# Debugging and Real Delivery

[中文](debugging-and-delivery.md) | English

## The Business Promise Comes Before the Test Tool

Before debugging, state the formal entry point, real input, work performed, and result the user can continue using. The test charter also records the environment, quality floor, risk hypothesis, irreversible actions, and stopping conditions.

An open page, successful API response, exited process, agent completion claim, nonempty file, or normal screenshot cannot prove the business outcome on its own.

## Three Independent Evidence Surfaces

Agent-led debugging needs three surfaces that check each other:

1. **Action surface**: advances the work through the UI, CLI, public API, or formal agent interface used by the real user or caller.
2. **Observation surface**: reads pages, network activity, processes, logs, formal state, persistent data, and final artifacts to establish what happened.
3. **Judgment surface**: checks content, completeness, sources, editability, persistence, isolation, and whether the user can continue, all against the business promise.

The three surfaces cannot rely on the same success signal. Observation may use read-only white-box evidence, but cannot bypass the product entry point to add data, change state, or manufacture a pass. Do not invent a second business API for testing when the product has no formal machine interface.

## Adaptive Test Charter

For each run, choose one complete primary path and one to three high-information risk branches based on the code change, prior failure, real platform, and data. Common risks include historical-state upgrades, mid-run edits, cancel and recovery, reconnect after network loss, duplicate submission, cross-entity contamination, and stability across repeated inputs.

Record the test identity first: immutable version, platform, environment, account or project, real input snapshot, allowed cost, and write boundary. One business owner controls each formal state so that several instances or agents cannot make the result impossible to attribute.

## Execution Order

1. Use the smallest relevant static checks, regression tests, build, and installation checks to remove deterministic errors.
2. Start from the only formal entry point. Do not edit the database or internal state directly.
3. Run the business path to an explicit success, failure, or recoverable terminal state. Queued, spinning, and temporary silence are not terminal states.
4. Check the final deliverable and formal state, not only the success message.
5. Exit and reopen the same object to verify persistence, recovery, and the absence of silently duplicated unfinished work.
6. After the primary path passes, attack the boundary most likely to fail according to the risk evidence.

Generated results cannot be tested against fixed wording, and the executing agent cannot be the only evaluator. Check structural minimums, factual minimums, and business quality separately. An independent reviewer or person may assess semantic quality, but the judgment still returns to real sources and deliverables.

## Preserve the Failure Site

When a failure occurs, first preserve the time, version, page, logs, process state, formal state, and artifacts. Do not immediately clear caches, switch to fake data, patch state by hand, or retry until something passes.

Separate failure layers: environment and permissions, installation and version residue, runtime, business state, presentation mapping, or result quality. An interface failure does not automatically implicate the network or model. An environment failure is not automatically a product defect.

## Falsifiable Root Cause

Before changing code, write one causal statement that an experiment can disprove:

> When a condition occurs, a formal owner fails to fulfill a responsibility because of a specific mechanism, so the user sees this symptom.

Choose the control experiment that best separates competing hypotheses. Compare a known-good version with the current version, an official entry point with a wrapper, formal state with its interface projection, small and large inputs, or an existing user state with an isolated state. One experiment separates the key hypotheses without changing several layers at once.

## Repair the Responsibility Boundary

A fix should restore the full lifecycle to its formal owner: merge duplicate sources of truth, remove false-success fallbacks, correct input and write boundaries, preserve the original task while restoring observation, and let formal business state drive the interface.

A deterministic defect gets the narrowest behavioral regression that proves the old implementation fails and the new one passes. Then retest through the same formal entry point, target platform, and real data. If the same user symptom returns, stop local patching and revisit the product goal, source of truth, and responsibility owner.

## Completion

- The formal entry point completed the real business task.
- Action, observation, and judgment evidence check each other.
- The final artifact is useful to the user.
- Human edits, costs, and key risks were not lost or fabricated.
- Formal state and artifacts remain consistent after reopening.
- The root cause belongs to the correct owner, with regression evidence and a real-environment retest.
- Uncovered areas are explicit and were not hidden behind a fallback or different data.

Specific automation tools, system commands, log paths, and project samples belong to the real project implementation, not this method.
