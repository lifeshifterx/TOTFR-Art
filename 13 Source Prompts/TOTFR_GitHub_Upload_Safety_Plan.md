# GitHub Upload Safety Plan

Status: MANDATORY TRANSPORT SOP
Version: 2026-09-04-HARDENED

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
4. If it fails, do not hammer retries; use the staged fallback only after preflight.
5. Max 12 staging chunk writes per run.
6. Verify final path/size before ledger update.
7. Stop transport scheduling when authoritative audit reports Missing: 0.

## 4. Session/resume
Never start a write unless the run can reasonably perform write + re-fetch verification + checkpoint. At any rate/quota/session/tool limit, stop new writes, classify the last attempt PROVEN PERSISTED / PROVEN ABSENT / UNKNOWN when possible, checkpoint, and never infer completion.

END-OF-FILE SENTINEL: TOTFR-GITHUB-UPLOAD-SAFETY-2026-09-04-HARDENED
