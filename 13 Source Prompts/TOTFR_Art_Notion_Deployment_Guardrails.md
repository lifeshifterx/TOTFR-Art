# TOTFR Art & Notion Deployment Guardrails

Status: MANDATORY PROJECT SOP — 2026-09-04-HARDENED

## 1. Fail closed
Never equate file existence, manifest state, API success, stored URL, or ledger status with completion.

Progression:
SOURCE VERIFIED → DESIGN APPROVED → CLEAN BASELINE VERIFIED → DEPLOYMENT WRITTEN → STRUCTURALLY VERIFIED → VISUALLY APPROVED → COMPLETE.

COMPLETE requires all prior states, zero blockers, zero unapproved legacy residue, and user-visible acceptance where applicable.

## 2. Startup/evidence
Before action:
1. Fetch this SOP from GitHub `development`.
2. Before GitHub writes, fetch `13 Source Prompts/TOTFR_GitHub_Upload_Safety_Plan.md`.
3. Record current SOP/Git ref.
4. Fetch live Notion schema/view before Notion writes.
5. Load current deployment + residue state.
6. STOP if rules or destination cannot be established.

Evidence order: rendered destination > live GitHub > inspected binary > live Notion > current manifest > package docs > historical docs. Record conflicts; memory/prior chats never replace live reads.

## 3. Three audits BEFORE every material action
Record all three before material action.

**A — Source:** exact source/ref, binary properties, canon, destination, player-safe/DM class, conflicting docs.

**B — Destination:** exact Notion page/database/view, card settings, preview/storage, image property, crop behavior, surface, title collision, schema impact, and all existing visual/link residue. Classify KEEP/REMOVE/REPLACE/UNKNOWN. UNKNOWN = STOP.

**C — Adversarial:** try to prove it wrong: mapping, invisible success, crop/text, broken source, spoilers, unintended changes, stale/hidden residue, rollback, write-size, session/tool capacity. Unresolved risk = STOP/NEEDS REVIEW.

## 4. Three validations AFTER every material action
1. STATE: re-fetch and prove persistence.
2. STRUCTURE: correct asset/page/view/property; no unintended content/schema/relation change; no duplicate/stale/broken reference; no spoiler regression.
3. VISUAL: validate rendered Notion surface, not metadata. API success is insufficient. Use browser inspection or user screenshot.

No visual evidence = VISUAL QA REQUIRED, never COMPLETE.

## 5. GitHub text-write hard gate
Observed ~20 KB truncation is a failure boundary, never a target.

- Main SOP target: <= 8,000 bytes.
- Any prepared direct text payload > 10,000 bytes = STOP and reduce/split.
- No probing.
- Do not manually expand a prepared document during the connector call.
- Controlled SOP/manifest ends with unique `END-OF-FILE SENTINEL`.
- After write, re-fetch; require SHA, headings, sentinel.
- Missing sentinel/section, malformed tail, or ambiguous fetch = WRITE FAILED; stop dependent work.
- Never increase limits because a risky write succeeded.
- If split, parent enumerates required modules. Missing module = STOP.

Upload safety plan controls transport.

## 6. Asset/Notion rules
- Never infer surface from filename; inspect every binary.
- Separate cover/card/header/icon/navigation variants when needed.
- Dimensions alone never prove responsive-crop fit.
- Avoid embedded cover titles unless tested.
- Prefer recrop/recompose/remove-text over regeneration.
- Preserve `v01`; corrected art gets new versions.
- Prefer existing Files & media properties.
- No first-page-image preview hacks where a dedicated property exists.
- Audit view preview behavior before changing it.
- No artwork-only schema changes without explicit approval after Audits B/C.
- Raw GitHub hotlinks are not default permanent storage; prefer validated Notion-native media.
- External URLs require render validation.
- Never rewrite lore, session data, dates, relations, properties, or DM content for image placement.

## 7. Mandatory legacy cleanup
Before redeployment, sweep TOTFR Notion for residue, including unlogged locations.

Per destination:
1. Capture current state.
2. Inventory cover/icon, Files & media, inline images/embeds/bookmarks, previews, view cover settings, external links.
3. Search old raw-GitHub URLs, filenames/versions, broken placeholders, duplicates, first-block workarounds.
4. Classify KEEP/REMOVE/REPLACE/UNKNOWN.
5. Clear REMOVE/REPLACE before new art; never hide bad content behind replacement.
6. UNKNOWN = STOP.
7. Re-fetch removals and re-scan storage/display locations.
8. Visually prove no blank/broken/duplicate/stale image remains.
9. CLEAN BASELINE VERIFIED requires all three cleanup validations.

Zero unapproved residue required; preserve archival `v01` unless deletion is authorized.

## 8. Pilot first
No broad redeployment until these pass cleanup + deployment + visual QA:
1. TOTFR Homepage
2. Chapter I
3. Braakport
4. Abbigail
5. Anchor Heart

Pilot failure blocks.

## 9. Batch/session/resume
- Notion cleanup/deployment: max 5 similar items; reduce to one when uncertain.
- Scheduled GitHub production uploads: max 3 files.
- Lower tool limits win.
- Never invent remaining context/session/connector/API/rate-limit capacity.
- Start mutations only when the atomic run can finish audits, write, validations, checkpoint.
- Checkpoint: SOP/Git ref, last validated state, any written-but-unvalidated item, residue state, next action, error/limit.
- Checkpoint failure = STOP; never reconstruct from memory.
- At rate/quota/tool/session limit: stop writes/retries, re-fetch last target if possible, classify PROVEN PERSISTED / PROVEN ABSENT / UNKNOWN, checkpoint; never COMPLETE.
- Resume only after reloading SOP + live GitHub/Notion + checkpoint; reconcile UNKNOWN first.
- Before each batch ask: if the next tool call were the last available, is the project safe/resumable? If uncertain, shrink batch.

Limits never relax safeguards.

## 10. Canon/spoilers
Current canon overrides old material. Artwork can spoil identities, transformations, villains, artifacts, locations, deaths, betrayals, encounters, outcomes. Keep unrevealed assets DM HOLD; never publish future events as completed history.

## 11. Completion disproof
Before COMPLETE, try to disprove it:
1. DESTINATION SWEEP: old covers/icons/media/content/previews/broken media.
2. REFERENCE SWEEP: old URLs/filenames; every remaining match intentional and approved.
3. VISUAL SWEEP: high-risk surfaces for blank/broken/crop/title/mismatch/duplicate/residue.

Residue/uncertainty = NOT COMPLETE. User-visible failure overrides ledger state.

## 12. Existing failed deployment
Prior completion claims are invalid proof. Existing changes, old links, broken media, wrong covers/icons/file fields, stale first-block images, duplicates, and preview workarounds remain untrusted until cleared/approved.

## 13. Failure recovery/manual fallback
On failure:
1. Never report completion.
2. Freeze affected surface class.
3. Record exact operation/result/destination/asset/last good state.
4. Re-run Audits A/B/C + residue inventory.
5. Classify failure: design, residue, storage/link, view, schema/property, connector/tool, permissions, crop/layout, write-size, session/limit.
6. Produce one evidence-backed recovery path and audit it before execution.
7. Repeat validations + residue sweep after correction.

If tools cannot safely clean Notion, give exact manual steps per destination: page/record, art fields/blocks, view preview, old URL patterns, clean state, replacement, final visual checks. Preserve campaign content/structure; otherwise report exact blocker.

## 14. Status/control
Statuses: SOURCE VERIFIED, DESIGN APPROVED, CLEANUP REQUIRED, CLEAN BASELINE VERIFIED, DEPLOYMENT WRITTEN, STRUCTURALLY VERIFIED, VISUAL QA REQUIRED, VISUALLY APPROVED, DM HOLD, NEEDS REVIEW, CANON CONFLICT, BROKEN/MISSING, NO DESTINATION, PAUSED AT VALIDATED CHECKPOINT, BLOCKED, COMPLETE. `Verified` alone is prohibited.

Any deviation must name the rule/reason, pass Audits A/B/C, and receive explicit user approval. Never weaken guardrails for convenience, speed, API/context limits, or because prior risk succeeded.

END-OF-FILE SENTINEL: TOTFR-ART-NOTION-GUARDRAILS-2026-09-04-HARDENED
