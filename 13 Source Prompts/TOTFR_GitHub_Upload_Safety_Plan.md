# GitHub Upload Safety Plan

Status: MANDATORY TRANSPORT SOP
Version: 2026-09-04-HARDENED-V3

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
- After one write, re-fetch the exact file and verify returned SHA, required headings, and final sentinel.
- Missing sentinel, truncated/malformed tail, ambiguous fetch, or missing sections = WRITE FAILED. Stop dependent work.
- Never increase these limits because a larger write succeeded before.

If a document needs more detail, split it into small required modules. The parent must enumerate all modules; missing module = STOP.

## 2. Binary uploads
- Never send image binaries as inline UTF-8 through `create_file`/`update_file`.
- Prefer approved binary/blob transport.
- Base64 staging chunks: <= 8,000 characters and <= 8,000 UTF-8 bytes each.
- Verify decoded final binary path and size.
- Never count staging pieces as production assets.

## 3. Recurring uploader limits
1. Max 3 production files per scheduled run.
2. Fetch `development` before upload; skip already-valid final files.
3. Try the approved binary path once.
4. If it fails, do not hammer retries; use staged fallback only after preflight.
5. Max 12 staging chunk writes per run.
6. Verify final path/size before ledger update.
7. Stop transport scheduling when authoritative audit reports Missing: 0 for the governed target.

## 4. Guardrail validator gate
Changes to README authority, mandatory SOPs, Surface Matrix schema/index/shards, Art Specs, this validator, mutation tests, or workflow require:
1. pre-write byte/sentinel checks;
2. one write + exact re-fetch;
3. `tools/validate_totfr_guardrails.py` to pass on the resulting tree;
4. `tools/test_totfr_guardrails.py` to prove known bad states are rejected;
5. the `Validate TOTFR Guardrails` GitHub Action to complete successfully for the resulting head.

A failed/pending/unknown validator state blocks dependent art/remaster/deployment work. Do not interpret the commit itself as validation.

## 5. CURRENT-HEAD CI FALLBACK when branch protection is absent
Repository protection must be inspected before dependent work. If `development` does not enforce the guardrail status check at the repository level, classify the gate as **PROCESS-ENFORCED**, not repository-enforced.

Before any dependent art generation/remaster, production upload, Surface Matrix authoring, or Notion cleanup/deployment:
1. Fetch the exact current `development` head SHA.
2. Fetch the `Validate TOTFR Guardrails` workflow run for that exact SHA.
3. Require `status=completed` and `conclusion=success`.
4. Confirm both the clean validator step and mutation-test step completed successfully.
5. If no exact-head run exists, is queued/in-progress, failed/cancelled/skipped, cannot be inspected, or refers to another SHA: STOP. Never inherit success from an earlier commit.
6. A later commit invalidates the prior head's CI authorization; repeat this gate.

Preferred repository hardening is branch protection/rulesets requiring the guardrail check and restricting bypass/direct pushes. If current connector permissions cannot administer repository rules, do not pretend protection was enabled; retain this exact-head fallback and report the manual hardening step.

## 6. Session/resume
Never start a write unless the run can reasonably perform write + re-fetch verification + checkpoint. At any rate/quota/session/tool limit, stop new writes, classify the last attempt PROVEN PERSISTED / PROVEN ABSENT / UNKNOWN when possible, checkpoint, and never infer completion.

END-OF-FILE SENTINEL: TOTFR-GITHUB-UPLOAD-SAFETY-2026-09-04-HARDENED-V3
