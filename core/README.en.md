# Cross-Track Core Candidates

[中文](README.md) | English

## Current Status

This directory does not contain a final specification for every industry. It contains only minimal constraints supported by real tasks in at least two independent tracks and still open to counterexamples.

The first evidence comes from:

- [Media production: canonical article and channel derivative validation](../tracks/media-production/validations/article-derivation.en.md)
- [Software development: single-purpose service delivery validation](../tracks/software-development/validations/single-purpose-service-delivery.en.md)
- [Knowledge management: cross-task enterprise knowledge reuse validation](../tracks/knowledge-base/validations/enterprise-knowledge-reuse.en.md)

The media and software tasks formed the initial three candidates. The later knowledge-reuse task narrowed the current-execution-surface candidate and added evidence from a third independent track to the other two.

## Candidate 1: Unfinished, Direction-Sensitive Work Needs a Replaceable Current Execution Surface

When work is unfinished, its direction may still change, and it must continue across sessions or agents, the current execution surface stores only:

- what this effort is meant to change;
- accepted facts and decisions;
- the current boundary and explicit non-goals;
- the next executable action;
- the outcome or risk that should stop the work and return it to a person.

It supports the continuation of work in progress. It does not store full history or replace product facts, long-term methods, source material, or runtime records. When work finishes or changes direction, replace the current state instead of appending forever. Completed, stable knowledge, content, and deliverables are reused through their formal sources of truth and new task input rather than a permanent handoff.

**Supporting and narrowing evidence**: The media task used the current series, independent question, and stopping point to avoid switching to the wrong line of work. The development task used the goal, live boundaries, next action, and rollback conditions to hand off execution. The knowledge task reused completed stable knowledge without old chat, the source file, or a permanent current execution surface. That counterexample narrowed this candidate from all long-running work to unfinished, direction-sensitive work.

**Refutation condition**: Continue narrowing or remove this candidate if real unfinished, direction-sensitive work continues reliably without an independent current execution surface, or if maintaining one repeatedly creates goal drift and a second source of truth.

## Candidate 2: Each Fact Has One Authoritative Owner

Long-running work often contains source facts, formal deliverables, derived views, a current execution surface, temporary process state, and live external state at the same time. They may reference each other, but they must not maintain the same fact independently.

Resolve conflicts by role. Current observable reality overrides an old plan. A formal source of truth overrides its derivatives. Confirmed decisions override unconfirmed inference. Temporary control state cannot rewrite formal content.

**Supporting evidence**: The media task separated canonical copy, channel drafts, and platform state. The development task separated the plan, private configuration, handoff, and live system state, then changed the execution path when live evidence contradicted the plan. The knowledge task separated current project requirements, stable enterprise knowledge, provenance, and the discovery index, showing that explicit relationships do not require shared ownership of one fact.

**Refutation condition**: If a class of work requires several objects to co-own the same fact and transactions, events, or relationships cannot express that requirement, redefine "fact" and "owner" instead of forcing deduplication.

## Candidate 3: Completion Requires a Formal Entry Point and an Inspectable Result

Generated files, updated state, successful API calls, process exits, agent claims, and interface messages provide partial evidence. Completion requires at least:

1. execution through the formal entry point used by the real work;
2. a result the target user or responsible person can inspect and continue using;
3. verification that explicitly protected existing results still hold;
4. an honest record of unverified, failed, or waiting states;
5. current human authorization and domain responsibility for irreversible decisions.

Completion is relative to the declared intent. Technical storage completion and successful business reuse may both be valid terminal states, but the former cannot stand in for the latter.

**Supporting evidence**: The media task required complete canonical copy, usable channel assets, and explicit publishing authorization. The development task verified both the new public result and the continued operation of existing services. The knowledge task first separated the technical result of writable, readable components, then used a new independent task and an editable deliverable to prove business reuse.

**Refutation condition**: Some work, including open exploration and basic research, has no external entry point or independent outcome. Such work needs a truthful intermediate deliverable, not a fabricated final state imposed by this candidate.

## Not Promoted

- No universal object taxonomy, directory structure, field set, database, or lifecycle state machine.
- No requirement that every domain use the same handoff, article, or acceptance filename.
- No promotion of the media publishing gate into a universal approval gate for development work.
- No promotion of development debugging tools or test layers into media or knowledge management rules.
- No assumption that the final artifact is a CMS, knowledge base, project management tool, skill, or visual dashboard.

Each track continues to own its goals, risks, and carriers. A new track should try to refute these three candidates before using them to prove itself correct.
