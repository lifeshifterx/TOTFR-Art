# TOTFR Deployment Run Ledger

Status: MANDATORY RUN FORMAT — 2026-09-04-V6

Each deployment attempt gets a unique directory:
`13 Source Prompts/Deployment Runs/<run_id>/`

Never reuse a prior run directory for a materially changed plan. Create a new run/revision.

## Required layout
- `run.json` — immutable frozen run manifest; created only after inventory + plan shards are final; never edited afterward.
- `state.json` — mutable progress/checkpoint only; never approval/completion authority.
- `plan/*.jsonl` — desired-state plan shards, <=8,000 UTF-8 bytes each.
- `attestations/*.json` — reviews bound to exact immutable run/plan blob SHAs.
- `wal/<target_id>.json` — write-ahead record before mutation.
- `receipts/<target_id>.json` — immutable post-mutation result.
- `visual/<target_id>.json` — durable authenticated rendered evidence metadata.
- `final.json` — only authoritative COMPLETE record after adversarial disproof.

No shared append file during execution. Parallel readers/reviewers create separate evidence files; only one Notion executor mutates production Notion.

## `run.json` — immutable authority
Required:
- `schema_version`: `1`, `run_id`
- immutable 40-hex `control_ref`
- 40-hex `development_head_at_plan`
- `notion_workspace_id`
- `inventory_state`: exactly `FROZEN`
- `inventory_evidence_ref`
- `plan_author_agent`, `plan_author_instance_id`, `plan_author_runtime_class`
- `notion_executor_agent`: exactly `notion_executor`, plus distinct executor instance ID
- `created_at`
- non-empty ordered `plan_shards`: repo path + Git blob SHA

Drafting happens before this manifest exists. Changing `run.json` or a plan blob requires a new run/revision and invalidates prior attestations/WAL/receipts.

## `state.json` — checkpoint only
Allowed `phase`: `PLANNED|APPROVED|EXECUTING|BLOCKED|VISUAL_QA_REQUIRED|CLOSED`; `circuit_state`: `CLOSED|OPEN`; plus sanitized blockers/checkpoint data.

State cannot grant authority. `CLOSED` is not COMPLETE without valid `final.json` and every evidence gate.

## Plan JSONL
One target object per line; final line EOF control.

Required: `target_id`, `asset_id`, risk tier 0/1/2, `destination_id`, `surface_class`, `action`, globally unique `mutation_key` for mutation, privacy, source path/commit/blob, desired source mode/ref, precondition, expected fingerprint, rollback.

Prohibited: mutable `/development/` desired URLs; source/URL commit mismatch; public DM source; first-block/page-content preview hacks; duplicate mutation keys; missing mutation precondition/expected fingerprint/rollback; unresolved facts disguised as blanks.

## Approval / trust boundary
Every active mutating Tier-1 run requires structural reviewer PASS bound to exact `run_json_blob_sha` + ordered `plan_shard_blob_shas`.

Attestations retain `reviewer_instance_id` and runtime fields for traceability only; they are not security identities unless the Trust Boundary later proves enforceable identity isolation.

Tier-2 includes schema/view/root navigation/player-DM/publication/control-plane changes. While `TOTFR_Agent_Trust_Boundary.json` says identity enforcement is `UNCONFIGURED`, Tier-2 agent execution is prohibited: state may remain `PLANNED` or `BLOCKED` only. Self-declared agent IDs or a repository file claiming human approval cannot override this.

After enforceable identity is configured, Tier-2 still requires adversarial review and the trust-boundary rules in force at the pinned `control_ref`.

## WAL / receipt
Before mutation create WAL bound to exact run/plan SHAs, mutation key, executor identity, exact precondition, intended mutation/expected post-state, rollback and timestamp.

Receipt binds exact WAL SHA and records result `SUCCESS|FAIL|CONCURRENT_CHANGE|UNKNOWN`, post-state fingerprint, stable Notion IDs, binary hash when retrievable, sanitized evidence, circuit/error state, and at least two recorded post-write observations. Both confirmations must match the expected normalized fingerprint before SUCCESS can contribute to completion.

## Visual evidence
Every mutating target needs a visual PASS bound to its exact receipt SHA and a durable artifact. Required fields:
- `target_id`, `destination_id`, `receipt_blob_sha`
- `review_role=visual_reviewer`, `reviewer_instance_id`, runtime
- `artifact_ref`, `artifact_sha256`, `captured_at`
- `privacy=PLAYER_SAFE|DM_HOLD`
- browser/runtime, viewport, `hard_reload=true`, `decision=PASS`

`artifact_ref` must be durable and privacy-correct under `TOTFR_Runtime_Evidence_Policy.json`. Signed/temporary URLs are transport, not evidence. DM visual artifacts cannot be stored in public evidence namespaces.

## Evidence safety
All run evidence <=8,000 bytes/file. Never persist signed Notion/S3 query strings, temporary AWS credentials, OAuth/API tokens, cookies, auth headers or secrets.

## Final / completion
Only `final.json` may assert COMPLETE. It must contain adversarial PASS bound to exact immutable run/plan SHAs and the exact final receipt + visual blob-SHA maps. Replacing a receipt or visual artifact after final review invalidates completion.

No open circuit, concurrency conflict, rollback conflict, UNKNOWN, missing durable visual artifact, unverified evidence domain, or unapproved residue may remain.

END-OF-FILE SENTINEL: TOTFR-DEPLOYMENT-RUN-LEDGER-2026-09-04-V6
