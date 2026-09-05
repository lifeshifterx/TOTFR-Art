# TOTFR Art Generation & Remaster QA SOP

Status: MANDATORY ART SOP — 2026-09-04-HARDENED-V2
Scope: every new, regenerated, edited, recropped, recomposed, text-removed, upscaled, or derived TOTFR visual before GitHub production storage or Notion deployment.

## 1. Fail closed
A successful/attractive generation is not production-ready.

Progression:
INPUT LOCKED → SURFACE SPEC LOCKED → PLAN APPROVED → GENERATED/EDITED → TECHNICAL QA → VISUAL QA → CROSS-SURFACE QA → DESIGN APPROVED.

Only DESIGN APPROVED may enter production storage/deployment.

## 2. Startup / matrix resolution
Before art work:
1. Fetch current Main, App/Tool, Art, and Upload Safety SOPs from GitHub `development`.
2. Fetch canonical column schema `13 Source Prompts/TOTFR_Surface_Matrix.csv`.
3. Fetch `13 Source Prompts/TOTFR_Surface_Matrix_Index.md`.
4. Resolve source category → indexed shard under `13 Source Prompts/Surface Matrix/`.
5. Fetch live shard and require exactly one active row for the asset ID/source path.
6. Validate shard <=8,000 UTF-8 bytes and required EOF control.
7. Missing shard/row, duplicate active row, stale row, schema mismatch, oversized shard, or missing sentinel = STOP.
8. Identify exact source binary/version and classify operation: KEEP, RECROP, REMOVE TEXT, RECOMPOSE, REGENERATE, NEW, DM HOLD.
9. Confirm current environment can faithfully perform the operation.
10. Editing a specific existing image requires usable source pixels in the current execution context. If unavailable, do not pretend to edit. Use a proven deterministic transform if sufficient; otherwise provide the exact source/upload or external-production action required.
11. Never generate from memory when required canon/reference/source is unavailable.

## 3. Three audits BEFORE generation/editing
Record all three in the resolved shard row/checkpoint.

**Audit A — Canon/source**
Prove exact subject/current canon, source/version, player-safe vs DM-only state, must-show facts, prohibited/spoiler facts, available references, and exclusion of obsolete outcomes.

**Audit B — Surface/composition**
Prove exact Notion destination/surface, target aspect/export, live crop/contain behavior where known, crop-safe focal zone, native-title/UI collision risk, text policy, and whether separate surface derivatives are required. Filename labels never establish surface.

**Audit C — Adversarial**
Try to make the plan fail: invented canon/symbols/text/anatomy/equipment; crop loss; title collision; unreadable black/red hierarchy; weak small-card readability; responsive-crop failure; source destruction; forced cross-surface reuse; spoiler exposure; unavailable source pixels/tool capability. Unresolved risk = STOP/NEEDS REVIEW.

## 4. Production-spec lock
Before generation/editing record:
- asset ID + new version;
- subject, operation, source version;
- exact destination/surface;
- target aspect/export;
- crop-safe focal zone;
- text policy: NONE or exact approved text;
- must-show / must-not-show;
- canon/spoiler class;
- style anchors;
- explicit rejection criteria;
- exact generation prompt/edit instructions;
- input references;
- tool/model/version when exposed.

Do not improvise outside the locked spec.

Defaults:
- ordinary page covers: no embedded title unless the audited surface requires it and visual testing proves fit;
- prefer native Notion titles;
- preserve useful source art; prefer recrop → text/layout fix → recompose → regenerate.

## 5. Generation/edit discipline
- One production candidate per generation action unless controlled alternatives are explicitly required.
- No contact-sheet/collage substitutes.
- Never overwrite `v01`; remasters use new versions.
- Do not silently change ancestry/race, age, gender presentation, equipment, heraldry, architecture, anatomy, item identity, or faction symbolism.
- Do not silently add words, pseudo-runes, logos, signatures, watermarks, borders, or labels.
- Generated typography is prohibited on ordinary covers.
- Exact typography uses a controlled text/layout step where possible.
- Deterministic crop/resize/export occurs only after composition QA.
- Generation success alone never advances status.

## 6. Three validations AFTER generation/editing
**Validation 1 — Technical binary**
Prove file opens/non-zero; correct format; actual dimensions/aspect; transparency; no corruption/alpha matte/clipping/border/export-compression damage; unique filename/version; original source preserved; prompt/edit lineage recorded.

**Validation 2 — Visual/semantic**
Inspect actual pixels full-size and at intended small/cropped view. Reject:
- misspelled/malformed/duplicate/unwanted text or gibberish;
- text in crop/UI zones;
- broken anatomy, fused weapons, impossible grips, warped faces;
- duplicated/floating/disconnected objects;
- wrong identity, insignia, location, item, architecture, or canon detail;
- contradictory perspective/lighting;
- crushed blacks, unreadable focal subject, excessive red hierarchy loss;
- AI artifacts, pseudo-watermarks/signatures;
- critical crop loss;
- spoiler/canon violation.

“Attractive” is not a pass criterion.

**Validation 3 — Cross-surface/consistency**
Compare against the resolved shard row, related chapter/category/faction family, approved TOTFR identity, approved variants of the same subject, visibility class, and intended Notion preview. Incompatible secondary surface = separate derivative, not forced reuse.

## 7. Reject / correct / approve
DESIGN APPROVED requires all three validations.

Failure:
1. mark DESIGN REJECTED / REMASTER REQUIRED;
2. record exact defect/cause;
3. re-run Audits A/B/C including that defect;
4. choose smallest correction;
5. repeat all QA;
6. rejected candidates never inherit approval.

Rejected art must not enter production folders. If retained for forensic/reference use, store outside production and label REJECTED.

## 8. Surface defaults
Defaults never replace the live shard row.
- Page covers: artwork-first, responsive-crop safe, native title usually supplies text.
- Gallery/cards: small-size readability, centered focal point, no essential edge detail/text.
- NPC/creature: identity/anatomy priority, headroom, canon equipment.
- Magic items: clear silhouette, no fake labels/runes unless canon.
- Inline headers: exact locked text, generous padding, separate from cover composition.
- Icons/crests: square/transparent where required, centered symbol, generous padding.

## 9. Batch/session
- One surface class at a time.
- Max 3 related art/remaster assets; reduce to one for new/failing classes.
- Do not start unless the same run can inspect the result and persist QA/checkpoint.
- Limit after generation but before QA = GENERATED/UNVALIDATED, never DESIGN APPROVED.
- Resume only after reloading required SOPs, schema/index/shard, source binary, and actual generated binary; repeat QA.

## 10. Handoff
Before GitHub production storage require DESIGN APPROVED, correct new path/version, dimensions/type, source lineage, spoiler class, intended Notion surface, and rejection history if relevant. Then obey Upload Safety. GitHub existence never upgrades design status.

## 11. Art completion disproof
Before calling art complete ask:
- What was not inspected?
- What could crop badly?
- Any generated text/gibberish or invented/obsolete canon?
- Does intended small/card view work?
- Does art duplicate native Notion text?
- Is another derivative required?
- Could the user immediately identify a defect I ignored?
- Is the matrix row unique, current, and in a bounded valid shard?

Any material uncertainty = NOT COMPLETE.

END-OF-FILE SENTINEL: TOTFR-ART-GENERATION-REMASTER-QA-2026-09-04-HARDENED-V2
