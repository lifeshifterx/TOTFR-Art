# TOTFR Transactional Agent Deployment SOP

Status: MANDATORY DEPLOYMENT MODULE — 2026-09-04-V1

Purpose: make the next Notion art deployment deterministic, idempotent, concurrency-safe, reviewable, and recoverable. The current workspace is treated as CONTAMINATED / UNTRUSTED until a new run proves otherwise.

## 1. Non-negotiable model
No free-form “apply the art” run. Deployment is a transaction ledger over an immutable desired-state plan.

Phases:
DISCOVER → FREEZE INVENTORY → BUILD DESIRED STATE → DRY RUN → INDEPENDENT ATTESTATION → MECHANISM CANARIES → SERIAL COMMIT → STRUCTURAL/BINARY VERIFY → AUTHENTICATED VISUAL VERIFY → DISPROOF → CLOSE.

Failure never advances the phase.

## 2. Control and source freeze
Every run records:
- unique `run_id`;
- immutable `control_ref` Git commit containing mandatory controls;
- exact `development` head observed at planning;
- exact approved asset commit/path/blob SHA;
- Notion workspace ID;
- target inventory version/hash;
- single `notion_executor` lease holder.

Agents load controls from `control_ref`, not ambient `development`. A changed control ref, plan blob, approved binary SHA, target inventory, or deployment branch invalidates inherited approval.

## 3. Publication boundary
Public GitHub distribution is PLAYER-SAFE only. DM HOLD/future/spoiler art cannot live in a public source namespace. If private DM storage is not configured, DM targets are `BLOCKED_PRIVATE_SOURCE`, not “held but ready.”

Desired external URLs must be commit-pinned, e.g. raw GitHub URLs containing an immutable 40-hex commit SHA. Branch URLs such as `/development/` are invalid desired state.

For gallery/file properties, prefer Notion-native file upload/import from the pinned approved source. Wait for upload status `uploaded`, attach before expiry, then fetch final property. Never persist temporary upload URLs.

## 4. Inventory completeness
Do not trust ledger counts or semantic search as exhaustive inventory. The run inventory must enumerate every governed destination ID/view/property from the Surface Matrix and live destination reads.

Current connector limitation: cross-data-source query is unavailable and single-data-source query is plan-limited. Therefore query results may accelerate discovery but cannot prove global completeness.

Inventory states:
- `FROZEN`: every governed target has exact page/database/data-source/view IDs and current state.
- `PARTIAL`: any governed target is unresolved; mutation is forbidden.

Unknown/unlogged residue discovered later reopens inventory and invalidates scale-out approval.

## 5. Desired-state diff / idempotency
For each target, record only the desired final state, not a sequence of guesses.

Action is one of:
- `NOOP_ALREADY_CORRECT`
- `REMOVE_RESIDUE`
- `SET_COVER`
- `SET_ICON`
- `SET_FILE_PROPERTY`
- `SET_VIEW_COVER_PROPERTY`
- `SCHEMA_MIGRATION_REQUIRED`
- `DM_HOLD_PRIVATE`
- `NO_DESTINATION`
- `BLOCKED`

A rerun must compute the same diff and skip already-correct state. Mutation count is determined by diff, never by asset count.

First-block/page-content preview hacks are prohibited for new deployment. A gallery without a stable media property becomes `SCHEMA_MIGRATION_REQUIRED`; it is not “fixed” by inserting art into campaign content.

## 6. Risk tiers
Tier 0: read-only/NOOP.
Tier 1: existing cover/icon/file-property value change using existing structure.
Tier 2: schema change, view configuration change, root/navigation change, player/DM visibility boundary, publication-boundary change, control-plane change.

Tier 2 requires domain reviewer + adversarial reviewer + machine validation; user-visible Tier 2 also requires visual reviewer. Reviewers must be distinct from author/executor. Prefer heterogeneous reviewer runtime/platform for one Tier-2 reviewer.

## 7. Concurrency preconditions
Notion has no deployment transaction or row lock. Therefore every mutation uses optimistic concurrency.

Capture before planning:
- `page_last_edited_at` for pages when available;
- exact relevant property/cover/icon value;
- exact data-source schema fingerprint for schema work;
- exact normalized view configuration fingerprint for view work.

Immediately before mutation, re-fetch. If the precondition changed, mark `CONCURRENT_CHANGE` and STOP that item. Never merge or overwrite a newer user/agent edit automatically.

Normalize fingerprints: strip ephemeral signed query strings/tokens and other time-varying transport fields; retain stable object IDs, canonical source URLs/paths, property values, view configuration, and content identity. A signed S3 URL itself is not stable state.

## 8. Lease / write-ahead / receipts
Exactly one `notion_executor` holds the run mutation lease. Other agents are read-only against production Notion.

Before each write create a write-ahead record containing target, approved plan SHA, precondition fingerprint, exact intended mutation, expected post-state, and rollback specification.

After one mutation:
1. re-fetch target;
2. prove post-state structurally;
3. when file bytes can be retrieved, hash destination bytes and compare to approved binary;
4. create immutable receipt;
5. do not mutate that target again unless a new plan revision is independently approved.

No shared append file between parallel agents. Use separate per-target receipts/attestations to avoid Git write contention.

## 9. Rollback safety
Rollback is another mutation, not a magical undo.

Every planned mutation must define prior stable values and a reverse action. Execute rollback only if current live state still matches the exact state written by this run. If another edit occurred after our write, rollback is forbidden; mark `ROLLBACK_CONFLICT` and require manual reconciliation.

Never use full-page `replace_content` for art rollback/deployment. Preserve campaign text, child pages, relations, schema, and unrelated properties.

## 10. Notion transport / rate control
Operational ceiling: average <=2 Notion requests/second for this project even though official API currently permits about 3 requests/second on average. One write in flight at a time. Respect 429 `Retry-After`; back off rather than alternate endpoints/retry storms.

External-file imports are asynchronous. Require upload status `uploaded`; `pending`, `failed`, `expired`, or unknown = STOP.

Evidence sanitizer must remove signed query strings, AWS credentials/tokens, OAuth/API secrets, cookies, and authorization data before any persistence to GitHub/ClickUp/checkpoints.

## 11. Canary by mechanism
The old fixed-page pilot is insufficient. Canary coverage is by mutation mechanism. Before scale-out, successfully prove at least one applicable instance of each planned mechanism:
- external commit-pinned cover/icon;
- native file property import;
- gallery view cover using dedicated file property;
- residue removal;
- any approved schema/view migration.

A mechanism failure blocks all targets using that mechanism.

## 12. Visual gate
Structural API state cannot approve visual rendering. `VISUALLY APPROVED` requires an authenticated browser-capable reviewer or explicit user-provided screenshot evidence.

For galleries/root/high-risk surfaces, validate at least two viewport classes and a hard reload. Check crop, blank/broken image, duplicate/stale image, title collision, card preview source, readability, and spoiler exposure.

If no authenticated render capability exists, status is `VISUAL QA REQUIRED`; run cannot be COMPLETE.

## 13. Final disproof
Before close, independent red-team reviewer must try to prove:
- a target was omitted;
- a mutable branch URL remains;
- a public DM asset/reference remains;
- a receipt lacks its precondition/plan SHA;
- current Notion state differs from receipt;
- a stale/broken/duplicate/first-block workaround remains;
- a signed/private token leaked into evidence;
- an approval was self-authored or based on changed plan/binary;
- visual evidence is absent/stale/wrong surface;
- an open circuit, concurrent change, rollback conflict, or UNKNOWN was ignored.

Any success = NOT COMPLETE.

END-OF-FILE SENTINEL: TOTFR-TRANSACTIONAL-AGENT-DEPLOYMENT-2026-09-04-V1
