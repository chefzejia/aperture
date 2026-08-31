# Cross-Track Core Candidates

[中文](README.md) | English

## Current Status

This directory does not contain a final specification for every industry. It contains only minimal constraints supported by real tasks in at least two independent tracks and still open to counterexamples.

The first evidence comes from:

- [Media production: canonical article and channel derivative validation](../tracks/media-production/validations/article-derivation.en.md)
- [Software development: single-purpose service delivery validation](../tracks/software-development/validations/single-purpose-service-delivery.en.md)

The knowledge management track already has a domain candidate method. It does not add support to the core in this round because it has not produced an independent validation record under the shared protocol.

## Candidate 1: The Current Execution Surface Must Be Replaceable

The current execution surface for long-running work stores only:

- what this effort is meant to change;
- accepted facts and decisions;
- the current boundary and explicit non-goals;
- the next executable action;
- the outcome or risk that should stop the work and return it to a person.

It allows work to continue across sessions and agents. It does not store full history or replace product facts, long-term methods, source material, or runtime records. When work finishes or changes direction, replace the current state instead of appending forever.

**Supporting evidence**: The media task used the current series, independent question, and stopping point to avoid switching to the wrong line of work. The development task used the goal, live boundaries, next action, and rollback conditions to hand off execution.

**Refutation condition**: Narrow this candidate if a real long-running task continues reliably without an independent current execution surface, or if maintaining one repeatedly creates goal drift and a second source of truth.

## Candidate 2: Each Fact Has One Authoritative Owner

Long-running work often contains source facts, formal deliverables, derived views, a current execution surface, temporary process state, and live external state at the same time. They may reference each other, but they must not maintain the same fact independently.

Resolve conflicts by role. Current observable reality overrides an old plan. A formal source of truth overrides its derivatives. Confirmed decisions override unconfirmed inference. Temporary control state cannot rewrite formal content.

**Supporting evidence**: The media task separated canonical copy, channel drafts, and platform state. The development task separated the plan, private configuration, handoff, and live system state, then changed the execution path when live evidence contradicted the plan.

**Refutation condition**: If a class of work requires several objects to co-own the same fact and transactions, events, or relationships cannot express that requirement, redefine "fact" and "owner" instead of forcing deduplication.

## Candidate 3: Completion Requires a Formal Entry Point and an Inspectable Result

Generated files, updated state, successful API calls, process exits, agent claims, and interface messages provide partial evidence. Completion requires at least:

1. execution through the formal entry point used by the real work;
2. a result the target user or responsible person can inspect and continue using;
3. verification that explicitly protected existing results still hold;
4. an honest record of unverified, failed, or waiting states;
5. current human authorization and domain responsibility for irreversible decisions.

**Supporting evidence**: The media task required complete canonical copy, usable channel assets, and explicit publishing authorization. The development task verified both the new public result and the continued operation of existing services.

**Refutation condition**: Some work, including open exploration and basic research, has no external entry point or independent outcome. Such work needs a truthful intermediate deliverable, not a fabricated final state imposed by this candidate.

## Not Promoted

- No universal object taxonomy, directory structure, field set, database, or lifecycle state machine.
- No requirement that every domain use the same handoff, article, or acceptance filename.
- No promotion of the media publishing gate into a universal approval gate for development work.
- No promotion of development debugging tools or test layers into media or knowledge management rules.
- No assumption that the final artifact is a CMS, knowledge base, project management tool, skill, or visual dashboard.

Each track continues to own its goals, risks, and carriers. A new track should try to refute these three candidates before using them to prove itself correct.
