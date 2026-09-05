# TOTFR Deployment Run Ledger

Status: MANDATORY RUN FORMAT — 2026-09-04-V3

Each deployment attempt gets a unique directory:
`13 Source Prompts/Deployment Runs/<run_id>/`

Never reuse a prior run directory for a materially changed plan. Create a new run/revision.

## Required layout
- `run.json` — run metadata and single-writer lease.
- `plan/*.jsonl` — desired-state plan shards, <=8,000 UTF-8 bytes each.
- `attestations/*.json` — independent reviews of exact run/plan blob SHAs.
- `wal/<target_id>.json` — write-ahead record before mutation.
- `receipts/<target_id>.json` — immutable post-mutation result.
- `visual/<target_id>.json` — authenticated rendered evidence.
- `final.json` — final adversarial disproof result.

No shared append file is allowed during execution. Parallel agents create separate files.

## `run.json`
Required:
- `schema_version`: `1`
- `run_id`
- `status`: `DRAFT|APPROVED|EXECUTING|BLOCKED|VISUAL_QA_REQUIRED|COMPLETE`
- immutable 40-hex `control_ref`
- 40-hex `development_head_at_plan`
- `notion_workspace_id`
- `inventory_state`: `FROZEN|PARTIAL`
- `inventory_evidence_ref`
- `plan_author_agent` + unique `plan_author_instance_id` + `plan_author_runtime_class`
- `notion_executor_agent`: exactly `notion_executor` + distinct `notion_executor_instance_id`
- `created_at`
- `plan_shards`: ordered array of repo path + Git blob SHA

Author and executor instances must differ. `APPROVED` or later requires FROZEN inventory. A changed run or plan blob invalidates all prior attestations.

## Plan JSONL
One target JSON object per line; final line is an EOF control object.

Required target fields:
- `target_id`, `asset_id`, `risk_tier` (`0|1|2`)
- `destination_id`, `surface_class`, `action`
- `mutation_key` for every mutating action; globally unique within the run, e.g. `page:<id>:property:<name>`, `page:<id>:cover`, `view:<id>:cover`
- `privacy`: `PLAYER_SAFE|DM_HOLD`
- `source_path`, `source_commit_sha`, `source_blob_sha`
- `desired_source_mode`: `PINNED_EXTERNAL|NOTION_NATIVE|PRIVATE_DM|NOTION_PRIVATE_NATIVE|NONE`
- `desired_source_ref`
- `precondition`: stable last-edited/property/schema/view fingerprint
- `expected_fingerprint`
- `rollback`: exact prior stable values/reverse action

Prohibited desired state includes branch-pinned `/development/` URLs, URL/source-commit mismatch, public DM source, first-block/page-content preview hacks, duplicate mutation keys, missing mutation precondition/expected fingerprint/rollback, and unresolved facts disguised as blanks.

## Attestation
Each separate attestation names:
- `run_id`, `review_role`, `reviewer_instance_id`, `runtime_class`
- exact `run_json_blob_sha`
- exact ordered `plan_shard_blob_shas`
- `decision`: `PASS|FAIL`
- `findings`, `evidence_refs`

Reviewer independently retrieves evidence and must be a distinct instance from author and executor. Every mutating APPROVED run requires a `structural_reviewer` PASS. Tier-2 also requires `adversarial_reviewer` PASS and at least one passing reviewer from a runtime class different from the plan author when runtime classes are available. Changed run/plan SHA invalidates all reviews.

## WAL
Before each mutation create a WAL with exact approved run/plan SHAs, mutation key, executor identity, exact precondition, intended mutation/expected post-state, rollback condition/action, and timestamp. No valid WAL = no mutation.

## Receipt
After the single mutation and re-read, receipt contains exact WAL blob SHA, result `SUCCESS|FAIL|CONCURRENT_CHANGE|UNKNOWN`, post-state fingerprint, stable Notion object/file IDs, destination binary hash when retrievable, sanitized evidence refs, and circuit/error state.

A COMPLETE run requires SUCCESS and `post_state_fingerprint == expected_fingerprint` for every mutating target.

## Visual record
Every mutating target requires a visual record before COMPLETE. It names the exact receipt blob SHA, `review_role=visual_reviewer`, distinct `reviewer_instance_id`, durable screenshot/artifact SHA-256, browser/runtime, viewport, hard-reload status, and `decision=PASS`. Ephemeral signed URLs are not visual evidence.

## Evidence safety
All run evidence <=8,000 bytes per file. Never persist signed Notion/S3 query strings, temporary AWS credentials, OAuth/API tokens, cookies, auth headers, or secrets.

## Final
`COMPLETE` requires all receipts/visual records to pass, no open circuit/concurrency/rollback conflict/UNKNOWN, and `final.json` containing a distinct-instance `adversarial_reviewer` PASS against the exact final run/plan SHAs.

END-OF-FILE SENTINEL: TOTFR-DEPLOYMENT-RUN-LEDGER-2026-09-04-V3
