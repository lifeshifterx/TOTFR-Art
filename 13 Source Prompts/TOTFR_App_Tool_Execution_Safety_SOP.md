# TOTFR App & Tool Execution Safety SOP

Status: MANDATORY TOOL-CONTROL SOP — 2026-09-04-HARDENED-V3
Scope: every external app/tool operation used in TOTFR art production, GitHub storage, Notion cleanup/deployment, or persistent checkpointing.

## 1. Capability before action
Never assume a tool can safely perform an operation because another tool, prior session, or similar endpoint could.

Before material app/tool use:
1. Load the current tool/function schema or verified capability description.
2. Classify the operation READ, WRITE, DELETE, GENERATE, EDIT, UPLOAD, or VISUAL INSPECTION.
3. Confirm the selected function performs that class of operation.
4. Obtain required IDs/paths/files from a live read; never invent them.
5. Identify known size, rate, session, file-access, rendering, or permission limits.
6. If capability is missing/ambiguous, STOP rather than substituting a mutation or guessing.

A write/update endpoint must never be used as a substitute for a read/inspection endpoint.

## 2. Universal app cycle
For every material external action:
DISCOVER CAPABILITY → READ LIVE STATE → AUDITS A/B/C → ONE ATOMIC ACTION → RE-READ → STRUCTURAL QA → VISUAL QA IF REQUIRED → CHECKPOINT.

Do not batch independent writes ahead of validation. If any step cannot be completed, the item cannot advance beyond its last proven state.

## 3. Image generation/editing controls
- Generation from a written spec is distinct from editing an existing source.
- Editing a specific existing image requires usable source pixels available to the image-editing capability in the current context.
- A URL, filename, opaque ID, prior claim, or web result does not prove source access.
- If pixels are inaccessible, do not claim an edit/remaster occurred. Use a proven deterministic transform if sufficient; otherwise give the exact source/upload/external-production step.
- One generated result is not approved until Art Generation SOP QA passes.
- Tool success never proves typography, anatomy, crop, canon, or destination fit.
- If exact dimensions are not guaranteed, record actual output and use an audited deterministic crop/resize only after composition QA.
- Never silently substitute a newly imagined scene for a source-preserving remaster.

## 4. GitHub controls
- Before every write, fetch the exact target path from the exact target branch/ref immediately before mutation. A blob SHA from another branch/ref is never reusable, even when branches are believed to share a base.
- Read current target branch and exact path before writes.
- Text writes obey `TOTFR_GitHub_Upload_Safety_Plan.md`.
- Binary art uses approved binary/blob or validated staging, never accidental UTF-8 treatment.
- Create vs update comes from live target-branch path existence.
- Re-fetch exact target-branch path/blob after write; commit success alone is insufficient.
- Never count ZIPs/chunks/staging as final production.
- Never use a successful commit as proof of design approval or Notion readiness.

## 5. Notion controls
- Search/fetch/read before every mutation; identify exact page/database/data source/view/property.
- Never issue update-view/update-page merely to discover state.
- Capture current state and rollback-relevant values before page/view/schema/media mutation.
- Do not infer board/gallery visibility from page-cover metadata or rendering from a stored URL/API success.
- Prefer the destination's intended media property when present.
- For Notion-native import, use `notion-create-attachment` only with a direct publicly reachable HTTPS/signed source that does not require cookies/headers/redirects; respect size/time limits; attach within validity window; re-fetch final page/property. Temporary upload/source URL is never final proof.
- Schema/view changes require explicit audited necessity; do not restructure campaign data for art convenience.
- Cleanup obeys zero-residue rules.
- If the environment cannot render the user-facing Notion UI, stop at STRUCTURALLY VERIFIED / VISUAL QA REQUIRED until browser/screenshot evidence exists.

## 6. Files/Library/checkpoint controls
- Library/checkpoint data is a resume aid, not higher authority than live GitHub/Notion/binaries.
- Persist SOP snapshots only from a version already validated at the authoritative source.
- **EXACT LIBRARY VERIFICATION:** after persistence, verify exact destination by title/path search or direct read using returned file/library ID. Broad folder listing alone is insufficient.
- Confirm exact name/path and expected size/content marker.
- If broad list and exact lookup disagree, treat list as potentially stale; exact lookup/read must resolve it or state becomes UNKNOWN/STOP.
- Never reconstruct a failed/missing checkpoint from memory as persisted truth.

## 7. Tool failure + circuit breaker
At unexpected error, safety block, wrong-tool behavior, permission denial, rate limit, timeout, ambiguous response, or failed validation:
1. STOP new mutations for the affected item and preserve exact error/operation.
2. Re-read target with a true read operation if possible.
3. Classify last action PROVEN PERSISTED, PROVEN ABSENT, or UNKNOWN.
4. Re-run capability check + Audits A/B/C; choose one evidence-backed recovery path only.
5. Do not hammer alternate mutation functions to “see what works.”
6. If no safe tool path exists, provide exact manual/external steps.
7. First material failure stops/re-audits that item.
8. Second failure on the same item/recovery path, or second tool anomaly in the same stage during one run, OPENS THE CIRCUIT: no more writes for that item/stage in that run.
9. Third material failure anywhere in one run triggers GLOBAL MUTATION FREEZE and checkpoint.
10. Circuit reset requires fresh startup, exact-current-head guardrail CI success, a changed evidence-backed recovery plan, Audits A/B/C PASS, and persisted checkpoint. A simple retry is not a reset.

## 8. Adversarial tool check
Before each batch ask:
- Am I using read to read and write to write?
- Did live state supply every ID/path/property?
- Is the SHA/path from this exact target branch/ref?
- Can the tool access the actual source file/pixels?
- Can it validate the user-visible result, or only metadata?
- Could the response be partial/truncated/stale?
- If the next call were the last available, is the project safe/resumable?
- Am I using a workaround because the correct capability is unavailable?
- Has any circuit-breaker threshold been reached?

Any concerning answer = shrink to one, switch to read-only investigation, or STOP.

## 9. Completion rule
No app/tool operation can independently produce COMPLETE. Completion comes only from the governed Art, GitHub, Notion, visual, residue, evidence, and disproof gates.

END-OF-FILE SENTINEL: TOTFR-APP-TOOL-EXECUTION-SAFETY-2026-09-04-HARDENED-V3
