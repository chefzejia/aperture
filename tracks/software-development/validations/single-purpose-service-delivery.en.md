# Single-Purpose Service Delivery Validation

[中文](single-purpose-service-delivery.md) | English

## Validation Target

A completed development and operations task added a single-purpose static service to existing shared infrastructure. It had to satisfy an external review requirement for public access and screenshots without affecting the existing network service or main product.

The development and operations project continues to own the real domains, servers, configuration, commands, and business identity. This record stores only the redacted work structure and validation conclusions.

## Actual Path

1. The user result was limited to "the reviewer can access and inspect the required information over the public internet," not a main-product redesign.
2. The handoff listed reusable assets, non-goals, protected services, human decisions, and acceptance entry points.
3. The design reused the existing static service and entry layer without adding a database, backend application, or second production system.
4. Execution read private configuration and live state first. The public plan did not copy credentials or login details.
5. The expected hot-reload path was unavailable at runtime. Live evidence overrode the documented assumption, so a reversible service restart loaded the change.
6. Acceptance checked public reachability, certificate success, complete page fields, and continued operation of the existing service and main product.
7. Live differences and final verification were written back into operating documentation so that the next person could continue without chat history.

## Five Tests

### Continuation Test: Pass

The handoff provides one outcome, scope, non-goals, authoritative material, risks, acceptance entry points, rollback, and decisions that require a person. A new agent can continue or review without old chats.

### Source-of-Truth Test: Pass

The plan owns the goal and boundary. Private configuration owns access facts. The live system owns runtime state. The handoff owns the current action. When live state differs from expectation, actual service state wins. The implementation does not force the old plan to preserve the document's appearance of correctness.

### Result Test: Pass

Configuration-file existence and command success do not prove completion. The new service was reachable through its public entry point, its certificate and page met the requirement, and two existing entry points remained healthy. The evidence covers both the new result and the prohibited regression.

### Feedback Test: Pass

The loading failure was neither hidden nor retried without limit. The failure was traced to the service's current control path, the execution path changed, and the difference and final behavior entered the operating documentation.

### Transfer Test: Partial Pass

User results, non-goals, live-state priority, formal-entry acceptance, and rollback boundaries transfer to other development tasks. The static service, certificate tooling, shared server, and external review fields are case-specific implementations and remain in the real project.

## Rule Disposition

### Enter Cross-Track Candidates

- The current execution surface stores the goal, accepted baseline, next action, and stopping point instead of full chat history.
- Documents, derived views, and live state play different roles. Current observable facts override old plans.
- Completion requires a formal entry point and a human-inspectable result, including verification of existing results that the task must not break.

### Remain in the Software Development Track

- New state, services, and abstractions pass a change gate based on an observed user problem, one owner, and real acceptance.
- Debugging needs three independent evidence surfaces: action, observation, and judgment.
- When a symptom returns or patches create more state, revisit the architectural responsibility boundary instead of adding conditions.

### Continue Observation

- The smallest boundary between strong-model exploration and stable project constraints.
- Which development tasks need an independent reviewer, and which can be accepted through several evidence surfaces used by one agent.
