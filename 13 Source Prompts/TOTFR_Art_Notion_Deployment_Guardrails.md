# TOTFR Art & Notion Deployment Guardrails

Status: MANDATORY PROJECT SOP

## 1. Core principle
Fail closed. File existence, a manifest, API success, a stored URL, or a ledger state does not prove completion.

Required states are separate: SOURCE VERIFIED → DESIGN APPROVED → CLEAN BASELINE VERIFIED → DEPLOYMENT WRITTEN → STRUCTURALLY VERIFIED → VISUALLY APPROVED → COMPLETE.

COMPLETE requires all prior states, zero unresolved blockers, zero unapproved legacy residue, and user-visible acceptance where applicable.

## 2. Evidence precedence
When evidence conflicts, use:
1. live destination + rendered result;
2. live GitHub `development`;
3. inspected binary content/dimensions/type/composition;
4. live Notion page/database/view schema;
5. current remaster/deployment manifest;
6. package queues/manifests;
7. old manifests/prompts/ledgers/summaries.

Never silently reconcile contradictions.

## 2A. Mandatory startup
Before any material action:
1. Fetch this SOP from `development`.
2. Before any GitHub text write, fetch `13 Source Prompts/TOTFR_GitHub_Upload_Safety_Plan.md`.
3. Record current SOP/Git ref in the run/checkpoint.
4. Fetch live Notion destination schema/view before planning writes.
5. Load current remaster/deployment and cleanup/residue state.
6. STOP if current rules or destination cannot be established.

Memory, prior chats, ledgers, or summaries never substitute for live reads.

## 2B. HARD GitHub text-write gate
Connector text writes have previously truncated near ~20 KB. That is a failure observation, not an operating threshold.

For EVERY GitHub `create_file`/`update_file` text payload in this project:
1. Build the exact final UTF-8 payload before the connector call.
2. Measure exact UTF-8 bytes, not characters.
3. HARD MAX = **12,000 bytes**. Above 12,000 = DO NOT CALL THE WRITE TOOL.
4. Reduce/split first. Never “try it and see.”
5. Compute expected Git blob SHA: SHA1(`b"blob " + str(byte_count) + b"\0" + payload_bytes`).
6. Record `TEXT_WRITE_PREFLIGHT: <bytes> <= 12000` and expected SHA.
7. Perform one write.
8. Re-fetch exact file; require expected blob SHA and complete content.
9. Mismatch/truncation/ambiguity = WRITE FAILED; stop dependent work.
10. Never raise this ceiling because a larger prior write succeeded.

If split, every part independently obeys 12,000 bytes and the parent enumerates all required parts. Missing part = STOP.

## 3. Three audits BEFORE material action
No edit/generation, GitHub production write, Notion cleanup/deployment, view/schema change, or completion update until all three are recorded.

### Audit A — Source/requirements
Prove exact source/path/version/ref, binary existence/properties, subject/canon, exact destination, player-safe/DM classification, applicable docs, and stale/conflicting evidence.

### Audit B — Destination + contamination
Prove from live Notion: exact page/database/data source/view; view/card settings; preview/storage mechanism; image property; crop/contain behavior where exposed; required surface; title/UI collision risk; schema impact; every cover/icon/media value/inline image/embed/bookmark/external link/preview workaround. Classify each KEEP/REMOVE/REPLACE/UNKNOWN. UNKNOWN = STOP.

### Audit C — Adversarial
Try to disprove the action: wrong mapping, invisible success, bad crop, text collision, broken/expiring source, spoiler exposure, unintended content/schema change, stale docs/links/blocks, hidden residue, unsafe rollback, insufficient session/tool capacity. Unresolved material risk = STOP or NEEDS REVIEW.

## 4. Three validations AFTER material action
1. **State:** re-fetch and prove intended cleanup/deployment persisted.
2. **Structure:** prove correct asset/page/view/property; no unintended text/schema/relation change; no duplicate/conflicting primary image; no stale/broken/obsolete reference; no spoiler regression; correct storage/preview mechanism.
3. **Visual:** validate rendered Notion presentation, not metadata. API success is insufficient. Use browser inspection or user screenshot.

Without visual evidence, maximum status is STRUCTURALLY VERIFIED / VISUAL QA REQUIRED, never COMPLETE.

## 5. Status vocabulary
Use: SOURCE VERIFIED, DESIGN AUDIT REQUIRED, DESIGN APPROVED, CLEANUP REQUIRED, CLEAN BASELINE VERIFIED, DEPLOYMENT READY, DEPLOYMENT WRITTEN, STRUCTURALLY VERIFIED, VISUAL QA REQUIRED, VISUALLY APPROVED, DM HOLD, NEEDS REVIEW, CANON CONFLICT, BROKEN/MISSING, NO APPROPRIATE DESTINATION, PAUSED AT VALIDATED CHECKPOINT, BLOCKED, COMPLETE.

`Verified` alone is prohibited.

## 6. Asset-design guardrails
- Never infer Notion surface from filename labels.
- Inspect every binary before reuse.
- Separate page cover, gallery/card, inline title/header, icon/crest, navigation variants when needed.
- Responsive crop means dimensions alone never prove fit.
- Ordinary covers should avoid embedded titles unless visually tested and required.
- Keep critical content in tested crop-safe zones.
- Prefer recrop/recompose/remove-text over regeneration.
- Preserve `v01`; corrected art uses new versions under `14 Notion Remaster/` or reviewed equivalent.

## 7. Notion deployment guardrails
- Prefer existing Files & media properties.
- Do not use first-page-image preview hacks where a dedicated property exists.
- Audit view preview behavior before changing it.
- No artwork-only schema change without explicit approval after Audits B/C.
- Raw GitHub hotlinks are not default permanent Notion storage; prefer validated Notion-native media where supported.
- External URLs require recorded render validation.
- Never rewrite lore, session data, dates, relations, properties, or DM content for image placement.

## 7A. Mandatory legacy cleanup
Before pilot/replacement deployment, run a project-wide residue discovery sweep, including destinations absent from old ledgers.

For each affected destination:
1. Capture pre-change state.
2. Inventory cover, icon, Files & media, inline images, embeds, bookmarks, page-content previews, gallery/board cover settings, external image links.
3. Search known residue including `raw.githubusercontent.com/lifeshifterx/TOTFR-Art/`, old filenames/versions, broken placeholders, duplicates, and failed first-block workarounds.
4. Classify every visual reference KEEP/REMOVE/REPLACE/UNKNOWN.
5. Clear REMOVE/REPLACE before new art. Never hide bad content behind replacement.
6. UNKNOWN = STOP.
7. Re-fetch removals and re-scan all display/storage locations.
8. Visually prove no blank/broken/duplicate/stale image remains.
9. CLEAN BASELINE VERIFIED requires state, structural, and visual cleanup validation.

Zero unapproved legacy residue is required. Preserve archival GitHub `v01` unless user authorizes deletion. If cleanup risks campaign text, child pages, relations, or non-art content, STOP and use Section 15.

## 8. GitHub guardrails
`TOTFR_GitHub_Upload_Safety_Plan.md` is mandatory for transport integrity. Section 2B governs all text writes.

For binary production writes: confirm `development`; compare live path; never count staging/chunks/ZIPs as production; verify final path/size; avoid repeated failed uploads; use staging only after structure validation. Do not use overwrite ZIP workflows for remastered files without reviewed path/overwrite analysis.

## 9. Manifest/checkpoint requirements
Records are evidence storage, not proof. Include current SOP/Git ref, source/remaster asset, binary properties, exact Notion destination/surface/storage/preview mechanism, player-safe/DM class, residue disposition, Audits A/B/C evidence, cleanup validations, deployment validations, final state, and notes. Reconcile conflicts against live GitHub, binaries, and Notion.

## 10. Pilot-first rule
No broad redeployment until these pass cleanup, deployment, and visual QA:
1. TOTFR Homepage
2. Chapter I
3. Braakport
4. Abbigail
5. Anchor Heart

One failed pilot blocks scale-out for its surface class.

## 11. Batch/session/stop rules
- Notion cleanup/deployment: max 5 materially similar items; reduce to one when uncertain.
- Scheduled GitHub production uploads: max 3 files.
- Lower/more-specific tool limits win.
- Never invent remaining context/session/connector/API/rate-limit capacity. Unknown capacity means smaller atomic batches.
- Never start a mutation unless the same atomic run can reasonably finish Audits A/B/C, mutation, validations, and checkpoint.
- Checkpoint at batch boundaries and after validated material items when practical: SOP/Git ref, surface/batch, last validated state, written-but-unvalidated item, residue state, exact next unstarted action, current error/limit.
- Checkpoint persistence failure = STOP new mutations; report last proven live state. Never reconstruct from memory.
- At rate/quota/tool/session limit: stop writes, do not hammer retries, re-fetch last target if possible, classify PROVEN PERSISTED / PROVEN ABSENT / UNKNOWN, checkpoint, never COMPLETE.
- Resume by reloading SOP + live GitHub/Notion + checkpoint; reconcile UNKNOWN first and revalidate last boundary.
- Before each batch ask: if the next tool call were the last available, would the project remain safe/resumable? If uncertain, shrink batch.
- Any unexplained mismatch, broken image, crop, residue, view behavior, or contradiction freezes that surface class and requires re-audit.

Limits never relax cleanup, audits, structural verification, visual QA, or completion gates.

## 12. Canon/spoiler
Current canon overrides old prompts/summaries. Artwork can spoil identities, transformations, villains, artifacts, locations, deaths, betrayals, encounters, and outcomes. Keep unrevealed assets DM HOLD. Never publish future session dates or unrevealed events as completed history.

## 13. Completion + zero-residue gate
Before COMPLETE, try to disprove it: identify inferred/unseen/stale evidence, technical success without visual proof, blank/broken/bad crop/title collision/mismatch/duplicate, and old links/media/preview settings.

Run three full-project audits:
1. Destination sweep: affected pages/records/views for old covers/icons/media/content images/embeds/bookmarks/preview settings/broken media.
2. Reference sweep: known old deployment URLs/filenames; every match intentional and approved.
3. Adversarial visual sweep: high-risk rendered surfaces checked specifically for failure.

Any unapproved residue or uncertainty = NOT COMPLETE. User-visible failure overrides ledger status immediately.

## 14. Existing failed deployment
Prior TOTFR Notion completion claims are invalid as proof. Existing image/page/view changes remain untrusted until re-audited. Old raw GitHub links, broken/blank media, incorrect covers/icons, wrong file properties, stale first-block images, duplicates, and preview workarounds are untrusted until classified and cleared/approved.

## 15. Failure recovery / manual fallback
On failure:
1. Never report completion.
2. Freeze affected surface class.
3. Record exact operation/result/destination/asset/last good state.
4. Re-run Audits A/B/C + residue inventory.
5. Classify failure: design, residue, storage/link, view, schema/property, tool/connector, permissions, crop/layout, write-size/preflight.
6. Produce one evidence-backed recovery path and audit it before execution.
7. Repeat all validations and residue sweep after correction.

If tools cannot safely remove bad Notion content, provide exact manual cleanup per destination: page/record, cover/icon, Files & media property, inline image/embed/bookmark/preview block, view preview source, old URL/filename patterns, expected clean state, exact replacement, final visual checks. Preserve campaign content/structure. If a safe step cannot be specified, report exact blocker.

## 16. Change control
This SOP is mandatory. Any deviation must name the rule/reason, pass Audits A/B/C, and receive explicit user approval. Never weaken guardrails for convenience, speed, API/context limits, or because a prior risky operation happened to succeed.
