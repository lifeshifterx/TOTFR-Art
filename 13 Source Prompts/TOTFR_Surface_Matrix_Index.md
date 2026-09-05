# TOTFR Surface Matrix Index

Status: MANDATORY MATRIX CONTROL — 2026-09-04-HARDENED-V2

`TOTFR_Surface_Matrix.csv` is the canonical **column schema only**. Never append production rows to that schema file.

Asset rows live in bounded shard files under:
`13 Source Prompts/Surface Matrix/`

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
- Every shard uses the exact schema columns.
- Every asset may have exactly one active row across all shards. Duplicate active rows = STOP.
- Missing row = STOP for art generation/remaster/deployment.
- Each shard obeys Upload Safety.
- Target shard size <=8,000 UTF-8 bytes. Any prepared shard >8,000 bytes = DO NOT WRITE; split first (`05_NPCs_A.csv`, `05_NPCs_B.csv`) and update this index before row writes.
- Every shard ends with a unique `__EOF_CONTROL__` row/sentinel.
- Do not create empty shards merely to imply progress.
- Never keep the same asset active in a legacy monolith and a shard.
- Index/shard existence is not proof of row correctness.

## 2. Creating or updating an audited row
Matrix authoring is a material action.

Before a new/changed row:
1. Load Main, App/Tool, Art, Upload Safety, schema, and this index.
2. Inspect the exact source binary/version.
3. Fetch the live Notion destination/database/view/property needed for the proposed surface.
4. Run and record Main Audits A/B/C using live evidence. If destination is not yet known, row remains uncreated/NEEDS REVIEW; do not guess.
5. Route by source category to the indexed shard.
6. Fetch all existing applicable shard(s) and prove no active row already exists for the asset ID/source path.
7. Build the complete row using the exact schema; unresolved required working facts are recorded as UNKNOWN and block downstream art/deployment.
8. Preflight the resulting full shard UTF-8 size. If >8,000 bytes, split before writing.
9. Preserve/replace the shard EOF control row at the true tail.
10. Perform one shard create/update.
11. Re-fetch the shard; verify exact asset row, no duplicate, valid column count/schema, acceptable size, and EOF control.
12. Only then may the row be treated as persisted. It still must be revalidated against live source/Notion before use in a later session.

Do not use a row write to change Notion or campaign content.

## 3. Resolving a row for work
1. Load this index.
2. Determine shard family from source category.
3. Fetch the live shard(s).
4. Find exactly one row for asset ID/source path.
5. Validate it against source binary, current canon, and live Notion state.
6. Missing shard/row, duplicate row, stale row, schema mismatch, oversized shard, or missing EOF = STOP and repair matrix control before art work.

## 4. Authority
Schema defines columns. Index defines routing/authoring. The live shard row is a working record only after Audits A/B/C validate it. None override live binaries or rendered/live Notion evidence.

Sharding is mandatory because a 115-row monolith would recreate the project text-write risk.

END-OF-FILE SENTINEL: TOTFR-SURFACE-MATRIX-INDEX-2026-09-04-HARDENED-V2
