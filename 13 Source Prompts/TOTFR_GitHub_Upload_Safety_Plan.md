# GitHub Upload Safety Plan

Status: MANDATORY TRANSPORT SOP
Version: 2026-09-04-HARDENED-V5

## 1. Non-negotiable text-write envelope
Observed behavior: connector text writes have previously truncated near ~20 KB. That is a failure observation, not an operating threshold.

For project `create_file`/`update_file` text:
- Prepare the final document before writing.
- Measure UTF-8 bytes, not characters, whenever a local/prepared source is available.
- Main project SOPs target <= 8,000 UTF-8 bytes.
- Any prepared direct text payload > 10,000 UTF-8 bytes = STOP; reduce or split before connector use.
- Never probe the limit with a live write.
- Do not manually expand a prepared document during the connector call.
- Every controlled SOP/manifest must end with a unique `END-OF-FILE SENTINEL`.
- After one write, re-fetch the exact target-branch file and verify returned SHA, required headings, and final sentinel.
- Missing sentinel, truncated/malformed tail, ambiguous fetch, or missing sections = WRITE FAILED. Stop dependent work.
- Never increase limits because a larger write succeeded before.
- Before every write, fetch the exact path on the exact target branch/ref. Never reuse a blob SHA obtained from another branch/ref.

If a document needs more detail, split it into small required modules. Missing required module = STOP.

## 2. Binary uploads
- Never send image binaries as inline UTF-8 through `create_file`/`update_file`.
- Prefer approved binary/blob transport.
- Base64 staging chunks: <= 8,000 characters and <= 8,000 UTF-8 bytes each.
- Verify decoded final binary path and size.
- Never count staging pieces as production assets.

## 3. Recurring uploader limits
1. Max 3 production files per scheduled run.
2. Fetch `development` before upload; skip already-valid final files.
3. Try approved binary path once.
4. If it fails, do not hammer retries; staged fallback only after preflight.
5. Max 12 staging chunk writes per run.
6. Verify final path/size before ledger update.
7. Stop transport scheduling only when the governed target's authoritative audit says Missing: 0; inventory completion never proves design/deployment completion.

## 4. Guardrail validator gate
Changes to README authority, mandatory SOPs, Surface Matrix schema/index/shards, Art Specs, validator, mutation tests, or workflow require:
1. pre-write byte/sentinel checks;
2. one write + exact target-branch re-fetch;
3. `tools/validate_totfr_guardrails.py` pass;
4. `tools/test_totfr_guardrails.py` prove known bad states are rejected;
5. `Validate TOTFR Guardrails` GitHub Action success for the exact resulting head.

Failed/pending/unknown validation blocks dependent art/remaster/deployment. Commit success is not validation.

## 5. PR-first control plane
Because `development` is not currently branch-protected, control-plane changes must use a dedicated `guardrails/*` branch and pull request.

Control-plane includes README authority, mandatory SOPs, validator/tests/workflow, Surface Matrix schema/index, and structural routing rules.
- Direct control-plane writes to `development` are prohibited unless the user explicitly authorizes an emergency exception after Audits A/B/C and rollback planning.
- Fetch the exact branch-local path/SHA immediately before each write.
- Open a PR to `development`; PR-head validator and mutation tests must pass.
- **PR FRESHNESS GATE:** before review/merge, compare the PR head against the current `development`. If the branch is behind, or the base advanced in any overlapping controlled file, STOP. Reconcile every upstream controlled-file delta, make the branch contain current `development` history, then require a new PR-head validation run. Green CI from the stale head is invalid.
- Review the full PR diff adversarially before merge. Once independent reviewer agents are available, at least one reviewer agent that did not author the change must approve the evidence/controls; authoring agents may not self-certify.
- Merge only the reviewed, green head SHA. After merge, require a new exact-`development`-head validation run; PR success cannot be inherited after merge.
- A later control-plane commit invalidates the prior authorization.

Preferred repository hardening remains branch protection/rulesets requiring this check, restricting direct pushes/bypass, and requiring review. If connector permissions cannot administer rules, do not claim protection exists; report the exact manual hardening step.

## 6. CURRENT-HEAD CI FALLBACK when branch protection is absent
Before dependent art generation/remaster, production upload, Matrix authoring, or Notion cleanup/deployment:
1. Fetch exact current `development` head SHA.
2. Fetch `Validate TOTFR Guardrails` run for that exact SHA.
3. Require `status=completed` and `conclusion=success`.
4. Confirm both clean-validator and mutation-test steps succeeded.
5. Missing/in-progress/failed/cancelled/skipped/uninspectable/wrong-SHA run = STOP.
6. Any later commit invalidates prior CI authorization; repeat.

This is PROCESS-ENFORCED until repository protection is actually enabled.

## 7. Session/resume
Never start a write unless the run can reasonably perform write + re-fetch verification + checkpoint. At any rate/quota/session/tool limit, stop new writes, classify last attempt PROVEN PERSISTED / PROVEN ABSENT / UNKNOWN when possible, checkpoint, and never infer completion.

END-OF-FILE SENTINEL: TOTFR-GITHUB-UPLOAD-SAFETY-2026-09-04-HARDENED-V5
