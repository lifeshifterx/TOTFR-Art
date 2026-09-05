# TOTFR Guardrail Coverage Matrix

Status: AUDIT EVIDENCE — 2026-09-04-HARDENED
Purpose: prove that known failure classes map to a preventive control, a detection control, and a fail-closed state. This file is evidence, not a substitute for the mandatory SOPs.

| Failure class | Preventive control | Detection/validation | Required fail state |
|---|---|---|---|
| Stale/contradictory manifest | Main evidence hierarchy + mandatory startup | Compare live GitHub/binary/Surface Matrix | NEEDS REVIEW / STOP |
| Missing Surface Matrix row | Art startup gate | Canonical matrix lookup | STOP |
| Wrong subject/canon | Art Audit A | Visual/semantic + cross-surface QA | DESIGN REJECTED |
| DM/future spoiler | Art Audit A/C + Main canon gate | Visibility re-check | DM HOLD |
| Filename assumed to define surface | Art Audit B | Surface Matrix comparison | STOP |
| Wrong aspect/crop | Art Audit B/C | Full + intended crop/small-view QA | DESIGN REJECTED |
| Text overlaps Notion UI | Text policy + cover defaults | Visual QA at target surface | DESIGN REJECTED |
| Gibberish/generated typography | Art generation discipline | Visual/semantic QA | DESIGN REJECTED |
| Broken anatomy/object fusion | Art rejection criteria | Pixel-level visual QA | DESIGN REJECTED |
| Style/readability failure | Locked style + adversarial plan | Cross-surface/visual QA | DESIGN REJECTED |
| Source-preserving edit without source pixels | App + Art capability gates | Source accessibility check | STOP / manual source step |
| Newly imagined image substituted for edit | App image-edit rule | Lineage/spec comparison | DESIGN REJECTED |
| Prompt/spec drift | Production-spec lock + lineage | Compare stored prompt/edit spec | DESIGN REJECTED |
| `v01` overwritten | Art version rule | Source path/version validation | WRITE FAILED / STOP |
| Rejected art committed | Art handoff gate | GitHub source lineage/status check | NOT COMPLETE |
| GitHub text truncation | Upload hard byte envelope + sentinel | Re-fetch sections/tail sentinel | WRITE FAILED |
| Binary treated as text | Upload + App GitHub rules | Final binary path/size/open QA | WRITE FAILED |
| Staging counted as production | Upload rules | Live tree/final-path audit | NOT COMPLETE |
| Wrong GitHub create/update path | App capability + live path read | Re-fetch exact path/blob | WRITE FAILED |
| Wrong Notion page/view/property | App read-first + Main Audit B | Re-fetch exact entity/structure | STOP / rollback |
| Write endpoint used for inspection | App capability rule | Operation-class check | STOP |
| Page cover mistaken for gallery preview | App Notion rule | Live view/preview fetch | STRUCTURAL FAILURE |
| API URL mistaken for visible rendering | Main/App visual rule | Browser/screenshot visual QA | VISUAL QA REQUIRED |
| Raw external link breaks | Native-media preference | Re-fetch + rendered visual QA | BROKEN / CLEANUP REQUIRED |
| Notion native upload temporary/unattached | App native attachment rule | Re-fetch final page/property | WRITE FAILED |
| Old link/image remains behind replacement | Main zero-residue cleanup | Re-scan + visual clean baseline | CLEANUP REQUIRED |
| First-block preview hack lingers | Residue inventory | Page/view re-scan | CLEANUP REQUIRED |
| Schema changed for convenience | Main/App Notion rules | Schema diff/re-fetch | STOP / rollback |
| Campaign content altered | Main structural validation | Content/schema/relation comparison | STOP / rollback |
| Pilot failure ignored | Main pilot gate | Pilot status check | SCALE-OUT BLOCKED |
| Session/context limit mid-action | Main batch/resume + App failure rule | Re-fetch last target/checkpoint | UNKNOWN / PAUSED |
| Rate/tool error retried blindly | App failure rule | Error log + re-read | STOP |
| Checkpoint write fails | Main session gate | Persistence verification | CHECKPOINT FAILURE / STOP |
| Memory used as resume truth | Main/App resume rules | Reload live SOP/state/checkpoint | STOP |
| Ledger says complete but UI fails | Main evidence precedence | User/browser visual evidence | NOT COMPLETE |
| Asset count treated as design readiness | README + Main chain | DESIGN APPROVED evidence per asset | NOT COMPLETE |
| Completion declared without disproof | Main completion sweep | Art/GitHub/Destination/Reference/Visual/Adversarial audits | NOT COMPLETE |

## Cross-stage handoff invariants
1. Art → GitHub: no production write without DESIGN APPROVED.
2. GitHub → Notion: no deployment from staging/rejected/unverified source.
3. Notion replacement: no new art before CLEAN BASELINE VERIFIED.
4. Structural success → visual success: no inference; rendered evidence required.
5. Visual success → COMPLETE: final project disproof audits still required.
6. Failure at any stage invalidates downstream inherited status for the affected item.

## Three-audit proof
**Audit 1 — Coverage:** each known failure from the incident history has prevention + detection + fail state above.

**Audit 2 — Contradiction:** module precedence is explicit: Main orchestrates; App governs tool use; Art governs design; Upload Safety governs GitHub transport; Surface Matrix governs per-asset surface facts. A module may be stricter than its parent but never weaker.

**Audit 3 — Adversarial:** assume one control fails. Downstream controls must still prevent COMPLETE: rejected art is blocked at handoff; bad GitHub writes fail re-fetch; wrong Notion structure fails structural QA; invisible/broken results fail visual QA; residue fails final sweeps; unknown session/tool state cannot become COMPLETE.

Residual external risk can never be reduced to zero: services may fail, permissions may change, and rendering may differ. The standard therefore guarantees fail-closed behavior rather than guaranteed external success.

END-OF-FILE SENTINEL: TOTFR-GUARDRAIL-COVERAGE-MATRIX-2026-09-04-HARDENED
