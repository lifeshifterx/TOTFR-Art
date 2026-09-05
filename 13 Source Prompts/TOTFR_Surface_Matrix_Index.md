# TOTFR Surface Matrix Index

Status: MANDATORY MATRIX CONTROL — 2026-09-04-HARDENED-V3

`TOTFR_Surface_Matrix.csv` is the canonical **column schema only**. Never append production rows to that schema file.

Asset rows live in bounded shard files under `13 Source Prompts/Surface Matrix/`.

Shard families:
1. `01_Branding_Homepage.csv`
2. `02_Chapters_Narrative.csv`
3. `03_Categories.csv`
4. `04_Locations.csv`
5. `05_NPCs.csv`
6. `06_Factions.csv`
7. `07_Creatures_MagicItems.csv`
8. `08_Utility.csv`
9. `09_Decorative.csv`

## 1. Shard rules
- Exact schema columns only.
- Exactly one active row per asset ID/source path across all shards. Duplicate = STOP.
- Missing row = STOP for art/remaster/deployment.
- Target shard <=8,000 UTF-8 bytes; >8,000 = SPLIT REQUIRED before write.
- Every shard ends with a unique `__EOF_CONTROL__` row.
- Empty shards are prohibited.
- Never keep the same asset active in a legacy monolith and a shard.

## 2. Evidence-bound fields
Rows must bind approval to exact evidence, not status words alone.
- `source_sha`: Git blob SHA of the exact source binary at `source_path`.
- `approved_binary_sha`: Git blob SHA of the exact binary approved for downstream use; for KEEP this may equal `source_sha`; otherwise it must match `remaster_path`.
- `design_evidence_ref`: evidence for completed art QA.
- `rollback_ref`: captured pre-deployment Notion state sufficient to restore the affected visual fields/blocks/view settings.
- `cleanup_evidence_ref`: clean-baseline evidence.
- `deployment_evidence_ref`: evidence of the exact Notion write/source used.
- `visual_evidence_ref`: rendered browser/screenshot evidence for final visual approval.
- `failure_count`: integer >=0 for the item in the current recovery cycle.
- `circuit_state`: `CLOSED` or `OPEN`.

Missing evidence required by a downstream state = invalid row/STOP.

## 3. Controlled vocabulary
Use these exact values where applicable; blank/UNKNOWN does not satisfy a gate.
- `audit_a`,`audit_b`,`audit_c`: `PASS`, `FAIL`, `UNKNOWN`.
- `technical_qa`,`visual_qa`,`cross_surface_qa`: `PASS`, `FAIL`, `NOT RUN`.
- `design_state`: `UNVALIDATED`, `DESIGN APPROVED`, `DESIGN REJECTED`, `DM HOLD`, `NEEDS REVIEW`.
- `cleanup_state`: `NOT STARTED`, `CLEANUP REQUIRED`, `CLEAN BASELINE VERIFIED`, `NOT APPLICABLE`.
- `deployment_state`: `NOT DEPLOYED`, `DEPLOYMENT WRITTEN`, `DM HOLD`, `NO DESTINATION`, `BROKEN/MISSING`.
- `structural_state`: `NOT VALIDATED`, `STRUCTURALLY VERIFIED`, `STRUCTURAL FAILURE`.
- `visual_state`: `NOT VALIDATED`, `VISUAL QA REQUIRED`, `VISUALLY APPROVED`, `VISUAL FAILURE`.
- `circuit_state`: `CLOSED`, `OPEN`.

## 4. State-transition invariants
Machine validation must reject impossible downstream states.
1. `DESIGN APPROVED` requires Audits A/B/C = PASS; technical/visual/cross-surface QA = PASS; `source_sha`, `approved_binary_sha`, and `design_evidence_ref` present.
2. `approved_binary_sha` must match the Git blob of `remaster_path`, or `source_path` for KEEP/no remaster.
3. `DEPLOYMENT WRITTEN` requires `DESIGN APPROVED`, `CLEAN BASELINE VERIFIED`, `rollback_ref`, `cleanup_evidence_ref`, and `deployment_evidence_ref`.
4. `STRUCTURALLY VERIFIED` requires `DEPLOYMENT WRITTEN`.
5. `VISUALLY APPROVED` requires `STRUCTURALLY VERIFIED` plus `visual_evidence_ref`.
6. Any source/remaster SHA change invalidates inherited downstream approval until the applicable audits/QA are rerun and evidence refreshed.
7. `circuit_state=OPEN` blocks new mutation or state advancement for that item/stage until the circuit-reset procedure is completed.

## 5. Creating/updating a row
Matrix authoring is a material action.
1. Load Main, App/Tool, Art, Upload Safety, schema, and this index.
2. Inspect exact source binary/version and compute/obtain its live Git blob SHA.
3. Fetch exact live Notion destination/database/view/property for the proposed surface.
4. Run/record Audits A/B/C. Unknown destination = NEEDS REVIEW; do not guess.
5. Route to indexed shard; fetch all applicable shards and prove no duplicate active row.
6. Build the complete row; unresolved required facts remain UNKNOWN and block downstream use.
7. Preflight full shard size and EOF control.
8. One create/update only; re-fetch and verify row, schema, duplicate state, size, SHA bindings where applicable, and EOF.
9. Row still requires live revalidation before use in a later session.

## 6. Circuit breaker / reset
- First material failure: stop the item and classify/re-audit.
- Second failure on the same item/recovery path, or second tool anomaly in the same stage during one run: set `circuit_state=OPEN`; no more writes for that item/stage in that run.
- Third material failure anywhere in one run: global mutation freeze; checkpoint and end mutations.
- Reset only after a fresh startup, exact-current-head guardrail CI success, new evidence-backed recovery path, Audits A/B/C PASS, and persisted checkpoint. Do not reset merely because a retry might work.

## 7. Authority
Schema defines columns. Index defines routing, evidence, transitions, and authoring. A live shard row is only a working record after validation. None override live binaries, live Notion, or rendered evidence.

Sharding remains mandatory because a 115-row monolith would recreate the text-write risk.

END-OF-FILE SENTINEL: TOTFR-SURFACE-MATRIX-INDEX-2026-09-04-HARDENED-V3
