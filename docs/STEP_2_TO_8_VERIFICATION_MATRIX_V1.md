# Steps 2–8 deterministic acceptance and failure-injection matrix v1

**DESIGN ONLY. None of these cases have been executed.** Each scenario has to be implemented with actual PostgreSQL, trusted snapshot broker, gateway, provider adapters and Docker before declaring verified completion. Test results require command/event IDs, fixture and environment revisions, actual expected/observed outcome and stored evidence reference. Never infer PASS from a static documentation check.

| ID | Scenario/input | Mandatory expected outcome |
| --- | --- | --- |
| S2-01 | Member requests peer path outside manifest, traversal/symlink/absolute path | Denied without leaking hidden file existence or bytes |
| S2-02 | Mixed-case/Unicode collision, unsafe special file, unapproved LFS/submodule or missing object | No verified export or SEAL admission |
| S2-03 | Five legitimate local snapshots, approved scoped grants and negative isolation probes | Checkpoint SEALED_REVIEW opens only after all observed active/authorized |
| S2-04 | Partial-range transfer, dropped/tampered frame, replayed cursor or expired grant | No delivered/verified claim; stale access blocked |
| S2-05 | Revoke returns timeout/UNKNOWN, broker restarts or access probe still succeeds | CLOSING remains blocked, new private work denied; reconcile effect before CLOSED |
| S2-06 | File content read returns successfully | No bundled/automatic SendCheckpointMessage; later independently authorized message is separate |
| S3-01 | Concurrent same-run final-integrator provision with five existing seats | One persistent Integrator identity; exactly five original seat IDs retained |
| S3-02 | Inject out-of-run foreign ID or mismatched review artifact hash | Rejected under composite ownership and pinned hash constraints |
| S3-03 | Blueprint frozen without five current /done/closeout or observed revoke | Not executable; Integrator not admitted |
| S4-01 | Same scoped command key/hash replay after state advances | Returns original receipt; no duplicate canonical event or external effect |
| S4-02 | Same scoped key but changed payload / user acceptance of original candidate ID | IDEMPOTENCY_CONFLICT or explicit wrong-target rejection; never silently retarget integrated result |
| S4-03 | Original seat tries Integrator output command; Integrator submits sealed member review | FORBIDDEN, no forged sixth reviewer |
| S4-04 | New required peer message races with /done and close | Either accepted and invalidates stale DONE before closure, or rejected by closing fence; no lost obligation |
| S4-05 | Review of V1 submitted against V2 or V1 provisional report to V2 premortem | STALE_GENERATION/version mismatch; do not count |
| S5-01 | Two real different seats send review at same timestamp across API processes | Both committed once under PG locks; canonical event positions ordered; no extra API queues |
| S5-02 | Fifth genuine same-generation submission concurrent duplicate/reveal | Exactly one atomic five-seat reveal; sealed bodies absent from pre-reveal caches/RAG/SSE |
| S5-03 | Provider charged but request response lost | UNKNOWN reservation preserved, reconciled or explicit incomplete; no blind retry or false refund |
| S5-04 | Host crash after SQL freeze intent before physical snapshot/export | SQL intent persists; observed external verification required; no invented success |
| S5-05 | Budget insufficient in protected five-member re-review/premortem pool | Integrator admission blocked or revised by explicit user policy, not borrowing funds |
| S5-06 | Hosted moderation required but egress not approved or API unavailable | Affected new operation denied; no implicit upload or model ALLOW bypass of deterministic guard |
| S8-01 | Member reports ready but snapshot hash/quiescence not observed | No current-generation checkpoint arrival; remains pending/blocked |
| S8-02 | Final investigation genuinely concludes no viable outcome | Preserved authentic conclusion with limits; no invented completed software candidate |
| S8-03 | Worker declares readiness, or budget exhaustion from fifth member | Does not satisfy fifth original member's readiness or review |
| S8-04 | Integrator says READY but write fencing, output hash, unknown provider effect absent | Review remains unopened; output-ready is merely intent |
| S8-05 | First actual frozen verified integrated artifact reviewed | Five independently sealed original-member FULL reviews on same hash, then one reveal |
| S8-06 | Localized substantive edit versus unknown/foundational change | Five fresh DELTA versus FULL review submissions; no inherited test pass |
| S8-07 | Exact frozen artifact/report premortem pair changes before fifth submission | No mixed-pair atomic reveal; new appropriate generation required |
| S8-08 | Council 4-to-1 endorsement contradicted by demonstrated minority counterexample | Evidence and hard Contract control; dissent remains attributed; no weighted mechanical vote |
| S8-09 | Disputed decision would expand permission/budget/scope | User-authorized revision required; no unilateral Integrator decision |
| S8-10 | Customer requests non-code synthesis, not Git project | Hashed evidence/artifact manifest, domain-relevant verification; never fabricated Git commit |
| S8-11 | User accepts exact result; archive restore or cleanup still fails | Acceptance remains true but RunCompleted remains false; preserve recoverable evidence |
| S8-12 | Trusted Docker stops whole member/integrator, restarts with volume | Same logical actor/current epoch after checks; persisted files survive but in-memory processes/unknown calls not assumed recoverable |
| S8-13 | Sealed evaluations leak via cached context, graph or disconnected gateway | Security test must fail; privacy boundary enforced before reveal |
| S8-14 | Actual original-five report includes failed/not-run mandatory checks | Honest failing/unfinished status, no fabricated verified completion |
| S8-15 | Current approved customer-source grant expires during Integrator active read | New read/processing denied; explicit reauthorization and observed grant required |
| S8-16 | Accepted project delivered then requested archive delete | Delete control runtime only after actual approved retained-reference restore evidence; product data never mistaken for control DB |

**Execution/reporting rule:** Mark tests `NOT_RUN` until executed against an identified implementation/build; on execution record PASS/FAIL/BLOCKED and actual evidence, never infer PASS from these expected outcomes. Multi-instance transaction/failure-injection, inaccessible tenant/source checks, actual provider billing, real observed revocation and retention restore require real running infrastructure. Nothing in this matrix implements those behaviors.

**Design closure criterion:** the approved technical approach and precise v1 command, state, schema and external-effect requirements are specified and cross-referenced. Implementation still requires writing real migrations/adapters/tests; version pins, user-chosen budgets, actual provider compatibility and deployment capacities remain implementation-time configuration.
