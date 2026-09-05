# TOTFR Deployment Run Ledger

Status: MANDATORY RUN FORMAT — 2026-09-04-V1

Each deployment attempt gets a unique directory:

`13 Source Prompts/Deployment Runs/<run_id>/`

Never reuse a prior run directory for a materially changed plan. Create a new run/revision.

## Required layout
- `run.json` — immutable run metadata and writer lease.
- `plan/*.jsonl` — bounded desired-state plan shards, <=8,000 UTF-8 bytes each.
- `attestations/*.json` — independent review of exact run/plan blob SHAs.
- `wal/<target_id>.json` — write-ahead record created before a Notion mutation.
- `receipts/<target_id>.json` — immutable post-mutation structural/binary result.
- `visual/<target_id>.json` — authenticated browser visual evidence metadata.
- `final.json` — final disproof result; created only after all gates.

No shared append file is allowed during execution. Parallel agents create separate files.

## `run.json` required fields
- `schema_version`: `1`
- `run_id`
- `status`: `DRAFT|APPROVED|EXECUTING|BLOCKED|VISUAL_QA_REQUIRED|COMPLETE`
- `control_ref`: immutable 40-hex control commit
- `development_head_at_plan`: 40-hex commit
- `notion_workspace_id`
- `inventory_state`: `FROZEN|PARTIAL`
- `inventory_evidence_ref`
- `plan_author_agent`
- `notion_executor_agent`: must be `notion_executor`
- `created_at`
- `plan_shards`: array of path + Git blob SHA

`APPROVED` requires `inventory_state=FROZEN` and all plan shard SHAs populated. A changed shard requires a new approval/revision.

## Plan JSONL record
One JSON object per line. Final line is an EOF control object.

Required target fields:
- `target_id`, `asset_id`, `risk_tier` (`0|1|2`)
- `destination_id`, `surface_class`
- `action`
- `privacy`: `PLAYER_SAFE|DM_HOLD`
- `source_path`, `source_commit_sha`, `source_blob_sha`
- `desired_source_mode`: `PINNED_EXTERNAL|NOTION_NATIVE|PRIVATE_DM|NONE`
- `desired_source_ref`
- `precondition`: stable page timestamp/fingerprint/schema/view fingerprint as applicable
- `expected_fingerprint`
- `rollback`: exact prior stable values/reverse action

Allowed actions are defined in the Transactional Agent Deployment SOP. `NOOP_ALREADY_CORRECT`, `DM_HOLD_PRIVATE`, `NO_DESTINATION`, and `BLOCKED` do not authorize Notion writes.

Prohibited desired state:
- branch-pinned `/development/` production URLs;
- public source for `DM_HOLD`;
- first-block/page-content gallery preview hack;
- missing precondition/rollback for any mutation;
- unresolved destination or UNKNOWN disguised as empty text.

## Attestation
Each attestation is separate and names:
- `run_id`
- `review_role`
- `reviewer_agent`
- exact `run_json_blob_sha`
- exact list of `plan_shard_blob_shas`
- `decision`: `PASS|FAIL`
- `findings`
- `evidence_refs`

Reviewer must independently retrieve evidence. A changed run/plan SHA invalidates attestation. Tier-2 plans require both domain and adversarial attestations; visual Tier-2 also requires visual reviewer evidence.

## WAL
Before each mutation, create a target WAL containing:
- exact approved plan/run SHAs;
- executor role;
- precondition read/fingerprint;
- intended mutation;
- expected post-state;
- rollback condition/action;
- timestamp.

No WAL = no mutation.

## Receipt
After the one mutation and re-read, create a target receipt containing:
- WAL blob SHA;
- result `SUCCESS|FAIL|CONCURRENT_CHANGE|UNKNOWN`;
- post-state fingerprint;
- stable Notion object/file IDs;
- destination binary hash when retrievable;
- sanitized evidence refs;
- error/circuit state.

Never persist signed Notion/S3 query strings, credentials, cookies, auth headers, or secrets.

## Visual record
Visual evidence names stable target/run/receipt references, browser/runtime, viewport, hard-reload status, screenshot/artifact reference, and decision. A screenshot must be durable enough for later review; ephemeral signed image URLs are not visual evidence.

## Final
`COMPLETE` is allowed only when all required targets have acceptable dispositions/receipts, all applicable visual records pass, no open circuit/concurrency/rollback conflict/UNKNOWN exists, and an independent adversarial final attestation passes against the final exact run evidence.

END-OF-FILE SENTINEL: TOTFR-DEPLOYMENT-RUN-LEDGER-2026-09-04-V1
