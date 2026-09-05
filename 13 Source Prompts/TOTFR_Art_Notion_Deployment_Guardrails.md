# TOTFR Art & Notion Deployment Guardrails

Status: MANDATORY PROJECT SOP — 2026-09-04-HARDENED-V6

## 0. VERIFY THEN TRUST
Treat remembered, cached, reported, previously green, or user-described state as UNTRUSTED until the current authoritative source is read. Trust applies only to the exact object/ref/SHA/config/result proven and only to that evidence domain.

Any branch/file/blob/workflow/ruleset/plan/Notion/binary change, session restart, failed validation, stale read, or contradiction invalidates dependent trust and requires re-verification.

## 1. Fail closed
Never equate generation, file existence, API/URL success, ledger status, agent review, or CI with completion.

ART → DESIGN APPROVED → SOURCE VERIFIED → CLEAN BASELINE VERIFIED → DEPLOYMENT WRITTEN → STRUCTURALLY VERIFIED → VISUALLY APPROVED → adversarial disproof → COMPLETE.

## 2. Startup / authority
Before material work:
1. Resolve immutable `control_ref`; load `AGENTS.md`, Main/App/Art/Upload/Transactional SOPs, Agent Role Matrix, Agent Trust Boundary, Runtime Evidence Policy, Required GitHub Protection, Publication Boundary, Deployment Run format, and Surface Matrix schema/index/shard from that exact commit.
2. Never substitute mutable `development`, memory, chat, another branch, or later commit.
3. Inspect source binary from its approved immutable source commit/path/blob.
4. Inspect exact live Notion destination IDs/view/property/content state.
5. Verify live GitHub integration ruleset and exact required CI state.
6. Missing/ambiguous module, source, matrix row, destination, precondition, checkpoint, or protection evidence = STOP.

## 3. Independent evidence domains
Prove separately:
- SOURCE: immutable commit/path/blob + inspected materialized binary.
- CANON/PRIVACY: current canon + PLAYER-SAFE/DM classification.
- DESTINATION: live Notion IDs/schema/view/property/content.
- CONCURRENCY: live fingerprint equals approved precondition.
- STRUCTURE: post-write desired state and zero collateral/residue.
- BINARY: delivered bytes equal approved bytes when retrievable.
- VISUAL: authenticated rendered UI + durable privacy-correct artifact.
- CONTROL: pinned controls + sufficient live GitHub protection + exact required CI.

One domain never proves another.

## 4. Three audits before material action
**A Source:** exact source/ref/blob, materialized binary, canon/privacy, conflicts, publication boundary.

**B Destination/Fit:** exact target, preview/storage/crop, collision, residue, precondition, rollback, idempotent desired state. UNKNOWN = STOP.

**C Adversarial:** try to prove mapping, privacy, crop, source, transport, residue, rollback, concurrency, prompt-injection, secret, session/rate/tool, identity, stale-approval, or control-plane failure. Unresolved material risk = STOP/NEEDS REVIEW.

Tool work obeys App SOP; art obeys Art QA; GitHub obeys Upload Safety; Notion obeys Transactional SOP.

## 5. After-action validation
1. Re-fetch exact target and prove persistence against plan/precondition.
2. Prove correct asset/path/page/view/property; no content/schema/relation collateral; no stale/duplicate/broken residue; verify bytes when possible.
3. Inspect actual pixels/rendered Notion surface and persist durable visual evidence.

No required render evidence = VISUAL QA REQUIRED.

## 6. Art / publication
Only DESIGN APPROVED art enters production. Approval binds exact reviewed materialized binary hash/version. Never overwrite `v01`.

Public distribution is PLAYER-SAFE only. DM/future/spoiler assets and evidence require private storage. Public history exposure remains exposure after branch deletion; a clean public namespace or private conversion is required before that boundary is considered remediated.

Desired external URLs are immutable commit-pinned sources, never mutable branch URLs. GitHub existence never upgrades status.

## 7. Transactional Notion deployment
Current workspace is CONTAMINATED/UNTRUSTED until a new governed run proves otherwise.

No broad/free-form deployment. Use frozen inventory + desired-state diff + exact plan hashes + trust-compliant review + one Notion writer + per-target WAL/receipt/visual evidence.

Per mutation:
PRECONDITION READ → LEASE → WAL → ONE WRITE → BOUNDED CONFIRMATION READS → STRUCTURAL/BINARY QA → RECEIPT → VISUAL GATE.

Live change = CONCURRENT_CHANGE / STOP. Rollback only when live state still equals this run's post-state; otherwise ROLLBACK_CONFLICT / STOP.

Remove old covers/icons/media/links/preview hacks before replacement. Re-fetch, rescan and visually prove zero unapproved legacy residue before CLEAN BASELINE VERIFIED. Never hide residue behind new art.

Avoid full-page replacement. New first-block/page-content gallery hacks are prohibited. Missing stable gallery media property = SCHEMA_MIGRATION_REQUIRED (Tier 2).

Never persist signed Notion/S3 query strings or temporary credentials.

## 8. Canaries / trust
Before scale-out prove one canary per planned Tier-1 mechanism: pinned cover/icon, native file property, gallery media property, residue removal.

Tier-2 means schema/view/root navigation/player-DM/publication/control-plane. While Agent Trust Boundary identity enforcement is UNCONFIGURED, Tier-2 agent execution is prohibited. Extra agent labels or repository attestations do not override it.

Exactly one `notion_executor` mutates Notion. Parallelize inspection/review, not mutation. Shared run budget <=2 Notion requests/second average; one write in flight.

Circuit: first material failure stops/re-audits item; second same-path failure/stage anomaly opens circuit; third material run failure freezes all mutation.

## 9. GitHub integration
`development` is merge/integration only for agents. Governed control/art changes use bounded working branches + PRs.

A `protected:true` label is insufficient. Live protection must satisfy `TOTFR_Required_GitHub_Protection.json`: PR gate, strict current-head `validate` + `control-plane-integrity`, deletion/non-fast-forward protection, and no unconditional integration bypass.

Insufficient protection = STOP; no CI-only fallback.

## 10. Completion disproof
Before COMPLETE prove:
1. every governed target inventoried/dispositioned;
2. every deployed asset DESIGN APPROVED and current-byte bound;
3. no mutable URL, public DM source/evidence, or unresolved spoiler exposure;
4. no old cover/icon/media/link/preview-hack/broken/duplicate residue;
5. every receipt matches current destination + immutable plan, including required confirmation reads;
6. required rendered checks + durable artifacts pass;
7. no signed token/secret persisted;
8. no fake identity, self/stale review, open circuit, CONCURRENT_CHANGE, ROLLBACK_CONFLICT or UNKNOWN ignored;
9. current integration protection + exact required CI contexts are verified.

Any contradiction or user-visible failure = NOT COMPLETE.

## 11. Existing failed state / fallback
Prior completion claims remain invalid. Existing branch URLs, page-content preview workarounds, public DM history, residue and design assumptions stay untrusted until remediated.

On failure: freeze affected mutation; preserve sanitized evidence; re-read live state; rerun A/B/C; choose one changed evidence-backed recovery; revalidate. Never probe capability with mutations or hammer alternate writes.

If an evidence domain cannot be automated safely, stop at last proven state and specify exact manual source/target/field/precondition/action/verification.

## 12. Status
Use explicit states: DESIGN APPROVED/REJECTED, SOURCE VERIFIED, CLEANUP REQUIRED, CLEAN BASELINE VERIFIED, DEPLOYMENT WRITTEN, STRUCTURALLY VERIFIED, VISUAL QA REQUIRED, VISUALLY APPROVED, DM HOLD, BLOCKED_PRIVATE_SOURCE, SCHEMA_MIGRATION_REQUIRED, CONCURRENT_CHANGE, ROLLBACK_CONFLICT, NEEDS REVIEW, BROKEN/MISSING, NO DESTINATION, PAUSED AT VALIDATED CHECKPOINT, BLOCKED, COMPLETE.

`Verified` alone is prohibited.

END-OF-FILE SENTINEL: TOTFR-ART-NOTION-GUARDRAILS-2026-09-04-HARDENED-V6
