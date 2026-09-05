# TOTFR Transactional Agent Deployment SOP

Status: MANDATORY DEPLOYMENT MODULE — 2026-09-04-V6

Purpose: make Notion art deployment deterministic, idempotent, concurrency-safe, reviewable and recoverable. Current workspace is CONTAMINATED/UNTRUSTED until a new run proves otherwise.

## 1. Model
No free-form “apply art” run. Deployment is a transaction ledger over immutable desired-state.

DISCOVER → FREEZE INVENTORY → DESIRED STATE → DRY RUN → FREEZE IMMUTABLE MANIFEST → INDEPENDENT REVIEW → MECHANISM CANARIES → SERIAL COMMIT → STRUCTURAL/BINARY VERIFY → AUTHENTICATED VISUAL VERIFY → DISPROOF → CLOSE.

Failure never advances phase.

## 2. Immutable authority vs progress
`run.json` is the immutable frozen run manifest. It is created only after inventory and plan shards are final and is never edited afterward. It records run ID, immutable `control_ref`, observed source/integration heads, workspace, FROZEN inventory evidence, plan author/executor traceability and exact plan shard blob SHAs.

`state.json` holds mutable phase/circuit/checkpoint only. It never approves or completes work and is not reviewer/WAL authority. Changing frozen run/plan requires a new run revision and invalidates prior reviews/evidence.

Only `final.json` may assert COMPLETE after all evidence gates. Agents load controls from `control_ref`, never ambient `development`.

## 3. Publication boundary
Public GitHub is PLAYER-SAFE only. DM HOLD/future/spoiler art cannot use public source. No configured private DM source = `BLOCKED_PRIVATE_SOURCE`.

Desired external URLs are immutable commit-pinned sources; `/development/` or another mutable branch URL is invalid desired state.

Prefer Notion-native import for gallery/file properties when supported, sourcing approved pinned/private bytes. Require upload state `uploaded`, attach before expiry, fetch final property. Temporary upload URLs are transport only.

## 4. Inventory
Ledger counts/search are not exhaustive proof. Frozen inventory enumerates every governed destination ID/view/property from the Surface Matrix + live reads.

Cross-data-source query is unavailable and single-data-source query may be plan-limited; queries aid discovery but cannot prove global completeness.

`FROZEN` means every governed target has exact live IDs/state. Anything unresolved means no frozen manifest and no mutation. Later unknown residue reopens inventory and invalidates scale-out.

## 5. Desired-state / idempotency
Record final desired state, not guesses. Actions: `NOOP_ALREADY_CORRECT`, `REMOVE_RESIDUE`, `SET_COVER`, `SET_ICON`, `SET_FILE_PROPERTY`, `SET_VIEW_COVER_PROPERTY`, `SCHEMA_MIGRATION_REQUIRED`, `DM_HOLD_PRIVATE`, `NO_DESTINATION`, `BLOCKED`.

Rerun recomputes diff and skips already-correct state. Mutation count comes from diff, not asset count. Every mutation has globally unique `mutation_key`; duplicate = STOP.

New first-block/page-content preview hacks are prohibited. Gallery without stable media property = `SCHEMA_MIGRATION_REQUIRED`, never campaign-content insertion.

## 6. Risk / trust boundary
Tier 0: read-only/NOOP. Tier 1: existing cover/icon/file-property value. Tier 2: schema/view/root navigation/player-DM boundary/publication/control plane.

Every active mutating Tier-1 run needs structural reviewer PASS bound to exact frozen run/plan blobs.

Tier-2 obeys `TOTFR_Agent_Trust_Boundary.json`. While `agent_identity_enforcement_state=UNCONFIGURED`, Tier-2 agent execution is prohibited. Additional self-declared reviewers, heterogeneous labels, or a repository file claiming human approval do not authorize execution. The state may remain PLANNED/BLOCKED only. The exact Tier-2 action must be performed manually by the user or wait until enforceable agent identity/tool isolation is configured.

User-visible completion still requires visual review.

## 7. Optimistic concurrency
Every mutation uses optimistic concurrency because Notion has no conditional transaction/row lock. Capture page `last_edited_at` when available plus exact relevant property/cover/icon; schema fingerprint for data-source changes; normalized view fingerprint for view changes.

Immediately before write, re-fetch. Changed precondition = `CONCURRENT_CHANGE` / STOP. Never merge/overwrite newer edits automatically.

Fingerprints strip signed query strings/tokens/time-varying transport but preserve stable IDs, canonical sources, values, view config and content identity.

## 8. Lease / WAL / receipt
Exactly one `notion_executor` holds mutation lease; all other roles are read-only against production Notion.

Before write create WAL bound to exact frozen run/plan SHAs with mutation key, precondition, intended mutation, expected post-state and rollback.

Then ONE mutation → bounded read-after-write confirmation → structural/binary proof → receipt. A successful receipt requires at least two recorded post-write observations, both matching the expected normalized fingerprint. Mismatch/timeout/stale divergence = UNKNOWN/STOP, never retry storm.

Do not mutate target again without independently approved plan revision. Separate per-target evidence avoids shared-file contention.

## 9. Rollback
Rollback is a new guarded mutation. Restore only if current live state still equals the exact state this run wrote. Later edit = `ROLLBACK_CONFLICT` / manual reconciliation.

Never use full-page `replace_content` for art deploy/rollback. Preserve campaign text, children, relations, schema and unrelated properties.

## 10. Transport / evidence safety
Operational ceiling <=2 Notion requests/second average across the whole run, reads and writes combined; one write in flight. Orchestrator allocates the shared request budget. Respect 429 `Retry-After`; no endpoint-switch/retry storms.

External import is async: `uploaded` required; pending/failed/expired/unknown = STOP.

Sanitize persisted evidence: remove signed query strings, AWS credentials/tokens, OAuth/API secrets, cookies and auth headers. Stable IDs/canonical refs only.

## 11. Canary by mechanism
Before scale-out prove one applicable canary for each planned mechanism: commit-pinned cover/icon, native file-property import, gallery cover via dedicated media property, residue removal, and any approved schema/view migration. Mechanism failure blocks all matching targets.

A Tier-2 canary remains blocked while agent identity enforcement is UNCONFIGURED.

## 12. Visual gate
API structure cannot approve rendering. `VISUALLY APPROVED` requires authenticated browser evidence or explicit user screenshot evidence bound to the exact receipt and stored under `TOTFR_Runtime_Evidence_Policy.json`.

Each visual record requires durable privacy-correct artifact reference + SHA-256, target/destination binding, capture time, browser/runtime, viewport, hard reload and PASS decision. Signed/temporary URLs are not durable evidence; DM visual evidence cannot live in public storage.

For galleries/root/high-risk surfaces inspect crop, blank/broken/duplicate/stale image, title collision, preview source, readability and spoilers. No authenticated render/durable evidence = `VISUAL QA REQUIRED`; run cannot be COMPLETE.

## 13. Final evidence lock / disproof
`final.json` binds exact frozen run/plan SHAs plus exact current receipt and visual blob-SHA maps. Replacing any receipt or visual artifact after final review invalidates completion.

Independent adversarial reviewer tries to prove: omitted target; mutable branch URL; public DM source; stale/swappable run/plan/WAL/receipt/visual evidence; current Notion differs from receipt; residue/preview hack; leaked token; fake identity/approval; absent durable visual proof; open circuit/CONCURRENT_CHANGE/ROLLBACK_CONFLICT/UNKNOWN ignored.

Any success = NOT COMPLETE.

END-OF-FILE SENTINEL: TOTFR-TRANSACTIONAL-AGENT-DEPLOYMENT-2026-09-04-V6
