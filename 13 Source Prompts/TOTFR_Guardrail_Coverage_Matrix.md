# TOTFR Guardrail Coverage Matrix

Status: AUDIT EVIDENCE — 2026-09-04-HARDENED-V5
Purpose: map known failure classes to prevention, detection, and fail-closed state. Evidence only; mandatory SOPs remain authoritative.

| Failure class | Preventive control | Detection/validation | Required fail state |
|---|---|---|---|
| Stale/contradictory manifest | Main evidence hierarchy/startup | Live GitHub/binary/matrix reconciliation | NEEDS REVIEW / STOP |
| Missing matrix index/shard/row | Art matrix-resolution gate | Index → shard → exact row | STOP |
| Matrix row authored from guess/stale destination | Index row-authoring gate + live source/Notion reads | Row re-fetch + live revalidation | STOP / NEEDS REVIEW |
| Duplicate active matrix row | Shard uniqueness rule | Cross-shard ID/path check | STOP |
| Surface Matrix grows near text limit | Shards <=8 KB | Pre-write UTF-8 byte check | SPLIT REQUIRED / STOP |
| Approval status not bound to exact binary | Evidence-bound `source_sha`/`approved_binary_sha` | Git blob recomputation | INVALID APPROVAL / STOP |
| Source/remaster changes after approval | SHA-binding invariant | Current file SHA vs stored approval SHA | STALE APPROVAL / RE-AUDIT |
| Impossible downstream state | Machine state-transition invariants | Validator prerequisite checks | INVALID STATE / STOP |
| Deployment lacks rollback/cleanup evidence | Matrix deployment invariant | Required evidence refs | CLEANUP/DEPLOYMENT BLOCKED |
| Visual approval lacks rendered evidence | Matrix visual invariant | `visual_evidence_ref` + structural prerequisite | VISUAL QA REQUIRED |
| Wrong subject/canon | Art Audit A | Visual/semantic + cross-surface QA | DESIGN REJECTED |
| DM/future spoiler | Art Audit A/C + canon gate | Visibility re-check | DM HOLD |
| Filename assumed to define surface | Art Audit B | Matrix row vs live target | STOP |
| Wrong aspect/crop | Art Audit B/C | Full + cropped/small-view QA | DESIGN REJECTED |
| Text overlaps Notion UI | Locked text policy | Target-surface visual QA | DESIGN REJECTED |
| Gibberish/generated typography | Art generation discipline | Pixel visual QA | DESIGN REJECTED |
| Broken anatomy/object fusion | Art rejection criteria | Pixel visual QA | DESIGN REJECTED |
| Style/readability failure | Locked spec/adversarial audit | Visual + cross-surface QA | DESIGN REJECTED |
| Source edit without accessible pixels | App + Art capability gates | Source-access check | STOP / manual source step |
| New image substituted for requested edit | App image-edit rule | Source/prompt lineage | DESIGN REJECTED |
| Prompt/spec drift | Production-spec lock | Stored prompt/edit lineage | DESIGN REJECTED |
| `v01` overwritten | Art version rule | Source/version/path validation | WRITE FAILED / STOP |
| Rejected art committed | Art handoff gate | Design-state/source lineage | NOT COMPLETE |
| GitHub text truncation | Upload byte envelope + sentinel | Re-fetch tail/sections | WRITE FAILED |
| Cross-branch blob SHA reused | Exact target-branch read before write | Target-branch re-fetch / 409 analysis | WRITE FAILED / RE-AUDIT |
| Guardrail/matrix structural drift | Machine validator + Action | Validator exit + workflow conclusion | BLOCKED / STOP |
| Validator accepts known bad state | Mutation test suite | Deliberate bad-state tests | BLOCKED / STOP |
| Direct control-plane write to unprotected `development` | PR-first control-plane rule | Branch/ref + PR-head CI review | PROCESS VIOLATION / STOP |
| CI is not branch-enforced | Exact-head CI fallback | Branch protection + exact-head run/jobs | PROCESS-ENFORCED / STOP until green |
| Prior CI success reused after later commit | Exact-head SHA rule | Head SHA vs workflow head_sha | STOP |
| Binary treated as text | Upload + App GitHub rules | Binary path/size/open QA | WRITE FAILED |
| Staging counted as production | Upload rules | Live final-path audit | NOT COMPLETE |
| Wrong GitHub create/update path | App live-path read | Re-fetch exact path/blob | WRITE FAILED |
| Library folder list omits recent persisted file | App EXACT LIBRARY VERIFICATION | Exact title/path search or direct read using returned ID | UNKNOWN until exact lookup; STOP if unresolved |
| Wrong Notion page/view/property | App read-first + Audit B | Exact entity/structure re-fetch | STOP / rollback |
| Write endpoint used for inspection | App capability rule | Operation-class check | STOP |
| Page cover mistaken for gallery preview | App Notion rule | Live view/preview fetch | STRUCTURAL FAILURE |
| Stored URL mistaken for visible render | Main/App visual rule | Browser/screenshot QA | VISUAL QA REQUIRED |
| External link breaks | Native-media preference | Re-fetch + rendered QA | BROKEN / CLEANUP REQUIRED |
| Temporary Notion upload unattached | App native attachment rule | Final page/property re-fetch | WRITE FAILED |
| Old link/image remains | Zero-residue cleanup | Re-scan + visual clean baseline | CLEANUP REQUIRED |
| First-block preview hack remains | Residue inventory | Page/view re-scan | CLEANUP REQUIRED |
| Schema changed for convenience | Main/App Notion rules | Schema diff/re-fetch | STOP / rollback |
| Campaign content altered | Structural validation | Content/schema/relation comparison | STOP / rollback |
| Pilot failure ignored | Main pilot gate | Pilot-state check | SCALE-OUT BLOCKED |
| Repeated failure consumes session | App/Matrix circuit breaker | Failure counters + run threshold | CIRCUIT OPEN / MUTATION FREEZE |
| Open circuit bypassed by retry | Circuit-reset prerequisites | Current row/checkpoint + fresh audits | STOP |
| Session/context limit mid-action | Main batch/resume | Last-target re-fetch/checkpoint | UNKNOWN / PAUSED |
| Rate/tool error retried blindly | App failure rule | Error log + true read | STOP |
| Checkpoint write fails | Main session gate | Exact Library persistence verification | CHECKPOINT FAILURE / STOP |
| Memory used as resume truth | Main/App resume rules | Reload SOP/live state/checkpoint | STOP |
| Ledger says complete but UI fails | Evidence precedence | User/browser evidence | NOT COMPLETE |
| 115 present treated as readiness | README/Main/legacy deprecation | DESIGN APPROVED evidence | NOT COMPLETE |
| Completion without disproof | Main completion gate | Art/GitHub/residue/visual/adversarial sweeps | NOT COMPLETE |

## Cross-stage invariants
1. Art → GitHub: no production write without DESIGN APPROVED bound to exact binary evidence.
2. Matrix: schema + index + bounded shard; exactly one active row per asset.
3. GitHub → Notion: no rejected/staging/unverified/stale-approved source.
4. Notion replacement: no new art before CLEAN BASELINE VERIFIED with rollback evidence.
5. Structural success never implies visual success.
6. Visual success never bypasses final disproof audits.
7. Failure invalidates downstream inherited status for the affected item/class.
8. Open circuit blocks mutation/state advancement until governed reset.
9. Unprotected `development` requires PR-first control-plane changes plus exact-head CI before downstream use.
10. Persistent Library writes require exact lookup/read proof; broad folder listing alone never establishes absence or success.

## Three-audit proof
**Audit 1 — Coverage:** incident failures and newly discovered sustainability failures have prevention + detection + fail state.

**Audit 2 — Contradiction:** Main orchestrates; App governs tool/circuit/persistence behavior; Art governs design; Upload Safety governs PR/transport/current-head authorization; Matrix schema/index/shards govern evidence-bound per-asset state. Stricter rule wins.

**Audit 3 — Adversarial:** assume a status, tool, listing, CI result, or prior approval lies. Exact Library lookup, binary SHA checks, state prerequisites, rollback/evidence refs, mutation tests, PR-head CI, exact-head CI, visual QA, residue sweeps, and circuit breakers independently block false completion or uncontrolled retry.

External services can fail, permissions can change, and rendering can differ. The standard targets fail-closed, bounded recovery and independently checkable evidence, not impossible guarantees about external systems.

END-OF-FILE SENTINEL: TOTFR-GUARDRAIL-COVERAGE-MATRIX-2026-09-04-HARDENED-V5
