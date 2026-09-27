# Implementation handoff

## Status and authority

This is a handoff for a later explicitly authorized implementation. The current delivery is a documentation repository, not an application. The owner approved the design and requested that it be placed in a new repository.

Read [the complete design](APP_DESIGN.md) first and [AGENTS.md](../AGENTS.md) second. The complete design remains authoritative over this operational summary. Later owner instructions may change the scope; record such changes rather than silently interpreting this handoff as permission for unrelated work.

The older single-lead swarm starter is not a valid implementation baseline. Do not import its fixed managerial structure, coding-first assumptions, dashboard, or runtime as if they implement the approved council.

## Product outcome

Build accountable parallel investigations, not an agent chatroom. The three defining graph capabilities are:

1. Trace conclusions depending on a specific source or assumption, including alternative supporting routes and affected report sections.
2. Explain claim narrowing using actual claim versions, a recorded challenge, relevant evidence, and the revision decision.
3. Trace apparently independent findings to shared original evidence, retaining unresolved provenance rather than guessing independence.

Use ordinary searchable records, evidence, checkpoints, and short handovers alongside the graph. Do not imply that a graph removes finite context windows.

## Ordered milestones

### A. Foundation

Establish canonical versioned records, scope/authorization checks, immutable source versions, observable execution events, and typed graph relationships. Keep assumptions, grouped premises, and alternative support paths explicit.

Implement the PostgreSQL-backed task queue with leases and reconciliation. Add provider adapters and a configurable capability registry. Use synthetic/prepared evidence before connecting live sources.

Exit condition: the three graph questions work against deterministic fixtures; authorization also applies to traversal, source snippets, search, context assembly, and exports. Recorded tool failure cannot be mistaken for a successful check.

### B. Working council

Implement equal council seats, independent private investigation branches, explicit publication, dynamically commissioned workers, targeted cross-examination, revisions, coverage records, and bounded minority investigation.

Implement budget reservations, branch limits, delegation limits, progress checks, and a protected review allowance. Scheduling must release capacity while parents wait for workers.

Implement host-aware executable scheduling separately from logical council membership. Build an approved environment-capability profile and per-task environment manifest, then construct the smallest sandbox that reproduces the task-relevant host behavior. Do not mirror the user's whole machine. Exclude unrelated files, credentials, browser state, caches, applications, and projects by default. Record sandbox fidelity as exact, compatible/emulated, or unavailable, and require an explicitly approved alternate backend or a recorded limitation when Docker cannot reproduce a required host property.

Allow more logical agents than concurrently executable sandboxes. Queue local builds/tests/tools according to CPU, memory, disk, GPU/device, and sandbox limits instead of oversubscribing the user's computer. Persist only explicit outputs such as commits, artifacts, test/evaluation records, and evidence; disposable sandbox residue is not project memory.

Exit condition: a non-coding investigation completes without a terminal, valid minority objections survive, and administrative voting cannot promote evidential status. More logical agents than local execution slots can make progress safely, and a host-specific task cannot be reported as verified from an incompatible sandbox.

### C. Continuity and review

Implement persistent logical agents with versioned sessions, bounded context packets, graph-assisted retrieval plus ordinary search, safe checkpoints, and pending-operation reconciliation.

Add provisional synthesis, independent six-month-plus premortem, reopened checks, final review dispositions, and versioned reports with editorial-only assembly authority.

Exit condition: forced rollovers preserve old objections and current claim versions; missing graph edges can be overcome through underlying search; a premortem scenario never becomes an observation.

### D. Interface and hardening

Build the views defined in section 11, including per-agent model dropdowns, context/session inspection, graph filtering, bounded expansion, edge provenance, original evidence viewer, and accessible table alternatives.

Add safe model migration, provider-specific data permissions, usage inspection, recovery, export, retention, and backup restoration checks.

Exit condition: the UI exposes recorded facts rather than an invented activity narrative. Exported claims remain traceable to permitted retained evidence. Interrupted workers and reconnecting clients reconcile state correctly.

### E. External evidence integrations

Connect authorized sources and a RAG adapter through the same evidence and capability contracts. Retrieval returns source-level evidence, context, scope, and limitations, not an unquestionable generated answer.

Exit condition: branches can perform independent searches, inspect original material, and seek counterevidence without granting source text instruction authority or expanding permissions.

## Verification expectations

Section 17 of the complete design is the acceptance suite, not a claim that tests already exist or pass. Add deterministic tests for runtime invariants and repeated evaluations for model-dependent behavior.

Separate test-provider runs from live DeepSeek requests. Separate local script execution from actual sandbox integration. Report which verification was performed and which was unavailable.

Compare graph-assisted continuation with a strong searchable-record baseline containing the same underlying information. Compare council performance with a capable single-agent baseline before claiming improvement.

## Implementation-time decisions that remain open

The design specifies behavior without pretending every parameter is settled. Resolve and document the exact model identifiers and capability checks, version pins, budget amounts and review-reserve allocation, context sizing and retrieval ranking, evidence-policy profiles, source adapters, secret-store implementation, and deployment configuration when work starts.

These open choices do not authorize replacing the peer council with a supervisor, removing provenance, or broadening the product into an unrestricted coding/deployment agent.

## Reporting a completed implementation step

Describe the behavior delivered, affected records and boundaries, tests actually executed, known limitations, and next unfinished milestone. Do not equate more messages or graph nodes with a better investigation. Do not label proposed work as implemented.
