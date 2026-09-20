# Council - code-level implementation plan

**Status:** owner-approved implementation proposal, recorded for component-by-component design review. This is documentation, not an implemented application.  
**Recorded:** September 10, 2026.  
**Branch:** `design/code-level-implementation`, created from `main` at `8f86db522b377f10eab79a2e75b11dc97ada7b86`.  
**Authority:** this document preserves the 15-section code-level proposal approved in the project conversation. [APP_DESIGN.md](APP_DESIGN.md) remains the complete product specification; [IMPLEMENTATION_HANDOFF.md](IMPLEMENTATION_HANDOFF.md) defines the existing milestones; [AGENTS.md](../AGENTS.md) preserves repository requirements. Later explicit owner instructions take precedence.  
**Scope of this publication:** record the approved proposal on a separate branch and begin reviewing its parts. Do not interpret this publication as a request to implement the entire application.  
**Verification boundary:** snippets below are design examples, not a runnable or tested implementation. No application tests, live provider requests, database migrations, or deployment are claimed to have run. External links are design references, not dependency pins or a guarantee of future API compatibility.

## Guiding engineering principle

Models propose actions and interpretations. Application services validate and apply them. PostgreSQL records what actually happened.

That is how we prevent the application from becoming several prompts loosely connected to a database. This structure follows the committed design and milestones. It does not introduce a supervisor above the council or make coding the agents' default activity.

## Contents

1. [Application structure](#1-application-structure-one-codebase-separate-execution-processes)
2. [Repository layout](#2-repository-layout)
3. [Database implementation](#3-database-implementation)
4. [Typed agent commands](#4-typed-agent-commands)
5. [Command application and transactions](#5-how-one-command-becomes-a-committed-change)
6. [The three defining graph queries](#6-the-graph-how-we-implement-the-three-defining-questions)
7. [Worker scheduling and recovery](#7-worker-scheduling-and-recovery)
8. [The actual agent loop](#8-the-actual-agent-loop)
9. [Model adapters and dropdowns](#9-model-adapters-and-the-dropdowns)
10. [Tools and evidence access](#10-tools-and-evidence-access)
11. [Context construction and rollover](#11-context-construction-and-rollover)
12. [API and frontend](#12-api-and-frontend-implementation)
13. [Review and reporting](#13-review-and-reporting-in-code)
14. [Testing](#14-testing-build-evidence-of-correctness-alongside-the-code)
15. [Implementation sequence](#15-the-actual-implementation-sequence)

## 1. Application structure: one codebase, separate execution processes

Build a modular monolith: one backend codebase with clearly separated modules, rather than a collection of microservices.

Initially, run:

| Process | What it does |
|---|---|
| API server | Handles the UI, authentication, commands, queries, and live updates. |
| Worker process | Executes agent sessions, tool operations, and investigation jobs. |
| Maintenance process | Recovers expired jobs, reconciles uncertain operations, and updates secondary indexes. |
| PostgreSQL | Stores application records, graph relationships, jobs, and checkpoints. |

The same backend package supplies all three application processes. They do not each need their own repository.

Large artifacts - source documents, retained tool outputs, analysis files - live in versioned file storage. PostgreSQL stores their metadata and references.

The API must not execute a complete investigation inside an HTTP request. Starting a run creates durable work and returns its identifier. Workers continue independently of whether the browser remains open.

Do not use FastAPI's ordinary `BackgroundTasks` as the durable investigation engine. Its documentation distinguishes small in-process background tasks from work that should execute through separate processes and queues. Reference: [FastAPI background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).

## 2. Repository layout

Part 2 makes the application/agent/environment boundaries explicit and mechanically enforceable.

```text
council/
|-- AGENTS.md
|-- docs/
|   |-- APP_DESIGN.md
|   |-- IMPLEMENTATION_HANDOFF.md
|   |-- CODE_IMPLEMENTATION_PLAN.md
|   |-- COMPONENT_REVIEW_PLAN.md
|   `-- REFERENCES.md
|
|-- backend/
|   |-- pyproject.toml
|   |-- uv.lock
|   |-- migrations/
|   |-- src/council/
|   |   |-- domain/
|   |   |   |-- entities/
|   |   |   |-- value_objects/
|   |   |   |-- commands.py
|   |   |   |-- events.py
|   |   |   |-- enums.py
|   |   |   |-- contracts.py
|   |   |   `-- errors.py
|   |   |
|   |   |-- application/
|   |   |   |-- runs/
|   |   |   |-- tasks/
|   |   |   |-- claims/
|   |   |   |-- evidence/
|   |   |   |-- publications/
|   |   |   |-- challenges/
|   |   |   |-- reviews/
|   |   |   |-- budgets/
|   |   |   `-- ports/
|   |   |
|   |   |-- agents/
|   |   |   |-- runtime/
|   |   |   |-- graph/
|   |   |   |   |-- projection/
|   |   |   |   `-- queries/
|   |   |   |-- context/
|   |   |   |-- providers/
|   |   |   |-- tools/
|   |   |   `-- prompts/
|   |   |
|   |   |-- environments/
|   |   |   |-- contracts.py
|   |   |   |-- discovery.py
|   |   |   |-- fidelity.py
|   |   |   |-- branches.py
|   |   |   |-- candidates.py
|   |   |   |-- promotion.py
|   |   |   `-- adapters/
|   |   |
|   |   |-- persistence/
|   |   |   |-- postgres/
|   |   |   |-- repositories/
|   |   |   |-- unit_of_work.py
|   |   |   `-- artifacts/
|   |   |
|   |   |-- security/
|   |   |   |-- authorization.py
|   |   |   |-- identity.py
|   |   |   `-- secrets.py
|   |   |
|   |   `-- api/
|   |       |-- app.py
|   |       |-- dependencies.py
|   |       |-- routes/
|   |       `-- sse/
|   |
|   `-- tests/
|       |-- unit/
|       |-- integration/
|       |-- contracts/
|       |-- architecture/
|       |-- evaluations/
|       `-- fixtures/
|
|-- frontend/
|   |-- package.json
|   `-- src/
|       |-- app/
|       |-- features/
|       |-- components/
|       `-- lib/
|
`-- infra/
    `-- compose.yaml
```

These are responsibility boundaries, not a requirement to create empty files up front.

### Core dependency rule

The dependency direction is inward:

```text
domain
  ^
application
  ^
api / agents / environment orchestration
  ^
infrastructure adapters
```

More precisely:

- `domain/` owns Council concepts and invariants and imports no framework, provider, database, HTTP, Docker, VM, or environment-specific implementation.
- `application/` owns valid Council use cases and state transitions. It depends on domain concepts and abstract ports, not concrete infrastructure.
- `agents/` owns reasoning machinery: council protocol, agent loops, workers, graph views, context assembly, providers, prompts, and agent tool access. Agents use the application; the application does not depend on agents.
- `environments/` owns canonical-baseline discovery, execution-relevant environment specifications, isolated branch environments, candidate revisions, fidelity records, and controlled promotion. It does not decide which candidate is intellectually best.
- `api/` is transport. It does not contain business rules or direct database mutation paths.
- `persistence/` implements storage ports. Application code must not import concrete ORM/database models.
- `security/` enforces actor authorization, identity, and secret boundaries across both humans and agents.

A human-originated action and an agent-originated action that change Council state must pass through the same application operation.

### Agent/application boundary

Agents observe approved read models and change Council state only through typed application commands. Rejections are structured and explain why the command was rejected so the requesting agent can adapt.

The application validates:

1. command/schema validity;
2. actor authorization;
3. current-state legality and concurrency/version constraints;
4. universal Council invariants;
5. configured environment policy.

It does **not** judge whether the agent's argument, hypothesis, conclusion, or implementation is intellectually good.

Tool calls and application commands are distinct. Tools retrieve information or operate on permitted external capabilities; commands change authoritative Council state.

### Core rules versus environment policy

Council core rules are universal. Environment-specific rules are supplied through declarative policy/capability profiles where possible.

Examples of environment policy include allowed tools, available sources, evidence requirements, branch-write permissions, external-write restrictions, budgets, and data-access scopes.

Do not create a separate hard-coded Council implementation for each deployment.

### Branch environment model

When an investigation concerns a mutable external target, the canonical environment is not changed during deliberation.

All council members derive isolated branch environments from the same recorded baseline. Workers inherit their parent member's branch and permissions; spawning a worker does not create an additional independent council branch.

A branch environment is **not** a full machine clone. It is the smallest practical environment that preserves all known conditions capable of materially changing the behavior under investigation.

Environment discovery records an execution-relevant environment specification that may include:

- OS/build/architecture and relevant kernel behavior;
- runtimes, libraries, services, filesystem semantics, and permissions;
- network, proxy, VPN, firewall, DNS, identity, certificate, and SSO constraints;
- security software, endpoint controls, and kernel drivers when relevant;
- hardware and device/driver dependencies;
- project/configuration dependencies;
- database schema, cardinality, latency, concurrency, indexes, and data-shape characteristics;
- relevant external integrations and their behavioral constraints.

Irrelevant installed software is not reproduced.

Each relevant condition must be classified at least as reproduced, simulated, intentionally omitted as irrelevant, unreproducible, or unknown. Fidelity gaps remain attached to candidate results and can force revalidation if later shown to matter.

Docker is one execution mechanism, not the environment abstraction. Containers, VMs, native-host test targets, hardware-backed targets, copy-on-write snapshots, isolated replicas, overlays, representative datasets, and simulated integrations may all be used where appropriate.

Large production systems do not require naive complete duplication. Use the smallest safe reproduction that preserves the behavior needed to validate the candidate.

### Candidate and promotion boundary

Agents may experiment broadly inside their own permitted branch environment, but they cannot directly mutate the canonical target.

A member explicitly turns branch work into a candidate revision containing the intended change set, evidence, test results, assumptions, limitations, and environment-fidelity record.

Publication exposes the candidate and declared findings, not unrestricted access to another member's live private workspace.

Selection and promotion are separate:

- **selection** is the council/user decision about which candidate to proceed with;
- **promotion** is the operational process that checks whether the selected candidate can safely be applied to the current canonical environment.

Promotion verifies the canonical version/baseline, required permissions, unresolved environment-fidelity gaps, required tests/validation, and target compatibility. If the canonical environment changed, the candidate must be rebased/revalidated rather than blindly applied.

### Mechanical enforcement

Part 2 requires architecture tests/linting so dependency rules are not documentation-only.

At minimum, CI must reject:

- `domain/` importing FastAPI, LangGraph, providers, persistence, environment adapters, or ORM models;
- `application/` importing FastAPI, concrete providers, concrete database repositories, or concrete environment adapters;
- `api/` or `agents/` writing database models directly instead of using application operations;
- provider-specific conditionals leaking through unrelated modules;
- tool adapters mutating authoritative Council state directly;
- agent code accessing canonical-environment write adapters;
- graph/context code becoming an alternate source of authoritative truth.

## 3. Database implementation

Use SQLAlchemy 2, PostgreSQL, and Alembic migrations.

Each request or independently executing task gets its own database session. Do not share one mutable SQLAlchemy `AsyncSession` across concurrent agents. SQLAlchemy documents separate sessions for concurrent tasks: [SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).

Migrations are committed and reviewed. Alembic's generated migrations are candidates, not automatically trustworthy changes; review and correct them: [Alembic autogeneration](https://alembic.sqlalchemy.org/en/latest/autogenerate.html).

### Important tables

| Area | Main tables |
|---|---|
| Ownership | `workspaces`, `projects`, `memberships`, `access_grants` |
| Investigations | `runs`, `run_config_versions`, `branches`, `agents`, `agent_sessions` |
| Work | `tasks`, `task_dependencies`, `jobs`, `operations` |
| Sources | `sources`, `source_versions`, `run_sources`, `evidence_items`, `evidence_origins` |
| Reasoning records | `claims`, `claim_versions`, `assumptions`, `assumption_versions`, `analysis_steps` |
| Support structure | `support_routes`, `route_premises`, `origin_links` |
| Review | `challenges`, `challenge_responses`, `claim_revisions`, `review_dispositions` |
| Continuity | `context_packets`, `context_packet_items`, runtime checkpoints |
| Audit and delivery | `events`, `outbox_messages`, `message_deliveries`, `command_receipts` |
| Models and spending | `model_profiles`, `model_invocations`, `budget_accounts`, `budget_reservations` |

Introduce them through milestones; do not build every table before the first working feature.

### Stable identities versus immutable versions

A claim needs both a stable identity and versioned content:

```text
claims
    id
    project_id
    run_id
    owning_agent_id
    current_version_id

claim_versions
    id
    claim_id
    version_number
    previous_version_id
    statement
    applicability_conditions
    claim_kind
    author_session_id
    created_at
```

The stable claim means the proposition being investigated. A version means the exact statement as recorded at this point.

Changing the wording creates a new version. It does not overwrite the earlier statement.

Review assessments are recorded separately. Reviewing an unchanged statement should not unnecessarily create a new textual version.

Important database constraints include unique version numbers per claim, valid references, same-project boundaries, and revision links belonging to the same claim.

### Sources also need versions

A URL is not a source snapshot.

`source_versions` records the retained content hash, artifact reference, retrieval time, extraction information, and original location.

`evidence_items` point into that version using a typed locator: text offsets, page references, dataset selections, or tool-result references.

When possible, the backend checks that a submitted quotation matches the retained source representation. Failure to find the quoted text must not silently produce a valid evidence record.

## 4. Typed agent commands

Agents interact through structured commands, not free-form instructions that another model interprets into database writes.

The following is an illustrative Pydantic contract, not implemented or verified application code:

```python
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class SupportRouteDraft(StrictModel):
    premise_ids: list[UUID] = Field(min_length=1, max_length=32)
    rationale: str = Field(min_length=1, max_length=8000)


class ClaimDraft(StrictModel):
    statement: str = Field(min_length=1, max_length=12000)
    applicability: str = Field(min_length=1, max_length=8000)
    kind: Literal[
        "source_statement",
        "inference",
        "hypothesis",
        "recommendation",
    ]
    support_routes: list[SupportRouteDraft] = Field(
        default_factory=list
    )
    limitations: list[str] = Field(default_factory=list)


class ReviseClaim(StrictModel):
    claim_id: UUID
    expected_version: int = Field(ge=1)
    replacement: ClaimDraft
    challenge_ids: list[UUID] = Field(default_factory=list)
    revision_reason: str = Field(min_length=1, max_length=8000)
```

Notice what is absent: `verified=True`, an author supplied by the model, or permission settings supplied by the model.

The backend derives the author from the authenticated agent session. It checks every referenced record and applies the appropriate initial status.

A model may submit an unsupported hypothesis; the application preserves it as such. It must not become supported because the model selected an impressive label.

Other commands include `CommissionWorker`, `SubmitChallenge`, `RespondToChallenge`, `PublishAnalysis`, and `RequestModelChange`.

These contracts form the boundary between flexible model behavior and controlled application behavior.

## 5. How one command becomes a committed change

Consider an agent narrowing a claim after criticism. The command follows this path:

```text
Agent tool call or API request
    -> identify authenticated actor
    -> validate command structure
    -> check permissions and referenced records
    -> check duplicate-command receipt
    -> check expected claim version
    -> create new claim version
    -> record revision reason and challenge links
    -> update essential graph relationships
    -> append audit event and outgoing notification
    -> commit transaction
```

The claim version, revision relationship, audit event, and essential graph changes are committed together. If any required write fails, the transaction rolls back.

### Handle simultaneous changes explicitly

Suppose two workers both attempt to revise version 4. The first creates version 5. The second receives a version-conflict result rather than silently overwriting it. That worker must read the new state and reconsider its proposal.

### Make retries safe

Each command gets a stable idempotency key and payload hash.

Repeating the same command returns its existing receipt. Reusing its key with a different payload returns a conflict.

This is especially important when the database committed successfully but the caller lost the response.

Never keep a database transaction open while waiting for a model response or external retrieval. External operations are recorded before execution and reconciled afterward.

For large artifacts, write and verify the file first, then publish its database reference. Failed database writes can leave an unreferenced artifact for cleanup; they must not leave a supposedly available source pointing to missing content.

## 6. The graph: how we implement the three defining questions

Use a small typed `records` registry for graph-addressable objects and a relationship projection over the canonical tables.

That avoids unreliable relationships such as a string `target_type` paired with an arbitrary identifier that may not exist.

Graph relationship records include endpoints, relationship type, originating event or assertion, attribution, and review status.

Agents do not receive a generic write-arbitrary-graph-edge tool. They submit a supported relationship proposal or use a domain command such as `ReviseClaim`. The service creates the corresponding records.

### A. Which conclusions depend on this?

This requires more than walking every outgoing arrow. Model support as explicit routes:

```text
Route R1:
    Evidence E1 AND Assumption A1
    -> Claim C1, version 2

Route R2:
    Evidence E2
    -> Claim C1, version 2
```

`support_routes` identifies a proposed supporting route. `route_premises` identifies everything that route requires.

When A1 is questioned, R1 needs reassessment. R2 may remain unaffected by that change, although that does not automatically make C1 true.

`graph/dependencies.py` returns affected claim versions, affected routes, alternative recorded routes, and relevant report sections. It distinguishes dependency relationships from mere citations.

PostgreSQL supports recursive traversal and explicit cycle handling: [recursive queries](https://www.postgresql.org/docs/current/queries-with.html).

Queries need maximum depth, node limits, timeouts, and visible truncation. An outer result limit alone is not the entire protection against an expensive traversal.

### B. Which challenge caused the claim to narrow?

This is a direct relational query, not an LLM reconstruction.

`claim_revisions` links:

```text
previous_version_id
new_version_id
revision_reason
author_session_id
```

A junction table links that revision to the recorded challenges and evidence considered.

`graph/revisions.py` returns the before-and-after statements and explicit recorded reason. Do not infer causation merely because a challenge preceded a revision.

### C. Which findings share underlying evidence?

Separate documents from evidence origins.

A document may reference a study, dataset, experiment, observation series, or another report. Several documents can therefore lead to the same origin.

`graph/lineage.py` follows reviewed origin relationships and groups common origins. Suspected relationships remain suggestions until checked.

Its response distinguishes known shared origins, separately traced origins, and unresolved lineage. Different URLs are not independent confirmation.

### Keep one authoritative system

The graph projection must be rebuildable from canonical records.

Do not keep one conclusion in `claim_versions` and a different conclusion inside an unrelated graph-memory system.

Essential relationships update transactionally. Secondary indexes may update asynchronously, but their freshness must be visible.

## 7. Worker scheduling and recovery

The durable queue lives in PostgreSQL initially.

A job represents executable work; a task represents the investigative assignment. They are related but not identical. One task may require several model turns, retrieval jobs, and reviews.

Workers claim jobs with short transactions using row locking. PostgreSQL documents `SKIP LOCKED` for multiple consumers of a queue-like table: [SELECT](https://www.postgresql.org/docs/current/sql-select.html).

The core claim operation resembles this, with parameters bound through SQLAlchemy. This example is not the entire scheduler and has not been executed as part of this documentation delivery:

```sql
WITH candidate AS (
    SELECT id
    FROM jobs
    WHERE state = 'queued'
      AND available_at <= now()
    ORDER BY priority DESC, created_at, id
    FOR UPDATE SKIP LOCKED
    LIMIT 1
)
UPDATE jobs AS job
SET state = 'leased',
    lease_owner = :worker_id,
    lease_expires_at =
        now() + make_interval(secs => :lease_seconds),
    lease_generation = job.lease_generation + 1
FROM candidate
WHERE job.id = candidate.id
RETURNING job.*;
```

The generation number matters. A worker whose lease expired must not later overwrite results from a replacement worker. Completion requires the currently valid lease generation.

Lease expiry does not mean blindly rerun everything.

If a model invocation or external action started but its result is unknown, recovery checks the operation record. Some operations can be safely repeated; others require reconciliation.

We can make our database commands idempotent. We cannot promise exactly-once execution from every external provider.

Parents waiting for children release execution capacity. Their pending dependencies are stored, and a result-delivery event makes them runnable again.

Spending reservations happen transactionally before parallel calls. Record estimated reservation, actual reported usage, and uncertain usage separately.

## 8. The actual agent loop

Implement one reusable agent-session loop, configured for either a council member or a worker.

Do not implement three unrelated agent implementations or one giant `CouncilAgent` class that owns the entire system.

The loop's persistent state stays small. Illustrative contract:

```python
from typing import Literal, TypedDict


class AgentState(TypedDict):
    session_id: str
    task_id: str
    context_packet_id: str | None
    invocation_id: str | None
    pending_operation_ids: list[str]
    status: Literal[
        "ready",
        "waiting",
        "paused",
        "finished",
        "failed",
    ]
```

The state primarily contains references. Full source material, operation results, and claim history live in the ledger.

Within LangGraph, the execution path is:

```text
Load current task
    -> assemble permitted context
    -> invoke selected model
    -> validate returned tool requests
    -> execute through capability gateway
    -> persist results
    -> continue, wait, checkpoint, or finish
```

LangGraph provides thread-scoped checkpoints and durable storage, but those mechanisms do not replace application records or permissions. Reference: [durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution).

Each model session gets its own checkpoint thread. Two workers cannot concurrently mutate the same session.

### Where the council protocol lives

`runtime/phases.py` manages publication barriers, review assignments, and stage transitions. It does not decide the substantive approach.

Each member publishes its initial analysis into a pending publication record. When the required initial submissions are present, or an explicitly recorded degraded-mode decision exists, the shared phase opens.

Afterward, members commission their own workers and challenges.

Administrative votes can allocate shared resources. There is no voting function that promotes a claim to true.

### Prompts remain versioned inputs

Keep prompts in `prompts/`, including council investigation, worker assignment, cross-examination, premortem, and report assembly.

Each invocation records the prompt version and model configuration.

Permissions, budget enforcement, publication rules, and evidence status are implemented in code, not only repeated in prompts.

## 9. Model adapters and the dropdowns

The runtime depends on our own provider interface:

```text
ModelRequest
    resolved_model_profile
    permitted_tool_definitions
    message_history_reference
    context_packet_reference
    output_allowance

ModelResult
    assistant_message
    tool_calls
    usage
    provider_request_id
    finish_reason
    private_continuation_reference
```

The adapter implements the provider-specific HTTP protocol.

Initially, `DeepSeekProvider` makes real requests.

`ScriptedProvider` returns controlled responses for tests, including malformed arguments, attempted unauthorized actions, timeouts, and conflicting claims.

The scripted provider is essential: reproduce failures without depending on a live model choosing to make them.

### Preserve provider-specific continuation correctly

DeepSeek's documented thinking-mode tool flow requires `reasoning_content` to be preserved in subsequent tool-enabled requests. The adapter retains the required continuation information rather than dropping it during normalization. It remains private session state, not shared council evidence. Verify the current contract during implementation: [DeepSeek thinking mode](https://api-docs.deepseek.com/guides/thinking_mode/).

A model change resolves a new profile, checks capabilities and data permissions, completes or reconciles pending operations, then opens a new session with a handover.

The dropdown issues a model-change request, not an immediate mutation of a running Python object.

Lock tested package versions and record model profile versions. Do not scatter provider model names and context sizes throughout application code.

## 10. Tools and evidence access

The tool registry maps each tool name to an argument schema, authorization policy, handler, result schema, and operational limits.

The initial toolbox contains research operations:

```text
search_evidence
read_evidence
trace_dependencies
inspect_claim_history
inspect_shared_origins
propose_claim
submit_challenge
respond_to_challenge
commission_worker
publish_analysis
```

Numerical analysis and sandbox execution can be added as optional capabilities. They are not necessary to prove the generic council works.

A tool handler calls application services. It does not accept arbitrary SQL from an agent.

### Authorization must reach retrieval

Every read is scoped to the authenticated agent, project, run, branch, and publication stage.

This includes graph traversal, search snippets, artifact downloads, and context assembly, not merely API endpoints.

Add PostgreSQL row-level security as defense in depth, using a restricted application role. PostgreSQL notes that superusers, roles with bypass privileges, and normally table owners can bypass policies, so role configuration matters: [row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).

The future RAG adapter returns evidence records and source locations through this same interface.

Raw source text is untrusted material. Instructions appearing inside it cannot change tool permissions or the agent's task.

## 11. Context construction and rollover

The context manager is a service, not another agent deciding what everyone should believe.

It calculates an input allowance from the selected model's configured limits:

```text
usable input allowance
    = context capacity
    - reserved output
    - expected protocol/tool overhead
    - safety margin
```

Token estimation must be model-specific where possible. When only an estimate is available, label and account for that uncertainty.

### How a context packet is assembled

First load mandatory state: the objective, permissions, active task, current claims, unresolved blocking challenges, and pending operations.

Then select relevant evidence and graph relationships.

Finally, add useful recent history and a short handover within the remaining allowance.

Ordinary text search remains available alongside graph traversal. Use PostgreSQL's built-in full-text search for the initial searchable evidence and history indexes before adding a separate retrieval database. Reference: [text search introduction](https://www.postgresql.org/docs/current/textsearch-intro.html).

Each packet records the exact record versions supplied and the ledger position used.

If mandatory material cannot fit, split the task or retrieve it in stages. Do not quietly drop an objection that invalidates the current conclusion.

### Rollover is a controlled transition

The current session reaches a safe boundary, records unfinished work, reconciles pending operations, and closes. The runtime then creates a replacement session under the same logical agent.

The new session uses the ledger, not a progressively compressed summary of earlier summaries, as the underlying memory.

Checkpoint replay goes through recorded operation identifiers. LangGraph's functional API documentation emphasizes checkpointing nondeterministic work and making replayed operations idempotent: [functional API](https://docs.langchain.com/oss/python/langgraph/functional-api).

## 12. API and frontend implementation

Use React, TypeScript, Vite, TanStack Query, and React Flow.

The frontend displays server state; it does not calculate evidential status or decide which challenges are resolved.

FastAPI supplies the OpenAPI contract. Generate TypeScript API types from that contract rather than manually maintain a second set of claim and graph interfaces. References: [FastAPI features](https://fastapi.tiangolo.com/features/) and [openapi-typescript](https://openapi-ts.dev/introduction).

TanStack Query handles server-state fetching and cache management. Local component state holds panel sizes, selections, and graph layout, not authoritative investigation data. Reference: [TanStack Query overview](https://tanstack.com/query/latest/docs/framework/react/overview).

### Initial endpoints

| Endpoint | Behavior |
|---|---|
| `POST /runs` | Create a versioned run configuration. |
| `POST /runs/{id}/start` | Validate and enqueue initial investigations. |
| `POST /runs/{id}/pause` | Request a safe pause. |
| `GET /runs/{id}/events` | Stream authorized committed updates. |
| `POST /agents/{id}/model-changes` | Queue a safe model migration. |
| `POST /runs/{id}/claims` | Submit a claim through the claim service. |
| `POST /claims/{id}/revisions` | Create a checked, versioned revision. |
| `GET /claims/{id}/history` | Return revision history and reasons. |
| `POST /runs/{id}/graph/dependencies` | Trace dependencies within explicit limits. |
| `POST /runs/{id}/graph/shared-origins` | Inspect evidence lineage. |

Graph query responses include snapshot position, limits, and truncation state.

React Flow renders returned nodes and edges. Its custom-node support permits distinct claim, source, challenge, and assumption components. It is not the graph database. Reference: [React Flow custom nodes](https://reactflow.dev/learn/customization/custom-nodes).

### Live updates must be recoverable

Server-sent events carry durable identifiers. Reconnecting clients request events after their last received position, then refresh affected queries.

Use a transactionally allocated per-run event sequence so the stream has an explicit ordering contract. Do not assume an arbitrary generated identifier is equivalent to committed event order.

Events contain minimal authorized information. Clients fetch detailed records through normal permission-checked endpoints.

For model selection, the UI displays the effective profile, where it was inherited from, and any pending migration.

## 13. Review and reporting in code

The review process creates ordinary tasks and structured results.

`PremortemScenario` records a hypothetical failure mechanism, affected claim versions, assumptions, checks possible now, and observations needed later.

It has a distinct record type. No normal command converts it into an observed event by changing a label.

`reviews.py` decides whether required review work has a recorded disposition. It does not decide that a majority opinion proves the conclusion.

The final report stores references to precise claim versions. The report assembler cannot silently broaden those claims.

A finalized report records unresolved objections, source scope, and review limitations. If an upstream claim changes later, the old report remains intact and is marked as requiring a new review or revision.

## 14. Testing: build evidence of correctness alongside the code

Separate four test layers:

| Layer | What it proves |
|---|---|
| Unit tests | Pure rules: version transitions, grouped premises, model inheritance, budget arithmetic. |
| PostgreSQL integration tests | Transactions, queue leases, row access, graph traversal, concurrent updates. |
| Provider contract tests | Serialization, continuation state, tool parsing, retries, error handling. |
| Repeated agent evaluations | Whether actual model-driven investigations preserve evidence and behave usefully. |

Database integration tests use real PostgreSQL, not SQLite substitutes for locking, permissions, and recursive-query behavior.

The first fixture contains one original study, two derivative summaries, an initially overstated claim, a corrective challenge, a narrowed version, and an alternative support route. That fixture exercises all three graph features.

Deliberately test a missing graph edge, an inaccessible source, an unresolved objection, and two workers racing to revise the same claim.

Failure injection includes a crash after a database commit but before acknowledgement, an expired worker returning late, and a provider call with an unknown outcome.

Continuous integration runs formatting, type checks, unit tests, migrations against an empty database, PostgreSQL integration tests, frontend type checking, and a frontend build.

Live DeepSeek tests remain explicitly marked and opt-in. A passing scripted-provider test is not reported as a passing live-model investigation.

## 15. The actual implementation sequence

Build in end-to-end slices, not the entire backend followed by the entire runtime before discovering that they do not connect.

| Slice | Working result |
|---|---|
| 1. Project skeleton | Backend starts, database connects, migrations run, configuration validates, CI executes. |
| 2. Evidence and claims | Register a source snapshot, extract evidence, submit a claim, retrieve its provenance. |
| 3. Revision history | Challenge a claim, narrow it, inspect the complete reason for the change. |
| 4. Dependency and lineage queries | Execute the three defining graph operations against prepared evidence. |
| 5. Durable execution | Queue jobs, recover interrupted work, enforce budgets, execute scripted model turns. |
| 6. Working council | Run independent branches, publish analyses, delegate workers, cross-examine findings. |
| 7. Continuity and review | Force context rollover, preserve objections, run the premortem, finalize a traceable report. |
| 8. Full interface and live integrations | Add the complete inspection UI, live-provider verification, external evidence adapters. |

A minimal developer inspection page can appear early, but the polished dashboard should not precede the records it is supposed to display.

For Milestone A, deliver the source/claim APIs, three graph queries, authorization, durable jobs, provider interface, scripted provider, DeepSeek adapter, and deterministic integration tests. Verify live API behavior separately.

## Engineering target

One agent action must pass through a typed command, an authorization check, a controlled operation, durable records, and an inspectable result. Then scale that mechanism to an entire council.

The swarm's intelligence can improve without making its history, permissions, and evidence handling depend on the model being correct every time.
