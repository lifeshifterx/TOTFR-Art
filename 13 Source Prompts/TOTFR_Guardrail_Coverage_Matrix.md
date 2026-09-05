# TOTFR Guardrail Coverage Matrix

Status: AUDIT EVIDENCE — 2026-09-04-HARDENED-V6
Purpose: map known failure classes to prevention, detection, and fail-closed state. SOPs remain authoritative.

| Failure | Prevention | Detection | Fail state |
|---|---|---|---|
| Stale/contradictory manifest | Evidence hierarchy/startup | Live GitHub/binary/matrix compare | NEEDS REVIEW / STOP |
| Missing matrix index/shard/row | Matrix resolution gate | Index → shard → exact row | STOP |
| Guessed/stale matrix destination | Live source + Notion row-authoring gate | Row re-fetch/live recheck | STOP / NEEDS REVIEW |
| Duplicate active matrix row | Shard uniqueness | Cross-shard ID/path scan | STOP |
| Matrix near text limit | Shards <=8 KB | UTF-8 pre-write count | SPLIT REQUIRED / STOP |
| Approval not bound to exact binary | `source_sha` + `approved_binary_sha` | Recompute Git blob SHA | INVALID APPROVAL / STOP |
| Source/remaster changed after approval | SHA binding | Current vs stored SHA | STALE APPROVAL / RE-AUDIT |
| Impossible downstream state | State invariants | Validator prerequisites | INVALID STATE / STOP |
| Deployment lacks rollback/cleanup proof | Deployment invariant | Evidence refs required | DEPLOYMENT BLOCKED |
| Visual approval lacks render proof | Visual invariant | `visual_evidence_ref` | VISUAL QA REQUIRED |
| Wrong subject/canon | Art Audit A | Semantic/cross-surface QA | DESIGN REJECTED |
| DM/future spoiler | Audit A/C + canon gate | Visibility recheck | DM HOLD |
| Filename assumed to define surface | Art Audit B | Matrix vs live target | STOP |
| Wrong aspect/crop | Audit B/C | Full + target crop QA | DESIGN REJECTED |
| Text overlaps Notion UI | Locked text policy | Target-surface QA | DESIGN REJECTED |
| Gibberish typography | Art discipline | Pixel QA | DESIGN REJECTED |
| Broken anatomy/object fusion | Art rejection rules | Pixel QA | DESIGN REJECTED |
| Style/readability failure | Locked spec/adversarial audit | Visual/cross-surface QA | DESIGN REJECTED |
| Edit attempted without source pixels | App + Art capability gates | Source-access check | STOP / MANUAL SOURCE |
| New image substituted for requested edit | Source-preserving edit rule | Lineage comparison | DESIGN REJECTED |
| Prompt/spec drift | Spec lock | Stored lineage check | DESIGN REJECTED |
| `v01` overwritten | Version rule | Path/version check | WRITE FAILED / STOP |
| Rejected art committed | Art handoff gate | Design/source status | NOT COMPLETE |
| GitHub text truncation | Byte envelope + sentinel | Re-fetch tail/sections | WRITE FAILED |
| Cross-branch blob SHA reused | Exact target-ref read | Re-fetch / 409 analysis | WRITE FAILED / RE-AUDIT |
| Structural guardrail drift | Validator + Action | Validator/CI result | BLOCKED / STOP |
| Validator accepts known bad state | Mutation suite | Deliberate bad states | BLOCKED / STOP |
| Direct control-plane write to unprotected `development` | PR-first rule | Branch + PR CI | PROCESS VIOLATION / STOP |
| CI not branch-enforced | Exact-head fallback | Protection + exact-head run/jobs | PROCESS-ENFORCED / STOP |
| Old CI reused after later commit | Exact-head rule | Head SHA vs run SHA | STOP |
| Binary treated as text | Binary transport rule | Final binary QA | WRITE FAILED |
| Staging counted as production | Transport rule | Final-path audit | NOT COMPLETE |
| Wrong GitHub create/update path | Live target-path read | Exact path/blob re-fetch | WRITE FAILED |
| Library list omits new file | EXACT LIBRARY VERIFICATION | Exact lookup/read by ID/path | UNKNOWN / STOP |
| Wrong Notion page/view/property | Read-first + Audit B | Exact entity re-fetch | STOP / ROLLBACK |
| Write endpoint used to inspect | Capability rule | Operation-class check | STOP |
| Page cover mistaken for gallery preview | Notion view rule | Live view/preview read | STRUCTURAL FAILURE |
| Stored URL mistaken for render | Visual rule | Browser/screenshot QA | VISUAL QA REQUIRED |
| External link breaks | Native-media preference | Re-fetch + render QA | BROKEN / CLEANUP |
| Temporary Notion upload unattached | Native attachment rule | Final page/property read | WRITE FAILED |
| Old link/image remains | Zero-residue cleanup | Re-scan + clean-baseline QA | CLEANUP REQUIRED |
| First-block preview hack remains | Residue inventory | Page/view re-scan | CLEANUP REQUIRED |
| Schema changed for convenience | Notion schema rule | Schema diff | STOP / ROLLBACK |
| Campaign content altered | Structural validation | Content/relation diff | STOP / ROLLBACK |
| Pilot failure ignored | Pilot gate | Pilot-state check | SCALE-OUT BLOCKED |
| Repeated failure consumes session | Circuit breaker | Failure counter/threshold | CIRCUIT OPEN / FREEZE |
| Open circuit bypassed | Reset prerequisites | Row/checkpoint + fresh audits | STOP |
| Session/context limit mid-action | Batch/resume gate | Last-target read/checkpoint | UNKNOWN / PAUSED |
| Rate/tool error blindly retried | Failure rule | Error log + true read | STOP |
| Checkpoint write fails | Persistence gate | Exact Library verification | CHECKPOINT FAILURE / STOP |
| Memory used as resume truth | Resume rule | Reload live SOP/state | STOP |
| Ledger says complete but UI fails | Evidence precedence | User/browser evidence | NOT COMPLETE |
| 115 present treated as readiness | Authority deprecation | DESIGN APPROVED evidence | NOT COMPLETE |
| Completion without disproof | Final gate | Art/GitHub/residue/visual/adversarial audits | NOT COMPLETE |

## Cross-stage invariants
1. Art → GitHub requires DESIGN APPROVED bound to exact binary evidence.
2. Matrix = schema + index + bounded shard; one active row per asset.
3. GitHub → Notion rejects staging, rejected, unverified, or stale-approved sources.
4. Notion replacement requires CLEAN BASELINE VERIFIED + rollback evidence.
5. Structural success never implies visual success.
6. Visual success never bypasses final disproof.
7. Failure invalidates inherited downstream status for the affected item/class.
8. OPEN circuit blocks mutation/state advancement until governed reset.
9. Unprotected `development` requires PR-first control-plane changes + exact-head CI.
10. Library persistence requires exact lookup/read; broad listing alone is insufficient.

## Three-audit proof
**Audit 1 — Coverage:** known incident and sustainability failures have prevention, detection, and fail state.

**Audit 2 — Contradiction:** Main orchestrates; App governs tool/circuit/persistence; Art governs design; Upload Safety governs PR/transport/current-head authorization; Matrix governs evidence-bound asset state. Stricter rule wins.

**Audit 3 — Adversarial:** assume status, tool, listing, CI, or approval is wrong. Exact Library lookup, binary SHA binding, state prerequisites, rollback/evidence refs, mutation tests, PR/exact-head CI, visual QA, residue sweeps, and circuit breakers independently stop false completion or uncontrolled retry.

External systems can fail. This standard requires fail-closed, bounded recovery and independently checkable evidence.

END-OF-FILE SENTINEL: TOTFR-GUARDRAIL-COVERAGE-MATRIX-2026-09-04-HARDENED-V6
