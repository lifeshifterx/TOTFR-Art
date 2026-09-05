# TOTFR Transactional Agent Deployment SOP

Status: MANDATORY DEPLOYMENT MODULE — 2026-09-04-V2

Purpose: make Notion art deployment deterministic, idempotent, concurrency-safe, reviewable and recoverable. Current workspace is CONTAMINATED/UNTRUSTED until a new run proves otherwise.

## 1. Model
No free-form “apply art” run. Deployment is a transaction ledger over immutable desired state.

DISCOVER → FREEZE INVENTORY → DESIRED STATE → DRY RUN → INDEPENDENT ATTESTATION → MECHANISM CANARIES → SERIAL COMMIT → STRUCTURAL/BINARY VERIFY → AUTHENTICATED VISUAL VERIFY → DISPROOF → CLOSE.

Failure never advances phase.

## 2. Freeze controls/source
Each run records unique `run_id`, immutable `control_ref`, observed `development` head, approved asset commit/path/blob SHA, workspace ID, inventory evidence, plan shard SHAs, plan author identity/runtime, and single `notion_executor` identity.

Agents load controls from `control_ref`, not ambient `development`. Changed control/plan/binary/inventory invalidates inherited approval.

## 3. Publication boundary
Public GitHub is PLAYER-SAFE only. DM HOLD/future/spoiler art cannot use public source. No configured private DM source = `BLOCKED_PRIVATE_SOURCE`.

Desired external URLs are commit-pinned with immutable 40-hex commit; `/development/` is invalid desired state.

Prefer Notion-native import for gallery/file properties when supported, sourcing approved pinned/private bytes. Require upload status `uploaded`, attach before expiry, fetch final property. Never persist temporary upload URLs.

## 4. Inventory
Ledger counts/search are not exhaustive proof. Frozen inventory enumerates every governed destination ID/view/property from Surface Matrix + live reads.

Connector limitation: cross-data-source query unavailable and single-data-source query plan-limited; query can aid discovery but cannot prove global completeness.

`FROZEN`: every governed target has exact live IDs/state. `PARTIAL`: anything unresolved; mutation forbidden. Later unknown residue reopens inventory and invalidates scale-out.

## 5. Desired-state / idempotency
Record final desired state, not guesses. Actions: `NOOP_ALREADY_CORRECT`, `REMOVE_RESIDUE`, `SET_COVER`, `SET_ICON`, `SET_FILE_PROPERTY`, `SET_VIEW_COVER_PROPERTY`, `SCHEMA_MIGRATION_REQUIRED`, `DM_HOLD_PRIVATE`, `NO_DESTINATION`, `BLOCKED`.

Rerun recomputes diff and skips already-correct state. Mutation count comes from diff, not asset count.

Every mutation has globally unique `mutation_key` for the exact field/view. Duplicate key = STOP.

New first-block/page-content preview hacks are prohibited. Gallery without stable media property = `SCHEMA_MIGRATION_REQUIRED`, never campaign-content insertion.

## 6. Risk/review
Tier 0: read-only/NOOP. Tier 1: existing cover/icon/file property value. Tier 2: schema/view/root navigation/player-DM boundary/publication/control plane.

Every mutating approved run needs independent structural reviewer PASS. Tier 2 additionally requires adversarial reviewer PASS + machine validation; user-visible completion requires visual reviewer. Author/executor/reviewer instances differ. For Tier 2, require at least one passing reviewer from a different runtime class than plan author when available.

## 7. Optimistic concurrency
Notion has no deployment transaction/row lock. Every mutation uses optimistic concurrency.

Capture page `last_edited_at` when available plus exact relevant property/cover/icon; schema fingerprint for data-source changes; normalized view fingerprint for view changes.

Immediately before write, re-fetch. Changed precondition = `CONCURRENT_CHANGE` / STOP. Never merge/overwrite newer user/agent edits automatically.

Fingerprint normalization strips signed query strings/tokens/time-varying transport data but preserves stable object IDs, canonical sources, property values, view config and content identity.

## 8. Lease / WAL / receipt
Exactly one `notion_executor` holds run mutation lease; all other roles read-only against production Notion.

Before write create WAL bound to exact run/plan SHAs with mutation key, precondition, intended mutation, expected post-state and rollback.

Then ONE mutation → re-fetch → structural proof → destination byte hash when retrievable → receipt. Do not mutate target again without independently approved plan revision.

No shared append file between parallel agents; separate per-target evidence avoids write contention.

## 9. Rollback
Rollback is guarded mutation. Planned mutation must define prior stable values/reverse action. Roll back only if current state still equals exact state this run wrote. Later edit = `ROLLBACK_CONFLICT` / manual reconciliation.

Never use full-page `replace_content` for art deploy/rollback. Preserve campaign text, child pages, relations, schema and unrelated properties.

## 10. Transport / evidence safety
Operational Notion ceiling <=2 requests/second average; one write in flight. Respect 429 `Retry-After`; no endpoint-switch/retry storms.

External import is async: `uploaded` required; pending/failed/expired/unknown = STOP.

Sanitize before persistence: remove signed query strings, AWS credentials/tokens, OAuth/API secrets, cookies, auth headers. Stable IDs/canonical refs only.

## 11. Canary by mechanism
Old fixed-page pilot is insufficient. Before scale-out prove one applicable canary for each planned mechanism: commit-pinned cover/icon, native file property import, gallery cover via dedicated file property, residue removal, approved schema/view migration.

Mechanism failure blocks all targets using it.

## 12. Visual gate
API structure cannot approve rendering. `VISUALLY APPROVED` requires authenticated browser-capable reviewer or explicit user screenshot evidence bound to the exact receipt.

For galleries/root/high-risk surfaces validate appropriate viewport classes + hard reload; inspect crop, blank/broken/duplicate/stale image, title collision, preview source, readability and spoiler exposure.

No authenticated render capability = `VISUAL QA REQUIRED`; run cannot be COMPLETE.

## 13. Final disproof
Independent adversarial reviewer tries to prove: omitted target; mutable branch URL; public DM source; stale run/plan/WAL/receipt; current Notion differs from receipt; residue/preview hack; leaked token; self/stale approval; absent/stale visual evidence; open circuit/CONCURRENT_CHANGE/ROLLBACK_CONFLICT/UNKNOWN ignored.

Any success = NOT COMPLETE.

END-OF-FILE SENTINEL: TOTFR-TRANSACTIONAL-AGENT-DEPLOYMENT-2026-09-04-V2
