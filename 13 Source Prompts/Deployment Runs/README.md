# TOTFR Deployment Run Ledger

Status: MANDATORY RUN FORMAT — 2026-09-04-V4

Each deployment attempt gets a unique directory:
`13 Source Prompts/Deployment Runs/<run_id>/`

Never reuse a prior run directory for a materially changed plan. Create a new run/revision.

## Required layout
- `run.json` — immutable frozen run manifest. Created only after inventory + plan shards are ready; never edited afterward.
- `state.json` — mutable progress/checkpoint only; never approval/completion authority.
- `plan/*.jsonl` — desired-state plan shards, <=8,000 UTF-8 bytes each.
- `attestations/*.json` — independent reviews of exact immutable run/plan blob SHAs.
- `wal/<target_id>.json` — write-ahead record before mutation.
- `receipts/<target_id>.json` — immutable post-mutation result.
- `visual/<target_id>.json` — authenticated rendered evidence.
- `final.json` — only authoritative COMPLETE record after adversarial disproof.

No shared append file during execution. Parallel agents create separate immutable evidence files.

## `run.json` — immutable authority
Required:
- `schema_version`: `1`, `run_id`
- immutable 40-hex `control_ref`
- 40-hex `development_head_at_plan`
- `notion_workspace_id`
- `inventory_state`: exactly `FROZEN`
- `inventory_evidence_ref`
- `plan_author_agent` + unique `plan_author_instance_id` + `plan_author_runtime_class`
- `notion_executor_agent`: exactly `notion_executor` + distinct `notion_executor_instance_id`
- `created_at`
- `plan_shards`: non-empty ordered array of repo path + Git blob SHA

Drafting happens before this manifest is created. A changed `run.json` or plan blob creates a new run/revision and invalidates all attestations/WAL/receipts.

## `state.json` — checkpoint only
Allowed `phase`: `PLANNED|APPROVED|EXECUTING|BLOCKED|VISUAL_QA_REQUIRED|CLOSED` plus `circuit_state`: `CLOSED|OPEN` and sanitized blocker/checkpoint data.

State may change without invalidating signed run/plan evidence because it never grants authority. `CLOSED` does not mean COMPLETE unless valid `final.json` and all evidence gates independently pass.

## Plan JSONL
One target JSON object per line; final line EOF control.

Required: `target_id`, `asset_id`, risk tier 0/1/2, `destination_id`, `surface_class`, `action`, globally unique `mutation_key` for mutation, privacy, source path/commit/blob, desired source mode/ref, precondition, expected fingerprint, rollback.

Prohibited: `/development/` desired URLs; pinned URL/source-commit mismatch; public DM source; first-block/page-content preview hacks; duplicate mutation keys; missing mutation precondition/expected fingerprint/rollback; unresolved facts disguised as blanks.

## Approval / attestations
Approval is evidence, not a status string. Every mutating run requires structural reviewer PASS bound to exact `run_json_blob_sha` + ordered `plan_shard_blob_shas`. Tier 2 also requires adversarial PASS and at least one passing reviewer runtime different from plan author when available.

Attestation names `run_id`, `review_role`, `reviewer_instance_id`, `runtime_class`, exact run/plan SHAs, `decision`, findings and evidence. Reviewer independently retrieves evidence and differs from author/executor.

`state.phase=APPROVED|EXECUTING|VISUAL_QA_REQUIRED|CLOSED` without required valid attestations = invalid.

## WAL / receipt
Before mutation create WAL bound to exact run/plan SHAs, mutation key, executor identity, exact precondition, intended mutation/expected post-state, rollback and timestamp. No WAL = no mutation.

Receipt binds exact WAL SHA and records `SUCCESS|FAIL|CONCURRENT_CHANGE|UNKNOWN`, post-state fingerprint, stable Notion IDs, destination binary hash when retrievable, sanitized evidence, circuit/error state.

Final completion requires SUCCESS and post fingerprint equal expected fingerprint for every mutation.

## Visual
Every mutating target needs visual PASS bound to exact receipt SHA: visual reviewer instance, runtime/browser, viewport, hard reload, durable screenshot/artifact SHA-256. Signed URLs are not visual evidence.

## Evidence safety
All run evidence <=8,000 bytes/file. Never persist signed Notion/S3 query strings, temporary AWS credentials, OAuth/API tokens, cookies, auth headers or secrets.

## Final / completion
Only `final.json` may assert COMPLETE. It must contain distinct-instance adversarial reviewer PASS bound to exact immutable run/plan SHAs and a digest/list of the final receipt + visual evidence set. No open circuit, concurrency conflict, rollback conflict or UNKNOWN may remain.

`state.json` is resumability metadata only and cannot create COMPLETE.

END-OF-FILE SENTINEL: TOTFR-DEPLOYMENT-RUN-LEDGER-2026-09-04-V4
