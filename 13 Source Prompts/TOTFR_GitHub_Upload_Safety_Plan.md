# GitHub Upload Safety Plan

Status: MANDATORY TRANSPORT SOP

## 1. Hard text-write preflight
Observed behavior: GitHub contents API text writes have previously truncated near ~20 KB. That observed threshold is NOT an operating limit.

For every project `create_file` or `update_file` text payload:
1. Construct the exact final UTF-8 payload before calling GitHub.
2. Measure UTF-8 bytes, not characters.
3. HARD MAX = **12,000 bytes**. Above 12,000 bytes: DO NOT CALL THE WRITE TOOL.
4. Reduce or split first; never test the limit with a live write.
5. Compute expected Git blob SHA: SHA1(`b"blob " + str(byte_count) + b"\0" + payload_bytes`).
6. Record byte count and expected SHA before write.
7. After one write, re-fetch the exact file and require the expected blob SHA and complete content.
8. Any mismatch/truncation/ambiguous result = WRITE FAILED; stop dependent work.
9. Never raise the 12,000-byte ceiling because a larger prior write succeeded.

This applies to SOPs, manifests, prompts, ledgers, documentation, changelogs, scripts written as text, and staged base64 text.

## 2. Binary uploads
- Do not send image binaries through `create_file`/`update_file` as inline UTF-8 text.
- Prefer binary/blob workflows where supported.
- If binary data must be staged as base64 text, each chunk must also be <= 12,000 characters AND <= 12,000 UTF-8 bytes.
- Verify decoded final binary path and size before marking uploaded.
- Never count staging pieces as production assets.

## 3. Recurring uploader limits
1. Process at most 3 production files per scheduled run.
2. Before each upload, fetch `development`; skip already-valid final files.
3. Try the approved binary upload path once.
4. If it fails, do not repeatedly hammer the same operation; use the documented staging fallback only after its preflight passes.
5. Cap staging at 12 chunk-write calls per run; continue the same file in a later run if needed.
6. Verify final path/size, then update the ledger.
7. Stop scheduling transport work when the authoritative manifest audit is Missing: 0.

## 4. Session/resume safety
Never start a write unless the run can reasonably perform the write, re-fetch verification, and checkpoint. At any rate/quota/session/tool limit, stop new writes, classify the last attempt as PROVEN PERSISTED / PROVEN ABSENT / UNKNOWN when possible, persist a resume point, and never infer completion.
