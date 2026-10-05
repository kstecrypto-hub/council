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

The interaction model is IRC-like:
- one shared checkpoint room;
- fixed Council-member identities;
- asynchronous text messages;
- presence/member listing;
- keepalive;
- a small completion/status command set.

The room is shared by all participating Council members. Targeting a message at a specific member does not create a secret direct-message channel; the checkpoint participants retain a common view of the discussion unless a future explicitly approved protocol revision says otherwise.

Full general-purpose IRC behavior is not required. The exact protocol/command subset remains to be finalized.

## 5. Completion signaling

Council members receive a small explicit command surface. At minimum the design includes a completion command exposed to the agent as:

```text
/done
```

A member using /done signals that it currently considers its communication obligations for the checkpoint complete.

This is not an immediate disconnect. If new checkpoint communication validly requires that member's attention before closure, the member may return to an active communication state.

Normal checkpoint communication closure occurs when all required participants are done and no accepted messages remain pending, subject to a bounded fallback/ceiling so a failed or looping agent cannot keep a checkpoint open indefinitely.

The exact DONE/ACTIVE/quiescing state contract will be specified in Part 4.

## 6. Network and capability implications

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

## 7. GitHub/repository administration

Council members own and develop their own repositories, but an agent sandbox must not require unrestricted GitHub-account administration authority in order to push its work.

Repository-content authority and repository-administration authority should remain separable.

The trusted runtime is responsible for checkpoint-related peer access grants/revocations. A Council member must not be able to bypass checkpoint isolation by permanently adding peers, changing visibility, or otherwise administratively exposing its repository outside the checkpoint policy.

Exact Git credential and administration mechanics remain implementation details for a later contract.

## 8. Persistence and provenance

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

## 9. Future distributed deployment

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

## 10. Still to decide

The next design pass must decide:
- whether to implement a tiny IRC/IRCv3-compatible server or a fully custom protocol;
- exact supported registration/authentication messages;
- exact allowed and rejected IRC commands/features;
- long-message framing/chunking;
- server timestamps and message IDs;
- reply/thread semantics, if any;
- exact /done wire representation;
- reconnect behavior inside an active checkpoint;
- bounded communication ceilings;
- transcript/event schemas.
