# Instructions for agents working in this repository

## Authority and current stage

This is an approved-design repository, not an implemented application. Read `docs/APP_DESIGN.md` in full before proposing or implementing changes. Read `docs/IMPLEMENTATION_HANDOFF.md` next. The latest explicit owner instruction is authoritative; supporting handoff notes do not silently override the complete design.

The initial authorization was to create a repository and publish the approved design. It was not an instruction to build the application. Do not start application implementation solely because this file exists. A later explicit implementation request authorizes work within its stated scope; do not then ask for redundant confirmation.

## Preserve these design commitments

- Peer investigators govern the council. Do not introduce a single lead/supervisor/judge with unilateral intellectual authority above it.
- The Project Orchestrator may own user-intent clarification, Project Contract versioning, neutral prompt generation, checkpoint scheduling, and clarification brokerage, but it must not become an intellectual supervisor, solution designer, winner selector, or hidden judge.
- The user does not communicate directly with individual council members or workers. User clarifications and scope changes go through the Project Orchestrator and become canonical versioned Project Contract revisions distributed consistently to affected branches.
- Every member investigates, delegates, challenges, and revises. Members own investigations, not conclusions they must defend.
- The core is domain-agnostic and must support a complete non-coding investigation with no terminal tool.
- DeepSeek is the initial default, not a globally hard-wired provider. Support per-seat and per-worker model overrides, safe session migration, and provider-specific data permissions.
- The same-model council must be labeled honestly. A new session is not a new independent reviewer.
- Keep independent unpublished branches private across retrieval, graph queries, context packets, caches, and exports. Communication occurs only through the versioned checkpoint policy or an approved adaptive checkpoint, with explicit publication scope.
- Runtime events are authoritative for observed execution. Agent-submitted semantic relationships remain attributed, reviewable interpretations.
- Keep evidence support separate from council agreement. Preserve contrary evidence, minority positions, uncertainties, and source lineage.
- Treat assumptions as first-class records. Preserve joint premises and alternative supporting routes. Do not equate citations with proof, chronology with causation, or different documents with independent evidence.
- Keep claim revisions append-only. Upstream changes trigger reassessment, not automatic declarations that all dependent claims are false.
- Use durable records, bounded context packets, ordinary search, graph-assisted retrieval, checkpoints, and summaries together. Do not put the full graph into every prompt or promise unlimited/lossless context.
- Perform the six-month-plus premortem as a hypothetical review now. Do not invent future observations or silently schedule future runs.
- A final report assembler has editorial authority only. It may not erase unresolved objections or silently pick the winner of a factual dispute.
- Require scoped permissions for tools and provider changes. Keep credentials outside model prompts, browser state, generated code, and ordinary logs.
- Account for retries, failures, child agents, and parallel reservations in budgets. Preserve review allowance. Exhaustion yields a partial outcome, not forced consensus.
- For executable projects, default to Council-managed isolated project environments rather than host replication. Agents may evolve their authorized candidate environment, but all durable environment changes must be captured reproducibly and pass a clean rebuild. Host matching is opt-in.
- In Match My PC mode, treat the approved Environment Contract as the boundary. Do not collect unrelated host data, infer permission from mere device/software presence, or silently upgrade compatible/bridged behavior to exact verification.
- Never give an agent or ordinary Council process unrestricted administrator, Docker-daemon, or kernel access. Elevated host operations go through the typed local privileged broker and only within approved capability scope.
- Match My PC does not authorize modifying the real host. Host software/configuration/driver/service changes require separate explicit permission and must be auditable and cleaned up or rolled back where practical.
- Treat the accepted reproducible project environment as part of the deliverable. Do not leave Council agents, provider credentials, agent GitHub credentials, hidden Council control mechanisms, or orchestration-only tooling in the user's final runtime.

## Implementation discipline when implementation is authorized

Reuse established runtime and continuation mechanisms where appropriate. Karpathy's autoresearch and the Ralph pattern are conceptual references, not instructions to copy coding-specific scope, permission-bypass flags, scalar optimization objectives, or indefinite execution. Verify current upstream behavior and licensing before reuse.

Implement and test canonical records and backend authorization before relying on a graph visualization. Make the three graph questions in the README executable product behavior, not decorative UI.

Do not import the earlier single-lead starter as the baseline. Do not create a separate graph or memory system that can silently disagree with the investigation ledger. Avoid adding a dedicated graph database, vector database, Redis, or Kubernetes until demonstrated requirements justify it and the design change is recorded.

Use the approved build sequence and acceptance criteria. Test deterministic invariants separately from repeated model-dependent evaluations. Distinguish local unit results, simulated providers, live provider runs, sandbox runs, and deployment verification.

Do not report a feature as implemented, a test as passed, a repository as pushed, or a service as deployed without concrete evidence. Record unverified assumptions and blockers plainly.

## Repository hygiene

Do not commit secrets, environment files, private research inputs, generated runtime records, credentials, caches, or production exports. Use synthetic or explicitly authorized fixtures for tests. Do not add an open-source license on the owner's behalf without authorization.

Keep documentation aligned with implemented behavior and record substantive deviations. Avoid unrelated refactors and dependencies that turn the investigation product into a generic coding-agent shell.
