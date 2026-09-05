# TOTFR Art & Notion Deployment Guardrails

Status: MANDATORY PROJECT SOP
Scope: Tales of the Forgotten Realms art creation, correction, GitHub storage, Notion deployment, validation, and completion reporting.

## 1. Core operating principle

Fail closed. Do not infer success from partial evidence. A task is not complete because a file exists, a manifest says complete, an API call succeeded, a Notion property contains a URL, or a ledger says Verified.

The following states are distinct and must never be collapsed:
1. Source exists.
2. Source binary is valid.
3. Asset is suitable for the intended Notion surface.
4. Deployment write succeeded.
5. Destination structure is correct.
6. Asset visibly renders correctly in the actual Notion presentation.
7. User-visible result is accepted.

Only state 7 permits COMPLETE.

## 2. Mandatory evidence precedence

When sources conflict, use this order and document the conflict:
1. Live destination state and actual rendered result.
2. Current live GitHub repository tree on `development`.
3. Actual binary file inspection: dimensions, format, content, transparency, and visual composition.
4. Current Notion database/page/view schema fetched live.
5. Current versioned deployment/remaster manifest.
6. Package/local manifests and queue files.
7. Older production manifests, recovery manifests, historical prompts, and prior assistant summaries.

Older documentation is never silently reconciled into newer truth. Contradictions must be recorded.

## 2A. Mandatory startup gate

At the start of every future TOTFR art creation, correction, GitHub transfer, or Notion deployment run:
1. Fetch the current version of this SOP from `development`.
2. Record the SOP path/version or Git commit being followed in the run log/manifest.
3. Fetch the live destination schema/view before planning writes.
4. Load the current deployment/remaster manifest and reconcile unresolved states.
5. If this SOP cannot be fetched or its version cannot be established, STOP before any material write.

Scheduled/automated runs are not exempt. Their prompt must explicitly instruct the agent to load and obey this SOP before doing work.

No prior chat summary, memory, ledger, or assistant statement may substitute for loading the current SOP and live state.

## 3. Three audits required BEFORE every material action

No image edit, generation, GitHub production write, Notion deployment write, view change, schema change, or completion-state update may occur until all three audits pass.

### Audit A — Source and requirements audit
Prove:
- exact source file/path/version;
- live GitHub branch/ref;
- binary exists and is non-zero;
- dimensions/aspect ratio/file type known;
- subject/canon identity known;
- intended Notion destination identified;
- player-safe vs DM-only status known;
- applicable project documentation identified;
- any stale or contradictory documentation called out.

### Audit B — Destination compatibility audit
Prove from live Notion:
- exact page/database/data source/view;
- view type and card size;
- preview mechanism: page cover, page content, or Files & media property;
- crop/contain behavior where exposed;
- intended image property name if one exists;
- whether page cover, gallery card, inline header, icon, or other surface is required;
- whether native Notion title/UI will overlap or duplicate embedded artwork text;
- whether a schema change would be required.

Unknown destination behavior = STOP. Do not guess from filenames.

### Audit C — Adversarial audit
Attempt to disprove the proposed action. Ask at minimum:
- What evidence could make this mapping wrong?
- Could this technically succeed but remain invisible?
- Could Notion crop or resize it badly?
- Could embedded text collide with native Notion UI?
- Could the source URL break, redirect, expire, or be blocked?
- Could this expose future/DM-only information?
- Could this alter campaign content or database structure unintentionally?
- Could a stale manifest or prior ledger entry be misleading me?
- Can the action be rolled back without data loss?

Any unresolved material risk = STOP or NEEDS REVIEW.

The result of Audit A, Audit B, and Audit C must be recorded in the deployment/remaster manifest or execution log with concise evidence. Unrecorded audits do not count as passed.

## 4. Three validations required AFTER every material action

### Validation 1 — State validation
Re-fetch the source/destination and prove the intended write actually persisted.

### Validation 2 — Structural validation
Prove:
- correct asset;
- correct page/record/view/property;
- no unintended text deletion or rewrite;
- no unintended schema/property/relation changes;
- no duplicate or conflicting primary imagery;
- no spoiler/visibility regression;
- expected storage mechanism is in use.

### Validation 3 — Visual validation
Validate the actual rendered Notion presentation, not metadata.

A connector/API response is insufficient for visual validation. If the current environment cannot render the same UI the user sees, require one of:
- a browser-capable visual inspection; or
- a user-provided screenshot of the exact pilot/destination surface.

Without actual visual evidence, the maximum status is STRUCTURALLY VERIFIED. It may not be marked VISUALLY APPROVED or COMPLETE.

## 5. Status vocabulary

Use only these deployment states:
- SOURCE VERIFIED
- DESIGN AUDIT REQUIRED
- DESIGN APPROVED
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

`Verified` alone is prohibited because it is ambiguous.

COMPLETE requires SOURCE VERIFIED + DESIGN APPROVED + DEPLOYMENT WRITTEN + STRUCTURALLY VERIFIED + VISUALLY APPROVED, plus no unresolved blocker for that item.

## 6. Asset-design guardrails

Do not assume `Banner`, `Cover`, `Portrait`, or filename naming implies a Notion surface.

Before reuse, inspect every binary. Similar labels may have different aspect ratios and composition.

Do not force one asset to serve multiple incompatible purposes. Separate variants when needed:
- Page cover;
- Gallery/card preview;
- Inline chapter/section header;
- Icon/crest;
- Navigation tile.

For Notion page covers, treat the visible crop as responsive. Pixel dimensions alone do not prove suitability.

Embedded typography is prohibited on ordinary page covers unless the live destination has been visually tested and the text is intentionally required. Prefer native Notion page titles. Text-bearing art should normally be a separate inline header/title asset.

Critical faces, symbols, text, and objects must remain inside a tested crop-safe composition zone.

Do not regenerate an asset when recrop/recompose/remove-text is sufficient. Preserve source art and canon.

Never overwrite original `v01` art during remastering. New corrected files go under a separate remaster area and use a new version suffix.

Recommended repository area:
`14 Notion Remaster/`
with surface-specific subfolders.

## 7. Notion deployment guardrails

Prefer an existing dedicated Files & media property when the database already provides one. Examples established in the live template include NPC/Creature portrait fields and Magic Item image fields.

Do not insert a first-page image merely to manipulate a gallery preview when a dedicated image property exists.

Do not change a gallery/board preview mechanism until its current view configuration and property population are both audited.

Do not add or alter database schema solely to accommodate artwork without explicit approval after Audit B/C establishes that no existing supported destination is appropriate.

Do not use raw GitHub hotlinks as the default permanent Notion storage strategy. GitHub remains the archival source. Prefer Notion-native uploaded media where supported and validated.

If an external URL is intentionally used, validate that the exact destination renders it and record the dependency.

Never rewrite campaign text, lore, dates, relations, properties, or DM content for image placement.

## 8. GitHub guardrails

Retain the existing GitHub upload safety plan for transport integrity. Its scope is transport only; it does not certify design suitability or Notion deployment quality.

Before any binary production write:
- confirm target branch `development`;
- compare exact path against live repository;
- do not count staging/chunks/ZIPs as production;
- verify final path and binary size;
- avoid repeated failed connector upload attempts;
- use the documented staging workflow only when needed and after structural package validation.

The existing ZIP unpack workflow overwrites matching paths. Do not use it for remastered production files without a reviewed path manifest and explicit overwrite analysis.

## 9. Manifest guardrails

A manifest is a ledger, not proof.

Every current deployment/remaster manifest must include:
- manifest version/date;
- Git commit/ref audited;
- source asset;
- remastered asset if applicable;
- binary dimensions/type;
- intended Notion destination;
- surface type;
- preview/storage mechanism;
- player-safe/DM classification;
- statuses for all three pre-action audits;
- deployment status;
- all three post-action validations;
- final state;
- evidence/notes.

If two manifests conflict, do not choose one silently. Reconcile both against the live tree and binaries.

## 10. Pilot-first deployment rule

No broad redeployment is allowed until a representative pilot passes visual QA.

Required five-surface pilot unless project requirements change:
1. TOTFR Homepage;
2. Chapter I;
3. Braakport;
4. Abbigail;
5. Anchor Heart.

These intentionally test different surfaces.

Every pilot item must independently pass all three pre-action audits and all three post-action validations.

One failed pilot blocks scale-out for its affected surface class. Fix the system first; do not continue bulk deployment around it.

## 11. Batch-size and stop rules

After pilot approval, work by one surface class at a time in small audited batches. Do not combine materially different Notion surfaces in a single deployment batch.

Default maximum for Notion deployment work: 5 materially similar items per batch unless lower tool/API limits require fewer.

GitHub production binary uploads remain governed by `TOTFR_GitHub_Upload_Safety_Plan.md`: at most 3 production files per scheduled run. The lower/more-specific limit always wins.

At the first unexplained failure, mismatch, broken image, unexpected crop, unexpected view behavior, or contradiction:
- stop that surface class;
- preserve evidence;
- mark affected items NEEDS REVIEW or VISUAL QA REQUIRED;
- re-run all three audits before another write.

Do not compensate for a failed write by trying unrelated mutation approaches repeatedly.

## 12. Canon and spoiler guardrails

Current campaign canon overrides historical prompts and obsolete summaries.

Artwork can itself be a spoiler. Future chapter identities, transformations, villains, artifacts, locations, deaths, betrayals, and outcomes must remain DM HOLD until revealed or explicitly released.

No future session date or unrevealed event may be published as completed history.

## 13. Completion reporting guardrails

Before using the word COMPLETE, perform a completion-disproof review:
- What have I only inferred?
- What did I not visually observe?
- Which evidence could be stale?
- Which successful API call might not equal user-visible success?
- Are there any blank areas, broken images, crop problems, title collisions, or mismatched destinations?
- Is every required item accounted for with evidence?
- Has the user-visible result been visually accepted where visual acceptance is required?

If any material uncertainty remains, do not report COMPLETE.

Never report counts such as `77 verified` unless every item satisfies the exact defined state. Never use a ledger count to override contrary user-visible evidence.

User-visible evidence of failure immediately invalidates a conflicting internal completion status and triggers re-audit.

## 14. Existing failed deployment state

Prior TOTFR Notion deployment completion claims are invalidated as proof of success. Existing image/page/view changes must be treated as untrusted until individually re-audited under this SOP. Cleanup, rollback, or reuse of those changes is itself a material action and must pass the three audits before modification.

Do not build new work on the previous `Verified = 77` assumption.

## 15. Change-control rule for this SOP

This SOP is mandatory for future TOTFR art/Notion work.

Any proposed deviation must:
1. state the exact rule being changed;
2. explain why;
3. pass the three-audit process;
4. receive explicit user approval before execution.

Do not weaken a guardrail silently for convenience, speed, API limitations, or context limits.
