# GitHub Upload Safety Plan

## Observed connector behavior
- GitHub contents API text writes have previously truncated payloads near ~20 KB.
- Do not send large image data through `create_file`/`update_file` as inline text.
- Prefer `create_blob(..., encoding="base64")` for binary files whenever the payload succeeds intact.
- If a file must be staged as text, use <= 12,000 base64 characters per chunk (well below the observed ~20 KB clamp).
- Verify the resulting blob/file size before marking the asset uploaded.

## Recurring uploader guardrails
1. Process at most 3 production files per scheduled run.
2. Before each upload, fetch `development` and skip files already present with plausible size.
3. First try direct binary blob upload.
4. If direct blob upload fails once for that file, do not retry repeatedly in the same run; stage it in <=12,000-character chunks and decode via the existing GitHub Action.
5. Cap staging work at 12 chunk-write calls per run. If a file requires more, continue that same file on the next run.
6. Verify final path and size, then update the upload ledger.
7. Never count staging pieces as production assets.
8. Stop scheduling work once the GitHub manifest audit reports Missing: 0.
