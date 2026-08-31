---
name: knowledge-base-infra-english-reference
description: English mirror of the knowledge base infrastructure method. The executable source of truth is SKILL.md. Use this file for public reading and translation review, not as a second runtime specification.
agent_created: true
---

[中文](SKILL.md) | English

# Knowledge Base Infrastructure

This method provides a shared specification for knowledge-base work across carriers, including plain folders, online document platforms, note applications, and drives. Each carrier combines content objects, organizing relationships, and a shell. The method does not depend on one product or local path.

The executable skill is self-contained. Its `references/` directory contains the runtime specification, and changes are made inside the skill with versioned archives. The current version is `v0.2-candidate`; it does not claim a frozen cross-domain method before validation in a second real domain.

## Core Principles

1. **AI is the primary reader**: RAG retrieval and agent calls are the main consumers, so decidability takes priority over appearance.
2. **Every rule must be decidable**: Write each rule as a pass or fail test. Words such as "clear," "concise," and "reasonable" need a test or must be removed.
3. **Separate invariants from strategies and revise them asymmetrically**: Invariants include lifecycle independence, the no-distortion rule, one source of truth and retirement, minimally sufficient names, metadata, two-level acceptance, feedback, and agent prohibitions. One valid counterexample can demote or remove an invariant. Adding or promoting one requires evidence from at least two independent domains. Strategies such as directory depth, naming templates, length warnings, batch size, and a `graveyard/` default may change after one real case.
4. **No adaptation by default**: Deploy with the invariants and default strategies. Add the smallest adaptation only after evidence shows a stable domain-method gap.
5. **Two-level acceptance**: Technical write completion requires successful retrieval, actual readback, and structural completeness. Validated business reuse is a separate state proved by successful use in a real task and enters the feedback loop. An unvalidated object cannot be treated as validated knowledge in cross-task decisions.
6. **Value formula**: content quality multiplied by retrieval accuracy multiplied by update speed. Storage alone has no value.

## Workflow

### Scenario A: Build a New Knowledge Base

1. Read `references/知识库元管理规范.en.md`, the complete `v0.2-candidate` specification.
2. Confirm the domain and carrier with the user. Do not pre-adapt by default. Start with the invariants and strategy defaults.
3. Create the minimum set: a logical structure, a root management specification containing local strategy overrides, and an adjudication area such as `inbox/`. Folder-based carriers default to at most three levels.
4. Names pass the name-only test: a reader can judge likely relevance without opening the object. Domain-specific terms appear literally, and the body includes a common synonym once.

### Scenario B: Domain Adaptation Triggered by Evidence

1. Confirm all four trigger conditions: the same class of problem fails repeatedly; the failure comes from a stable domain-method gap rather than missing material, permissions, or host capability; the gap cannot be derived from general rules; and the trigger point is explicit. Do not adapt if one condition is missing.
2. Add only the smallest rule that repairs the proven gap, and keep it decidable. Apply Chapter 3 and the strategy table in Chapter 2.
3. Calibrate retrieval with 20 to 50 real questions as the minimum. Freeze deployment only after readback checks and real-task reuse complete both acceptance levels.
4. Before revising the specification, read `references/知识库架构讨论纪要-2026-08-28.md`, available in Chinese, for the derivation and review history. Follow the asymmetric revision procedure in Chapter 4.

### Scenario C: Organize an Existing Knowledge Base

1. Read the management specification at the knowledge-base root before changing anything. Move uncovered cases into the adjudication area for human judgment. Do not invent rules.
2. Apply three lifecycle tests. The object must stand alone without unresolvable references, either by including necessary context or by using a stable readable relationship that does not create a duplicate source of truth. It must support independent reuse, update, and retirement. Stop splitting when another split removes independent value. Content that jointly proves one thing remains together.
3. Faithful compilation is allowed. Convert source containers into agent-readable semantic content while preserving meaningful table relationships. Do not change facts, numbers, meaning, subjects, limits, or commitments. Keep source references, read the result back through the knowledge entry point, and require human confirmation before irreversible source loss.
4. A length of 300 to 2,000 Chinese characters is a warning only. Review the object boundary outside that range, but do not force a split.
5. Work in batches. The default is at most ten objects, adjusted for object complexity and failure impact. Report each batch, stop on failure, and keep actions reversible.
6. Obsolete content leaves active retrieval and records the reason and replacement. The exit method follows platform capability and compliance. Folder-based carriers default to `graveyard/` plus an obsolete prefix. Do not delete irreversibly without platform policy and human confirmation.
7. Report technical write completion only after retrieval, actual readback, and structural completeness all pass. Record business reuse later as an independent state; it does not block write completion.

### Scenario D: Periodic Quality Review

1. Sample real queries and reuse records. Mark retrieval misses, wrong matches, readback failures, and reuse failures.
2. Repair the knowledge base by renaming, adding synonyms, splitting, merging, or retiring objects. When evidence requires a specification change, follow Chapter 4, increment the version, and archive the old one.

## Reject These Patterns

- An undecidable adjective appears without a test.
- The logical structure is organized by department, source, or file format.
- One object contains several independent lifecycle topics that do not jointly prove one thing.
- "Organization" changes facts, meaning, subjects, limits, or commitments.
- Obsolete content remains in active retrieval, or an object without a source and readable body counts as written.
- An unvalidated object is used as validated knowledge in cross-task decisions.
- A strategy is enforced as an invariant despite a justified carrier or domain difference.
- Content is stored but never reviewed through feedback.

## References

- `references/知识库元管理规范.en.md`: complete `v0.2-candidate` specification, including invariants, strategy layer, adaptation, revision procedure, and rejected patterns.
- `references/知识库架构讨论纪要-2026-08-28.md`: Chinese-only record of method derivation, ontology references, the `v0.1` to `v0.2` review, and `v0.2-candidate` corrections.
