# TOTFR Art & Notion Deployment Guardrails

Status: MANDATORY PROJECT SOP — 2026-09-04-HARDENED-V2

## 1. Fail closed / chain
Never equate generation success, file existence, manifest state, API success, URL, or ledger status with completion.

1. ART GENERATION/REMASTER → DESIGN APPROVED
2. GITHUB STORAGE → SOURCE VERIFIED
3. NOTION → CLEAN BASELINE VERIFIED → DEPLOYMENT WRITTEN → STRUCTURALLY VERIFIED → VISUALLY APPROVED
4. PROJECT → COMPLETE only after disproof audits.

Later stages never excuse earlier failures.

## 2. Mandatory startup
Before action:
1. Fetch this SOP from GitHub `development`.
2. Fetch `13 Source Prompts/TOTFR_App_Tool_Execution_Safety_SOP.md`.
3. Fetch `13 Source Prompts/TOTFR_Art_Generation_Remaster_QA_SOP.md`.
4. Before GitHub writes, fetch `13 Source Prompts/TOTFR_GitHub_Upload_Safety_Plan.md`.
5. Record SOP/module/Git refs.
6. Art: load Surface Matrix + source. Notion: fetch live schema/view + residue.
7. STOP if a module, source, Surface Matrix row, destination, or checkpoint is unknown.

Memory/chats never replace live reads. Evidence: rendered destination > live GitHub > inspected binary > live Notion > current Surface Matrix/manifest > older docs.

## 3. Three audits BEFORE every material action
Record all three.

**A Source:** exact source/ref/version, binary properties, canon, destination/surface, player-safe/DM class, conflicts.

**B Destination/Fit:** exact target; Notion page/database/view/card/preview/storage/image property/crop where relevant; title collision; schema impact; visual/link residue classified KEEP/REMOVE/REPLACE/UNKNOWN. UNKNOWN = STOP.

**C Adversarial:** try to prove failure: mapping, invisible success, crop/text defect, generated artifacts, broken source, spoiler, unintended change, stale residue, rollback, write-size/session/tool capacity. Unresolved risk = STOP/NEEDS REVIEW.

All app/tool actions obey App/Tool SOP. Art obeys Art SOP. GitHub writes obey Upload Safety.

## 4. Three validations AFTER material action
1. STATE: re-fetch and prove persistence.
2. STRUCTURE: correct asset/path/page/view/property; no unintended content/schema/relation change; no duplicate/stale/broken reference; no spoiler regression.
3. VISUAL/SEMANTIC: inspect generated pixels or rendered Notion surface as applicable. API success/metadata is insufficient.

No required visual evidence = VISUAL QA REQUIRED.

## 5. GitHub write gate
All GitHub writes obey Upload Safety. For controlled text: stay within its hard byte envelope, never probe limits, require an end sentinel, and re-fetch after one write. Any truncation/missing section/sentinel/ambiguity = WRITE FAILED. Missing required split module = STOP.

## 6. Art gate
No art enters production unless Art Generation SOP reports DESIGN APPROVED.

The Art SOP governs source/canon/surface locks, capability, composition/text, rejection criteria, technical/visual/cross-surface QA, `v01` preservation, rejection handling, and derivatives. GitHub existence never upgrades art status.

## 7. Notion cleanup/deployment
Before replacement, sweep all TOTFR Notion for residue, including unlogged targets.

Per destination:
1. Capture state.
2. Inventory cover/icon, Files & media, inline images/embeds/bookmarks, previews, view cover settings, external links.
3. Search old raw-GitHub URLs, filenames/versions, broken placeholders, duplicates, first-block workarounds.
4. Classify KEEP/REMOVE/REPLACE/UNKNOWN.
5. Clear REMOVE/REPLACE before new art. UNKNOWN = STOP.
6. Re-fetch removals; re-scan storage/display locations.
7. Visually prove no blank/broken/duplicate/stale image.
8. CLEAN BASELINE VERIFIED requires state + structural + visual cleanup validation.

Deploy only DESIGN APPROVED art by the audited surface mechanism. Prefer Files & media; no preview hacks when a dedicated property exists. Audit preview first. No art-only schema change without approval. Raw GitHub hotlinks are not default storage; external URLs require render validation. Never rewrite campaign content for art.

Zero unapproved residue required; preserve archival `v01` unless deletion authorized.

## 8. Pilot first
No broad redeployment until Homepage, Chapter I, Braakport, Abbigail, and Anchor Heart each pass art QA + cleanup + deployment + visual QA. Pilot failure blocks scale-out.

## 9. Batch/session/resume
- Art generation/remaster: max 3 related assets; one for new/failing classes.
- Notion cleanup/deployment: max 5 similar; one when uncertain.
- Scheduled GitHub production uploads: max 3.
- Lower tool limits win.
- Never invent remaining context/session/connector/API/rate capacity.
- Start mutation only if same run can finish audits, action, validations, checkpoint.
- Checkpoint: SOP/module/Git refs, last validated state, unvalidated item, residue, next action, error/limit.
- Checkpoint failure = STOP; never reconstruct from memory.
- At limit: stop actions/retries, re-fetch last target if possible, classify PROVEN PERSISTED / PROVEN ABSENT / UNKNOWN, checkpoint; never COMPLETE.
- Resume after reloading required SOPs + live state + source/checkpoint; reconcile UNKNOWN first.
- Before batch ask: if next call were last, is project safe/resumable? If uncertain, shrink batch.

Limits never relax QA.

## 10. Canon/spoilers
Current canon overrides old material. Artwork can itself spoil unrevealed identities, events, artifacts, and outcomes. Unrevealed assets remain DM HOLD; never publish future events as history.

## 11. Completion disproof
Before COMPLETE:
1. ART: every deployed asset DESIGN APPROVED; no rejected/unvalidated art.
2. GITHUB: expected current source/version on `development`; staging/chunks/obsolete files not final.
3. DESTINATION: no old covers/icons/media/content/previews/broken/duplicate residue.
4. REFERENCE: old URL/filename matches intentional/approved.
5. VISUAL: high-risk surfaces checked for blank/broken/crop/title/mismatch/readability/artifacts.
6. ADVERSARIAL: challenge counts, manifests, checkpoints, prior success against live evidence.

Residue, rejected/unvalidated art, UNKNOWN, or material uncertainty = NOT COMPLETE. User-visible failure overrides ledgers.

## 12. Existing failed state
Prior completion claims are invalid. Existing art/links/media/fields/preview workarounds and old design assumptions remain untrusted until re-audited.

## 13. Failure recovery/manual fallback
On failure:
1. Never report completion; freeze affected stage/class.
2. Record exact operation/result/destination/asset/last good state.
3. Re-run Audits A/B/C + applicable module checks.
4. Classify failure: design, generation, source pixels, residue, storage/link, view, schema/property, connector/tool, permissions, crop/layout, write-size, session/limit.
5. Produce one evidence-backed recovery path and audit before execution.
6. Repeat validations; failed items never inherit approval.

If tools cannot safely act, give exact manual/external steps: source/spec, asset/path, page/record, field/block/view, old URL patterns, clean state, replacement, visual checks. Preserve campaign content/structure; otherwise report exact blocker.

## 14. Status/control
Statuses include: INPUT/SURFACE/PLAN LOCKED, GENERATED/UNVALIDATED, DESIGN REJECTED/APPROVED, SOURCE VERIFIED, CLEANUP REQUIRED, CLEAN BASELINE VERIFIED, DEPLOYMENT WRITTEN, STRUCTURALLY VERIFIED, VISUAL QA REQUIRED, VISUALLY APPROVED, DM HOLD, NEEDS REVIEW, CANON CONFLICT, BROKEN/MISSING, NO DESTINATION, PAUSED AT VALIDATED CHECKPOINT, BLOCKED, COMPLETE.

`Verified` alone prohibited. Deviation requires named rule/reason, Audits A/B/C, explicit user approval.

END-OF-FILE SENTINEL: TOTFR-ART-NOTION-GUARDRAILS-2026-09-04-HARDENED-V2
