# Instructions for agents working in this repository

## Authority and current stage

This is an approved-design repository, not an implemented application. Read `docs/APP_DESIGN.md` in full before proposing or implementing changes. Then read `docs/POSTGRES_DATA_MODEL.md` and `docs/TYPED_INTERACTION_CONTRACTS.md`; read `docs/IMPLEMENTATION_HANDOFF.md` next. The latest explicit owner instruction is authoritative; supporting handoff notes do not silently override the complete design.

The initial authorization was to create a repository and publish the approved design. It was not an instruction to build the application. Do not start application implementation solely because this file exists. A later explicit implementation request authorizes work within its stated scope; do not then ask for redundant confirmation.

## Preserve these design commitments

- Peer investigators govern the council. Do not introduce a single lead/supervisor/judge with unilateral intellectual authority above it.
- The Project Orchestrator is deliberately narrow: it owns canonical prompt generation, small prompt/clarification memory, transformation of raw user replies into stable agent-ready instructions, and a versioned **project-specific semantic phase/checkpoint plan** presented for user approval. It does not intellectually judge milestone quality, become a solution designer, winner selector, hidden judge, or unilaterally govern peer-review/publication protocol. Each Council member declares its own CHECKPOINT_READY.
- Council members and workers may originate questions to the user. The raw user reply must never flow directly back to the requesting agent: it passes through the Project Orchestrator, which may improve form but not substance, then returns a processed answer. Local clarifications remain local where appropriate; project-wide requirement changes propagate consistently to affected branches.
- Every member investigates, delegates, challenges, and revises. Members own investigations, not conclusions they must defend.
- The core is domain-agnostic and must support a complete non-coding investigation with no terminal tool.
- DeepSeek is the initial default, not a globally hard-wired provider. Support per-seat and per-worker model overrides, safe session migration, and provider-specific data permissions.
- The same-model council must be labeled honestly. A new session is not a new independent reviewer.
- Keep independent unpublished branches private across retrieval, graph queries, context packets, caches, and exports. Communication occurs only through the versioned checkpoint policy or an approved adaptive checkpoint, with explicit publication scope.
- Runtime events are authoritative for observed execution. Agent-submitted semantic relationships remain attributed, reviewable interpretations.
- Preserve the Part 4 action-linked state invariant: no externally meaningful state/activity may be implemented as a label only. Follow the registered trigger -> behavior -> interaction/UI -> command -> event -> transition/recovery contract. Durable interaction requests, not activity labels, cause blocking user decision surfaces.
- Keep evidence support separate from council agreement. Preserve contrary evidence, minority positions, uncertainties, and source lineage.
- Treat assumptions as first-class records. Preserve joint premises and alternative supporting routes. Do not equate citations with proof, chronology with causation, or different documents with independent evidence.
- Keep claim revisions append-only. Upstream changes trigger reassessment, not automatic declarations that all dependent claims are false.
- Use durable records, bounded context packets, ordinary search, graph-assisted retrieval, checkpoints, and summaries together. Do not put the full graph into every prompt or promise unlimited/lossless context.
- Perform the six-month-plus premortem as a hypothetical review now. Do not invent future observations or silently schedule future runs.
- A final report assembler has editorial authority only. It may not erase unresolved objections or silently pick the winner of a factual dispute.
- Require scoped permissions for tools and provider changes. Keep credentials outside model prompts, browser state, generated code, and ordinary logs.
- Account for retries, failures, child agents, and parallel reservations in budgets. Preserve the user's approved per-phase token/cost ceilings and protected checkpoint/review/finalization allowance. Exhaustion leaves the member BUDGET_EXHAUSTED / INCOMPLETE, never CHECKPOINT_READY, /done, or forced consensus. Propose, but never impose without approval, the configurable 70/25/5 budget split; use nonbinding uncertain token forecasts only for planning.
- Step 7 schedules whole member environments in fixed 1->5 seat order when capacity frees; do not impose mandatory periodic private-work slices, fixed reasoning-call counts, or general reasoning deadlines. Individual provider/tool operations still require safety timeouts. Default remote concurrency starts at two per provider (subject to stricter actual limits), local inference at one until verified safe; use resource-vector admission and preserve host headroom.
- Bring Your Own API Key or compatible local inference is the MVP; provider bills the user directly and Council owns no prepaid token wallet. Provider secrets remain outside all agent-controlled sandboxes and are reachable only through authorized, revocable runtime bridges. Council budget limits govern its own dispatch, not final provider invoices.
- For executable projects, execution isolation is transparent to the agent. The agent acts as though it owns a normal machine and controls everything visible inside its environment, including destructive changes. The runtime owns only the invisible isolation/lifecycle boundary and must prevent escape, cross-branch access, protected credential access, or direct canonical-state mutation. Host matching is opt-in.
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

## October 13, 2026 architecture amendment

Read docs/ARCHITECTURE_DECISIONS.md and docs/architecture_contract.json alongside the amended specifications. The owner's public-checkpoint policy applies to generated member repositories, not this source repository. Preserve five fixed members, sealed independent reviews, externally isolated peer verification, **member-declared semantic milestones with user-approved phase token/cost ceilings (no mandatory periodic private-work slices)**, conservative reservation accounting, commit-safe event replay, and separate communication/verification/acceptance records.

A documentation edit can be SPECIFIED without being IMPLEMENTED or VERIFIED. Do not close a runtime step from prose, a generated schema, static checks, mocks, or a successful push. Implementation completion requires code and scoped evidence; verification requires executed tests with recorded environment and results. Existing accepted design sections do not imply that later amendments or application work are complete. No application implementation is authorized merely by this maintenance update.


## October 14, 2026 design-stage closure of Steps 3–5

Steps 3, 4 and 5 have completed **design specifications** (see the October 14 closure sections of docs/POSTGRES_DATA_MODEL.md, docs/TYPED_INTERACTION_CONTRACTS.md and docs/PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md). The Council application, database migrations, provider/host interactions, runtime tests and evaluation results remain NOT STARTED / NOT RUN.

- One project-lifetime isolated PostgreSQL per trusted Council deployment; exactly five logical member seats; branch-private/source-linked context; separate immutable user approvals; full GitHub internet-public publication manifest and observed visibility transitions; all-five sealed reviews, atomic reveal, communication obligations and version-bound DONE; Git evidence validation before teardown.
- Typed command schemas and actor permissions are authoritative. **Authenticate and authorize, then deduplicate a same-key/same-hash command before applying new-command stale-state/transition guards.** An identical successful approval replay must not launch a second run or be rejected solely because the first changed the target version.
- Lock deployment event-clock first and use deterministic aggregate/budget order. Commit canonical state, external-operation intent, event, outbox and result atomically; dispatch GitHub/provider/Docker effects only after commit. Reconcile unknown effects; never infer a successful public/private transition, cancellation, refunded usage, or final archive from a requested action.
- The runtime does not intellectually judge CHECKPOINT_READY, turn BUDGET_EXHAUSTED into completion, reveal sealed reviewer text early, or erase disagreements. State/UI labels do not constitute real authorization or passing tests.

Implementation completion requires code references and actual test evidence. A documentation update alone may only say DESIGNED.
