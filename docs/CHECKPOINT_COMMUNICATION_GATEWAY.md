# Checkpoint Communication Gateway

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

At checkpoint opening, runtime:

1. records each participating repository and exact opening commit;
2. grants participating peers reciprocal read access to the authorized repositories;
3. creates the checkpoint communication session;
4. creates checkpoint-scoped member credentials;
5. enables the temporary environment-to-gateway routes;
6. verifies membership/connectivity;
7. enters the communication/review period.

At checkpoint closure, runtime:

1. stops accepting new checkpoint messages;
2. drains already accepted messages where applicable;
3. persists the final transcript and communication metadata;
4. records closing repository commits;
5. revokes checkpoint credentials;
6. removes environment-to-gateway routes;
7. destroys the checkpoint communication session;
8. revokes reciprocal peer repository access;
9. verifies revocation;
10. returns Council members to private work.

The persistent gateway process may remain alive. An existing gateway process does not imply that agents are able to communicate.

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

A TEST_REQUEST is a peer communication request, not an automatic task assignment. The target Council member remains intellectually and operationally autonomous: it may run the requested test, reject/dispute the premise, defer it, or answer from its own inspection. Because participating members have read access to peer repositories during the checkpoint, the requesting member may also clone/run/test the peer candidate independently in its own environment. The communication protocol must not silently create work inside another branch merely because one peer requested it.

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

The exact DONE/ACTIVE/quiescing state contract will be specified in Part 4.

A normal /done request succeeds only when:
- the member has no required OPEN/unacknowledged peer actions;
- any required items have an explicit disposition;
- the member has no accepted outbound message still pending delivery.

A new message/action that explicitly requires a DONE member's attention may return that member to ACTIVE before checkpoint closure.

## 7. Network and capability implications

The invariant "Council members cannot communicate between checkpoints" cannot depend on prompt obedience.

Therefore unrestricted arbitrary sandbox networking cannot be treated as compatible with strict checkpoint isolation.

External access must be mediated by Council-controlled capabilities/gateways where communication side effects matter. Examples include:
- model/provider gateway;
- research/web capability;
- Git/repository capability;
- checkpoint communication gateway.

Between checkpoints:
- peer repository access is absent;
- checkpoint communication sessions are absent;
- checkpoint credentials are invalid/absent;
- checkpoint gateway routes from the agent environments are absent.

The exact broader outbound-network policy is a later environment/capability design decision, but it must preserve the no-out-of-band-peer-communication invariant.

## 8. GitHub/repository administration

Council members own and develop their own repositories, but an agent sandbox must not require unrestricted GitHub-account administration authority in order to push its work.

Repository-content authority and repository-administration authority should remain separable.

The trusted runtime is responsible for checkpoint-related peer access grants/revocations. A Council member must not be able to bypass checkpoint isolation by permanently adding peers, changing visibility, or otherwise administratively exposing its repository outside the checkpoint policy.

Exact Git credential and administration mechanics remain implementation details for a later contract.

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
- repository-access grant/revocation events;
- communication-route creation/removal events;
- whether closure was normal or ceiling-forced.

Agents may retain information they legitimately learned during the checkpoint. Closing communication prevents access to **new** peer information; it does not attempt to erase already shared knowledge.

## 10. Future distributed deployment

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

## 11. Still to decide

The next design pass must decide:
- exact local stream framing/transport;
- runtime-bridge authentication and checkpoint-scoped authorization;
- maximum logical message/action sizes;
- exact message/action schemas and protocol versioning;
- reply/thread semantics beyond parent message/action references;
- exact /done wire representation and ACTIVE/DONE/DISCONNECTED state transitions;
- reconnect/replay behavior inside an active checkpoint;
- bounded communication ceilings;
- transcript/event schemas;
- which structured peer actions, if any, become first-class investigation-graph nodes automatically.
