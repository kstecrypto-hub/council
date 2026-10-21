# Part 6 - evidence, provenance, and investigation graph

**October 13, 2026 amendment:** [decision/status index](ARCHITECTURE_DECISIONS.md). Requirements below are specifications; application implementation is NOT STARTED and runtime tests are NOT RUN.

**Status:** DESIGNED.  
**Scope:** how an active Council project records evidence, claims, assumptions, challenges, revisions, and their provenance.  
**Implementation status:** specification only.

## 1. Purpose

Step 6 makes Council able to answer:

- What supports this conclusion?
- What evidence or assumptions does it depend on?
- What challenged it?
- What changed after review?
- Where did a piece of evidence actually come from?
- Are apparently separate findings relying on the same underlying source?

This is not the long-term cross-project memory system from Step 11.

## 2. Core rule

> The graph records provenance and explicit argument structure; it does not decide truth.

The canonical records are the source of truth. The graph is a queryable projection over them and must never become an independent authority.

## 3. Canonical record types

The active project records, at minimum:

- Source
- SourceVersion
- EvidenceItem
- Assumption
- AnalysisStep
- Claim
- ClaimVersion
- SupportGroup
- Challenge
- ChallengeResponse
- Revision
- CoverageItem

The exact SQL fields may evolve during implementation, but these concepts remain distinct.

## 4. Evidence must be attributable

Every EvidenceItem resolves back to the exact thing it came from.

Examples:

- document evidence -> source version + passage/page/section locator;
- dataset evidence -> dataset snapshot + query/rows/columns/units/transformation;
- test evidence -> repo commit + environment snapshot + command/procedure + actual result;
- tool/API evidence -> durable operation/request + actual returned result;
- user-provided assertion -> attributed user statement, not silently promoted to verified fact.

Where applicable, provenance also records:

- logical agent;
- model/profile;
- session;
- task;
- repository commit;
- environment snapshot;
- checkpoint/publication through which it became peer-visible.

There is no anonymous "the AI found this" evidence.

## 5. Evidence and claims are different

Observed material and the interpretation drawn from it are separate records.

Example:

```text
Evidence:
Hybrid recall = 93%
Vector recall = 81%

Claim:
Hybrid retrieval is preferable for this project's corpus.
```

A peer may accept the evidence while disputing the claim.

## 6. Assumptions are first-class

Assumptions are explicitly recorded when a conclusion depends on something not established as evidence.

If an assumption changes or is invalidated, dependent claims are marked for reassessment through recorded dependencies. They are not automatically declared false.

## 7. Versioned claims and review history

Substantive claim changes create new immutable ClaimVersions.

A challenge targets an exact ClaimVersion. A later Revision can record that challenge, new evidence, or another explicit reason as the cause of the change.

Example:

```text
Claim C7:v1
  <- challenged by CH12
  <- revision R5
Claim C7:v2 supersedes C7:v1
```

This lets Council answer "why did this claim change?" without inferring causality merely from timestamps.

Old claim versions remain available.

## 8. Mechanical versus interpretive relationships

The runtime may create relationships that are mechanically known, such as:

- PRODUCED_BY
- USED
- OUTPUT_OF
- FROM_SOURCE_VERSION
- FROM_REPO_COMMIT
- FROM_ENVIRONMENT
- PUBLISHED_AT_CHECKPOINT
- DELIVERED_TO
- SUPERSEDES

Agents may assert interpretive relationships such as:

- SUPPORTS
- CHALLENGES
- DEPENDS_ON
- NARROWS
- CONTRADICTS
- SHARES_UNDERLYING_SOURCE_WITH

Interpretive relationships must retain their author, justification, relevant evidence references, and review status.

The runtime must not silently promote an agent interpretation into a mechanical fact.

## 9. Support groups

When a conclusion requires multiple premises together, Council records that combination explicitly rather than flattening it into independent arrows.

Example:

```text
SupportGroup SG1:
- Evidence E1
- Evidence E2
- Assumption A1

SG1 -> supports -> Claim C4
```

Alternative support routes are represented separately.

If one member of SG1 becomes invalid or needs reassessment, Council can distinguish:

- the only support route was affected; from
- one support route was affected but another remains.

The system records support structure; it is not a formal theorem prover.

## 10. Challenges and disagreement

Challenges remain explicit records.

A challenge:

- targets an exact claim/version, assumption, analysis, or other reviewable record;
- records the challenging member;
- records the objection;
- may include evidence or a requested verification;
- retains its response/disposition history.

Disagreement is preserved rather than overwritten.

Step 6 does not require consensus and does not assign intellectual authority to the runtime.

## 11. Shared-source lineage

Different documents may depend on the same underlying study, dataset, observation, or report.

Known shared origins are recorded so Council does not treat duplicated evidence as independent corroboration.

Suspected shared origin remains a reviewable interpretation, not a fact.

The system must not produce an unjustified numerical "source independence score."

## 12. Claim/evidence status without fake precision

Step 6 does not require generic numerical truth/confidence scores.

Where useful, records may use simple review states such as:

- UNASSESSED
- SUPPORTED
- CONTESTED
- NEEDS_REASSESSMENT
- WITHDRAWN

Evidence may also preserve what kind of thing it is, for example:

- SOURCE_STATEMENT
- USER_ASSERTION
- OBSERVATION
- COMPUTED_RESULT
- TEST_RESULT
- INFERENCE
- HYPOTHESIS
- RECOMMENDATION
- SCENARIO

These labels describe provenance/role; they do not automatically certify truth.

## 13. Graph integrity

The graph is a projection of canonical records.

Requirements:

- revision/supersession chains cannot cycle;
- dependency traversal uses cycle detection;
- circular support is flagged rather than treated as independent corroboration;
- large artifacts/results remain outside graph labels and are referenced by stable IDs;
- one agent cannot silently delete another agent's challenge or rewrite recorded history.

## 14. Search fallback

Missing graph edges must not mean missing information.

Agents and the UI can still search canonical history, including:

- events;
- evidence;
- claims;
- challenges;
- publications;
- transcripts;
- repository metadata;
- task/tool history.

The graph accelerates structured traversal; it is not a brittle mandatory index.

## 15. Explicit non-goals

Step 6 does not require:

- a dedicated graph database;
- a universal ontology;
- a theorem prover;
- automatic causal inference;
- generic confidence percentages;
- automatic source-independence scoring;
- a large domain-specific evidence taxonomy.

These may be revisited only when real project/evaluation evidence justifies them.

## October 16 — approved source and integrated-version impact semantics (Step 8.4 ADR-26/28/29)

The five independent candidates/findings feed a source/evidence-bound Integration/Synthesis Blueprint. A distinct non-voting integrator may make **recorded bounded technical choices** within user-approved priorities, referencing alternatives, compatible constraints, underlying evidence, dissent and exact revised artifact versions. Graph mechanical edges record exact source/evidence/experiment/claim versions -> blueprint contribution -> integration decision/deviation -> output artifact version -> actual verification -> five-member reviewed disposition -> premortem concern (hypothetical). An integrator judgment of technical merit remains an **attributed interpretation**, not a trusted mechanical fact.

For integrated revisions, affected claims, protected checks, source dependencies and report lines are traced with existing explicit dependency/support-group relationships. **A missing graph edge is not proof of independence**. Where unchanged applicability can be demonstrated, record exact equivalence evidence; for localized substantive updates, require five authentic fresh sealed **delta reviews** of the new version and its dependent scope, while wide/high-risk/unknown changes demand full five-member sealed review. Prior PASSED results remain historical facts about their own precise versions, never assertions that an updated artifact passed without real evidence.

A frozen integrated deliverable/report pair is the exact subject of **five independently sealed six-month-plus premortem submissions**. Hypothetical risk mechanisms, present-day suggested tests and later reassessment triggers remain separate from observed evidence. Material changes invalidate affected current applicability without rewriting history. No automatic general-purpose truth scores, no fifth reviewer substitution, no fabricated studies or tests. [Full policy](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md). **Design only; not implemented or tested.**

## October 16 — ADR-26 Council Decision Register: convergence, independent evidence and dissent

Per material synthesis choice, preserve the five original member positions before public discussion *where genuinely captured in independent sealed review*, their final post-discussion positions, supported reasons for revision, their underlying evidence and possible common data/training/source overlap. The versioned Blueprint's **Council Decision Register** records the recommended approach and counterexamples/limiting conditions. A 4/5 or 5/5 consensus can be a meaningful **rebuttable qualitative preference signal** when evidence is tied, but is not independently replicated proof, a fixed weighted vote, or license to erase a minority member's reproducible defect observation. The Integrator follows the Council's evidence-backed recommendation by default. Any material deviation attaches attributed evidence/compatibility causes to the original choice and the exact updated final artifact revision for five-member re-review, not hidden model preference. This uses existing provenance graph and sealed-review infrastructure, not a sixth selector. [Detailed ADR-26 refinement](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md). Architecture only; implementation/tests NOT STARTED / NOT RUN.

## 16. Completion boundary

Part 6 is DESIGNED because the product-level behavior is fixed for:

- evidence attribution;
- separation of evidence from interpretation;
- explicit assumptions;
- claim versioning;
- challenge/revision history;
- runtime-vs-agent relationship authority;
- multi-premise support groups;
- shared-source lineage;
- graph integrity;
- searchable fallback when graph coverage is incomplete.

## October 13 verification provenance and retained learning

Executable peer tests use a separate disposable verification environment, never a reviewer's persistent branch environment. It has pinned read-only inputs and isolated scratch storage; it cannot write member repositories, continuation files, protected acceptance definitions, or control-plane state. Provider/admin credentials and unrestricted network access are absent. The requester still chooses and interprets the test. A trusted runner records actual snapshot/environment/harness hashes, command, execution outcome, and exported output hashes. Candidate-supplied tests remain distinguishable from protected acceptance checks. Recorded execution is evidence of what ran, not automatic proof of methodological adequacy.

A user-accepted candidate is eligible for retention, not automatically a validated general rule. Every reusable lesson retains applicable task/environment/version conditions, source and test evidence, limitations, failures/counterexamples, uncertainty, and reassessment triggers. Do not label empirical lessons unconditionally PROVEN. Keep the memory snapshot fixed during a run; independent retrieval must not become live cross-branch communication.

Before deleting the temporary control database, export the accepted project and selected learning/evidence to a durable Git-backed archive. Validate the transitive reference closure from a fresh archive checkout or retained artifact store, with hashes and permissions checked and no dependency on the live Council database, temporary sandbox paths, expiring URLs, or credentials. Essential missing/restricted evidence blocks teardown or requires an explicitly approved archive/retention change that honestly downgrades the unsupported lesson. Do not silently retain forbidden source data or silently delete the only evidence.

Export acceptance/contract history and relevant provenance needed by retained lessons/reports; transient sessions, leases, and caches need not be retained. Archived failed approaches remain distinguishable from accepted candidates. Temporary restore validation and cleanup must be safe to retry. Final archive visibility follows explicit authorization and is not inferred from earlier public checkpoints.


## October 21 ADR-50 — minimal ontology and per-finding graph saves

[Owner-approved immediate evidence-graph updates](STEP_11_ADR50_MINIMAL_OPERATION_ONTOLOGY_AND_IMMEDIATE_EVIDENCE_PERSISTENCE.md): keep the graph a **projection over canonical Step 5 operation/attempt, Step 6 evidence/claim and Step 8 experiment/finding records** with a deliberately small general-purpose `Actor, Operation, Observation, Artifact, Finding, Hypothesis` reference vocabulary. Broker-observed actual action/tool/result links are mechanical (`RUNTIME` origin); reasoning agents supply semantic `SUPPORTED_BY`, `SUPPORTS`, `CONTRADICTS`, `TESTS`, `REVISES` relationship interpretations **as part of their existing action/findings**, with source IDs and attributable reasons, not through a second LLM interpretation pass. A substantive claim and its essential evidence relationships and event commit **immediately and atomically**; no loss window awaiting a periodic memory rewrite. Mere tool errors and repeated routine operations remain auditable in Step 5 without forcing extra semantic graph nodes, working-context summaries or graph retrieval. Search/visual indexes may update asynchronously with an explicit event watermark and consistent canonical fallback. Do not promote tool text to authority, infer test PASS from exit code alone, or leak private-branch evidence across the five member scopes. **Owner-approved design only, implementation NOT STARTED, runtime/security/token tests NOT RUN.**
