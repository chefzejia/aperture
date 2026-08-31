# Software Development Track

[中文](README.md) | English

## Track Question

As agents take on more design, coding, testing, and debugging work, how can a project preserve user intent, sources of truth, responsibility boundaries, and real delivery while avoiding local patches, false completion, and drifting project state?

This track studies cross-project development governance and real acceptance. It does not store product architecture, server assets, network configuration, deployment credentials, machine environments, or project runtime state.

## Local Validation Field

The personal development and operations repository continues to own its development governance, debugging specification, infrastructure material, and operational records. Product repositories continue to own their product facts, architecture, handoffs, code, and tests. The public repository extracts only cross-project methods and redacted validation conclusions.

## Observed Candidate Structure

- Start with one user-inspectable result. Modules, pages, and lines of code cannot replace the goal.
- Project constitution, product facts, architecture sources of truth, current handoff, operating methods, and history have different responsibilities. Chat is not a durable source of truth.
- Design for the smallest sufficient correct system, not the smallest patch to a wrong direction. New state, fallbacks, protocols, and abstractions need evidence from a real problem and real acceptance.
- Separate formal business state from temporary control state. Each fact has one authoritative owner.
- Debugging needs three independent evidence surfaces: action, observation, and judgment. Success messages, exit codes, and file existence do not prove business completion on their own.
- A fix restores the correct responsibility boundary and leaves regression evidence. When the same symptom returns, stop adding patches and revisit the goal, sources of truth, and architecture.
- Formal entry points, real environments, real data, and a deliverable the user can continue using prove completion.

These judgments currently belong to the software development track. Server inventories, network topology, commands, tool versions, and product-specific processes will not enter the public method.

## Current Methods and Evidence

- [Agent-Assisted Development Governance](governance.en.md): manages development from the user result, sources of truth, design change gate, and milestone handoff.
- [Debugging and Real Delivery](debugging-and-delivery.en.md): uses action, observation, and judgment as independent evidence surfaces to locate root causes and prove business completion.
- [Single-Purpose Service Delivery Validation](validations/single-purpose-service-delivery.en.md): tests continuation, source-of-truth selection, results, and feedback against a completed real task that shared an existing runtime environment.

This track migrates only cross-project methods and redacted conclusions. Product architecture, code, servers, network configuration, operational commands, and machine state remain in their original projects.

## Questions to Validate

- Can a new agent recover the user result, project sources of truth, and current stopping point without old chats?
- Which boundaries between strong-model exploration and durable project constraints improve reliability, and which become restraints?
- How can real end-to-end tests, regression tests, and human judgment prove delivery without building a second test business?
- Can development principles for sources of truth, feedback, and responsibility explain similar failures in knowledge management or media production?
