# Part 6 - evidence, provenance, and investigation graph

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
