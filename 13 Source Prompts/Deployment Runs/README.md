# TOTFR Deployment Run Ledger

Status: MANDATORY RUN FORMAT — 2026-09-04-V2

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
- `plan_author_agent`
- `notion_executor_agent`: exactly `notion_executor`
- `created_at`
- `plan_shards`: ordered array of repo path + Git blob SHA

`APPROVED` or later requires FROZEN inventory. A changed run or plan blob invalidates all prior attestations.

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

Allowed actions are defined in the Transactional Agent Deployment SOP. Non-mutating dispositions never authorize Notion writes.

Prohibited desired state:
- branch-pinned `/development/` URLs;
- pinned URL commit different from `source_commit_sha`;
- public source for DM HOLD;
- first-block/page-content gallery preview hack;
- duplicate `mutation_key`;
- missing precondition, expected fingerprint, or rollback for mutation;
- unresolved destination/UNKNOWN represented as blank.

## Attestation
Each separate attestation names:
- `run_id`, `review_role`, `reviewer_agent`
- exact `run_json_blob_sha`
- exact ordered `plan_shard_blob_shas`
- `decision`: `PASS|FAIL`
- `findings`, `evidence_refs`

Reviewer independently retrieves evidence. Reviewer cannot be plan author or Notion executor. Changed run/plan SHA invalidates the attestation. Tier-2 requires domain + adversarial PASS; user-visible Tier-2 also needs later visual evidence.

## WAL
Before each mutation create a WAL with:
- exact approved run/plan SHAs;
- `mutation_key`;
- executor role;
- exact precondition read/fingerprint;
- intended mutation + expected post-state;
- rollback condition/action;
- timestamp.

No valid WAL = no mutation.

## Receipt
After the single mutation and re-read, receipt contains:
- exact `wal_blob_sha`
- result `SUCCESS|FAIL|CONCURRENT_CHANGE|UNKNOWN`
- `post_state_fingerprint`
- stable Notion object/file IDs
- destination binary hash when retrievable
- sanitized evidence refs
- error/circuit state

A COMPLETE run requires SUCCESS and `post_state_fingerprint == expected_fingerprint` for every mutating target.

## Visual record
Every user-visible mutating target requires a visual record before COMPLETE. It must name the exact receipt blob SHA, `review_role=visual_reviewer`, durable screenshot/artifact SHA-256, browser/runtime, viewport, hard-reload status, and `decision=PASS`. Ephemeral signed URLs are not visual evidence.

## Evidence safety
All run evidence <=8,000 bytes per file. Never persist signed Notion/S3 query strings, temporary AWS credentials, OAuth/API tokens, cookies, auth headers, or secrets.

## Final
`COMPLETE` requires all applicable receipts and visual records to pass, no open circuit/concurrency/rollback conflict/UNKNOWN, and `final.json` containing an independent `adversarial_reviewer` PASS against the exact final run/plan SHAs.

END-OF-FILE SENTINEL: TOTFR-DEPLOYMENT-RUN-LEDGER-2026-09-04-V2
