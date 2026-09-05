# GitHub Upload Safety Plan

Status: MANDATORY TRANSPORT SOP
Version: 2026-09-04-HARDENED-V7

## 0. VERIFY THEN TRUST
Never trust a remembered branch, SHA, prior green run, protection badge, upload response, or previous fetch. Read the exact target/ref/state immediately before the dependent action. Later changes invalidate dependent trust.

## 1. Non-negotiable text-write envelope
Observed behavior: connector text writes previously truncated near ~20 KB. That is a failure observation, never an operating target.

For project `create_file`/`update_file` text:
- prepare final document before writing;
- measure UTF-8 bytes when a prepared source exists;
- main SOP target <=8,000 bytes;
- prepared direct text payload >10,000 bytes = STOP/split;
- never probe the live limit;
- every controlled SOP/manifest ends with unique EOF sentinel;
- after one write, re-fetch exact target-branch file and verify SHA, required sections and tail sentinel;
- missing/truncated/ambiguous result = WRITE FAILED / STOP;
- never raise thresholds because a larger historical write succeeded;
- fetch exact path on exact target branch immediately before every update; a SHA from another branch/ref is never reusable.

## 2. Binary uploads / materialized art
- Never send image binaries as UTF-8 text.
- Only DESIGN APPROVED materialized binary may enter production transport.
- Reviewed binary hash/dimensions/version must match uploaded bytes; drift invalidates approval.
- Prefer approved binary/blob transport. Base64 staging chunks <=8,000 characters/bytes each.
- Verify decoded final path, size and hash where available.
- Staging pieces/ZIPs never count as production assets.

## 3. Protected integration model
`development` is integration/merge only, not an agent workspace.

Before governed GitHub production/control action, live CI must prove an active default-branch ruleset satisfies `TOTFR_Required_GitHub_Protection.json`: PR requirement, strict/current-head checks, required contexts `validate` + `control-plane-integrity`, deletion/non-fast-forward protection, and no unconditional integration bypass.

A GitHub `protected:true` label alone is insufficient. Missing/failed/uninspectable protection = STOP. **CURRENT-HEAD CI FALLBACK is RETIRED AND PROHIBITED**; inadequate live protection cannot be replaced by a successful workflow run.

## 4. Working branches / uploader
Control work uses `guardrails/*` or `agents/*`. Art uses bounded `art-run/<run_id>` working branches created from exact current `development`.

For each batch:
1. verify live protection;
2. fetch exact current integration SHA;
3. create/reuse only approved working branch bound to that base/run;
4. max 3 production files; reduce to one for new/failing path;
5. fetch exact working-branch target; skip only when exact approved binary matches;
6. attempt approved binary path once; no retry storm;
7. staged fallback only after preflight; max 12 staging chunk writes/run;
8. re-fetch working-branch final path and verify path/size/hash;
9. PR to `development`; no agent direct integration write;
10. require `validate` + `control-plane-integrity` on exact PR head;
11. adversarially review diff/provenance;
12. after merge fetch exact new integration head and require push checks before downstream consumption.

Inventory Missing: 0 never proves design/deployment completion.

## 5. PR-first control plane
README authority, AGENTS, mandatory SOP/policies, validators/tests/workflows, Surface Matrix schema/index/routing and Deployment Run formats are control-plane.

- Use isolated working branch + PR.
- Fetch exact branch-local path/SHA before every write.
- **PR FRESHNESS GATE:** if behind or integration base changed in overlapping controlled files, STOP, reconcile all deltas, rerun checks. Old green CI is invalid.
- Required checks: `validate` and `control-plane-integrity` on exact current PR head.
- Full diff requires adversarial review. Self-declared agent IDs do not create security independence; Tier-2 agent execution remains blocked while identity enforcement is UNCONFIGURED.
- Merge only exact reviewed head; later commit invalidates approval.
- Post-merge exact-head checks must pass before downstream authority.

`tools/test_totfr_guardrails.py` and all other required hostile-test suites must run; removing a test gate is a control failure.

## 6. Workflow integrity
Required workflows run on every PR, including art-only PRs; suppressive path filters are prohibited.

Workflows use pinned action SHAs, read-only token permissions, no persisted checkout credentials, bounded timeout and stale-run cancellation. Independent `control-plane-integrity` validates main workflow and live protection; both contexts must be required by the integration ruleset.

## 7. Session / retry / circuit
Never start a write unless same run can reasonably complete write + exact re-fetch + validation + checkpoint.

At rate/quota/session/tool limit or transport error: stop new writes; classify last attempt PROVEN PERSISTED / PROVEN ABSENT / UNKNOWN; checkpoint exact branch/path/SHA/run; retry only after changed evidence-backed recovery; second same-path failure opens stage circuit; third material run failure triggers global mutation freeze.

## 8. Transport completion disproof
Before transport COMPLETE prove:
- uploaded bytes equal DESIGN APPROVED materialized bytes;
- exact final path/ref/hash verified;
- staging residue not counted as production;
- no DM/future asset entered public player-safe distribution;
- exact PR head passed both checks;
- live integration ruleset was sufficient at authorization;
- merged integration head re-read and post-merge checks passed;
- no stale branch/SHA, bypass, UNKNOWN or open circuit ignored.

Any failed proof = NOT COMPLETE.

END-OF-FILE SENTINEL: TOTFR-GITHUB-UPLOAD-SAFETY-2026-09-04-HARDENED-V7
