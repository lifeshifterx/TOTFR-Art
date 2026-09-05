# TOTFR Art & Notion Deployment Guardrails

Status: MANDATORY PROJECT SOP
Scope: TOTFR art creation/correction, GitHub storage, Notion cleanup/deployment, validation, and completion reporting.

## 1. Core principle
Fail closed. File existence, a manifest, API success, a stored URL, or a ledger state does not prove completion.

Keep these states separate:
1. Source exists.
2. Source binary is valid.
3. Design fits the intended Notion surface.
4. Bad/legacy deployment residue is removed or explicitly approved.
5. Clean destination baseline is verified.
6. Deployment write persisted.
7. Destination structure is correct.
8. Actual Notion rendering is visually correct.
9. User-visible result is accepted.

Only state 9 permits COMPLETE.

## 2. Evidence precedence
When evidence conflicts, use and document this order:
1. Live destination state + rendered result.
2. Live GitHub `development` tree.
3. Actual binary inspection: content, dimensions, type, transparency, composition.
4. Live Notion page/database/view schema.
5. Current versioned deployment/remaster manifest.
6. Package/local manifests and queues.
7. Older manifests/prompts/ledgers/summaries.

Never silently reconcile contradictions.

## 2A. Mandatory startup gate
Every TOTFR art/GitHub/Notion run must:
1. Fetch this SOP from `development`.
2. Record its path and Git commit/ref in the run log/manifest.
3. Fetch the live destination schema/view before planning writes.
4. Load the current deployment/remaster manifest and unresolved states.
5. Load the cleanup/residue state for the surface being touched.
6. STOP before material writes if the SOP/version or live destination cannot be established.

Scheduled runs are not exempt. Prior chat summaries, memory, ledgers, or assistant statements cannot substitute for the current SOP and live state.

## 3. Three audits BEFORE every material action
No image edit/generation, GitHub production write, Notion cleanup/deployment write, view/schema change, or completion-state update occurs until all three audits pass and are recorded.

### Audit A — Source/requirements
Prove:
- exact source path/version and live Git ref;
- non-zero binary, dimensions/aspect/type;
- subject/canon identity;
- exact intended Notion destination;
- player-safe vs DM-only classification;
- applicable documentation and any stale/contradictory sources.

### Audit B — Destination compatibility + contamination
Prove from live Notion:
- exact page/database/data source/view;
- view/card configuration and preview mechanism;
- crop/contain behavior where exposed;
- exact image property if one exists;
- required surface: cover, card, inline header, icon, etc.;
- native-title/UI collision risk;
- whether schema changes are required;
- every existing cover, icon, media property, inline image, embed, bookmark, external image link, and preview workaround on the target;
- each existing visual reference classified KEEP, REMOVE, REPLACE, or UNKNOWN.

UNKNOWN residue or destination behavior = STOP.

### Audit C — Adversarial
Attempt to disprove the action. Ask:
- Could the mapping be wrong?
- Could the write succeed but remain invisible?
- Could crop/resize or embedded text fail visually?
- Could an external source break/redirect/expire?
- Could this expose DM/future information?
- Could it alter campaign data/structure?
- Could stale docs, old blocks, file properties, links, or ledgers mislead me?
- Could bad content remain hidden behind the replacement?
- Is rollback safe?

Unresolved material risk = STOP or NEEDS REVIEW.

## 4. Three validations AFTER every material action
### Validation 1 — State
Re-fetch and prove the cleanup/deployment write persisted.

### Validation 2 — Structure
Prove correct asset/page/view/property; no unintended text/schema/relation change; no duplicate/conflicting primary image; no stale/broken/obsolete visual reference; no spoiler regression; correct storage/preview mechanism.

### Validation 3 — Visual
Validate the actual rendered Notion presentation, not metadata. Connector/API success is insufficient. Use browser-capable visual inspection or a user screenshot of the exact surface.

Without visual evidence, maximum status is STRUCTURALLY VERIFIED; never VISUALLY APPROVED or COMPLETE.

## 5. Status vocabulary
Use only:
- SOURCE VERIFIED
- DESIGN AUDIT REQUIRED
- DESIGN APPROVED
- CLEANUP REQUIRED
- CLEAN BASELINE VERIFIED
- DEPLOYMENT READY
- DEPLOYMENT WRITTEN
- STRUCTURALLY VERIFIED
- VISUAL QA REQUIRED
- VISUALLY APPROVED
- DM HOLD
- NEEDS REVIEW
- CANON CONFLICT
- BROKEN/MISSING
- NO APPROPRIATE DESTINATION
- COMPLETE

`Verified` alone is prohibited.

COMPLETE requires SOURCE VERIFIED + DESIGN APPROVED + CLEAN BASELINE VERIFIED + DEPLOYMENT WRITTEN + STRUCTURALLY VERIFIED + VISUALLY APPROVED, with no unresolved blocker or legacy residue.

## 6. Asset-design guardrails
- Never infer a Notion surface from `Banner`, `Cover`, `Portrait`, or filenames alone.
- Inspect every binary before reuse.
- Separate variants when surfaces differ: page cover, gallery/card, inline title/header, icon/crest, navigation tile.
- Treat page-cover cropping as responsive; dimensions alone never prove fit.
- Ordinary page covers should not contain embedded titles unless visually tested and intentionally required. Prefer native Notion titles.
- Keep critical text/faces/symbols/objects inside a tested crop-safe zone.
- Prefer recrop/recompose/remove-text over regeneration when possible.
- Never overwrite original `v01` art during remastering. Use a new version in `14 Notion Remaster/` or an equivalent reviewed structure.

## 7. Notion deployment guardrails
- Prefer an existing Files & media property when the database provides one.
- Do not insert a first-page image just to manipulate a gallery preview when a dedicated property exists.
- Do not change view preview behavior until current view configuration and property population are audited.
- Do not change schema solely for artwork without explicit approval after Audits B/C.
- Do not use raw GitHub hotlinks as the default permanent Notion storage method. GitHub is archival source; prefer validated Notion-native media where supported.
- If an external URL is intentionally used, validate rendering and record the dependency.
- Never rewrite lore, session data, dates, relations, properties, or DM content for image placement.

## 7A. Mandatory legacy cleanup / decontamination
Before the pilot or any replacement deployment, run a project-wide contamination discovery sweep across the TOTFR Notion space to identify every prior art/link deployment location, including locations omitted from old ledgers. Build the residue inventory first; do not assume the previous deployment list was complete.

Then, before any replacement art is installed, establish a clean baseline for each affected destination.

1. Capture current state before mutation.
2. Inventory page cover, icon, Files & media values, inline images, embeds, bookmarks, page-content preview images, gallery/board cover settings, and external image links.
3. Search for prior TOTFR deployment residue, including known `raw.githubusercontent.com/lifeshifterx/TOTFR-Art/` links, old asset filenames/versions, broken placeholders, duplicates, and failed-deployment first-block workarounds.
4. Classify every item KEEP, REMOVE, REPLACE, or UNKNOWN with a reason.
5. Remove/clear REMOVE and REPLACE items **before** installing replacements. Never hide bad content behind new art.
6. UNKNOWN = STOP until resolved.
7. Re-fetch and prove removals persisted.
8. Re-scan every relevant storage/display location and prove the destination is clean.
9. Visually confirm no blank/broken/duplicate/stale image remains before replacement deployment. For a user-visible surface, if the current environment cannot render it, require a user/browser screenshot of that exact clean state.
10. Mark CLEAN BASELINE VERIFIED only after all three cleanup validations pass, including visual evidence for user-visible surfaces.

Clean baseline means ZERO unapproved legacy residue on that target. Any bad link, obsolete image, broken media, duplicate primary image, stale preview workaround, or hidden old deployment artifact blocks completion.

This cleanup targets Notion deployment residue. Preserve archival/source `v01` GitHub art unless the user explicitly authorizes repository deletion. If cleanup would delete/rewrite campaign text, child pages, relations, or non-art content, STOP and use Section 15.

## 8. GitHub guardrails
The existing `TOTFR_GitHub_Upload_Safety_Plan.md` remains mandatory for transport integrity only; it does not certify design or Notion quality.

Before binary production writes:
- confirm `development`;
- compare exact live path;
- never count staging/chunks/ZIPs as production;
- verify final path/size;
- avoid repeated failed connector uploads;
- use staging only after package-structure validation.

The ZIP unpack workflow overwrites matching paths. Do not use it for remastered files without a reviewed path manifest and overwrite analysis.

## 9. Manifest requirements
A manifest is a ledger, not proof. Current deployment/remaster records must include:
- version/date and SOP Git commit/ref;
- Git ref audited;
- source + remastered asset if applicable;
- dimensions/type;
- exact Notion destination/surface/preview/storage mechanism;
- player-safe/DM class;
- residue inventory/disposition;
- evidence/status for Audits A/B/C;
- cleanup status + three cleanup validations;
- deployment status + three post-deployment validations;
- final state and evidence/notes.

Conflicting manifests must be reconciled against live GitHub, binaries, and live Notion; never choose silently.

## 10. Pilot-first rule
No broad redeployment until these representative pilots pass cleanup, deployment, and visual QA:
1. TOTFR Homepage
2. Chapter I
3. Braakport
4. Abbigail
5. Anchor Heart

Each pilot must pass Audits A/B/C, CLEAN BASELINE VERIFIED, and all three post-deployment validations. One failed pilot blocks scale-out for its surface class.

## 11. Batch and stop rules
After pilot approval, work one surface class at a time.
- Notion cleanup/deployment: max 5 materially similar items per batch unless lower limits apply.
- GitHub scheduled production uploads: max 3 files per `TOTFR_GitHub_Upload_Safety_Plan.md`. Lower/more-specific limit wins.

At the first unexplained failure, mismatch, broken image, unexpected crop, leftover residue, unexpected view behavior, or contradiction:
1. Invalidate completion for affected items/class.
2. Stop that surface class.
3. Preserve exact evidence and last known good state.
4. Mark CLEANUP REQUIRED, NEEDS REVIEW, or VISUAL QA REQUIRED.
5. Re-run Audits A/B/C and Section 7A before another write.

Do not respond to a failed write by trying unrelated mutation approaches repeatedly.

## 12. Canon and spoiler guardrails
Current campaign canon overrides old prompts/summaries. Artwork can itself spoil identities, transformations, villains, artifacts, locations, deaths, betrayals, encounters, or outcomes. Keep unrevealed items DM HOLD until explicitly released. Never publish future session dates or unrevealed events as completed history.

## 13. Completion + zero-residue gate
Before COMPLETE, run a completion-disproof review: identify anything inferred, unseen, stale, technically successful but visually unproven, broken/blank, badly cropped, title-colliding, mismapped, duplicated, or still carrying old links/media/preview settings.

Then run **three full-project completion audits**:
1. **Destination sweep:** every affected page/record/view for old covers/icons/media values/content images/embeds/bookmarks/preview settings/broken media.
2. **Reference sweep:** search known old deployment URLs/filenames; every match must be intentional archival documentation or approved current content.
3. **Adversarial visual sweep:** re-check representative/high-risk rendered surfaces specifically trying to disprove completion.

Any unapproved residue or material uncertainty = NOT COMPLETE; re-audit and correct.

Never let ledger counts override user-visible failure. User-visible failure immediately invalidates conflicting completion status.

## 14. Existing failed deployment state
All prior TOTFR Notion completion claims are invalid as proof. Existing image/page/view changes are untrusted until individually re-audited.

Before corrected deployment, affected destinations must pass Section 7A. Old raw GitHub links, broken/blank media, incorrect covers/icons, wrong Files & media values, stale first-block images, duplicates, and failed-attempt preview workarounds are presumed untrusted until classified and cleared or explicitly approved.

Cleanup/rollback/reuse is a material action and must pass Audits A/B/C. Do not build on the old `Verified = 77` assumption.

## 15. Failure recovery and manual fallback
If cleanup/deployment/validation fails:
1. Never report partial success as completion.
2. Freeze writes to the affected surface class.
3. Record exact operation/result, destination, asset, and last known good state.
4. Re-run Audits A/B/C plus the full residue inventory.
5. Identify the failure class: design, residue, storage/link, view, schema/property, tool/connector, permissions, or crop/layout.
6. Produce one evidence-backed recovery path and audit it again before execution.
7. After correction, repeat all three post-action validations and the residue sweep. A failed item never inherits its prior completion state.

If tools cannot safely remove bad Notion content, do not improvise destructive workarounds. Give the user an exact manual cleanup checklist per destination, including where applicable:
- page/database/record name;
- cover/icon to remove/replace;
- Files & media property to clear;
- broken/old inline image, embed, bookmark, or preview block to delete;
- gallery/board preview source to restore/change per the audited Surface Matrix;
- old URL/filename patterns to search;
- expected clean state;
- exact replacement asset/destination;
- final reload/visual checks/screenshots needed to prove zero residue.

Manual cleanup must preserve campaign text, child pages, relations, properties, DM-only content, and chronology. If a safe step cannot be specified confidently, report the exact blocker instead of guessing.

## 16. Change control
This SOP is mandatory. Any deviation must state the rule, reason, pass Audits A/B/C, and receive explicit user approval before execution. Never weaken guardrails for convenience, speed, API limits, or context limits.
