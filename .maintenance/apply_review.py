"""One-off, documentation-only application of the owner's 2026-10-13 review.

This script neither implements Council nor changes repository visibility.
The maintenance workflow/script are excluded from the final main-branch tree.
"""
from pathlib import Path
import json
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]
paths = [ROOT / x for x in ('README.md', 'AGENTS.md', 'VERIFICATION.md')]
paths += sorted((ROOT / 'docs').glob('*.md'))
paths += sorted((ROOT / 'docs').glob('*.txt'))
d = {str(p.relative_to(ROOT)): p.read_text(encoding='utf-8') for p in paths}

def replace(path, old, new, required=True):
    count = d[path].count(old)
    if required and count != 1:
        raise ValueError(f'{path}: expected one anchor, got {count}: {old[:90]!r}')
    d[path] = d[path].replace(old, new)

def section(path, start, end, body):
    a = d[path].find(start)
    b = d[path].find(end, a + len(start))
    if a < 0 or b < 0:
        raise ValueError(f'{path}: missing section boundary {start!r} / {end!r}')
    d[path] = d[path][:a] + textwrap.dedent(body).strip() + '\n\n' + d[path][b:]

def append(path, body):
    d[path] = d[path].rstrip() + '\n\n' + textwrap.dedent(body).strip() + '\n'

# Rename the unimplemented command semantics consistently, not only in prose.
renames = {
    'OpenCheckpointRepositoryAccess': 'PublishCheckpointRepositories',
    'CheckpointRepositoryAccessOpened': 'CheckpointRepositoriesPublished',
    'RevokeCheckpointRepositoryAccess': 'MakeCheckpointRepositoriesPrivate',
    'CheckpointRepositoryAccessRevoked': 'CheckpointRepositoriesMadePrivate',
    'solution_registry': 'Git-backed accepted-project archive',
    'solution registry': 'Git-backed accepted-project archive',
    'Solution registry': 'Git-backed accepted-project archive',
    'three configurable council seats': 'five fixed logical council seats',
    'three council members': 'five fixed logical council members',
    '3-4 peer council members': 'five fixed logical council members',
    '3-4 council members': 'five fixed logical council members',
    '3-4 peers': 'five fixed logical peers',
    '3\u20134': 'five',
    '3-4': 'five',
}
for path in d:
    for old, new in renames.items():
        d[path] = d[path].replace(old, new)

public = '''Each of five fixed logical Council members owns its candidate repository under its own GitHub identity. Between checkpoints it is private. At an approved checkpoint the trusted runtime makes the member repositories **public on GitHub**, records exact frozen commits and observed visibility, and later makes them private again before private development resumes. Peer collaborator grants are not the publication mechanism. Reviewers never receive another member's write or administration credentials.

Public means internet-wide publication, not merely access for Council peers. Approval must cover all repository content/history and other surfaces made public, including logs, releases, and artifacts where applicable. Secrets, personal/private inputs, unapproved intellectual property, and sealed reviews must stay outside the published repository. A publication manifest records approved refs/history, content hashes, scope, and authorization; checking only the latest checkout is insufficient. A failed safety check blocks publication. A confidential project that cannot authorize this exposure cannot use this publication mode; do not silently publish it or silently substitute a different protocol.

Once published, copies and public forks cannot be recalled by making the original private. The private transition protects later unpublished work, not already disclosed information. Runtime-controlled outbound access, repository writes, comments/issues, caches, and retrieval must not provide hidden inter-member communication outside the checkpoint protocol. Public read access is not write access, and visibility is not a frozen-snapshot guarantee: record/pin approved SHAs and enforce the write freeze outside member control.

Visibility changes are durable external operations. OPENING cannot declare publication successful until observed state is verified. Partial/unknown publication blocks review and is reconciled; any real exposure is recorded even after rollback. On closing, terminate communication authority, make repositories private, verify visibility and required isolation controls, and only then permit new private commits. A failed private transition keeps affected work blocked. This policy applies to generated member repositories, not to the Council source repository itself.'''

sealed = '''Checkpoint sequence: all-five arrival barrier -> freeze and publication safety checks -> public repositories -> SEALED_REVIEW -> shared REVIEWING -> CLOSING -> confirmed private visibility -> CLOSED/private revision.

During SEALED_REVIEW each member independently submits an immutable assessment bound to the checkpoint, candidate SHAs, reviewer identity, evidence, objections, and proposed tests. The gateway withholds peer assessments and shared debate until every required member has submitted. Reviews remain in scoped canonical storage, never in a public repository or shared retrieval cache before reveal. Finite slices/budgets apply; a missing reviewer blocks the reveal barrier or produces an explicitly incomplete/aborted review, never a fabricated fifth assessment. No fixed skeptical personas or forced disagreement are required.

Executable peer tests use a separate disposable verification environment, never a reviewer's persistent branch environment. It has pinned read-only inputs and isolated scratch storage; it cannot write member repositories, continuation files, protected acceptance definitions, or control-plane state. Provider/admin credentials and unrestricted network access are absent. The requester still chooses and interprets the test. A trusted runner records actual snapshot/environment/harness hashes, command, execution outcome, and exported output hashes. Candidate-supplied tests remain distinguishable from protected acceptance checks. Recorded execution is evidence of what ran, not automatic proof of methodological adequacy.'''

done = '''Communication completion, verification coverage, candidate readiness, and user acceptance are separate records. DISPUTED or DEFERRED can satisfy a response obligation without resolving the underlying risk or passing an acceptance criterion. Required checks remain NOT_RUN, BLOCKED, FAILED, or PASSED with evidence; an explicit policy waiver is recorded separately and is never a test pass. Forced closure records incomplete review and outstanding obligations.

MarkCheckpointCommunicationDone carries checkpoint_generation, processed_message_sequence, and expected_obligation_version. Under the same checkpoint lock/version guard used to accept messages/actions and close the checkpoint, reject stale declarations, unanswered required obligations, unprocessed required messages, or active verification work. A relevant accepted message or new required action invalidates the affected DONE certificate and reactivates that member. Delivery to a socket is not evidence of processing. Internal bookkeeping alone must not endlessly invalidate completion. Close atomically only after current certificates cover the current review/obligation frontier; record ceiling-forced closure distinctly.

The UI and final review expose communication_closed, verification_coverage, candidate_readiness, and acceptance_decision independently. An incomplete candidate may be presented for an informed user decision where the existing contract allows it; presentation or acceptance does not alter failed/unperformed verification.'''

fidelity = '''Checkpoint milestones specify outcomes/evidence to review, not a preferred sequence of solution components unless the user required those components. For example, require a reproducible baseline and measured failure modes rather than requiring every retrieval design to add reranking and fusion.

Processed clarifications retain links to source user statements, scope, semantic strength (preference, requirement, permission, prohibition, or unresolved ambiguity), and the exact contract revision. Raw answers remain retained for authorized audit/user confirmation, not delivered directly to agents. Material ambiguity and consequential changes to permissions, spending, publication, or requirements require the appropriate explicit confirmation. Ordinary faithful rewording does not add an Auditor bottleneck.

Branch-local clarification context stays branch-local in the Orchestrator's memory, retrieval, caches, and later normalization, not just in outgoing messages. Only approved project-wide revisions enter shared clarification context. The Orchestrator still has no solution-selection or intellectual supervisory authority.'''

ordering = '''Use one deployment-local transactional event-clock row for the initial single-PostgreSQL deployment. Every event-producing canonical transaction obtains that row lock before aggregate/budget locks, allocates its event positions by updating the row, and holds the lock through commit/rollback. Allocate all events of the transaction together. Do not use an ordinary sequence, SERIAL, or IDENTITY allocation as a committed-delivery watermark. This deliberately simple serialization trades throughput for clear ordering; measure before replacing it with a different recorded ordering design.

The clock, canonical mutation, events, idempotent result, and outbox entries commit together. No external call runs while holding that transaction. Rollback publishes nothing. Snapshot data and its committed event watermark come from one consistent database snapshot. Replay filters authorization and orders committed canonical events; visibility filtering must not turn hidden events into a spurious missing-data error.

Outbox workers claim unpublished rows, not just IDs greater than the last observed ID. A retry cannot skip an older unpublished row. Consumers deduplicate by event identity and advance projection offsets atomically with effects only across processed committed events. Out-of-order notification delivery triggers ordered canonical replay/buffering rather than falsely advancing a watermark. The snapshot/SSE race and the lower-number-transaction-commits-later scenario require integration tests.

LangGraph checkpoints are continuation projections, not a second authority over effects, permission, or completion. Bind continuation to logical member, execution epoch, contract/permission versions, and source event position. On restore, reconcile against canonical operations and obligations before executing a step. Replayed framework nodes must reuse logical operation identities and may not redispatch uncertain consequential effects. Runtime side-effect and accounting records prevail over an old checkpoint.'''

recovery = '''Unknown outcomes have operation-specific dependency gates. Read-only retrieval/inference may allow safe independent progress after fencing and isolation checks, while stale results remain quarantined and uncertain usage remains reserved. Consequential writes must be reconciled before replay and block work dependent on their outcome. Authority, public/private visibility, and isolation mutations fail closed for the affected boundary until safe state is verified. Unknown does not mean successful, failed, cancelled, free, or that the entire run must stay blocked forever.

Reserve spending transactionally before dispatch across run, branch, parent/worker, and protected review/finalization allowances. Include member, worker, retry, Orchestrator, verifier, and finalization use. Reserve a conservative bound using explicit pricing/units and input/output limits; unknown pricing cannot pass a cost ceiling as zero. Pre-dispatch expiry may release a reservation; dispatched/unknown requests retain it until reconciliation or conservative settlement. A retry needs independently authorized allowance unless the provider contract proves reuse of the same charged operation. Protected review funds are not ordinary development balance. Fixed-precision accounting and consistent lock ordering are required; concrete provider adapters and tests remain pending.'''

memory = '''A user-accepted candidate is eligible for retention, not automatically a validated general rule. Every reusable lesson retains applicable task/environment/version conditions, source and test evidence, limitations, failures/counterexamples, uncertainty, and reassessment triggers. Do not label empirical lessons unconditionally PROVEN. Keep the memory snapshot fixed during a run; independent retrieval must not become live cross-branch communication.

Before deleting the temporary control database, export the accepted project and selected learning/evidence to a durable Git-backed archive. Validate the transitive reference closure from a fresh archive checkout or retained artifact store, with hashes and permissions checked and no dependency on the live Council database, temporary sandbox paths, expiring URLs, or credentials. Essential missing/restricted evidence blocks teardown or requires an explicitly approved archive/retention change that honestly downgrades the unsupported lesson. Do not silently retain forbidden source data or silently delete the only evidence.

Export acceptance/contract history and relevant provenance needed by retained lessons/reports; transient sessions, leases, and caches need not be retained. Archived failed approaches remain distinguishable from accepted candidates. Temporary restore validation and cleanup must be safe to retry. Final archive visibility follows explicit authorization and is not inferred from earlier public checkpoints.'''

evaluation = '''Pre-register tasks, model/tool permissions, total budget, evaluation method, trial count/variations, and reporting rules. Compare: (A) a strong single agent with the comparison budget; (B) five independent attempts with a fixed external evaluation/selection procedure and no peer discussion; (C) five members with sealed review, discussion, and revision; and (D) targeted ablations such as without sealed review or graph-assisted retrieval. Use the same protected evaluation procedure where applicable, retain unsuccessful trials, and report cost-matched quality separately from wall-clock latency/resource use.

Measure defects uniquely found through peer review, valid corrections incorporated, regressions introduced after review, unresolved required checks, and total spend including review. An evaluation procedure scores experimental outcomes; it does not replace the user's authority to accept a delivered candidate. Static documentation checks are not evidence that Council improves quality. Live evaluation and statistical conclusions remain NOT RUN.'''

# Main design: edit current prose rather than only attaching an overriding addendum.
app = 'docs/APP_DESIGN.md'
section(app, '### Independent beginnings', '### Collective direction without constant voting', '''
### Independent beginnings

Before seeing peers' analyses, each member produces its own investigation plan and preliminary findings. Workers, retrieval, graphs, caches, and exports cannot expose another branch's unpublished interpretations. Authorized original sources may be shared.

''' + fidelity + '\n\n' + public + '\n\n' + sealed + '''

Members choose their own methods and signal semantic milestone readiness. Runtime capacity slices do not imply readiness. All five must reach a checkpoint before publication/review begins; a failed reviewer never counts as ready or agreeing. Checkpoint plans remain versioned and can be revised for approved project changes without an Orchestrator solution judgment.

During shared review, communication and verification-only /work remain mutually exclusive per member. Incoming messages/actions queue while that member works or is suspended. Peers continue discussion. Candidate implementation, commits, and pushes resume only after checkpoint closure and confirmed privacy. Frozen authorized peer snapshots may be retained but never silently refreshed with later private work.

Each member authors a closeout. The runtime builds a deterministic Checkpoint Return Packet with that closeout, relevant original messages/actions, exact frozen snapshot references, verification evidence, unresolved/disputed items, and the full transcript reference. It supplies revision inputs, not instructions or automatically imposed peer tasks.

''' + done + '''

The detailed transport, publication, and completion contract is in [CHECKPOINT_COMMUNICATION_GATEWAY.md](CHECKPOINT_COMMUNICATION_GATEWAY.md); the final mature-candidate checkpoint uses the same mechanism.
''')
replace(app, 'These numbers and policies are editable starting defaults, not claims about an optimal configuration.', 'Resource limits and provider settings are provisional configurable defaults, not claims about an optimum. The five logical Council seats are fixed for this protocol; changing membership requires an explicit versioned design/run decision.')
replace(app, 'The number of logical council agents remains independent from the number of concurrently executing local sandboxes. Resource scheduling controls local parallelism; it does not change council membership or the reasoning protocol.\n\nThe number of logical council agents remains independent from the number of concurrently executing local sandboxes. Resource scheduling controls local parallelism; it does not change council membership or the reasoning protocol.', 'The number of logical council agents remains independent from the number of concurrently executing local sandboxes. Resource scheduling controls local parallelism; it does not change council membership or the reasoning protocol.')
replace(app, 'When a member reaches the current semantic checkpoint,', 'Private work has finite execution slices with durable yield and stable seat rotation even before semantic readiness; withholding readiness cannot monopolize a slot. Yield resumes the same unfinished phase and never advances the all-five barrier. When a member reaches the current semantic checkpoint,')
append(app, '## October 13 architecture integration requirements\n\n' + ordering + '\n\n' + recovery + '\n\n' + memory + '\n\n### Required experimental comparison\n\n' + evaluation)

# Authority and publication policy.
auth = 'docs/PART_4A_AUTHORITY_BOUNDARIES.md'
section(auth, '### 6.1 Repository ownership and checkpoint visibility', '## 7. Transparent execution isolation', '### 6.1 Repository ownership and checkpoint visibility\n\n' + public + '\n\n' + sealed + '\n\nCheckpoint discussion remains runtime-gateway mediated. Peer executable verification is an isolated capability, not authority over the reviewer\'s persistent branch. Private implementation waits for confirmed checkpoint closure.')
append(auth, '## October 13 clarification and checkpoint neutrality refinement\n\n' + fidelity)

# Gateway state protocol.
gateway = 'docs/CHECKPOINT_COMMUNICATION_GATEWAY.md'
section(gateway, '## 3. Checkpoint lifecycle integration', '## 4. Communication model', '''
## 3. Checkpoint lifecycle integration

All five members reach an outcome-based semantic barrier. Early arrivals freeze their candidate and release execution capacity; finite private-work slices also release capacity before readiness. No failed/blocked member is silently excluded. A one-slot deployment rotates the same five logical agents through all stages.

''' + public + '\n\n' + sealed + '''

Runtime creates checkpoint-scoped gateway membership/credentials during opening, but shared send/replay is gated off during SEALED_REVIEW. SubmitIndependentCheckpointReview records a private immutable assessment. RevealCheckpointReviews publishes those records to all five participants atomically only after all required submissions exist; shared discussion then begins.

On normal closure, atomically fence new review messages, persist the final transcript/closeouts and completion frontier, terminate work excursions and checkpoint authority/routes, make repositories private, verify external visibility/isolation, create deterministic return packets, and emit CheckpointClosed. Each external operation remains recoverable rather than hidden inside a SQL transaction. Forced closure preserves its reason and unperformed work and never masquerades as full review.

The persistent gateway process may remain running without any active communication authority. Inactive members receive ordered backlog and current obligations on resumption; they do not receive another member's sealed assessment prematurely.
''')
append(gateway, '## October 13 completion and verification guards\n\n' + done)

# Typed state/command definitions.
typed = 'docs/TYPED_INTERACTION_CONTRACTS.md'
section(typed, '### 3.5 Checkpoint lifecycle', '### 3.6 Candidate lifecycle', '''
### 3.5 Checkpoint lifecycle

Checkpoint states: SCHEDULED, TRIGGERED, OPENING, SEALED_REVIEW, REVIEWING, CLOSING, CLOSED, CANCELLED, FAILED.

TRIGGERED does not publish anything. OPENING pins all five candidates, validates internet-publication approval/history/safety, creates recoverable visibility operations, and verifies actual public state. Only successful opening enters SEALED_REVIEW. Partial/unknown publication remains guarded and reconciled.

SEALED_REVIEW permits independent repository inspection and isolated verification but not shared discussion or access to peer assessments. Each member submits an immutable review bound to the frozen candidates. RevealCheckpointReviews atomically publishes all required submissions and enters REVIEWING. Missing reviewers remain explicit blockers; ceiling-forced abort is incomplete, not successful review.

During REVIEWING candidates stay frozen. /work uses separate disposable verifiers; no implementation commits or pushes. Normal CLOSING requires current versioned DONE certificates, processed message/obligation frontiers, and no active work excursion. CLOSING fences the gateway, persists closeouts/transcript, removes temporary authority, makes repositories private, verifies the safe boundary, and creates return packets before CLOSED permits private revision. Failures remain observable/blocked rather than emitting a premature successful closure.

Communication completion, verification coverage, candidate readiness, and acceptance remain independent. See section 25 and CHECKPOINT_COMMUNICATION_GATEWAY.md.
''')
replace(typed, 'The Project Orchestrator receives the raw answer and its small prompt/clarification memory;', 'The Project Orchestrator receives the raw answer and only its authorized project-wide plus requesting-branch prompt/clarification memory;', required=False)
replace(typed, '6. the Project Orchestrator receives the raw answer and its small prompt/clarification memory;', '6. the Project Orchestrator receives the raw answer and only its authorized project-wide plus requesting-branch prompt/clarification memory;', required=False)
replace(typed, '- CreateCheckpointCommunicationSession\n', '- CreateCheckpointCommunicationSession\n- SubmitIndependentCheckpointReview\n- RevealCheckpointReviews\n')
replace(typed, '- CheckpointCommunicationSessionCreated\n', '- CheckpointCommunicationSessionCreated\n- IndependentCheckpointReviewSubmitted\n- CheckpointPeerReviewsRevealed\n')
replace(typed, '| CreateCheckpointCommunicationSession | CheckpointCommunicationSessionCreated | checkpoint REVIEWING communication active | communication controls active |', '| CreateCheckpointCommunicationSession | CheckpointCommunicationSessionCreated | checkpoint session initialized; shared communication remains gated during SEALED_REVIEW | independent-review controls only |\n| SubmitIndependentCheckpointReview | IndependentCheckpointReviewSubmitted | immutable reviewer assessment recorded privately | own submission status |\n| RevealCheckpointReviews | CheckpointPeerReviewsRevealed | all-five submissions revealed; SEALED_REVIEW -> REVIEWING | shared review controls active |')
replace(typed, '| PublishCheckpointRepositories | CheckpointRepositoriesPublished | frozen peer snapshots become readable | review UI available |', '| PublishCheckpointRepositories | CheckpointRepositoriesPublished | approved repositories confirmed internet-public; frozen SHAs pinned | sealed-review UI available after opening guards |')
replace(typed, '| MakeCheckpointRepositoriesPrivate | CheckpointRepositoriesMadePrivate | peer live access removed | peer repo live access disappears |', '| MakeCheckpointRepositoriesPrivate | CheckpointRepositoriesMadePrivate | repositories confirmed private; prior public copies not recalled | visibility status updated; new private work still waits for CLOSED |')
replace(typed, 'Part 4 is DESIGNED because implementation no longer needs a new product decision to determine:', 'The original Part 4 baseline specified the following boundaries. The October 13 state/command refinements reopen integration work; the revised part must not be marked complete until the extended registry and guards are reconciled:')
replace(typed, '**Status:** DESIGNED. Part 4 defines the approved command/event/state/interaction contract boundary; implementation details belong to later parts.', '**Status:** DESIGN AMENDED; extended state/command integration remains open. The approved baseline and October 13 requirements are specifications, not implemented behavior.')
append(typed, '''
## 25. October 13 required state-contract refinements

''' + done + '\n\n' + fidelity + '''

Additional contract payloads:

- SubmitIndependentCheckpointReview: checkpoint_id/generation, reviewer identity, frozen candidate references, immutable assessment/evidence, idempotency key. Legal only in SEALED_REVIEW for the submitting member; it emits IndependentCheckpointReviewSubmitted without peer delivery.
- RevealCheckpointReviews: expected checkpoint generation and required submission IDs/hashes. Runtime-only, all-five guard, atomic visibility/delivery activation plus CheckpointPeerReviewsRevealed. No model selects which reviews to reveal.
- MarkCheckpointCommunicationDone: processed_message_sequence and expected_obligation_version as well as checkpoint generation. A stale frontier returns STALE_TARGET or REQUIRED_ACTIONS_OPEN, never successful DONE.
- PublishCheckpointRepositories / MakeCheckpointRepositoriesPrivate: publication authorization, repository set, pinned refs, desired visibility, external-operation identities, and verified observed state. A requested transition is not its completion event.
- PauseRun first stops new ordinary admissions and quiesces; RunPaused is emitted only once the required pause boundary is actually reached. Unknown external requests remain separately recorded. StopRun does not claim external cancellation merely from local revocation.

Command/result schemas, registry wiring, UI mappings, and deterministic tests for these additions remain pending implementation. No new completion status is asserted by this amendment.
''')

# PostgreSQL ordering/retention: remove the obsolete permanent SQL registry.
pg = 'docs/POSTGRES_DATA_MODEL.md'
replace(pg, 'Only an ACCEPTED candidate snapshot can be promoted to the Git-backed accepted-project archive.', 'Only an ACCEPTED candidate snapshot is retained as an accepted deliverable in the Git-backed archive. Failed approaches may be retained as attributed lessons; acceptance is not evidence of general validity.')
section(pg, '## 14. Acceptance, archival, and deletion', '## 15. Concurrency and transaction rules', '''
## 14. Acceptance, archival, and deletion

1. Freeze the accepted candidate and record the exact user decision.
2. Preserve actual clean-rebuild/acceptance results; do not claim reproducibility without the required successful checks.
3. Export the accepted project, reproducible environment, authorized learning package, and essential provenance/evidence to Git and durable referenced artifact storage.
4. Validate reference closure and restoreability from the retained archive without the temporary control database.
5. Reconcile consequential external effects and unresolved spending/authority operations, retaining the records needed to resolve any still-open obligations.
6. Apply the explicitly authorized repository archival/visibility policy.
7. Only after validation, delete Council's control database/volume, temporary sandboxes, sessions, checkpoint machinery, caches, and credentials. Product-owned databases remain product data.

''' + memory + '\n\nRetention delays remain policy. They do not waive evidence, external-operation reconciliation, or source-access obligations.')
replace(pg, '- `solution_versions(solution_id, version_no DESC)`\n', '', required=False)
replace(pg, '- GIN full-text index on the registry `search_document`\n', '', required=False)
replace(pg, '- `event_position` BIGINT PK, monotonically increasing', '- `event_position` BIGINT PK, deployment-local committed order allocated by the transactional event clock, not a PostgreSQL sequence')
append(pg, '''
## 19. October 13 schema refinements (not migrations)

''' + ordering + '''

Required additional record groups:

- council_core.event_clock: singleton per deployment with last_position; locked through each event-producing canonical transaction.
- checkpoint repository publications: checkpoint/generation, repository, approved refs/history manifest and hashes, user authorization, desired/observed visibility, external operation IDs, first observed exposure, private confirmation, errors. This does not make private database rows public.
- independent checkpoint reviews: immutable checkpoint/generation/reviewer/candidate-bound assessment and evidence hashes; private until an atomic all-five reveal/delivery record.
- checkpoint review frontiers: message sequence, obligation version, review generation, member processed watermark, and version-bound DONE certificate. Communication state is separate from verification/check status and candidate readiness.
- clarification lineage: raw response reference, processed response, source statement locators, scope/strength, branch-local context manifest, confirmation, and effective contract revision.
- budget accounts/reservations/settlements: fixed-precision units, pricing version, run/branch/parent scope, operation/attempt, pre-dispatch bound, protected review allocation, dispatch state, actual usage, and unresolved liability. Expiry cannot refund a dispatched/unknown operation.
- member execution slices and blocked records: stable seat cursor, execution epoch, resource vector, slice/grace policy, durable suspension point, block reason/dependency, retry ceiling, and confirmed release state.
- archive manifests/validation: retained hashes and reference closure, authorization, validation outcome, missing evidence, and teardown eligibility.

These are accepted data requirements. Concrete field types, constraints, migration code, lock ordering beyond the stated event-clock rule, adapters, and integration tests remain open. There is no permanent SQL learning schema.
''')

part5 = 'docs/PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md'
replace(part5, '**Status:** DESIGNED.', '**Status:** DESIGN AMENDED; transaction integration and runtime verification remain pending.')
replace(part5, '- GitHub access/grants/revocation;', '- GitHub repository public/private visibility changes and scoped content operations;')
replace(part5, 'Council -> GitHub: grant peer access', 'Council -> GitHub: make an approved member repository public')
replace(part5, 'Part 5 is DESIGNED because implementation no longer needs a product-level decision to determine:', 'The baseline establishes the following design boundaries; the October 13 ordering, accounting, and recovery refinements must be integrated and tested before any implementation-complete claim:')
append(part5, '## 13. Commit ordering and framework recovery\n\n' + ordering + '\n\n## 14. Uncertain effects and reservation transactions\n\n' + recovery + '\n\nRepository visibility remains an external operation: requested/public/private state and verified publication/closure are separate commits. A SQL transaction must never pretend to atomically toggle GitHub visibility. All listed runtime acceptance tests remain NOT RUN.')
append('docs/PART_6_EVIDENCE_PROVENANCE_GRAPH.md', '## October 13 verification provenance and retained learning\n\n' + sealed.split('Executable peer tests', 1)[1].join(['Executable peer tests', '']) + '\n\n' + memory)

# Handoff and MVP carry the same accepted model.
handoff = 'docs/IMPLEMENTATION_HANDOFF.md'
start = 'Implement checkpoint execution around each Council member\'s own repository.'
a = d[handoff].index(start)
b = d[handoff].index('\n\n', a)
d[handoff] = d[handoff][:a] + 'Implement the following checkpoint boundary; it replaces the former collaborator-access flow.\n\n' + public + '\n\n' + sealed + '\n\n' + done + d[handoff][b:]
append(handoff, '## October 13 implementation ordering and open work\n\nFinish finite private-work slices, blocked-member handling, operation-specific recovery, atomic reservations, and commit-safe event replay before large UI work. Implement disposable verifiers and sealed review next, then exercise a one-slot five-member run with forced restarts and concurrent completion/message races.\n\n' + fidelity + '\n\n' + evaluation + '\n\nSee ARCHITECTURE_DECISIONS.md and architecture_contract.json for amendment status. Documentation checks do not complete runtime steps. Step 7 still needs defaults, adapters, state wiring, and tests; Step 8 still needs the full agent loop/termination policy; Step 11 still needs concrete memory selection, archive promotion, and validation implementation.')

mvp = 'docs/MVP_SCOPE_BY_STEP.txt'
replace(mvp, '- council_core, council_runtime, and Git-backed accepted-project archive logical schemas.', '- council_core and council_runtime logical schemas; accepted learning is Git-backed, not a permanent SQL schema.')
replace(mvp, '- Minimal Git-backed accepted-project archive sufficient to retain accepted candidate metadata.', '- Minimal Git-backed archive/index sufficient to retain accepted candidate metadata and validated evidence references.')
replace(mvp, '- Repositories can later become mutually readable at the appropriate checkpoint.', '- Member repositories become internet-public at approved checkpoints, then private again before new private work; prior public copies cannot be recalled.')
replace(mvp, '  * open checkpoint repository access for allowed peers;', '  * make approved member repositories public, verify frozen publication scope, and collect sealed reviews;')
replace(mvp, '  * record opening/closing repository commits and revoke peer access;', '  * record opening/closing commits and confirm private visibility before private work resumes;')
for step in (3, 4, 5, 7, 8, 11):
    d[mvp] = re.sub(r'(STEP ' + str(step) + r' - [^\n]+\nStatus: )[^\n]+', r'\1IN DESIGN - approved amendments recorded; remaining design/integration work open', d[mvp])
append(mvp, '''
OCTOBER 13, 2026 - ACCEPTED ARCHITECTURE CORRECTIONS
=================================================

The changes below are requirements, not implemented features. Runtime implementation: NOT STARTED. Runtime tests and comparative evaluations: NOT RUN. No implementation step is closed by this update.

1. Five fixed logical members; private -> PUBLIC GitHub repositories at approved checkpoints -> private before new work. Public history/copies cannot be recalled. Publication safety/authorization is mandatory.
2. Finite private-work slices independent from semantic milestones; deterministic fair rotation; explicit blocked-member/recovery ceilings; no silently reduced Council.
3. Separate disposable peer-test environments with protected acceptance definitions and trusted execution provenance.
4. Operation-specific unknown-outcome policy and old-epoch fencing; safe independent work can resume without guessing consequential effects.
5. Atomic pre-dispatch budget reservations for every caller; protected review funds; unresolved requests retain accounting; resource-vector admission.
6. Commit-safe transactional event clock/outbox/projection watermarks; framework checkpoints subordinate to canonical operations.
7. Outcome-based milestones, source-linked clarification strength, explicit consequential confirmations, and branch-local Orchestrator context.
8. All-five sealed independent assessments before shared debate.
9. Versioned /done certificates; communication closure separate from verification coverage/readiness/user acceptance.
10. Conditioned, evidenced Git lessons; frozen per-run memory snapshot; reference-closure validation before database teardown.
11. Single-agent, five-independent/no-discussion, full-Council, and ablation comparisons using consistent protected evaluation and cost reporting.
12. One machine-readable architecture contract and explicit specification/implementation/test status.

Still open: Step 7 concrete limits/provider adapters/accounting schema/state wiring; Step 8 complete agent-loop and termination design; Step 10 containment technology and integration; Step 11 selection/promotion/archive validation details; all executable runtime acceptance tests and repeated evaluations. See docs/ARCHITECTURE_DECISIONS.md.
''')

# Remove remaining contradictory publication wording in older cross-references.
for path in d:
    substitutions = {
        'grants only the authorized reciprocal read access': 'makes only approved member repositories public after publication guards',
        'grants participating peers reciprocal read access to the authorized repositories': 'makes the approved member repositories public after publication guards',
        'reciprocal peer access is revoked': 'member repositories are made private and visibility is verified',
        'revokes reciprocal peer access': 'makes member repositories private and verifies visibility',
        'revokes reciprocal access': 'makes member repositories private and verifies visibility',
        'revokes reciprocal peer repository access': 'makes member repositories private and verifies visibility',
        'reciprocal repository access': 'checkpoint repository public/private visibility',
        'reciprocal read access': 'approved public repository visibility',
        'period during which reciprocal read access existed': 'observed public visibility window',
        'inside their own execution environment': 'inside separate disposable verification environments',
        'independently in its own environment': 'independently in a separate disposable verification environment',
        'peer candidate independently in its own environment': 'peer candidate independently in a separate disposable verification environment',
        'checkpoint-visible repository in its own environment': 'checkpoint-visible repository in a separate disposable verification environment',
        'test the target\'s checkpoint-visible repository in its own environment': 'test the target\'s checkpoint-visible repository in a separate disposable verification environment',
        'granted authorized read access to the peer snapshot being reviewed': 'verified authorized public publication of the frozen peer snapshot being reviewed',
        'Complex fairness/starvation policies beyond simple queue aging/priority.': 'Sophisticated priority scoring; bounded slices and deterministic seat rotation are still required in the MVP.',
    }
    for old, new in substitutions.items():
        d[path] = d[path].replace(old, new)

append('AGENTS.md', '''
## October 13, 2026 architecture amendment

Read docs/ARCHITECTURE_DECISIONS.md and docs/architecture_contract.json alongside the amended specifications. The owner's public-checkpoint policy applies to generated member repositories, not this source repository. Preserve five fixed members, sealed independent reviews, externally isolated peer verification, bounded private-work slices, conservative reservation accounting, commit-safe event replay, and the separate communication/verification/acceptance records.

A documentation edit can be SPECIFIED without being IMPLEMENTED or VERIFIED. Do not close a runtime step from prose, a generated schema, static checks, mocks, or a successful push. Implementation completion requires code and scoped evidence; verification requires executed tests with recorded environment and results. Existing accepted design sections do not imply that later amendments or application work are complete. No application implementation is authorized merely by this maintenance update.
''')
append('README.md', '''
## Architecture review update - October 13, 2026

The approved corrections are integrated into the current design documents. See [decision/status index](docs/ARCHITECTURE_DECISIONS.md) and [machine-readable contract](docs/architecture_contract.json).

Generated member repositories are private between checkpoints and public during approved frozen-snapshot review; public exposure is not reversible. Council has five fixed logical members, sealed independent reviews, isolated peer testing, bounded execution slices, and explicit recovery/accounting/completion boundaries.

**Application implementation: NOT STARTED. Runtime acceptance tests and comparative evaluations: NOT RUN.** Step 7 and the remaining Step 8/10/11 work are not marked completed by these specification changes.

Run `python3 tools/check_specs.py` for static documentation/contract checks only. These checks cannot establish runtime correctness or research performance.
''')
append('VERIFICATION.md', '''
## October 13 architecture correction verification scope

`python3 tools/check_specs.py` checks the machine-readable contract, explicit pending runtime statuses, removal of selected contradictory defaults, and local documentation links. `git diff --check` checks patch whitespace. These are documentation checks, not application tests.

The required runtime scenarios in docs/ARCHITECTURE_DECISIONS.md remain NOT RUN: single-slot fairness, all-five barriers, visibility failures, sealed review isolation, hostile peer-test containment, unknown external effects, reservation races, committed event replay, stale /done races, clarification isolation, and archive reference closure. Provider integration, sandbox integration, database migrations, live experiments, and deployment have not been verified by this update.

Do not mark implementation or runtime verification complete from a passed documentation check or a pushed commit.
''')
append('docs/REFERENCES.md', '''
## Architecture-review references checked October 13, 2026

- GitHub repository visibility: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility . Public publication exposes repository content and related history; public forks remain public when the original becomes private. Council's publication safeguards are design requirements, not tested integration behavior.
- PostgreSQL transaction isolation and sequence behavior: https://www.postgresql.org/docs/current/transaction-iso.html . Sequence allocation is not transactional commit order; the event-clock protocol is Council's chosen design and still needs integration tests.
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence . Framework continuation does not replace Council's own operation/authorization/accounting authority; concrete adapter/replay behavior must be verified during implementation.
''')

# Compact decision index; detailed requirements live in the edited topic documents.
d['docs/ARCHITECTURE_DECISIONS.md'] = '''# Architecture decisions and verification boundary

**Owner approval:** October 13, 2026. **Delivery:** specification amendments only.
**Application implementation:** NOT STARTED. **Runtime tests/evaluations:** NOT RUN.

The owner corrected the repository policy to public member repositories at checkpoints and approved the other architecture-review improvements. Current topic documents incorporate these decisions; this index tracks them without declaring implementation complete. The latest owner instruction remains authoritative.

| ID | Accepted requirement | Primary specification | Design status | Runtime implementation / tests |
|---|---|---|---|---|
| ADR-01 | Private/public/private member repositories; publication consent/history checks; frozen SHAs; no collaborator grants | PART_4A_AUTHORITY_BOUNDARIES.md | Specified; GitHub integration pending | NOT STARTED / NOT RUN |
| ADR-02 | Five fixed members; bounded private slices; all-five barrier; explicit blocked/failed members | PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md | In design; concrete limits/wiring pending | NOT STARTED / NOT RUN |
| ADR-03 | Separate disposable peer verifiers and protected acceptance evidence | CHECKPOINT_COMMUNICATION_GATEWAY.md | Specified; containment backend pending | NOT STARTED / NOT RUN |
| ADR-04 | Operation-class uncertainty gates and stale-epoch fencing | PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md | Specified; adapters/recovery wiring pending | NOT STARTED / NOT RUN |
| ADR-05 | Atomic conservative reservations, protected review allowance, resource-vector admission | PART_7_MEMBER_SCHEDULING_RECOVERY_RESOURCES.md | In design; schema/defaults pending | NOT STARTED / NOT RUN |
| ADR-06 | Transactional committed event ordering; no skipped outbox rows; canonical state above framework checkpoints | POSTGRES_DATA_MODEL.md | Specified; migrations/concurrency tests pending | NOT STARTED / NOT RUN |
| ADR-07 | Outcome milestones; faithful source-linked clarifications; scoped Orchestrator memory | PART_4A_AUTHORITY_BOUNDARIES.md | Specified; contracts/UI integration pending | NOT STARTED / NOT RUN |
| ADR-08 | Sealed independent reviews before shared discussion | CHECKPOINT_COMMUNICATION_GATEWAY.md | Specified; Step 8 integration pending | NOT STARTED / NOT RUN |
| ADR-09 | Version-bound /done; communication/verification/readiness/acceptance separation | TYPED_INTERACTION_CONTRACTS.md | In design; complete state wiring pending | NOT STARTED / NOT RUN |
| ADR-10 | Conditional evidence-backed Git lessons; frozen memory; verified archive closure before teardown | POSTGRES_DATA_MODEL.md | Specified; Step 11 policy/implementation pending | NOT STARTED / NOT RUN |
| ADR-11 | Single agent, five independent attempts, full Council, and ablations under consistent evaluation | APP_DESIGN.md | Evaluation requirements specified | NOT STARTED / NOT RUN |
| ADR-12 | Reconciled defaults and explicit status/evidence tracking | architecture_contract.json | Documentation/contract maintenance only | Council runtime NOT STARTED / NOT RUN |

## Completion policy

SPECIFIED means requirements have been written. IN DESIGN means named design decisions or integration details remain open. IMPLEMENTED requires executable behavior and a code reference. VERIFIED requires actual test execution, scope/environment, and result evidence. A test plan, stub, mock, static documentation check, or successful push cannot by itself complete a runtime step. No row above marks runtime work completed.

Step 7 remains open for concrete slice/grace/recovery ceilings, capacity sizing/provider compatibility, reservation schemas, pause/stop wiring, and enforcement tests. Step 8 still needs the full member loop and termination/progress policy. Step 10 still needs tested containment. Step 11 still needs memory selection, lesson promotion, and archive-validation implementation. Earlier design-baseline approvals are not evidence that these new details are finished.

## Required runtime evidence (all pending)

- [ ] One-slot execution gives all five eligible members turns without waiting for the first member's readiness; slice yield does not cross a semantic checkpoint.
- [ ] Missing/failed members cannot silently shrink Council or pass either arrival or sealed-review barriers.
- [ ] Public opening checks all exposed refs/history/surfaces; partial/unknown transitions remain guarded; failed private closure prevents new unpublished commits; prior exposure is never claimed erased.
- [ ] Sealed reviews do not leak via repository commits, gateway, retrieval, caches, or member context before reveal.
- [ ] Peer test code cannot write another persistent workspace, continuation state, credentials, or protected acceptance definitions.
- [ ] Unknown inference allows safe unrelated progress with retained accounting; unknown writes are not blindly repeated; uncertain authority fails closed.
- [ ] Simultaneous member/worker/Orchestrator requests cannot overspend or consume protected review funds; timeout does not refund uncertain dispatched usage.
- [ ] Delayed commits, rollback, duplicate/out-of-order outbox delivery, and snapshot/SSE races cannot lose canonical events or falsely advance projections.
- [ ] Restored framework state cannot override canonical permissions, current epochs, or external-operation outcomes.
- [ ] New messages/actions race with /done and closure without being missed; deferred tests do not become passes.
- [ ] Processed clarification strength/scope is preserved; branch-local normalization memory does not influence unauthorized branches.
- [ ] Retained lessons resolve evidence after a fresh archive checkout without the temporary database; broken references prevent teardown.
- [ ] Comparative experiments and ablations run with fixed evaluation, full spend accounting, and failure/regression reporting.
'''

contract = {
    'schema_version': 1,
    'decision_date': '2026-10-13',
    'scope': 'specification_only',
    'logical_member_count': 5,
    'member_count_changes_require_explicit_revision': True,
    'repository_visibility_cycle': ['private', 'public', 'private'],
    'changes_council_source_repository_visibility': False,
    'public_exposure_reversible': False,
    'checkpoint_phases': ['arrival_barrier', 'opening', 'sealed_review', 'reviewing', 'closing', 'closed'],
    'peer_verification_environment': 'separate_disposable',
    'private_work_requires_finite_slices': True,
    'done_requires': ['checkpoint_generation', 'processed_message_sequence', 'expected_obligation_version'],
    'separate_outcomes': ['communication_closure', 'verification_coverage', 'candidate_readiness', 'user_acceptance'],
    'event_ordering': 'deployment_transactional_event_clock',
    'long_term_learning_store': 'git_backed_archive',
    'runtime_implementation_status': 'NOT_STARTED',
    'runtime_test_status': 'NOT_RUN',
    'requirements': [
        {'id': f'ADR-{i:02}', 'design_status': 'IN_DESIGN' if i in (2,5,9) else 'SPECIFIED', 'implementation_status': 'NOT_STARTED', 'test_status': 'NOT_RUN', 'implementation_evidence': [], 'test_evidence': []}
        for i in range(1, 13)
    ],
}
d['docs/architecture_contract.json'] = json.dumps(contract, indent=2) + '\n'

# Cross-document entrypoints point to the same amendment without erasing baseline detail.
for path in ('docs/APP_DESIGN.md', 'docs/POSTGRES_DATA_MODEL.md', 'docs/TYPED_INTERACTION_CONTRACTS.md', 'docs/CHECKPOINT_COMMUNICATION_GATEWAY.md', 'docs/PART_4A_AUTHORITY_BOUNDARIES.md', 'docs/PART_5_TRANSACTIONS_IDEMPOTENCY_CONFLICTS.md', 'docs/PART_6_EVIDENCE_PROVENANCE_GRAPH.md', 'docs/IMPLEMENTATION_HANDOFF.md'):
    first, rest = d[path].split('\n', 1)
    d[path] = first + '\n\n**October 13, 2026 amendment:** [decision/status index](ARCHITECTURE_DECISIONS.md). Requirements below are specifications; application implementation is NOT STARTED and runtime tests are NOT RUN.\n' + rest

check = r'''"""Static specification checks only; no Council runtime is exercised."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
contract = json.loads((root / 'docs/architecture_contract.json').read_text())
assert contract['logical_member_count'] == 5
assert contract['repository_visibility_cycle'] == ['private', 'public', 'private']
assert contract['public_exposure_reversible'] is False
assert contract['changes_council_source_repository_visibility'] is False
assert contract['peer_verification_environment'] == 'separate_disposable'
assert contract['private_work_requires_finite_slices'] is True
assert 'sealed_review' in contract['checkpoint_phases']
assert set(contract['done_requires']) == {'checkpoint_generation', 'processed_message_sequence', 'expected_obligation_version'}
assert len(contract['separate_outcomes']) == 4
assert contract['event_ordering'] == 'deployment_transactional_event_clock'
assert contract['long_term_learning_store'] == 'git_backed_archive'
assert len({x['id'] for x in contract['requirements']}) == 12
for item in contract['requirements']:
    if item['implementation_status'] == 'IMPLEMENTED':
        assert item['implementation_evidence'], item['id']
    if item['test_status'] == 'PASSED':
        assert item['test_evidence'], item['id']

files = list((root / 'docs').glob('*.md')) + list((root / 'docs').glob('*.txt'))
files += [root / 'README.md', root / 'AGENTS.md', root / 'VERIFICATION.md']
for path in files:
    text = path.read_text(encoding='utf-8')
    for pattern in (r'three configurable council seats', r'three council members', r'3[-\u2013]4', r'solution_registry', r'solution_versions\(solution_id', r'Internet-wide public visibility is not an architectural requirement', r'Temporary collaborator/read access.*preferred default'):
        assert not re.search(pattern, text, re.I), (path.name, pattern)
    for link in re.findall(r'\]\(([^)\s]+)(?:\s+[^)]*)?\)', text):
        if '://' in link or link.startswith(('#', 'mailto:')):
            continue
        target = link.split('#', 1)[0]
        if target:
            assert (path.parent / target).exists(), (path.name, link)
assert 'SEALED_REVIEW' in (root / 'docs/TYPED_INTERACTION_CONTRACTS.md').read_text()
assert 'NOT STARTED' in (root / 'README.md').read_text()
print(f'Static specification checks passed: {len(files)} documents and 12 tracked requirements.')
print('Scope: documentation/contract consistency only. Runtime tests and comparative evaluations NOT RUN.')
'''
d['tools/check_specs.py'] = check

# No writes take place until all required source anchors were found.
for path, content in d.items():
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content.rstrip() + '\n', encoding='utf-8')
print('Updated specification files; runtime implementation and runtime tests remain pending.')
