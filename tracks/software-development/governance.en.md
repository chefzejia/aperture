# Agent-Assisted Development Governance

[中文](governance.md) | English

## Goal

Agents can perform much of the design, coding, testing, and debugging work. Development governance still protects four things: user intent does not drift, each system fact has one owner, local symptoms do not expand the design without control, and real delivery proves completion.

Governance does not control every reasoning step. It owns the goal, formal state, irreversible decisions, and acceptance responsibility.

## Start with the User Result

Write one user-inspectable outcome for every product or milestone:

```text
What a specific user provides
  -> what real work the system performs
  -> what result the user can continue using
```

Also state:

- which risks and decisions remain human responsibilities;
- what is explicitly out of scope;
- which evidence can prove that the outcome occurred.

Modules, pages, agent count, code volume, and task lists are not product outcomes. If the goal changes during implementation, update product facts and acceptance criteria before expanding the system.

## Separate Sources of Truth by Responsibility

A long-running project distinguishes at least these roles. Each project chooses the carriers:

- **Project constitution**: short, stable boundaries, prohibited areas, and authoritative reading order;
- **Product facts**: users, product goals, behavior boundaries, and success criteria;
- **Architecture facts**: durable technical boundaries, formal state, and ownership;
- **Current execution surface**: the current milestone, accepted baseline, next action, and stopping point;
- **Operating entry points**: build, installation, release, recovery, and real-environment procedures;
- **History**: evidence from completed, failed, or obsolete work.

Chats, logs, and old handoffs cannot become long-term truth. Each rule has one authoritative source. Other locations link to it instead of copying and drifting. External skills and personal habits become project constraints only when written into formal project documentation.

## Smallest Sufficient Correct Design

A correct design is neither the least code nor the largest abstraction. It has correct responsibility boundaries, manageable cost, and a path to real delivery at the current stage.

Before adding persistent state, fallbacks, compatibility layers, state machines, queues, background services, internal agents, protocols, or general abstractions, answer five questions:

1. Which observed user or maintenance problem does this solve?
2. Who becomes the only source of truth and the only writer?
3. Why can official capabilities, platform capabilities, or the existing structure not solve it?
4. What observable loss occurs if it is not implemented?
5. Which real acceptance test proves that it is necessary and correct?

"We may need it later," "more complete," "more engineered," and "another safety layer" do not pass the change gate. Reuse an official or existing correct path first. Govern only the parts the project needs to own.

## Formal State and Temporary Control State

User files, confirmed decisions, formal business data, and deliverables may become durable truth. Candidates, runtime logs, loading state, progress, caches, intermediate files, previews, and unconfirmed inference are temporary control state by default.

Temporary state cannot overwrite formal content or become a second business model because the interface needs to display it. If temporary state must persist, define its lifecycle, cleanup rule, only writer, and recovery semantics.

## Current Execution Surface

Use one replaceable current execution surface for medium and long tasks. Do not make chat carry project state. It stores only:

- one user outcome;
- the current milestone and non-goals;
- accepted and unaccepted parts;
- the next precise action and stopping point;
- acceptance evidence;
- the current code and commit boundary.

Archive it when the work finishes or becomes obsolete. Move durable rules back into the product or architecture source of truth before a new execution surface references them.

## Implementation and Review

Read authoritative documents and worktree state before implementation. Unknown changes belong to the user or another task by default. Every changed file must trace to the current user outcome. Do not clean unrelated modules along the way.

Review asks:

- Does the change still serve the original user result?
- Did it create a second source of truth or hide failure behind a fallback?
- Did it expose internal state as a product concept?
- Did it add an abstraction for an imagined future?
- Is there behavioral evidence that the old implementation failed and the new one passes?
- Did validation use the corresponding real runtime environment?

High-risk or cross-boundary changes need independent review or human acceptance. The implementer cannot establish completion by explanation alone.

## Signals to Stop Local Patching

Stop adding conditions and revisit the goal, source of truth, and responsibility boundary when any of these occur:

- the same user symptom returns after a fix;
- one defect needs several new persistent states to explain it;
- fallback or recovery logic enters the normal path;
- several modules maintain the same business fact;
- the fix keeps expanding without approaching the user's deliverable;
- tests prove implementation details but not the user result.

A correct refactor usually removes a wrong abstraction or merges ownership instead of adding more guards.

## Completion

Validation may start with static checks and narrow regression tests. Final acceptance must reach the formal product entry point, real environment, real data, and a user-inspectable deliverable. Mocks, fixtures, success messages, exit codes, and file existence provide partial evidence only.

Completion means the user receives the target result through the formal entry point, key risks remain visible, formal state is auditable, incomplete work is not presented as success, and the next engineer can continue without chat history.

## Excluded from the Public Method

- one product's architecture, state model, runtime commands, and release process;
- servers, ports, domains, network topology, and machine configuration;
- version preferences for frameworks, test tools, models, or agents;
- complete incident logs, customer data, and internal credentials;
- project-specific safety boundaries and rollback scripts.

Real projects continue to own these facts. This track carries only governance constraints that still hold across projects.
