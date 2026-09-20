# Part 2 of 15 — Repository Layout & Enforceable Boundaries

**Status:** approved component design; not yet implemented.  
**Branch:** `design/code-level-implementation`.  
**Authority:** this document refines Part 2 of [CODE_IMPLEMENTATION_PLAN.md](../CODE_IMPLEMENTATION_PLAN.md). It does not authorize application implementation or merge to `main`.

## 1. Approved Part 2 principles

### 1.1 Council core remains agnostic

Council semantics are domain-, model/provider-, source-, tool-, caller-, and executor-agnostic.

Concrete infrastructure may still be opinionated where abstraction would provide no useful portability.

### 1.2 Application and agents are different systems

The application owns authoritative Council concepts and valid state transitions.

The agent subsystem owns reasoning and investigation machinery:

- council protocol;
- logical agent/session loop;
- workers;
- graph views and provenance queries used by agents;
- context construction and rollover;
- model providers;
- prompts;
- agent tools.

Agents operate **on** the application. The application does not depend on agent reasoning machinery.

### 1.3 Typed commands are the write boundary

Agents do not mutate authoritative application state directly.

They submit typed application commands. The application checks:

1. command/schema validity;
2. actor authorization;
3. legal state transition;
4. version/concurrency constraints;
5. universal Council invariants;
6. applicable environment policy.

A rejected command returns a structured reason, retryability, and relevant corrective state so the requesting agent can adapt.

The application does not decide whether the agent's argument or conclusion is intellectually good.

### 1.4 Tools and application commands are separate

A tool call retrieves information or uses an external capability.

An application command changes authoritative Council state.

Tool adapters cannot silently become alternate database/state-mutation paths.

### 1.5 Universal rules versus environment policy

Council core rules remain universal.

Deployment-specific restrictions are expressed through policy/capability profiles where possible rather than separate hard-coded Council implementations.

Environment policy can govern:

- available tools;
- accessible sources;
- evidence requirements;
- branch-write permissions;
- external/consequential writes;
- data-access scopes;
- budget/resource limits.

### 1.6 Canonical and branch environments are separate

During deliberation, investigative branches do not mutate the canonical target.

Each council member receives an isolated branch environment derived from the same recorded canonical baseline.

Workers operate inside their parent member's branch and do not count as additional independent council branches.

### 1.7 Environment copies are behavioral, not literal

A branch environment is not a byte-for-byte clone of the user's machine.

Council first records an **execution-relevant environment specification** containing the smallest practical set of known conditions capable of materially changing the behavior under investigation.

Possible relevant conditions include:

- OS/build/architecture and kernel-sensitive behavior;
- runtimes, libraries, services, filesystem behavior, and permissions;
- network, firewall, proxy, VPN, DNS, identity, certificates, and SSO;
- endpoint security, security products, and kernel drivers when they can alter behavior;
- hardware/device/driver dependencies;
- project configuration;
- database schema, cardinality, indexes, latency, concurrency, and representative data shape;
- external integrations and their constraints.

Irrelevant software is excluded.

Each material condition is classified as:

- reproduced;
- simulated;
- intentionally omitted as irrelevant;
- unreproducible;
- unknown.

Fidelity gaps remain attached to candidate results and can require revalidation.

### 1.8 Docker is an implementation mechanism, not the environment abstraction

Docker may be appropriate for many branch workloads and restricted code execution.

It is not assumed to reproduce OS-, kernel-, driver-, device-, endpoint-security-, or hardware-sensitive behavior.

The environment system may therefore use containers, VMs, native-host test targets, hardware-backed targets, copy-on-write snapshots, isolated database replicas, overlays, representative/anonymized datasets, or simulated integrations.

### 1.9 Large environments should not be naively duplicated

A large production database or company environment does not need complete physical duplication per agent.

The environment adapter may share immutable/read-only baselines and give each branch isolated overlays or replicas when that preserves the behavior relevant to the investigation.

### 1.10 Candidate, selection, and promotion are distinct

Agents may experiment inside their own branch environments.

A branch explicitly produces a **candidate revision** containing:

- intended changes;
- findings/evidence;
- test/validation results;
- assumptions;
- limitations;
- environment-fidelity record.

Publication exposes the candidate and declared findings, not another member's unrestricted live workspace.

Selection chooses the candidate to proceed with.

Promotion is a separate operational step that verifies current canonical version, permissions, required tests, compatibility, and unresolved fidelity gaps before applying any real change.

A stale candidate is rebased/revalidated rather than blindly promoted.

## 2. Approved repository shape

```text
backend/src/council/
|
|-- domain/
|-- application/
|
|-- agents/
|   |-- runtime/
|   |-- graph/
|   |-- context/
|   |-- providers/
|   |-- tools/
|   `-- prompts/
|
|-- environments/
|   |-- contracts.py
|   |-- discovery.py
|   |-- fidelity.py
|   |-- branches.py
|   |-- candidates.py
|   |-- promotion.py
|   `-- adapters/
|
|-- persistence/
|-- security/
`-- api/
```

`services/` from the earlier proposal is renamed to `application/` because this layer owns Council use cases, not generic service helpers.

## 3. Responsibility boundaries

| Module | Owns | Must not own |
|---|---|---|
| `domain` | Council entities, value objects, invariants, command/event contracts | FastAPI, DB/ORM, providers, environment mechanisms |
| `application` | Council use cases and authoritative state transitions | HTTP, provider-specific logic, concrete DB/environment adapters |
| `agents` | Reasoning, council protocol, graph/context, workers, providers, agent tools | Canonical writes, authoritative persistence |
| `environments` | Baseline discovery, branch environments, fidelity, candidates, promotion | Intellectual candidate ranking |
| `persistence` | Concrete storage and artifact implementations | Council decisions |
| `security` | Identity, authorization, secret boundaries | Investigation reasoning |
| `api` | Transport, request/response, SSE | Business rules or direct persistence writes |

## 4. Enforceable dependency direction

The target dependency direction is inward:

```text
domain
  ^
application
  ^
api / agents / environment orchestration
  ^
concrete infrastructure adapters
```

Hard prohibitions already approved:

- `domain` cannot import frameworks, providers, persistence, or environment implementations;
- `application` cannot import FastAPI, concrete providers, concrete persistence repositories, or concrete environment adapters;
- `api` and `agents` cannot mutate ORM/database records directly;
- graph/context cannot become an alternate authoritative state store;
- provider-specific behavior cannot leak through unrelated modules;
- tool adapters cannot mutate Council state directly;
- agent code cannot access canonical-environment write adapters.

## 5. Final import matrix

The following dependency matrix is approved.

| Package | May import | Must not import |
|---|---|---|
| `domain` | standard library, other `domain` modules | application, agents, environments, persistence, security implementations, API, frameworks/providers/ORM |
| `application` | `domain`, `application` modules/ports | agents, API, concrete persistence, concrete providers, concrete environment adapters |
| `agents.runtime` | application public interfaces, agent modules, environment contracts, security capability interfaces | ORM/database models, canonical write adapters |
| `agents.graph` | approved application read interfaces, domain identifiers/contracts | direct persistence mutation, provider implementations as authority |
| `agents.context` | approved application reads, graph query interfaces, evidence/source interfaces | direct authoritative writes |
| `agents.providers` | provider contracts, domain/value types needed for model I/O | application business-rule ownership, persistence mutation |
| `agents.tools` | application command/query interfaces, environment/tool capability contracts | direct authoritative state mutation, raw canonical credentials |
| `environments` core/contracts | domain/value types, application ports needed for recorded operations | agent intellectual logic |
| `environments.adapters` | environment contracts plus concrete infrastructure libraries | application business rules, candidate ranking |
| `persistence` | domain/application persistence ports, concrete DB/artifact libraries | agent reasoning or API behavior |
| `security` implementations | security contracts/ports, concrete identity/secret backends | investigation reasoning |
| `api` | application public interfaces, security interfaces, read models | direct ORM/database mutation, provider/environment implementation details except composition wiring |

Composition-root code may instantiate concrete adapters and connect them to abstract ports. That exception does not grant ordinary modules permission to import concrete implementations freely.

## 6. Shared versus branch-local record ownership

Part 2 fixes record **classes**, while Part 3 will define SQL tables.

### 6.1 Canonical/shared baseline records

These describe the real starting target and common authorized inputs:

- run identity/configuration;
- canonical environment identity and version;
- execution-relevant environment specification;
- source identities and retained source versions;
- common raw evidence/source material;
- environment policy/capability profile;
- council membership and branch identities.

These records are shared, but access remains permission scoped.

### 6.2 Branch-private records

Until publication, these remain visible only within the owning branch and its authorized workers:

- private hypotheses and notes;
- unpublished findings/claims;
- branch-local graph annotations;
- branch-local context/checkpoints;
- worker outputs;
- experimental environment changes;
- unsubmitted candidate drafts;
- unpublished test interpretations.

Shared raw-source caching is allowed, but another branch's interpretation must not leak through caches, previews, graph neighborhoods, retrieval, or context assembly.

### 6.3 Published/shared records

An explicit publication operation moves a declared artifact across the privacy boundary.

Published records may include:

- findings;
- claims;
- evidence references;
- assumptions;
- methods;
- gaps/limitations;
- candidate revision manifests;
- declared validation/test results;
- challenges and responses.

Publication does not expose the branch's entire live workspace.

### 6.4 Candidate-specific records

Each candidate revision records:

- branch and actor identity;
- baseline environment version;
- intended change set;
- environment diff;
- relevant evidence;
- tests/validation actually performed;
- assumptions and known limitations;
- environment-fidelity classification;
- unresolved blockers.

### 6.5 Promotion/canonical-operation records

Promotion is its own durable history:

- selected candidate;
- target canonical version;
- pre-promotion validation;
- permissions/approval;
- rebase/revalidation if required;
- applied operations;
- resulting canonical version;
- rollback/reconciliation state.

Investigative agents cannot rewrite this history.

## 7. Minimum environment-adapter contract

Environment adapters are capability based. They expose only supported operations and must explicitly declare unsupported capabilities.

The abstract contract contains these conceptual operations:

```text
describe_capabilities()
discover()
capture_baseline()
create_branch()
read()
branch_write()
execute()
test()
diff()
capture_candidate()
validate_fidelity()
validate_promotion()
promote()
rollback_or_reconcile()
```

### Required semantics

- `describe_capabilities()` declares which operations are supported and relevant constraints.
- `discover()` identifies execution-relevant conditions without assuming every machine property matters.
- `capture_baseline()` records the canonical version/snapshot from which council branches derive.
- `create_branch()` creates an isolated branch representation without granting canonical write access.
- `read()` exposes permitted target state.
- `branch_write()` changes only the branch environment.
- `execute()` / `test()` operate only where the adapter declares them meaningful and safe.
- `diff()` explains branch-versus-baseline changes.
- `capture_candidate()` freezes the intended candidate revision and fidelity record.
- `validate_fidelity()` reports reproduced/simulated/irrelevant/unreproducible/unknown conditions.
- `validate_promotion()` checks current canonical compatibility and operational prerequisites without ranking candidate quality.
- `promote()` is available only to adapters and actors explicitly authorized for canonical mutation.
- `rollback_or_reconcile()` declares how partial/failed canonical operations are handled when rollback is supported or impossible.

A document/research environment may legitimately declare execution, promotion, or rollback unsupported. A Git/software environment may support all of them. A database environment may implement them through snapshots/overlays rather than file branches.

## 8. Architecture enforcement mechanism

Part 2 chooses automated import contracts plus architecture tests.

When implementation begins:

1. configure **Import Linter** contracts (or an explicitly documented replacement if tooling constraints require one) for package dependency direction;
2. run those contracts in CI on every change;
3. add deterministic architecture tests for rules that imports alone cannot prove, such as:
   - no direct ORM mutation from API/agent/tool code;
   - canonical write adapters unavailable to investigative agent composition;
   - graph/context records cannot become authoritative mutation paths;
   - branch adapters cannot silently target canonical resources;
4. make architectural violations build/test failures, not warnings.

The exact package version is an implementation-time dependency decision; the enforcement behavior defined here is not optional.

## 9. Part 2 completion decision

All Part 2 architectural questions required before database design are now resolved:

- repository ownership boundaries;
- dependency direction and exact import matrix;
- agent/application typed-command boundary;
- universal rules versus environment policy;
- canonical versus branch environment separation;
- execution-relevant environment fidelity model;
- Docker/VM/native/other mechanism abstraction;
- shared versus branch-private/publication/candidate/promotion record classes;
- minimum environment-adapter contract;
- candidate/selection/promotion separation;
- automated architecture enforcement.

Detailed persistence representation now belongs to Part 3.

## 10. Deferred to later parts

The following are intentionally deferred and do not prevent Part 2 approval:

- exact PostgreSQL tables/indexes/migrations — Part 3;
- exact command classes/payloads — Part 4;
- transaction/idempotency implementation — Part 5;
- graph query algorithms — Part 6;
- queue leases/fencing/fairness — Part 7;
- detailed agent phase state machine — Part 8;
- provider wire formats — Part 9;
- tool-specific authorization implementations — Part 10;
- context ranking/rollover algorithms — Part 11;
- API/SSE payloads — Part 12;
- final review/report assembly — Part 13;
- full test implementation — Part 14;
- implementation/build slices — Part 15.

## 11. Part 2 acceptance condition

Part 2 is approved because a future implementation agent can now answer, without architectural guesswork:

1. which package owns a behavior;
2. which direction dependencies are allowed to flow;
3. how agents may read and request changes without bypassing the application;
4. how environment-specific behavior is added without forking Council core;
5. how an execution-relevant branch environment differs from the canonical target;
6. how candidates cross from private branch work into publication and then promotion;
7. which boundary violations automatically fail CI.

No application code needs to exist for Part 2 itself to be considered designed.
