# TOTFR Art Generation & Remaster QA SOP

Status: MANDATORY ART SOP — 2026-09-04-HARDENED
Scope: every new, regenerated, edited, recropped, recomposed, text-removed, upscaled, or derived TOTFR visual before GitHub production storage or Notion deployment.

## 1. Fail closed
A successful or attractive generation is not production-ready. Required progression:
INPUT LOCKED → SURFACE SPEC LOCKED → PLAN APPROVED → GENERATED/EDITED → TECHNICAL QA → VISUAL QA → CROSS-SURFACE QA → DESIGN APPROVED.

Only DESIGN APPROVED may enter production storage/deployment.

## 2. Startup / capability gate
Before art work:
1. Fetch the current main guardrail SOP and this SOP from GitHub `development`.
2. Load the asset row from canonical `13 Source Prompts/TOTFR_Surface_Matrix.csv`; no row = STOP.
3. Classify operation: KEEP, RECROP, REMOVE TEXT, RECOMPOSE, REGENERATE, NEW, DM HOLD.
4. Identify exact source binary/version and destination surface.
5. Confirm the current environment can faithfully perform the operation.
6. Editing a specific existing image requires usable source pixels in the current execution context. If unavailable, do not pretend to edit. Use a proven deterministic transform if sufficient; otherwise stop and provide the exact source/upload or external-generation action required.
7. Never generate from memory when required canon/reference/source is unavailable.

UNKNOWN source, operation, surface, or capability = STOP.

## 3. Three audits BEFORE generation/editing
Record all three.

**Audit A — Canon/source**
Prove exact subject/current canon, source/version, player-safe vs DM-only state, must-show facts, prohibited/spoiler facts, available references, and that obsolete outcomes are excluded.

**Audit B — Surface/composition**
Prove exact Notion destination/surface class; target aspect/export; live crop/contain behavior where known; safe zone for critical faces/symbols/text/objects; native-title/UI collision risk; embedded-text policy; and whether multiple surface-specific derivatives are required. Filename labels never establish surface.

**Audit C — Adversarial plan**
Try to make the plan fail: invented canon/symbols/text/anatomy/equipment; crop loss; title collision; unreadable dark/red treatment; poor small-card readability; full-frame success but responsive-crop failure; unnecessary destruction of `v01`; wrong reuse across surfaces; spoiler exposure. Unresolved risk = STOP/NEEDS REVIEW.

## 4. Production-spec lock
Before generation/editing record:
- asset ID + new version;
- subject + operation + source version;
- exact surface;
- aspect/export target;
- crop-safe focal zone;
- text policy: NONE or exact allowed text;
- must-show / must-not-show;
- canon/spoiler class;
- style anchors;
- explicit rejection criteria;
- exact generation prompt/edit instructions, input references, and tool/model/version when exposed.

Do not improvise outside the locked spec.

Default covers: no embedded page title unless Surface Matrix requires it and visual testing proves compatibility. Prefer native Notion titles.
Default remaster: preserve useful source art; prefer recrop/recompose/remove-text over regeneration when sufficient.

## 5. Generation/edit discipline
- One production candidate per generation action unless controlled alternatives are explicitly required.
- No contact sheet/collage substitutes.
- Never overwrite `v01`; remasters use new versions.
- Do not silently change ancestry/race, age, gender presentation, equipment, heraldry, architecture, anatomy, item identity, or faction symbolism.
- Do not silently add words, pseudo-runes, logos, signatures, watermarks, borders, or labels.
- Generated typography is prohibited on ordinary covers.
- Exact typography uses a controlled text/layout step where possible.
- Deterministic crop/resize/export occurs only after crop-safe composition QA.
- Generation success alone never advances status.

## 6. Three validations AFTER generation/editing
**Validation 1 — Technical binary**
Prove file opens/non-zero; correct format; actual pixel dimensions/aspect recorded; transparency correct; no corruption/alpha matte/clipping/border or export-compression damage; correct unique filename/version; original source preserved; prompt/edit-spec lineage recorded.

**Validation 2 — Visual/semantic**
Inspect actual pixels full-size and at intended small/cropped view. Reject:
- misspelled/malformed/duplicate/unwanted text or gibberish;
- text near crop/UI zones;
- broken anatomy, fused weapons, impossible grips, warped faces;
- duplicated/floating/disconnected objects;
- wrong insignia, identity, location, item, architecture, or canon detail;
- contradictory perspective/lighting;
- crushed blacks, unreadable focal subject, excessive red hierarchy loss;
- AI artifacts, pseudo-watermarks/signatures;
- critical crop loss;
- spoiler/canon violation.

“Attractive” is not a pass criterion.

**Validation 3 — Cross-surface/consistency**
Compare with Surface Matrix, related chapter/category/faction family, approved TOTFR identity, approved variants of same subject, visibility class, and intended Notion preview. Incompatible secondary surface = separate derivative, not forced reuse.

## 7. Reject / correct / approve
DESIGN APPROVED requires all three validations.

Failure:
1. mark DESIGN REJECTED / REMASTER REQUIRED;
2. record exact defect/cause;
3. re-run Audits A/B/C including that defect;
4. choose smallest correction: recrop → text/layout fix → recompose → regenerate;
5. repeat QA;
6. rejected candidates never inherit approval.

Rejected art must not enter production folders. If retained for forensic/reference use, store outside production and label REJECTED.

## 8. Surface defaults
Defaults never replace the Surface Matrix.

- **Page covers:** artwork-first, responsive-crop safe, native title usually supplies text, critical content away from crop edges.
- **Gallery/cards:** readable small, centered focal point, no essential edge detail, no embedded text by default.
- **NPC/creature:** identity/anatomy priority, no title text, headroom, canon equipment.
- **Magic items:** immediately identifiable clean silhouette; no fake labels/runes unless canon.
- **Inline headers:** exact locked text only, generous padding, separate from cover composition.
- **Icons/crests:** square/transparent where required, centered symbol, generous padding.

## 9. Batch/session safeguards
- One surface class at a time.
- Max 3 related generation/remaster assets before checkpoint/review; reduce to one for new/failing surface classes.
- Do not begin generation/editing unless the same run can reasonably inspect the result and record QA/checkpoint.
- Limit after generation but before QA = GENERATED/UNVALIDATED, never DESIGN APPROVED.
- Resume only after reloading both SOPs, source, Surface Matrix, and actual generated binary; repeat post-generation QA.

## 10. Handoff to GitHub
Before production storage require DESIGN APPROVED, correct new path/version, dimensions/type, source lineage, spoiler class, intended Notion surface, and rejection history if relevant. Then obey `TOTFR_GitHub_Upload_Safety_Plan.md`. GitHub existence never upgrades design status.

## 11. Art completion disproof
Before calling art complete ask:
- What was not inspected?
- What could crop badly?
- Any generated text/gibberish?
- Any invented/obsolete canon?
- Does small-card view work?
- Does art duplicate native Notion text?
- Is another surface-specific derivative required?
- Could a user immediately identify a defect I ignored?

Any material uncertainty = NOT COMPLETE.

END-OF-FILE SENTINEL: TOTFR-ART-GENERATION-REMASTER-QA-2026-09-04-HARDENED
