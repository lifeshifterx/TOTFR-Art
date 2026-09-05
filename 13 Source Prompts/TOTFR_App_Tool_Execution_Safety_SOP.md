# TOTFR App & Tool Execution Safety SOP

Status: MANDATORY TOOL-CONTROL SOP — 2026-09-04-HARDENED
Scope: every external app/tool operation used in TOTFR art production, GitHub storage, Notion cleanup/deployment, or persistent checkpointing.

## 1. Capability before action
Never assume a tool can safely perform an operation because another tool, prior session, or similar endpoint could.

Before material app/tool use:
1. Load the current tool/function schema or verified capability description.
2. Identify whether the operation is READ, WRITE, DELETE, GENERATE, EDIT, UPLOAD, or VISUAL INSPECTION.
3. Confirm the selected function actually performs that class of operation.
4. Identify required IDs/paths/files from a live read; never invent them.
5. Identify known size, rate, session, file-access, rendering, or permission limits.
6. If capability is missing/ambiguous, STOP rather than substituting a mutation or guessing.

A write/update endpoint must never be used as a substitute for a read/inspection endpoint.

## 2. Universal app cycle
For every material external action:
DISCOVER CAPABILITY → READ LIVE STATE → AUDITS A/B/C → ONE ATOMIC ACTION → RE-READ → STRUCTURAL QA → VISUAL QA IF REQUIRED → CHECKPOINT.

Do not batch independent writes ahead of validation.

If any step cannot be completed, the item cannot advance beyond its last proven state.

## 3. Image generation/editing controls
- Generation from a written spec is distinct from editing an existing source.
- Editing a specific existing image requires usable source pixels available to the image-editing capability in the current context.
- A URL, filename, opaque ID, prior claim that an image exists, or web search result does not prove the editor can access the source.
- If source pixels are inaccessible, do not claim an edit/remaster occurred. Use a proven deterministic transform if sufficient; otherwise provide the exact required upload/source step or external production prompt.
- One generated result is not approved until Art Generation SOP QA passes.
- Tool success never proves typography, anatomy, crop, canon, or destination fit.
- If exact output dimensions are not natively guaranteed, record the generated dimensions and use a separately audited deterministic crop/resize/export step only after composition QA.
- Do not silently substitute a newly imagined scene for a requested source-preserving remaster.

## 4. GitHub controls
- Read current `development` and exact target path before writes.
- Text writes obey `TOTFR_GitHub_Upload_Safety_Plan.md`.
- Binary art must use an approved binary/blob or validated staging workflow, never accidental UTF-8 treatment.
- Create vs update is determined from live path existence.
- After write, re-fetch exact path/blob and verify the intended object, not only the commit response.
- Never count ZIPs/chunks/staging as final production.
- Never use a successful commit as proof of design approval or Notion readiness.

## 5. Notion controls
- Search/fetch/read before every mutation; identify exact page/database/data source/view/property.
- Use read/search/fetch functions for inspection. Never issue update-view/update-page merely to discover current state.
- Before page/view/schema/media mutation, capture current state and rollback-relevant values.
- Do not infer board/gallery visibility from page-cover metadata.
- Do not infer visual rendering from a stored URL or API success.
- Prefer the destination's existing intended media property when present.
- When using Notion-native file import, prefer `notion-create-attachment` only with a direct publicly reachable HTTPS source or valid signed URL that does not require cookies/headers or redirects; respect workspace file-size/time limits; attach the returned upload within its validity window; then re-fetch the final page/property. A temporary upload or source URL is never the final proof.
- Schema/view changes require explicit audited necessity; image placement must not restructure campaign data for convenience.
- Cleanup uses the zero-residue rules in the main SOP.
- If the environment cannot render the user-facing Notion UI, status stops at STRUCTURALLY VERIFIED / VISUAL QA REQUIRED until browser/screenshot evidence exists.

## 6. Files/Library/checkpoint controls
- Persistent Library/checkpoint data is a resume aid, not higher authority than live GitHub/Notion/binaries.
- Overwrite/update persistent SOP snapshots only from a version already validated at the authoritative source.
- Verify resulting path/version/size after persistence writes.
- Never reconstruct a failed/missing checkpoint from memory and present it as persisted truth.
- A checkpoint records UNKNOWN states rather than resolving them by assumption.

## 7. Tool failure classification
At unexpected error, safety block, wrong-tool behavior, permission denial, rate limit, timeout, or ambiguous response:
1. STOP new mutations for the affected stage/class.
2. Preserve exact error/operation.
3. Re-read the target with a true read operation if possible.
4. Classify last action PROVEN PERSISTED, PROVEN ABSENT, or UNKNOWN.
5. Re-run capability check + Audits A/B/C.
6. Use one evidence-backed recovery path only.
7. Do not hammer alternate mutation functions to “see what works.”
8. If no safe tool path exists, provide exact manual/external steps.

## 8. Adversarial tool check
Before each batch ask:
- Am I using a read tool to read and a write tool to write?
- Did live state supply every ID/path/property?
- Can the tool access the actual source file/pixels?
- Can it validate the user-visible result, or only metadata?
- Could the response be partial/truncated/stale?
- If this is the last available call, is the project safe and resumable?
- Am I about to use a workaround because the correct capability is unavailable?

Any concerning answer = shrink to one, change to read-only investigation, or STOP.

## 9. Completion rule
No app/tool operation can independently produce COMPLETE. Completion comes only from the governed project chain and its required Art, GitHub, Notion, visual, residue, and disproof gates.

END-OF-FILE SENTINEL: TOTFR-APP-TOOL-EXECUTION-SAFETY-2026-09-04-HARDENED
