# GitHub Upload Safety Plan

Status: MANDATORY TRANSPORT SOP
Version: 2026-09-04-HARDENED-V6

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
- fetch exact path on exact target branch immediately before every update; cross-branch SHA reuse is prohibited.

## 2. Binary uploads / materialized art
- Never send image binaries as UTF-8 text.
- Only DESIGN APPROVED materialized binary may enter production transport.
- The reviewed binary hash/dimensions/version must match the binary being uploaded; byte drift invalidates approval.
- Prefer approved binary/blob transport. Base64 staging chunks <=8,000 characters/bytes each.
- Verify decoded final binary path, size and hash where available.
- Staging pieces/ZIPs never count as production assets.

## 3. Protected integration model
`development` is an integration/merge target, not an agent workspace.

Before any governed GitHub production/control action, live CI must prove an active default-branch ruleset satisfies `TOTFR_Required_GitHub_Protection.json`: PR requirement, strict/current-head required checks, required contexts `validate` + `control-plane-integrity`, deletion/non-fast-forward protection, and no unconditional bypass on that integration ruleset.

A GitHub `protected:true` label alone is insufficient. Missing/failed/uninspectable live protection = STOP. There is no CI-only fallback for inadequate integration protection.

## 4. Working branches and production uploader
Control work uses `guardrails/*` or `agents/*`. Art production uses bounded `art-run/<run_id>` or equivalent working branches created from the exact current `development` head.

For each production batch:
1. verify live protection first;
2. fetch exact current `development` SHA;
3. create/reuse only the approved working branch bound to that base/run;
4. max 3 production files per uploader batch; reduce to one for new/failing transport paths;
5. fetch exact working-branch target before upload; skip only if exact approved binary already matches;
6. attempt approved binary path once; no retry storm;
7. staged fallback only after transport preflight; max 12 staging chunk writes/run;
8. re-fetch exact working-branch final path and verify path/size/hash;
9. open/update PR to `development`; no agent direct write to `development`;
10. require both required CI contexts on the exact PR head;
11. adversarially review diff and provenance before merge;
12. after merge, fetch exact new `development` head and require its push CI checks before downstream deployment consumes that source.

Inventory Missing: 0 never proves design/deployment completion.

## 5. Control-plane PR gate
README authority, AGENTS, mandatory SOP/policies, validators/tests/workflows, Surface Matrix schema/index/routing and deployment-run formats are control-plane changes.

- Use isolated working branch + PR.
- Fetch exact branch-local path/SHA before each write.
- **PR FRESHNESS GATE:** before merge compare PR head to current integration base. If behind or base changed in overlapping controlled files, STOP, reconcile every delta, then rerun all checks. Green CI from a stale head is invalid.
- Required checks: `validate` and `control-plane-integrity`, both on exact current PR head.
- Review full diff adversarially. Self-declared agent IDs do not create a security boundary; Tier-2 control changes remain blocked from agent execution while Agent Trust Boundary identity enforcement is UNCONFIGURED.
- Merge only the exact reviewed head. A later commit invalidates approval.
- Post-merge exact-head checks must pass before controls become downstream authority.

## 6. Workflow integrity
Required validation workflows run on every pull request, including art-only PRs; path filters that can suppress required checks are prohibited.

Workflows use pinned action SHAs, read-only token permissions, no persisted checkout credentials, bounded timeout and stale-run cancellation. The independent `control-plane-integrity` check verifies the main validation workflow and live protection policy; both contexts must be required by the integration ruleset.

## 7. Session / retry / circuit
Never start a write unless the run can reasonably complete write + exact re-fetch + validation + checkpoint.

At rate/quota/session/tool limit or unexpected transport error:
- stop new writes;
- classify last attempt PROVEN PERSISTED / PROVEN ABSENT / UNKNOWN when possible;
- checkpoint exact branch/path/SHA/run state;
- retry only after changed evidence-backed recovery path;
- second same-path failure opens stage circuit; third material run failure triggers global mutation freeze.

## 8. Transport completion disproof
Before calling GitHub transport complete prove:
- uploaded bytes equal DESIGN APPROVED materialized bytes;
- exact final path/ref/hash verified;
- no staging residue is being counted as production;
- no DM/future asset entered public player-safe distribution;
- exact PR head passed both required checks;
- integration ruleset was live and sufficient at authorization time;
- merged integration head was re-read and post-merge checks passed;
- no stale branch/SHA, bypass, UNKNOWN or open circuit was ignored.

Any failed proof = NOT COMPLETE.

END-OF-FILE SENTINEL: TOTFR-GITHUB-UPLOAD-SAFETY-2026-09-04-HARDENED-V6
