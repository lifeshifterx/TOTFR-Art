# TOTFR Surface Matrix Index

Status: MANDATORY MATRIX CONTROL — 2026-09-04-HARDENED

`TOTFR_Surface_Matrix.csv` is the canonical **column schema only**. Do not append production asset rows to that schema file.

Asset rows are stored in bounded shard files under:
`13 Source Prompts/Surface Matrix/`

Planned shard families:
1. `01_Branding_Homepage.csv`
2. `02_Chapters_Narrative.csv`
3. `03_Categories.csv`
4. `04_Locations.csv`
5. `05_NPCs.csv`
6. `06_Factions.csv`
7. `07_Creatures_MagicItems.csv`
8. `08_Utility.csv`
9. `09_Decorative.csv`

## Rules
- Every shard uses exact columns defined by `TOTFR_Surface_Matrix.csv`.
- Every asset may have exactly one active row across all shards. Duplicate active rows = STOP.
- Missing row = STOP.
- Each shard is controlled text and obeys Upload Safety.
- Target shard size <=8,000 UTF-8 bytes. Before exceeding, split deterministically (`05_NPCs_A.csv`, `05_NPCs_B.csv`) and update this index first.
- Any prepared shard >8,000 bytes = DO NOT WRITE; split first.
- Every shard ends with a unique `__EOF_CONTROL__` row/sentinel.
- Do not create empty shard files merely to imply audit completion. Create/populate only as audited rows are produced.
- Index/shard existence is not proof of row correctness.
- Never keep the same asset active in a legacy monolith and a shard.

## Resolution
1. Load this index.
2. Determine shard family from source category.
3. Fetch the live shard.
4. Find exactly one row for asset ID/source path.
5. Validate that row against the source binary, current canon, and live Notion state.
6. Missing shard/row, duplicate row, stale row, or shard over limit = STOP and fix matrix control before art work.

## Authority
The schema defines columns. This index defines shard routing. The live shard row defines the current per-asset working record only after Audits A/B/C validate it. None of these files override live binary or Notion evidence.

This sharded design is mandatory because a 115-row monolithic matrix would recreate the project text-write risk.

END-OF-FILE SENTINEL: TOTFR-SURFACE-MATRIX-INDEX-2026-09-04-HARDENED
