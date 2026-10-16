# Checkpoint Communication Gateway

**October 13, 2026 amendment:** [decision/status index](ARCHITECTURE_DECISIONS.md). Requirements below are specifications; application implementation is NOT STARTED and runtime tests are NOT RUN.

**Status:** approved architecture baseline; protocol command surface still to be finalized.  
**Scope:** temporary Council-member communication during Orchestrator-defined project checkpoints.  
**Implementation status:** specification only.

## 1. Deployment model

Each Council deployment runs its own lightweight **Checkpoint Communication Gateway** on the same trusted control plane as the Council application.

The gateway is persistent deployment infrastructure. Communication capability is not persistent.

A checkpoint creates an ephemeral communication session containing:
- checkpoint-specific room/session identity;
- participating Council-member identities;
- short-lived checkpoint credentials;
- temporary sandbox-to-gateway reachability;
- message/transcript state;
- per-member communication-completion state.

When the checkpoint closes, those checkpoint-specific resources are destroyed or revoked.

The architecture does **not** require a global Council communication server. Local deployments must be able to operate without routing Council discussion through Council-operated central infrastructure.

A managed remote relay may be added later for distributed Council deployments whose agents execute on different machines/networks. It is an optional transport backend and must preserve the same checkpoint isolation and authorization semantics.

## 2. Security boundary

There is never a direct sandbox-to-sandbox communication route.

All Council-member communication during a checkpoint traverses the Checkpoint Communication Gateway.

The communication client may exist inside an agent-controlled execution environment, but communication authority remains outside that environment in the trusted Council runtime.

An agent may copy, modify, or keep the client executable. That must not let the agent communicate when no checkpoint communication session is active.

Communication requires all of:
- an active checkpoint communication session;
- an authorized Council-member identity;
- a valid checkpoint-scoped credential;
- runtime-authorized membership in that checkpoint session;
- an active runtime network route from the member environment to the gateway.

Checkpoint closure invalidates/removes these conditions.

## 3. Checkpoint lifecycle integration

All five members reach an outcome-based semantic barrier. Early arrivals freeze their candidate and release execution capacity; blocked, intentionally paused or budget-exhausted members release capacity under the whole-member scheduler without being counted as ready. No mandatory periodic private-work slices exist. No failed/blocked member is silently excluded. A one-slot deployment rotates the same five logical agents through all stages.

Each member owns its own **customer-controlled local Git repository** in its sandbox storage. A trusted local repository/snapshot gateway—not public GitHub—creates a content-hashed, selected, frozen, read-only checkpoint export. At the approved semantic milestone, the gateway grants each authorized reviewer **only the approved frozen snapshot**, not the member's full Git history or writable/private workspace. Verified snapshot content, approved source/data scope, exact source/tree hash and recipient read grants are distinct canonical records. See [local repository and memory architecture](LOCAL_REPOSITORY_AND_KNOWLEDGE_RETENTION.md).

**Internet-public repository publication is no longer the default.** Any optional public/hosted export is a separately approved external operation. Local checkpoint sharing stays entirely in the customer's chosen trust boundary; owning the source does not mean Council the vendor receives it. Missing/unscannable files, sensitive material, unexpected LFS/submodule dependencies or unsafe snapshot content block grant until resolved.

Checkpoint OPENING verifies the full five-member frozen snapshot set, manifest hashes and intended read-only recipient access. During closing the runtime revokes each temporary snapshot grant/route and proves isolation before private development resumes. Previously received source information may be known to reviewers; revocation prevents additional access but does not promise to erase their memory. Partial/unknown grants or revocations are reconciled, not treated as successes. No member can acquire another's write/admin credential or open a direct cross-sandbox connection.

Checkpoint sequence: all-five member arrivals -> freeze approved local snapshot exports -> scoped verified peer grants -> SEALED_REVIEW -> shared REVIEWING -> CLOSING -> verified access/route revocation -> CLOSED/private revision.

During SEALED_REVIEW each member independently submits an immutable assessment bound to the checkpoint, candidate SHAs, reviewer identity, evidence, objections, and proposed tests. The gateway withholds peer assessments and shared debate until every required member has submitted. Reviews remain in scoped canonical storage, never in a public repository or shared retrieval cache before reveal. Finite slices/budgets apply; a missing reviewer blocks the reveal barrier or produces an explicitly incomplete/aborted review, never a fabricated fifth assessment. No fixed skeptical personas or forced disagreement are required.

Executable peer tests use a separate disposable verification environment, never a reviewer's persistent branch environment. It has pinned read-only inputs and isolated scratch storage; it cannot write member repositories, continuation files, protected acceptance definitions, or control-plane state. Provider/admin credentials and unrestricted network access are absent. The requester still chooses and interprets the test. A trusted runner records actual snapshot/environment/harness hashes, command, execution outcome, and exported output hashes. Candidate-supplied tests remain distinguishable from protected acceptance checks. Recorded execution is evidence of what ran, not automatic proof of methodological adequacy.

Runtime creates checkpoint-scoped gateway membership/credentials during opening, but shared send/replay is gated off during SEALED_REVIEW. SubmitIndependentCheckpointReview records a private immutable assessment. RevealCheckpointReviews publishes those records to all five participants atomically only after all required submissions exist; shared discussion then begins.

On normal closure, atomically fence new review messages, persist the final transcript/closeouts and completion frontier, terminate work excursions and checkpoint authority/routes, revoke temporary customer-local peer snapshot grants, verify observed grant/route isolation, create deterministic return packets, and emit CheckpointClosed. Each external operation remains recoverable rather than hidden inside a SQL transaction. Forced closure preserves its reason and unperformed work and never masquerades as full review.

The persistent gateway process may remain running without any active communication authority. Inactive members receive ordered backlog and current obligations on resumption; they do not receive another member's sealed assessment prematurely.

**October 15 owner-approved Step 2 boundary:** Peer snapshot tree/file/pinned-artifact **read requests** use the same narrow member-facing IRC-inspired checkpoint bridge, but a separate trusted customer-local Git/snapshot service outside all sandboxes holds and authorizes source. The gateway is not a Git server or repository owner. Company-local member Git workspaces remain private, frozen exports are immutable/hash-verified/read-only, and sizeable data travels in bounded verified response streams rather than shared IRC chat or prompt context. Communication permissions and snapshot access close together, with separately verified grant revocation. Precise DTOs and transfers remain IN DESIGN; implementation/tests NOT STARTED / NOT RUN. [Details](STEP_2_CUSTOMER_LOCAL_GIT_CHECKPOINT.md).

## 4. Communication model

IRC/IRCv3 is the design reference, not the exposed protocol.

Agents do **not** receive a raw IRC socket or direct access to a general-purpose IRC server. Instead, each agent uses a minimal Council-controlled local message stream. A runtime-side bridge outside the sandbox forwards only authorized checkpoint traffic to the Checkpoint Communication Gateway.

Conceptually:

```text
Agent
  -> local Council chat stream/client
  == sandbox boundary ==
  -> runtime communication bridge
  -> Checkpoint Communication Gateway
```

The agent-visible surface is intentionally small. It supports:
- sending a checkpoint message;
- receiving ordered checkpoint messages;
- fixed Council-member identities;
- checkpoint presence/status;
- keepalive/connection health;
- structured peer actions;
- completion signaling such as /done.

There is no agent-visible concept of arbitrary channels, IRC operators, direct client connections, private IRC messaging, CTCP/DCC, invites, modes, channel creation, or federation.

The room is shared by all participating Council members. A message may target another member for attention, but it remains visible to the checkpoint participants unless a future explicitly approved protocol revision says otherwise.

The protocol reuses the useful semantics learned from IRC/IRCv3—server-mediated identity, shared-room conversation, ordering, message IDs, server timestamps, replies, presence, and keepalive—without inheriting IRC's unnecessary command surface or legacy message-size constraints.

Logical messages may be arbitrarily larger than one transport frame, subject to a configurable resource ceiling. The local stream/runtime bridge transparently fragments a logical message into smaller frames, and the gateway reassembles and verifies it before exposing it as one accepted message. Agents do not reason about chunks.

A logical message records at least:
- client request/message correlation ID;
- server-assigned immutable message_id;
- total logical length;
- frame/chunk count;
- content hash/checksum;
- complete reconstructed body.

Partial messages are never exposed as valid Council communication. Missing/corrupt fragments cause retry/reconciliation or explicit message failure.

The local agent-facing stream may be backed by a local socket/pipe or another narrow transport. The agent should not need to know the gateway's network topology, long-lived credentials, or host address. The runtime bridge owns external connectivity and can remove that route completely when the checkpoint closes.

## 5. Structured peer actions without losing detail

Checkpoint communication has two layers:

1. **complete natural-language conversation**, preserved verbatim; and
2. **structured peer actions**, used to index important communication and track obligations.

Structured actions never replace the underlying text.

The authoritative detail source for a peer action is always its retained full body plus the exact referenced artifacts/messages. A short structured summary is metadata only.

Initial structured action types:

- QUESTION
- CHALLENGE
- FINDING
- TEST_REQUEST
- TEST_RESULT
- PROPOSAL

The originating Council member explicitly declares the semantic action type through the agent-visible command surface. The runtime does not use another model to infer whether a message is a question, challenge, finding, test request, test result, or proposal.

Examples of the intended agent surface include:

```text
/question @Council-B <full logical message>
/challenge @Council-A <full logical message>
/finding <full logical message>
/test-request @Council-C <full logical message>
/test-result <action_id> <full logical message>
/proposal <full logical message>
/reply <action_id> <full logical message>
/done
```

Exact syntax remains versionable, but semantic classification belongs to the originating agent.

A structured action contains, at minimum:

- action_id;
- action_type;
- originating member;
- target member(s), when applicable;
- checkpoint_id;
- server-assigned message_id;
- full immutable text body;
- optional short label/summary;
- reply_to_message_id or parent_action_id when applicable;
- repository reference(s);
- exact commit SHA(s) when code/artifacts are discussed;
- optional path/line/test/evidence reference(s);
- whether a response is required;
- current disposition;
- created/server timestamp.

The structured fields are pointers and workflow metadata, not a lossy rewrite of the action.

### 5.1 Detail-preservation rules

The system must preserve all of the following:

- the exact original message body;
- every follow-up/addendum linked to the action;
- exact repository commit/path/test references supplied by the agent;
- every response linked by message/action ID;
- the action's state/disposition history.

An agent may append an **ADDENDUM** to an existing action rather than editing history in place.

Automatic summaries, UI labels, embeddings, or model-generated descriptions may help retrieval but are never authoritative substitutes for the retained original text.

### 5.2 Promoting ordinary conversation

Agents do not have to predict perfectly whether something will become important.

An ordinary message may later be promoted into a structured action by referencing its immutable message ID. Promotion does not rewrite or duplicate the original message; it attaches action metadata to the existing retained communication.

This prevents the protocol from forcing agents to choose between natural discussion and rigid forms.

### 5.3 Action dispositions

Actions that require follow-up are tracked until they receive an explicit disposition.

Initial dispositions:

- OPEN
- ACKNOWLEDGED
- RESOLVED
- DISPUTED
- DEFERRED
- WITHDRAWN
- NOT_APPLICABLE

A checkpoint does not require consensus. A CHALLENGE may close as DISPUTED and remain visible as an unresolved disagreement. A TEST_REQUEST may close as DEFERRED with a reason if it cannot be completed within the checkpoint.

A TEST_REQUEST is a peer communication request, not an automatic task assignment. The target Council member remains intellectually and operationally autonomous: it may run the requested test, reject/dispute the premise, defer it, or answer from its own inspection. Because participating members have read access to peer repositories during the checkpoint, the requesting member may also clone/run/test the peer candidate independently in a separate disposable verification environment. The communication protocol must not silently create work inside another branch merely because one peer requested it.

The runtime must never turn silence into RESOLVED.

### 5.4 Preventing important actions from being missed

Each member receives an **open-action queue** in addition to the chronological transcript.

On reconnect, the gateway replays:
- missed full messages; and
- all open structured actions relevant to that member.

A member's /done cannot silently bypass required peer obligations. If required actions addressed to that member remain OPEN or merely unacknowledged, the gateway rejects /done or returns a structured warning requiring an explicit disposition first.

This does not force agreement. The member may respond and mark the item RESOLVED, DISPUTED, DEFERRED, or another valid terminal disposition.

Informational FINDING/TEST_RESULT actions need not block /done unless explicitly marked as requiring acknowledgement.

The core invariant is:

> Structure ensures important items are findable and dispositioned; the complete verbatim communication ensures technical detail is never compressed away.

## 6. Completion signaling

Council members receive a small explicit command surface. At minimum the design includes a completion command exposed to the agent as:

```text
/done
```

A member using /done signals that it currently considers its communication obligations for the checkpoint complete.

This is not an immediate disconnect. If new checkpoint communication validly requires that member's attention before closure, the member may return to an active communication state.

Normal checkpoint communication closure occurs when all required participants are done and no accepted messages remain pending, subject to a bounded fallback/ceiling so a failed or looping agent cannot keep a checkpoint open indefinitely.

The AVAILABLE/WORKING/DONE/DISCONNECTED states and version-bound completion guards are defined in Part 4 and the October 13 refinements below; wire framing and executable integration remain pending.

A normal /done request succeeds only when:
- the member has no required OPEN/unacknowledged peer actions;
- any required items have an explicit disposition;
- the member has no accepted outbound message still pending delivery;
- its processed message frontier and expected obligation version match the current checkpoint generation;
- it has no active verification work, and the completion decision is committed under the same guard as message/action acceptance and closure.

A new message/action that explicitly requires a DONE member's attention invalidates its completion certificate and returns that member to AVAILABLE before checkpoint closure.

### 6.1 Communication and work are mutually exclusive per member

Checkpoint discussion does not globally freeze all agents. Instead, each Council member may alternate between communication and a bounded work excursion.

Initial member activity states:

- AVAILABLE — participating in checkpoint communication;
- WORKING — temporarily executing bounded work and unable to communicate live;
- DONE — no current communication obligations;
- DISCONNECTED — unexpectedly unavailable from the communication stream.

A member may enter bounded work explicitly, for example:

```text
/work TR-18
```

where the argument references the QUESTION, CHALLENGE, TEST_REQUEST, or other peer action that motivated the work. A member may also initiate bounded work for an independently identified verification need, provided the reason is recorded.

When a member enters WORKING:

- it cannot send checkpoint chat messages;
- it does not receive live conversational interruptions;
- only the verification/testing tool surface required for the bounded work becomes available;
- other Council members continue communicating normally;
- all new messages/actions addressed to the working member are accepted, durably ordered, and queued;
- peer repo visibility remains limited to the checkpoint-authorized snapshots/access policy;
- the working member's activity is visible only as a coarse runtime state, not as a live terminal/tool stream.

WORKING is verification-only. It may run tests, reproduce failures, benchmark, inspect logs, execute existing code, compare outputs, inspect checkpoint-visible repositories, and generate temporary test evidence.

WORKING may not modify the authoritative candidate. It may not edit source code, refactor, add features, alter architecture, commit, or push.

Executable verification must run in a separate disposable verifier with pinned checkpoint inputs, no writable reviewer workspace/continuation mounts, and externally retained execution evidence. Temporary test-side mutations, generated files, or harness changes remain disposable and cannot become authoritative candidate changes during the checkpoint.

When bounded work completes, fails, or reaches its runtime ceiling, the member returns to AVAILABLE and receives:
- every complete queued logical message in order;
- every newly created structured action relevant to it;
- its refreshed open-obligation queue;
- the recorded outcome/status of the work excursion.

The member may then publish a TEST_RESULT/FINDING/reply or continue discussion.

The invariant is:

> Communication and execution are mutually exclusive per Council member, not globally per checkpoint.

This permits A and C to continue discussion while B is running a requested test, without interrupting B or losing anything addressed to B.

### 6.2 Bounded work excursions

/work does not reopen unlimited private development. It creates a checkpoint-scoped, bounded work excursion with durable provenance.

A work excursion records at minimum:
- work_excursion_id;
- member_id;
- checkpoint_id;
- triggering action/message, if any;
- stated reason;
- exact frozen/disposable snapshot identity used;
- start/end timestamps;
- completion/failure/ceiling outcome;
- temporary artifacts/results the member later chooses to cite.

Runtime resource/time ceilings prevent an agent from using /work to abandon checkpoint discussion indefinitely.

A checkpoint work excursion must never create authoritative repository commits. Any implementation implied by a test result happens only after checkpoint communication closes and the member returns to private development.

This prevents an infinite checkpoint loop in which discussion causes a fix, the fix creates new review surface, and the checkpoint repeatedly reopens implementation work.

A TEST_REQUEST remains advisory. The target member decides whether to enter /work, answer from existing evidence, dispute the request, or defer it. The requesting member may independently test the peer's checkpoint-visible repository in a separate disposable verification environment.

## 7. Network and capability implications

The invariant "Council members cannot communicate between checkpoints" cannot depend on prompt obedience.

Therefore unrestricted arbitrary sandbox networking cannot be treated as compatible with strict checkpoint isolation.

External access must be mediated by Council-controlled capabilities/gateways where communication side effects matter. Examples include:
- model/provider gateway;
- research/web capability;
- Git/repository capability;
- checkpoint communication gateway.

Between checkpoints:
- live access to new unpublished peer repository work is absent; previously authorized frozen snapshots may remain available;
- checkpoint communication sessions are absent;
- checkpoint credentials are invalid/absent;
- checkpoint gateway routes from the agent environments are absent.

The exact broader outbound-network policy is a later environment/capability design decision, but it must preserve the no-out-of-band-peer-communication invariant.

## 8. Local repository / snapshot gateway administration

Each member may use local Git freely inside its own authorized sandbox and persistent workspace. The **trusted local snapshot gateway outside member control** owns temporary peer-grant authorization, fixed snapshot exports, read-only mounts, revocation and verification. Members do not need any third-party Git account credentials for MVP operation.

Content authority over a member's own files is not administrative authority over other members' storage, local gateway routes or protected harnesses. A member cannot permanently grant peer access or bypass checkpoint communication boundaries. Optional customer-owned Forgejo/enterprise Git adapters must preserve the same guarantees. Exact gateway authorization and mount protocols are Step 10/Step 12 implementation work.

## 9. Persistence and provenance

The live communication session is ephemeral. Its transcript is durable.

For each checkpoint Council retains, at minimum:
- checkpoint identity and semantic milestone;
- participating Council members;
- opening repository commit per participant;
- communication-session start/end;
- ordered message transcript;
- sender identity for each message;
- completion-state transitions such as /done;
- formal challenges/findings linked from the discussion where applicable;
- closing repository commit per participant;
- local snapshot export/grant/revoke requests and verified outcomes, manifest hashes, partial grant/revocation failures, and any separately user-authorized external publication history;
- communication-route creation/removal events;
- whether closure was normal or ceiling-forced.

Agents may retain information they legitimately learned during the checkpoint. Closing communication prevents access to **new** peer information; it does not attempt to erase already shared knowledge.

## 10. Checkpoint return to private development

When checkpoint communication closes, each Council member receives a deterministic **Checkpoint Return Packet**. The packet is evidence and context for the next private phase, not an instruction set from the runtime.

For each member, the packet includes at minimum:
- checkpoint identity and semantic milestone;
- that member's frozen opening snapshot/commit;
- exact peer snapshots/commits that were legitimately visible during the checkpoint;
- a reference/index to the complete durable checkpoint transcript;
- structured peer actions relevant to the member and their final checkpoint dispositions;
- test results, findings, and other evidence produced during checkpoint verification;
- unresolved/disputed items that remain relevant;
- the member's own checkpoint closeout statement.

### 10.1 Agent-authored closeout

Before the checkpoint fully closes, each participating member provides a short agent-authored closeout describing what it intends to carry back into private development: issues to revisit, evidence it accepts or disputes, comparisons it wants to make, and other conclusions it considers relevant.

The runtime does not generate or rewrite this intellectual closeout. It stores and returns it alongside the objective checkpoint record.

### 10.2 Evidence, not orders

Unresolved challenges, questions, and test results become revision inputs. They do not automatically become implementation tasks and do not give one Council member authority over another member's branch.

A member may respond in its next private phase by changing its approach, investigating further, proving a peer concern wrong, or leaving the branch unchanged with its own reasoning.

### 10.3 Frozen peer knowledge

A member may retain a frozen local copy/reference of peer repository snapshots it was legitimately authorized to inspect during the checkpoint. Those snapshots never update after the checkpoint closes.

This preserves a precise information boundary: knowledge legitimately shared through the checkpoint remains available, but later peer development remains private until the next authorized checkpoint.

### 10.4 Transcript availability versus prompt injection

The full transcript remains durably retrievable, but it is not automatically injected in full into every subsequent model context.

The default return context contains the member's closeout, relevant structured actions, evidence/test results, exact snapshot references, and transcript/message identifiers. Full verbatim discussion can be retrieved when needed.

### 10.5 Cross-checkpoint action history

Structured actions survive checkpoint closure as historical provenance. Their checkpoint disposition remains recorded. A later checkpoint may reference or supersede an earlier action without reopening the old communication session.

This gives the overall project loop:

```text
private independent work
-> semantic checkpoint reached
-> pin candidate versions and validate customer-authorized snapshot manifests
-> verify selected immutable read-only local peer snapshot grants
-> sealed independent review by all five members
-> reveal assessments and open shared discussion
-> verification-only /work as needed
-> all members done
-> agent-authored closeouts
-> close communication, revoke local snapshot grants/routes and verify isolation
-> deterministic return packets
-> private revision
-> next semantic checkpoint
```

The core rule is:

> A checkpoint gives each Council member evidence, criticism, and peer knowledge; the member itself decides how that information changes its next private branch.

## 11. Future distributed deployment

If Council members later execute across different physical hosts, the same logical interface may use a remotely hosted relay.

The abstraction remains:

```text
CheckpointCommunicationGateway
  -> Local deployment backend
  -> Optional managed relay backend
```

A remote relay must not change:
- checkpoint-scoped identities;
- membership isolation;
- credential expiry;
- transcript semantics;
- completion signaling;
- hard shutdown behavior;
- repository visibility rules.

Multi-tenant hosting, if ever implemented, is an infrastructure optimization rather than the security model. The protocol must behave as though each Council deployment owns an isolated communication authority.

## October 16 — Step 8.4 final comparison and post-integration five-member review

The owner approved **one final integrated deliverable** rather than a default vote for the best of five unrelated outputs. The existing IRC-inspired **typed command-only** gateway remains the only member communication and approved peer-object request surface for (1) final five-investigation comparison, then (2) **five original members independently reviewing the actual integrated version** in a later separated frozen review. Each phase retains five genuine sealed assessments/atomic reveal, full messages/actions, verification-only `/work`, current generation and /done frontiers, faithful closeouts, actual verified snapshot access revocation and no file+chat bundling. A member who concluded a negative investigation participates as a reviewer without being represented as having built a working candidate.

The Integrator is a separate non-voting *execution* identity, not an IRC sixth member; it receives server-resolved authorized immutable source/evidence objects only under a **new explicit integration grant** after comparison checkpoint closure and cannot send agent-controlled files or mount other member workspaces. The integration result gets a **new pinned artifact identity** and post-integration review scope; material revisions do not inherit the old five reviews automatically. The same scheme applies to research/docs/engineering designs via approved non-code artifact types. Detailed v1 framing, transfer/snapshot grant and re-review generation contracts still IN DESIGN; no implementation/tests. [Details](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md).

## October 16 Step 8.4 approved delta/full reviews and independently sealed premortem (ADR-28–29)

Preserve current five-member identity, immutable source/object read grants, typed text-only message and content-request separation, all-five sealed review privacy, atomic reveal and checkpoint frontiers. **Initial actual integrated output** receives five sealed original-member reviews. A **new substantive integrated output version** opens a distinct generation bound to the exact content hash: five **scoped/delta** submissions where defensible dependency closure proves local scope, or five **full** new submissions for widespread, high-risk or uncertain impact. A model declaring cosmetic equivalence is not enough to reuse old assessments; only supported unchanged applicability can survive. Missing fifth assessment or late old-version review cannot silently advance a barrier.

The six-month-plus premortem is a **separate SEALED_PREMORTEM** round against one immutable pair (integrated artifact version + provisional report revision), with five authentic independently drafted member analyses and **one atomic all-five reveal**. Member narratives remain secret across IRC, retrieval, cache, UI and shared graph read surfaces until reveal; treat premises as hypothetical. Later material version changes invalidate affected applicability and trigger scoped/full new premortem review as appropriate. No sixth-member integrator review, no raw file attachments, no editable authoritative candidate during `/work`, and no user-approval bypass. Exact DTO/generation, cancellation/reconnect and reliable closure still IN DESIGN. [Step 8.4 §9](STEP_8_4_COLLECTIVE_SYNTHESIS_AND_FINAL_INTEGRATION.md). Runtime NOT STARTED, tests NOT RUN.

## October 16 approved Step 8.5A — structured Council decisions and Blueprint handoff

During the final five-member comparison checkpoint, meaningful positions, reasons for changes, evidence, challenges, recommended integration direction, and minority objections are **actual authenticated original-member structured peer actions** under the existing gateway. The trusted backend may compile them into a Blueprint/Decision Register, but cannot invent missing member agreement by summarizing a transcript. Members can raise misattribution or omission challenges through the existing required-action/obligation/frontier protocol.

The **frozen immutable Blueprint** is not the same as an **executable Integrator handoff**. Freeze must bind exact source versions, permitted manifests, authenticated member authorship, sealed-review reveal and current discussion generation/frontier. Actual Integrator admission requires **normal five-member /done and closeout, no outstanding required communication or verifier work, closure fenced under current generation, and independently observed revocation of all final-comparison grants/routes**. An explicitly forced-incomplete closeout may retain a truthful report but is not authorization to treat Blueprint as executable; legitimate DISPUTED/DEFERRED conclusions survive as disclosed conditions without blocking mechanically complete dialogue. Fresh integrator grants are independently authorized after closure. Existing text-only command/file-result separation, moderation/data egress, minority obligations, and no sixth peer remain unchanged. [Details](STEP_8_5_STRUCTURED_COUNCIL_BLUEPRINT_HANDOFF.md). Design only, no runtime or tests.

## October 16 Step 8.5B — exact immutable integrated-output review handoff (ADR-32–35)

After [Step 8.5A](STEP_8_5_STRUCTURED_COUNCIL_BLUEPRINT_HANDOFF.md) genuine verified Blueprint handoff, a single persistent non-voting Integrator works under separately granted scope. **It cannot open a review merely by writing `output ready`**. Trusted runtime must separately observe the pinned result's actual content hash, allowed evidence/manifest, safe whole-integrator suspension/fenced writes and relevant UNKNOWN effect reconciliation. Only then may existing gateway open a **new, read-only review generation over that exact integrated artifact** for the **original five Council member identities**. Do not repurpose the final-comparison checkpoint's grants or treat the Integrator as a sixth reviewer. All five authenticate and independently submit sealed evaluations of the identical pinned target; atomic five-review reveal, no direct files, verification-only `/work`, missing-reviewer guards, actual closeout/revoke and evidence lineage remain.

A material new integrated revision is authored in the same logical Integrator's own reopened execution interval after current review closes and grant revocation is observed. Revised artifact identity is new; old reviewed hashes and passing checks remain historical. The new five-member review follows approved ADR-28 delta/full impact scopes, and frozen-integrated-report premortem follows ADR-29. Backend crash/replay preserves exact review target/generation and does not reveal partial assessments or duplicate reviewed output. [Step 8.5B](STEP_8_5B_FINAL_INTEGRATOR_EXECUTION_AND_RECOVERY.md). No implementation or tests.

## October 16 — approved 8.5C+D simultaneous-submission protocol (ADR-36–40)

[Combined Step 8.5C+D contract](STEP_8_5C_8_5D_COMMAND_STATE_RECOVERY_AND_FINALIZATION.md) approves lightweight bounded **per-current-checkpoint/review/premortem-generation internal API dispatch queues** to serialize conflicting submissions without forcing artificial arrival-time separation. The original five members can submit simultaneously: each authenticated seat's immutable sealed assessment is preserved, with one private row/seat/generation and existing **atomic all-five reveal only after the fifth genuine committed submission**. API queues improve contention but cannot replace PostgreSQL current message/obligation frontier locks, canonical event-clock ordering, idempotency, generation guards, cross-instance concurrency safety, private graph/UI/transport scopes or verified external read-grant revocation. In-memory queue ACKs are not durable acceptance. Revision and premortem scopes stay bound to immutable artifact/report hashes; no sixth integrator seat or additional gateway/microservice. Spec only, no implemented queues or tests.

## 12. Still to decide

The next design pass must decide:
- exact local stream framing/transport;
- runtime-bridge authentication and checkpoint-scoped authorization;
- maximum logical message/action sizes;
- exact message/action schemas and protocol versioning;
- reply/thread semantics beyond parent message/action references;
- exact /done wire representation and integration of AVAILABLE/WORKING/DONE/DISCONNECTED transitions with versioned completion frontiers;
- reconnect/replay behavior inside an active checkpoint;
- bounded communication ceilings;
- transcript/event schemas;
- which structured peer actions, if any, become first-class investigation-graph nodes automatically.

## October 13 completion and verification guards

Communication completion, verification coverage, candidate readiness, and user acceptance are separate records. DISPUTED or DEFERRED can satisfy a response obligation without resolving the underlying risk or passing an acceptance criterion. Required checks remain NOT_RUN, BLOCKED, FAILED, or PASSED with evidence; an explicit policy waiver is recorded separately and is never a test pass. Forced closure records incomplete review and outstanding obligations.

MarkCheckpointCommunicationDone carries checkpoint_generation, processed_message_sequence, and expected_obligation_version. Under the same checkpoint lock/version guard used to accept messages/actions and close the checkpoint, reject stale declarations, unanswered required obligations, unprocessed required messages, or active verification work. A relevant accepted message or new required action invalidates the affected DONE certificate and reactivates that member. Delivery to a socket is not evidence of processing. Internal bookkeeping alone must not endlessly invalidate completion. Close atomically only after current certificates cover the current review/obligation frontier; record ceiling-forced closure distinctly.

The UI and final review expose communication_closed, verification_coverage, candidate_readiness, and acceptance_decision independently. An incomplete candidate may be presented for an informed user decision where the existing contract allows it; presentation or acceptance does not alter failed/unperformed verification.


**October 16 owner simplification (supersedes earlier ADR-40 queue requirement):** Do **not** add per-key internal-API submission queues, queue-specific DTOs or a new failure-recovery manager. Reuse the existing **Step 7 low-spec whole-agent scheduler**, existing **Step 5 PostgreSQL transaction/locks/idempotency/outbox** for simultaneous submissions, and **Docker persistent volumes/container lifecycle** for infrastructure recovery. The existing trusted runtime—not Docker—still owns agent permissions/checkpoint/budgets and reconciliation of uncertain external API/Git/provider effects. ADR-36–39 remain approved; ADR-40 is **SUPERSEDED**. [Authoritative lean 8.5C+D specification](STEP_8_5C_8_5D_COMMAND_STATE_RECOVERY_AND_FINALIZATION.md). **Architecture only, no runtime implementation or tests.**
