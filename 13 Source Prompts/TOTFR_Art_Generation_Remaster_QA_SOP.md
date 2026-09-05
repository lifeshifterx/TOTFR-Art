# TOTFR Art Generation & Remaster QA SOP

Status: MANDATORY ART SOP — 2026-09-04-HARDENED-V4
Scope: every new, regenerated, edited, recropped, recomposed, text-removed, upscaled, or derived TOTFR visual before GitHub storage or Notion deployment.

## 1. Fail closed
A successful or attractive generation is not production-ready.

INPUT LOCKED → SURFACE SPEC LOCKED → PLAN APPROVED → GENERATED/EDITED → MATERIALIZED BINARY → TECHNICAL QA → VISUAL QA → CROSS-SURFACE QA → DESIGN APPROVED.

Only DESIGN APPROVED may enter production storage/deployment.

## 2. Authority and exact inputs
Before art work:
1. Resolve immutable `control_ref` from the approved run/control PR. Load Main, App/Tool, Art, Upload Safety, `13 Source Prompts/TOTFR_Surface_Matrix.csv`, `13 Source Prompts/TOTFR_Surface_Matrix_Index.md`, the exact indexed shard, Agent Trust Boundary, and Evidence Policy from that exact commit. Never substitute mutable `development`, memory, chat, or another branch.
2. Resolve the exact source asset from its explicitly approved source commit/path/blob. Control ref and source commit may differ; neither may be silently replaced by current branch state.
3. Resolve source category → indexed bounded shard and require exactly one active asset row. Missing/duplicate/stale row, schema mismatch, oversized shard, or missing EOF = STOP.
4. Fetch exact live Notion destination/view/property state only for destination-fit evidence. Live Notion state is not control authority.
5. Classify operation KEEP, RECROP, REMOVE TEXT, RECOMPOSE, REGENERATE, NEW, or DM HOLD.
6. Confirm the current environment can faithfully perform the operation.
7. Editing a specific existing image requires usable source pixels in the execution context. Filename/URL/opaque ID/prior claim does not prove pixel access. If unavailable, use a proven deterministic transform when sufficient or stop with the exact source/manual production requirement.
8. Never generate from memory when required canon/reference/source is unavailable.

## 3. Three audits BEFORE generation/editing
Record all three against the exact asset row/spec.

**Audit A — Canon/source:** exact subject/current canon, source/version/blob, player-safe vs DM-only state, must-show facts, prohibited/spoiler facts, references, obsolete outcomes excluded.

**Audit B — Surface/composition:** exact Notion destination/surface, target aspect/export, crop/contain behavior, crop-safe focal zone, native-title/UI collision, text policy, and required surface derivatives. Filename labels never establish surface.

**Audit C — Adversarial:** try to prove invented canon/symbols/text/anatomy/equipment; crop loss; title collision; unreadable black/red hierarchy; poor small-card view; responsive-crop failure; source destruction; forced cross-surface reuse; spoiler leak; unavailable source pixels/tool capability. Unresolved risk = STOP.

## 4. Production-spec lock
Before generation/editing record:
- asset ID, source blob/version, target version;
- subject and operation;
- exact destination/surface and target aspect/export;
- crop-safe focal zone;
- text policy: NONE or exact approved text;
- must-show / must-not-show;
- canon/spoiler class;
- style anchors and rejection criteria;
- exact generation/edit instructions and input references;
- tool/model/version when exposed.

Do not improvise outside the locked spec. Ordinary page covers default to no embedded title; native Notion title usually carries text. Prefer recrop → text/layout fix → recompose → regenerate.

## 5. Generation/edit discipline
- One production candidate per generation action unless controlled alternatives are explicitly required.
- No contact-sheet/collage substitutes.
- Never overwrite `v01`; remasters use new versions.
- Do not silently change ancestry/race, age, gender presentation, equipment, heraldry, architecture, anatomy, item identity, faction symbolism, or story state.
- Do not silently add words, pseudo-runes, logos, signatures, watermarks, borders, or labels.
- Generated typography is prohibited on ordinary covers. Exact typography uses a controlled text/layout step where possible.
- Deterministic crop/resize/export occurs only after composition QA.
- Generation success alone never advances status.

## 6. Materialized-binary gate
Before DESIGN APPROVED, the selected result must exist as an accessible stable binary, not merely a rendered chat preview or tool response.

Record:
- stable artifact/file reference;
- SHA-256 or Git blob SHA when appropriate;
- actual width/height, format, file size, transparency state where relevant;
- source/input lineage and exact output version.

The same materialized binary must be the binary reviewed and later handed to GitHub. If later bytes differ, approval is invalid and QA restarts.

## 7. Three validations AFTER generation/editing
**Technical binary:** file opens/non-zero; expected format; actual dimensions/aspect; transparency; no corruption/alpha matte/clipping/border/compression damage; unique filename/version; source preserved; materialized hash/lineage recorded.

**Visual/semantic:** inspect actual pixels full-size and intended small/cropped view. Reject malformed/duplicate/unwanted text; text in crop/UI zones; broken anatomy/fused weapons/impossible grips/warped faces; duplicated/floating objects; wrong identity/insignia/location/item/architecture/canon; contradictory perspective/lighting; crushed blacks; lost focal hierarchy; AI artifacts; pseudo-watermarks; crop loss; spoiler violations. “Attractive” is not a pass criterion.

**Cross-surface/consistency:** compare exact matrix row, related family, approved TOTFR identity, variants of same subject, visibility class, and intended Notion preview. Incompatible secondary surface requires a separate derivative.

## 8. Reject / correct / approve
DESIGN APPROVED requires all three audits, materialized-binary proof, and all three validations. Producer cannot self-certify final art approval.

Failure: DESIGN REJECTED/REMASTER REQUIRED → record defect/cause → rerun A/B/C including defect → smallest correction → repeat all QA. Rejected candidates never inherit approval and never enter production folders.

## 9. Surface defaults
Defaults never replace the live audited row.
- Page cover: artwork-first, responsive-crop safe, native title usually supplies text.
- Gallery/card: small-size readability, centered focal point, no essential edge text/detail.
- NPC/creature: identity/anatomy priority, headroom, canon equipment.
- Magic item: clear silhouette, no fake labels/runes unless canon.
- Inline header: exact locked text, generous padding, separate from cover composition.
- Icon/crest: square/transparent where required, centered symbol, generous padding.

## 10. Batch/session
One surface class at a time. Max 3 related art/remaster assets; reduce to one for new/failing classes. Do not start unless the same run can inspect/materialize result and persist QA/checkpoint. Session/tool limit after generation but before QA = GENERATED/UNVALIDATED, never DESIGN APPROVED.

Resume only after reloading pinned controls, exact schema/index/shard, exact source binary, and exact materialized generated binary; repeat QA.

## 11. Handoff and disproof
Before GitHub storage require DESIGN APPROVED, exact new path/version, materialized binary hash/dimensions/type, source lineage, spoiler class, intended Notion surface, and rejection history if relevant. GitHub existence never upgrades design status.

Before art completion ask: what was not inspected; what can crop badly; any gibberish/invented canon; does small/card view work; does art duplicate native title; is another derivative required; did reviewed bytes equal handed-off bytes; could the user immediately identify a defect; is matrix row unique/current/bounded? Any material uncertainty = NOT COMPLETE.

END-OF-FILE SENTINEL: TOTFR-ART-GENERATION-REMASTER-QA-2026-09-04-HARDENED-V4
