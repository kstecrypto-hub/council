# Instructions for agents working in this repository

## Authority and current stage

This is an approved-design repository, not an implemented application. Read `docs/APP_DESIGN.md` in full before proposing or implementing changes. Read `docs/IMPLEMENTATION_HANDOFF.md` next. The latest explicit owner instruction is authoritative; supporting handoff notes do not silently override the complete design.

The initial authorization was to create a repository and publish the approved design. It was not an instruction to build the application. Do not start application implementation solely because this file exists. A later explicit implementation request authorizes work within its stated scope; do not then ask for redundant confirmation.

## Preserve these design commitments

- Peer investigators govern the council. Do not introduce a single lead/supervisor/judge with unilateral intellectual authority above it.
- Every member investigates, delegates, challenges, and revises. Members own investigations, not conclusions they must defend.
- The core is domain-agnostic and must support a complete non-coding investigation with no terminal tool.
- DeepSeek is the initial default, not a globally hard-wired provider. Support per-seat and per-worker model overrides, safe session migration, and provider-specific data permissions.
- The same-model council must be labeled honestly. A new session is not a new independent reviewer.
- Keep independent unpublished branches private across retrieval, graph queries, context packets, caches, and exports.
- Runtime events are authoritative for observed execution. Agent-submitted semantic relationships remain attributed, reviewable interpretations.
- Keep evidence support separate from council agreement. Preserve contrary evidence, minority positions, uncertainties, and source lineage.
- Treat assumptions as first-class records. Preserve joint premises and alternative supporting routes. Do not equate citations with proof, chronology with causation, or different documents with independent evidence.
- Keep claim revisions append-only. Upstream changes trigger reassessment, not automatic declarations that all dependent claims are false.
- Use durable records, bounded context packets, ordinary search, graph-assisted retrieval, checkpoints, and summaries together. Do not put the full graph into every prompt or promise unlimited/lossless context.
- Perform the six-month-plus premortem as a hypothetical review now. Do not invent future observations or silently schedule future runs.
- A final report assembler has editorial authority only. It may not erase unresolved objections or silently pick the winner of a factual dispute.
- Require scoped permissions for tools and provider changes. Keep credentials outside model prompts, browser state, generated code, and ordinary logs.
- Account for retries, failures, child agents, and parallel reservations in budgets. Preserve review allowance. Exhaustion yields a partial outcome, not forced consensus.

## Implementation discipline when implementation is authorized

Reuse established runtime and continuation mechanisms where appropriate. Karpathy's autoresearch and the Ralph pattern are conceptual references, not instructions to copy coding-specific scope, permission-bypass flags, scalar optimization objectives, or indefinite execution. Verify current upstream behavior and licensing before reuse.

Implement and test canonical records and backend authorization before relying on a graph visualization. Make the three graph questions in the README executable product behavior, not decorative UI.

Do not import the earlier single-lead starter as the baseline. Do not create a separate graph or memory system that can silently disagree with the investigation ledger. Avoid adding a dedicated graph database, vector database, Redis, or Kubernetes until demonstrated requirements justify it and the design change is recorded.

Use the approved build sequence and acceptance criteria. Test deterministic invariants separately from repeated model-dependent evaluations. Distinguish local unit results, simulated providers, live provider runs, sandbox runs, and deployment verification.

Do not report a feature as implemented, a test as passed, a repository as pushed, or a service as deployed without concrete evidence. Record unverified assumptions and blockers plainly.

## Repository hygiene

Do not commit secrets, environment files, private research inputs, generated runtime records, credentials, caches, or production exports. Use synthetic or explicitly authorized fixtures for tests. Do not add an open-source license on the owner's behalf without authorization.

Keep documentation aligned with implemented behavior and record substantive deviations. Avoid unrelated refactors and dependencies that turn the investigation product into a generic coding-agent shell.
