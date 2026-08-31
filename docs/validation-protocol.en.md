# Cross-Domain Validation Protocol

[中文](validation-protocol.md) | English

## Purpose

This protocol explains how real projects test agent-native methods for long-running work while the public repository stays abstract, public, and reviewable.

Validation does not prove that a document is internally consistent. It checks whether another agent can continue real work from durable information, select the correct source of truth, use a formal entry point, produce an acceptable result, and let feedback change the next run.

## Two Boundaries

### Public Method Repository

The public repository stores only:

- candidate questions, methods, and decidable tests;
- redacted validation records that can support a conclusion on their own;
- valid counterexamples and decisions to promote, narrow, or remove a rule;
- professional rules that still need to run within a domain track.

### Local Real Projects

Local projects continue to store:

- personal articles, images, account operations, and platform state;
- customer material, bids, enterprise knowledge, and business inputs;
- product code, runtime state, logs, test data, and release records;
- servers, networks, credentials, machine paths, and local tool configuration.

Write local source mappings and unredacted temporary analysis to `.local/`, which Git ignores. Do not copy real projects or source material into this repository. Public documents must not contain absolute machine paths, accounts, customer identities, credentials, private repository details, or information that could reconstruct private business material.

## One Validation

Each validation selects one complete task that has already happened or can be executed for real, then answers six questions:

1. **Intent**: What did the user want to change, and what outcome would have value?
2. **Context**: Which valid facts, methods, and prior decisions did the task use?
3. **Source of truth**: Who owned the current facts, and how were conflicts and obsolete information handled?
4. **Action**: Which formal entry point did the agent use, and which decisions remained human responsibilities?
5. **Result**: Which user-inspectable artifact or real-world change proved completion?
6. **Feedback**: How did failures, edits, or use outcomes change the next run?

Record the actual path and failures first. Do not rewrite events to fit the existing theory.

## Five Tests

- **Continuation test**: Can a new session or agent recover the goal, boundary, and next action from the formal entry point without reading old chats?
- **Source-of-truth test**: When sources, formal deliverables, derivatives, old versions, and temporary state coexist, can the agent select the current authority?
- **Result test**: Can a real entry point and a user-inspectable result prove completion without relying on an agent's claim or file existence?
- **Feedback test**: Does a real failure or human edit change later work, and can we trace what it changed?
- **Transfer test**: Does the candidate constraint still hold outside the current tool or track? If not, is the difference explicitly retained in the domain track?

These tests are not a fixed scorecard. Run only the tests that the current judgment depends on, and disclose what remains untested.

## Rule Disposition

Every validation ends with one decision:

- **Enter cross-track candidates**: Real tasks in at least two independent tracks support the same constraint, and no valid counterexample exists.
- **Remain in the track**: The rule works for this professional task but depends on the track's goals, risks, or carrier.
- **Continue observation**: Evidence cannot decide yet. Keep the question and identify the next real task that could distinguish the hypotheses.
- **Narrow or remove**: A reproducible, recorded counterexample shows that the rule itself caused failure.

Finite cases cannot prove applicability to every industry. Cross-track candidates remain open to refutation from new tracks.

## Public Record Boundary

A public validation record retains only the minimum facts needed to support its judgment: task type, trigger, prior rule, observation, counterexample or supporting evidence, and rule disposition. The local project continues to own raw material. Public records must not copy full articles, customer documents, repositories, screenshots, logs, or platform data.
