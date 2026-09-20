# Part 2 of 15 — Repository Layout & Enforceable Boundaries

**Status:** active component design; major architecture decisions approved, completion checklist below.  
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

## 5. Part 2 completion checklist

Part 2 is considered complete when the following four remaining items are finalized and recorded.

### A. Exact import matrix

Define, package by package, what may import what.

This must cover at least:

- domain;
- application;
- agents.runtime;
- agents.graph;
- agents.context;
- agents.providers;
- agents.tools;
- environments;
- persistence;
- security;
- api.

The matrix should distinguish interfaces/contracts from concrete implementations.

### B. Shared versus branch-local record ownership

Define which records are:

- canonical/shared baseline;
- branch-private;
- explicitly published/shared;
- candidate-specific;
- promotion/canonical-operation records.

This is a package-boundary decision in Part 2; detailed SQL tables remain Part 3.

### C. Minimum environment-adapter contract

Define the abstract operations every environment adapter must expose or explicitly declare unsupported, including the capability model around:

- inspect/discover;
- snapshot/baseline;
- create branch;
- read;
- branch write;
- execute/test;
- diff;
- produce candidate;
- validate fidelity;
- promote;
- rollback/reconcile where supported.

The contract must be capability-based so a research/document environment is not forced to implement meaningless software operations.

### D. Architecture enforcement mechanism

Choose the implementation-time enforcement approach for import/dependency rules and require architecture tests in CI.

The specific Python package/tool can remain replaceable, but the repository must have a deterministic automated check that fails on forbidden imports/boundary violations.

## 6. Not blockers for Part 2

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

## 7. Part 2 acceptance condition

Part 2 is approved when a future implementation agent can answer, without architectural guesswork:

1. which package owns a behavior;
2. which direction dependencies are allowed to flow;
3. how agents may read and request changes without bypassing the application;
4. how environment-specific behavior is added without forking Council core;
5. how an execution-relevant branch environment differs from the canonical target;
6. how candidates cross from private branch work into publication and then promotion;
7. which boundary violations automatically fail CI.

No application code needs to exist for Part 2 itself to be considered designed.
