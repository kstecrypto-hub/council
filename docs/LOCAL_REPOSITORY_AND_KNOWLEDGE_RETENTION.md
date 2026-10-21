# Local-first repositories, checkpoint sharing, and privacy-preserving learning

**Architecture amendment approved October 14, 2026 (ADR-17 / ADR-18).** The owner approves customer-controlled local Git and scoped checkpoint snapshot sharing instead of internet-public GitHub repositories by default, and customer-controlled knowledge retention with **explicit opt-in and review** before any cross-customer generalization. The owner further specifies **success-first retrieval** and **contextual—not universal—failure learning**.

**Design status:** APPROVED DIRECTION / IN DESIGN for integration across existing Steps 2–5, 8, 10, 11, 12. **Runtime implementation:** NOT STARTED. **Tests:** NOT RUN. This file supersedes the *former default public-GitHub checkpoint and centrally reusable customer-derived knowledge* assumptions in older specifications. It does not assert an implemented local Git gateway or a completed Step 11 memory-ranking policy.

## October 15 approved Step 2 subdesign: company-local Git and read-only IRC-gateway access

**The owner accepted the Step 2 repository and peer-read architecture; this is a design approval, not implementation or full Step 2 design closure.** See [the dedicated Step 2 design record](STEP_2_CUSTOMER_LOCAL_GIT_CHECKPOINT.md).

- Five project-lifetime member repositories use **native local Git on the customer/company-controlled machine or approved private infrastructure**. No Council/vendor-hosted Git, GitHub account or third-party source transfer is necessary or authorized by default.
- On a legitimate checkpoint, freeze the members' selected commits and produce content-hashed read-only file-tree snapshots, without exporting full history or unreleased work by default.
- Members can read other members' authorized frozen snapshots via the existing **IRC-inspired Council checkpoint bridge**. A separate trusted customer-local snapshot service stores/authorizes them; large file responses use bounded artifact transfer, not group-chat messages or automatic model-context loading.
- Read access and communication share a checkpoint lifecycle, with independently verified revocation before the next private phase. Sealed review and verification-only `/work` remain intact.
- Source ownership, temporary repository cleanup, final customer-selected export, dependency/LFS/large-artifact inclusion, and any remote model/tool data egress are governed by **explicit company policy**, not vendor defaults.

**Open:** exact protocol DTOs, mount/export/import policy, partial/UNKNOWN transfer and revoke recovery, and integration into Steps 3-5 and 8. Step 2 remains **IN DESIGN**; application implementation and runtime tests remain **NOT STARTED / NOT RUN**.

## 1. Nonnegotiable data-ownership and deployment boundaries

- **Default:** a Council deployment and the five isolated member sandboxes operate on the **customer's own workstation/server or an explicitly customer-approved private deployment**. The customer controls code, checkpoint snapshots, logs, credentials, intermediate artifacts and retention.
- Council the product/vendor does **not** need to receive, mirror or host customer's Git repositories or source to perform peer review. **No internet-public publication is required or permitted by default.**
- External hosting, remote source-control integrations, telemetry, model-provider egress or vendor-managed services are **separately scoped explicit customer decisions**. Moving Git local does **not** prevent data from leaving through remote model prompts, tool network calls, source URLs or logging; permissions and egress policy must separately protect them.
- A customer's self-hosted Git service remains within their chosen trust boundary; **local-first is not the same as exposing a Git server to the public internet**. For confidentiality-sensitive deployments, the external network and inference endpoints must be restricted according to the approved contract.
- The Council *source* repo `kstecrypto-hub/council` is an independent design/development repository. None of these policies require changing its visibility or migrating the owner's documentation repo.

## 2. Git storage and checkpoint sharing: recommended MVP

Keep **real Git**, not a replacement Git dialect encoded in PostgreSQL. Git tracks file/commit history; Council PostgreSQL tracks canonical runs, artifact/snapshot permissions and review/communication states.

**Baseline MVP:** one local native Git repository/worktree per Council member, in that member's authorized persistent storage; a **trusted host-side repository/snapshot gateway** outside agent-controlled sandboxes mediates checkpoint export/delivery. Members can use Git freely in their own branch/sandbox, but cannot see other members' unshared repositories or obtain control-plane Git/host credentials.

At an all-five approved semantic checkpoint:

1. Freeze/record each member's exact commit/tree ID, candidate state, and project-specific required evidence; independently verify the fixed snapshot exists.
2. Create a **selected, immutable, content-hashed, read-only export** of the approved snapshot plus an explicit manifest. Prefer a file-tree archive/sanitized snapshot, not a complete repository with reachable ancestors/hidden refs, unless the contract specifically requires authorized history. Git `archive` exports a named tree; a Git bundle/full clone can include history and must not be treated as history-free.
3. Validate exact manifest scope; sensitive/secrets/PII/customer permissions, executable entry points, embedded dependencies, LFS/submodules, generated files and large artifacts need explicit inclusion/exclusion rules. If a safe required snapshot cannot be formed, checkpoint opening is blocked and reported—not silently widened.
4. Gateway grants authorized reviewers access to the *frozen export only* inside their scoped read-only checkpoint view or disposable verifier. The original member repository and writable workspace stay inaccessible. No general peer-to-peer path, administrator Git credentials, extra collaborator grants, or direct access to other members' persistent directories.
5. Five **sealed** assessments remain reviewer-private until the existing atomic all-five reveal. Shared messages and `/work` remain restricted to the established checkpoint session and verification-only sandbox. No code changes to the authoritative frozen candidate while reviewing.
6. On checkpoint closure, revoke fresh peer snapshot access and gateway routes, verify isolation and cleanup, retain only scope-authorized immutable references/snapshots/return packets. Previously delivered and cached information cannot be made unknowable; design retention and recovery accordingly. Only then permit new private revisions.

**Checkpoint publication now means scoped peer-visible publication inside the customer's trust boundary**, **not internet publication**. Preserve existing idempotent operation/UNKNOWN outcome semantics for gateway snapshot creation, copy, delivery, mount, revocation and cleanup. Verify success from observed storage/access state, not SQL intent. Historic PUBLIC/PRIVATE GitHub transition events remain in design history; do not emit those success events for a local-snapshot operation.

**Backend adapter boundary:** `create_repo`, `identify_version`, `freeze_version`, `export_selected_snapshot`, `verify_export_scope_hash`, `grant_checkpoint_read`, `revoke_checkpoint_read`, `archive_accepted_version`, `restore_validate`. Exact v1 DTO names, storage formats, chunking, and optional backend support remain to be designed/tested. **Native local Git is the MVP candidate**; self-hosted Forgejo and customer-approved existing GitLab/other enterprise services are optional adapters. None are prerequisite for the MVP; no need to trust a third-party hosted account. Do not install or expose Forgejo/GitLab without owner/deployment authorization.

## 3. Retention: who keeps what, where

**Tier A — active project:** customer-local Council control PostgreSQL, Git member workspaces, experiment evidence, logs and artifacts for active run. Strict user-approved access and deletion policy.

**Tier B — customer-owned reusable project knowledge:** optional durable customer-local Git/archive + content-addressed artifact store, indexed via local/private retrieval; exact successful final project and reproduction instructions may be kept **only when the customer's policy permits**. A reconstruction manifest may include pinned dependencies, environment/build/test commands, accepted source/artifact references, permissions and limitations, verified outcomes, decisions and scoped failed experiments. **No vendor access is implied**. Without retained proprietary source/binary/artifacts, an abstract recipe cannot recreate those exact files.

**Tier C — Council general knowledge:** independently authored/public-source techniques, templates and other permitted material. Customer-derived generalization is *not extracted, uploaded or shared across customers by default*. It may be added only after **separate, informed customer authorization for specific content and recipients**, plus confidentiality/privacy/IP/license screening, data minimization and provenance/consent recording. Generalized text can still be confidential or identifying; redaction alone does not establish release rights. Denial, missing approval or withdrawal handled per enforceable policy => no sharing. Do not infer shared rights from ordinary use, project acceptance, public checkpoint access or a model-generated summary.

The general library is never a covert telemetry sink. Retrieval respects tenant/workspace boundaries and the receiving customer's permitted source set. Distilled entries remain tagged with origin, authorized audience, applicable version/context, supporting *permitted* evidence, and usage/reassessment limitations. If source evidence cannot legally be retained or shared, downgrade confidence and avoid falsely claiming verification.

At close: export/validate only policy-authorized deliverables and memory before destroying the **temporary** Council control PG/sandboxes. Inability to preserve essential evidence blocks a claim of reproducibility or general proof, but must not override a customer's deletion requirements; mark unsupported claims and handle teardown under explicit retention/legal policy rather than retaining forbidden data.

## 4. Success-first retrieval; failures are conditional evidence, never blacklists

**Accepted owner correction (ADR-18):** When a member needs a previous implementation strategy, first look for **working approaches** relevant to the requested objective and current constraints. Show workable alternatives and their tested limits before exploring lessons from failed attempts. Failed approaches remain indexed, but **a previous failure never by itself excludes the approach from consideration** on a new, merely similar task.

### 4.1 Suggested retrieval and presentation contract

1. **Find applicable successes first:** rank candidate procedures, working implementations and reconstruction guides by objective/capability fit, permissions, environment and dependency versions, performance/scale/workload constraints, strength/independence of actual validation, known limitations and freshness. Do not collapse different viable strategies into a single universal winner; preserve competing alternatives and member independence.
2. **Attach contextual risk lessons:** retrieve failed/inconclusive experiments connected to those candidate strategies or current constraints. Present as warnings, counterexamples and suggested checks; keep alternative techniques discoverable. These are evidence to help test a strategy, **not a runtime prohibition or automatic hidden search filter**.
3. **Evaluate applicability, not just superficial similarity:** compare original problem, environment, software/hardware versions, configuration, workload/scale, data properties, acceptance criteria, failure mode and actual causal mechanism (if demonstrated). Record which factors match, differ, or remain unknown.
4. **Strongly matching failures may change priority, not erase choices:** if the same causal failure mechanism is well-supported under essentially identical environment, versions, scale and constraints, show a **high-confidence applicability warning** and optionally deprioritize the strategy transparently. Keep it inspectable and retestable. A known technical impossibility or explicit current requirement/permission prohibition can disallow an action through the ordinary authorization/requirements guard; a prior empirical failure is not that guard. Even an almost identical prior failure calls for rechecking whether conditions still hold. A member may choose an experiment to reconsider it.
5. **Record the new observation:** success, failure, untested, blocked or inconclusive stays scoped to the new conditions and traceable evidence. It does not retroactively turn all adjacent cases into impossible/successful.

### 4.2 Example of a contextual failure, not a ban

Bad memory: `Approach A DOES NOT WORK for database synchronization.`

Good memory: `Approach A produced lock contention on PostgreSQL version X for workload Y, at concurrency Z, with configuration C; tests T1/T2 measured the degradation. This does not establish performance under other loads/versions/transaction patterns. If reconsidering A, repeat benchmark under the new target workload and examine transaction isolation.`

If the next project has a different scale or constraints, Council **still surfaces Approach A** as a candidate and warns about the specific observed risk. Even if the problem is highly similar, it is not silently discarded: the member can test whether the same underlying mechanism still applies.

### 4.3 Memory evidence labels and safe ranking

Use context-scoped labels such as `SUCCESS_OBSERVED_IN_CONTEXT`, `FAILED_IN_CONTEXT`, `INCONCLUSIVE`, `NOT_TESTED` and `BLOCKED`. `REPRODUCED_IN_CONTEXT` can record repeated measurements, but never imply globally `PROVEN`. A failure should store observed behavior, source/test version, suspected versus demonstrated cause, uncertainty, and conditions under which it **might** be relevant.

A successful prior approach is a **starting point, not a guarantee**. Absence of an observed successful approach is not evidence that others are impossible. Retrieval must not bias all five members into copying one historical answer: all begin with the same authorized frozen library/index revision, but make independent queries, hypotheses and solution decisions.

### 4.4 Reuse and efficiency measurement

Customer-local projects can reuse their own pinned recipes/code/artifacts when authorized; the generalized library can provide applicable patterns, not proprietary implementations. Measure effects on actual token spend, number of experiments, time and solution quality against a non-memory baseline; savings are a hypothesis, not yet demonstrated.

## October 16 — Final integrated artifact, domain-neutral retention

The owner approved **five independent investigations -> evidence-based collective synthesis -> one Final Integration/Synthesis Agent -> one integrated artifact -> five original-member reviews -> user acceptance**. The integrator creates a distinct customer-owned working repository **for software** or an authorized versioned artifact workspace **for research/design/docs**, never replacing the five original member repos or obtaining writable access to their private branches. Approved immutable source/evidence from closed final comparison checkpoints is shared with the integrator only through a new scoped trusted read grant; original checkpoint grants never leak across phases. References from the final output to each meaningful earlier contribution, exclusions, compatibility choices and changed revisions follow existing source/experiment graph and retention permissions.

The long-term customer archive's *default accepted target* is the **actual versioned integrated deliverable** and authorized evidence/reconstruction manifest, **not** an automatically chosen winner from the five candidates. Original solutions, partial unsuccessful investigations and integration attempts remain attributable; retention/deletion stays separately customer-authorized. Domain-neutral research reports cannot invent data or claim unperformed validation; non-software artifacts do not require Git source. See [Step 8.4](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md). Architecture only; no implementation or tests.

## 5. Dependencies, status and outstanding decisions

- **Steps 2/3:** change member repository authority and snapshot/export records from public-visibility toggles to local customer-controlled object/scope grants, while retaining optional external-backend metadata when authorized.
- **Steps 4/5/8:** introduce distinct typed local snapshot/visibility/grant/revoke and observed results, preserving five-member barrier, sealed-review obligations and existing transaction/UNKNOWN handling. Adapt `/work` to customer-private read-only snapshots.
- **Step 10:** validate hard boundaries between member volumes, trusted gateway, other member snapshots and remote tool egress. The member remains free to spawn arbitrary workers inside its authorized sandbox.
- **Step 11:** design the authoritative retention policy, customer-local versus general memory storage/index, retrieval scoring and evidence-aware conditional failed-approach warnings. Do **not** label the entirety of Step 11 complete from this amendment.
- **Step 12:** surface customer-owned storage/egress/retention options, explicit sharing approvals, archive reconstruction evidence and risk warnings without overstating validation.

**Open design matters:** precise gateway/adapter protocol, authenticated read-only snapshot mounting, consistency and crashes during export/revoke, legacy public-GitHub migration/compatibility, exact retention/deletion and customer opt-in UX, semantic lesson metadata/index schema, pricing/benchmark measurements. No live customer's code was retrieved or modified as part of this decision.

**State:** ADR-17 local-first and ADR-18 success-first contextual failures are **APPROVED DESIGN DIRECTIONS**. Integration of older specs is not yet verified as complete; Step 11 is still **IN DESIGN** and implementation/testing across all affected steps remains **NOT STARTED / NOT RUN**.

## 6. Where the architecture design continues

**Recommended next design discussion: Step 2 local repository / checkpoint snapshot boundary.** Define the smallest native-Git + host-gateway contract able to (a) pin a member-owned commit/tree, (b) export exactly customer-authorized files and artifacts without unintentionally exposing ancestor commits or hidden refs, (c) bind recipient-specific read-only grants to the checkpoint generation, (d) verify actual content hashes and recipient access, and (e) revoke temporary access with UNKNOWN/retry reconciliation. Decide selected tree archive versus mounted snapshot, treatment of missing dependencies/submodules/LFS, and minimal storage layout. Preserve five independent private members and sealed reviews.

**After that decision:** reconcile Step **3** snapshot/access records, Step **4** typed commands/events, and Step **5** transactional external-operation guards with the selected adapter. Only then is the local-first Step 2–5 redesign ready for a design-closure assessment. Resume Step **8.3** (member phase/final candidate readiness, incomplete/blocked outcomes and termination), then Step **8.4** checkpoint/finalization integration. Complete Step **11** separately: customer-owned retention/deletion choices, opt-in generalization, evidence-backed contextual outcome records, success-first retrieval, conditional failure warnings, and strict isolation between customers. Actual Step 10/11 implementation and runtime validation require a separate build authorization.

These are **outstanding design tasks**, not runtime functionality or completed acceptance tests.


## October 21 ADR-49 — memory continuity without another store

[ADR-49 owner-approved Step 11 continuation decision](STEP_11_ADR49_GRAPH_WORKING_MEMORY_AND_CONTINUATION.md): temporary customer-controlled Council canonical PostgreSQL, typed evidence graph, member-private working notes and bounded context manifests/continuation packets are enough to persist **same-member reasoning context** during tool cooldown or context rollover. Do not persist it as a new global/tenant-shared AI memory. Recover the latest permitted graph/source material with original evidence versions; canonical tool operation/permission/budget/epoch truth always overrides memories. Do not bypass the pinned shared historical memory snapshot, five private member branches, authorized read-only checkpoint grants or customer-specific Git/archive retention. No separate graph/vector database or RAG vendor is required just to resume. **Policy APPROVED, Step 11 detailed integration IN DESIGN; no code/runtime tests.**
