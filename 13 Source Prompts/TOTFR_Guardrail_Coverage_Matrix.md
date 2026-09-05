# TOTFR Guardrail Coverage Matrix

Status: AUDIT EVIDENCE — 2026-09-04-HARDENED-V2
Purpose: map known failure classes to prevention, detection, and fail-closed state. Evidence only; mandatory SOPs remain authoritative.

| Failure class | Preventive control | Detection/validation | Required fail state |
|---|---|---|---|
| Stale/contradictory manifest | Main evidence hierarchy/startup | Live GitHub/binary/matrix reconciliation | NEEDS REVIEW / STOP |
| Missing matrix index/shard/row | Art matrix-resolution gate | Index → shard → exact row | STOP |
| Duplicate active matrix row | Shard uniqueness rule | Cross-shard asset ID/path check | STOP |
| Surface Matrix grows near text limit | Sharded index; <=8 KB shard target | UTF-8 byte check before write | SPLIT REQUIRED / STOP |
| Wrong subject/canon | Art Audit A | Visual/semantic + cross-surface QA | DESIGN REJECTED |
| DM/future spoiler | Art Audit A/C + Main canon gate | Visibility re-check | DM HOLD |
| Filename assumed to define surface | Art Audit B | Matrix row vs live target | STOP |
| Wrong aspect/crop | Art Audit B/C | Full + cropped/small-view QA | DESIGN REJECTED |
| Text overlaps Notion UI | Locked text policy | Target-surface visual QA | DESIGN REJECTED |
| Gibberish/generated typography | Art generation discipline | Pixel visual QA | DESIGN REJECTED |
| Broken anatomy/object fusion | Art rejection criteria | Pixel visual QA | DESIGN REJECTED |
| Style/readability failure | Locked spec/adversarial audit | Visual + cross-surface QA | DESIGN REJECTED |
| Source edit without accessible pixels | App + Art capability gates | Source accessibility check | STOP / manual source step |
| New image substituted for requested edit | App image-edit rule | Source/prompt lineage comparison | DESIGN REJECTED |
| Prompt/spec drift | Production-spec lock | Stored prompt/edit lineage check | DESIGN REJECTED |
| `v01` overwritten | Art version rule | Source/version/path validation | WRITE FAILED / STOP |
| Rejected art committed | Art handoff gate | Design-state/source lineage check | NOT COMPLETE |
| GitHub text truncation | Upload byte envelope + sentinel | Re-fetch sections/tail sentinel | WRITE FAILED |
| Binary treated as text | Upload + App GitHub rules | Binary path/size/open QA | WRITE FAILED |
| Staging counted as production | Upload rules | Live final-path audit | NOT COMPLETE |
| Wrong GitHub create/update path | App live-path read | Re-fetch exact path/blob | WRITE FAILED |
| Wrong Notion page/view/property | App read-first + Audit B | Exact entity/structure re-fetch | STOP / rollback |
| Write endpoint used for inspection | App capability rule | Operation-class check | STOP |
| Page cover mistaken for gallery preview | App Notion rule | Live view/preview fetch | STRUCTURAL FAILURE |
| Stored URL mistaken for visible render | Main/App visual rule | Browser/screenshot QA | VISUAL QA REQUIRED |
| External link breaks | Native-media preference | Re-fetch + rendered QA | BROKEN / CLEANUP REQUIRED |
| Temporary Notion upload unattached | App native attachment rule | Final page/property re-fetch | WRITE FAILED |
| Old link/image remains | Main zero-residue cleanup | Re-scan + visual clean baseline | CLEANUP REQUIRED |
| First-block preview hack remains | Residue inventory | Page/view re-scan | CLEANUP REQUIRED |
| Schema changed for convenience | Main/App Notion rules | Schema diff/re-fetch | STOP / rollback |
| Campaign content altered | Structural validation | Content/schema/relation comparison | STOP / rollback |
| Pilot failure ignored | Main pilot gate | Pilot-state check | SCALE-OUT BLOCKED |
| Session/context limit mid-action | Main batch/resume | Last-target re-fetch/checkpoint | UNKNOWN / PAUSED |
| Rate/tool error retried blindly | App failure rule | Error log + true read | STOP |
| Checkpoint write fails | Main session gate | Persistence verification | CHECKPOINT FAILURE / STOP |
| Memory used as resume truth | Main/App resume rules | Reload SOP/live state/checkpoint | STOP |
| Ledger says complete but UI fails | Evidence precedence | User/browser evidence | NOT COMPLETE |
| 115 present treated as readiness | README/Main/legacy manifest deprecation | DESIGN APPROVED evidence | NOT COMPLETE |
| Completion without disproof | Main completion gate | Art/GitHub/residue/visual/adversarial sweeps | NOT COMPLETE |

## Cross-stage invariants
1. Art → GitHub: no production write without DESIGN APPROVED.
2. Matrix control: schema + index + bounded shard; exactly one live row per asset.
3. GitHub → Notion: no rejected/staging/unverified source.
4. Notion replacement: no new art before CLEAN BASELINE VERIFIED.
5. Structural success never implies visual success.
6. Visual success never bypasses final disproof audits.
7. Failure at any stage invalidates downstream inherited status for the affected item/class.

## Three-audit proof
**Audit 1 — Coverage:** known failures from the incident history have prevention + detection + fail state above.

**Audit 2 — Contradiction:** Main orchestrates; App governs tool use; Art governs design/matrix resolution; Upload Safety governs GitHub transport; Surface Matrix schema/index/shards govern per-asset surface facts. A module may be stricter than its parent, never weaker.

**Audit 3 — Adversarial:** assume one control fails. Downstream gates still block false completion: rejected art fails handoff; bad GitHub writes fail re-fetch; wrong Notion structure fails structural QA; invisible/broken results fail visual QA; residue fails sweeps; unknown session/tool state cannot become COMPLETE; oversized matrix shards must split before write.

External services can still fail, permissions can change, and rendering can differ. The standard guarantees fail-closed behavior and evidence-backed recovery, not guaranteed external service success.

END-OF-FILE SENTINEL: TOTFR-GUARDRAIL-COVERAGE-MATRIX-2026-09-04-HARDENED-V2
