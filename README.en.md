# Agentic Work Infra

[中文](README.md) | English

## Project

This project studies one infrastructure problem created by the current automation wave:

> As agents perform more cognitive work, how should people, agents, and long-lived work assets be organized so that work can continue across sessions, tools, and teams, and improve through real outcomes?

The project is not about one model, Agent App, knowledge base product, or content management system. It studies the work foundation they all depend on. We currently call that foundation "agent-native work infrastructure," but later evidence may change the name.

## Why This Needs Its Own Project

Models and Agent Harnesses reduce the cost of completing complex tasks. Finishing one task does not make long-running work sustainable. Real work still suffers from drifting goals, lost context, conflicting sources of truth, unverified outcomes, and feedback that never changes the next run.

Media production, enterprise knowledge bases, bidding, finance, and product development look different. They may still share one work pattern: a person states an intent, an agent works from context, the person chooses a direction, reality tests the result, and the outcome changes future work.

This is a cross-domain hypothesis under test, not an established universal rule.

## Core Questions

The project starts with five questions:

1. **Intent**: Why does a long-running effort begin, and what change would make it valuable?
2. **Context**: Which information should an agent use, and which information is valid, uncertain, or obsolete?
3. **Source of truth**: Where do current decisions and deliverables live, and how do other objects relate to them?
4. **Result**: What proves that work produced an acceptable real outcome instead of another file?
5. **Accumulation**: How do delivery, use, and feedback change the next task and increase capability over time?

## Current Hypotheses

- Long-running work continuity matters more than isolated "content" objects.
- A knowledge base, a production workflow, a handoff, and a visual dashboard may be different views of one work system rather than a fixed hierarchy.
- The same physical object may play different roles in different tasks. File type alone cannot determine how it should be managed.
- Shared methods should contain only constraints that survive across domains. Directories, fields, platforms, and concrete workflows belong to domain strategies or carrier implementations.

All four statements are candidates. One reproducible counterexample caused by a rule is enough to narrow or remove it. Successful cases in several domains can increase confidence, but cannot turn experience into an unfalsifiable principle.

## Validation

The project works backward from real work instead of designing a general platform first:

1. Select independent real scenarios and record how work starts, proceeds, is accepted, and accumulates.
2. Find failures that repeat across scenarios, then determine whether they come from a shared work gap, domain knowledge, or tool capability.
3. Extract the smallest candidate model and actively search for counterexamples.
4. Separate cross-domain constraints from domain strategies, then return to real tasks for another test.
5. Let evidence decide whether the final artifact should be a method, protocol, skill, visual workbench, or a combination.

The first tracks are knowledge management, media production, and software development. Bidding and field delivery engineering contribute local cases to knowledge management and professional delivery. These are starting points, not proof of universal applicability.

## Project Layers

The public repository owns shared methods and public evidence. Real work remains in its original projects:

```text
Public method repository
|-- Cross-track core candidates
|-- Cross-domain validation protocol
|-- Knowledge management track
|-- Media production track
`-- Software development track

Local real projects
|-- Personal content and platform operations
|-- Enterprise knowledge bases and professional delivery
|-- Product code
`-- Development, operations, and machine environments
```

Public tracks define domain questions, candidate methods, and public-safe validation conclusions. This repository does not copy articles, customer material, product code, account state, infrastructure configuration, or raw logs. Local source mappings and unredacted temporary analysis stay in the ignored `.local/` directory. Original projects continue to own the source material.

The first media and software tasks formed three initial [cross-track core candidates](core/README.en.md). The later knowledge-reuse task narrowed the current execution surface to unfinished, direction-sensitive work and added evidence from a third independent track for one authoritative owner per fact and completion through a formal entry point plus an inspectable result. These candidates remain open to refutation and further narrowing. They are not a universal directory structure, data model, or product specification.

A constraint may enter `core/` only after real tasks in at least two independent tracks support it. One reproducible counterexample caused by the candidate is enough to narrow or remove it.

## Expected Outputs

The project currently aims to produce three inspectable artifacts:

1. **A long-running work continuity specification** covering intent, context, sources of truth, results, and feedback across tasks.
2. **A cross-domain validation protocol** for supporting, refuting, or narrowing candidate methods through real work.
3. **Domain methods** for knowledge management, media production, software development, and other tracks when evidence supports them.

Skills, protocol implementations, and visual workbenches may follow. They are not prerequisites for the current research.

## Out of Scope

- Renaming a traditional CMS, knowledge base, or project management tool as agent infrastructure.
- Choosing the final product form or building a visual dashboard before the method holds.
- Promoting one repository's directories, filenames, publishing process, or business terms into universal rules.
- Creating empty templates, status dashboards, roadmaps, or object taxonomies for the sake of completeness.

## Documents

- [AGENTS.md](AGENTS.en.md): long-lived project boundaries, reading order, and research discipline.
- [Current research handoff](docs/handoffs/current.en.md): the sole source for the current question, accepted baseline, and next action.
- [Cross-track core candidates](core/README.en.md): minimal constraints supported by at least two independent tracks and still open to counterexamples.
- [Cross-domain validation protocol](docs/validation-protocol.en.md): how local projects provide evidence and how conclusions enter the public repository.
- [Knowledge management track](tracks/knowledge-base/README.en.md): candidate knowledge management methods and their executable skill.
- [Media production track](tracks/media-production/README.en.md): boundaries, candidate structure, and validation questions for media production.
- [Software development track](tracks/software-development/README.en.md): boundaries, candidate structure, and validation questions for software development.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
