#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib,json,os,re,sys
ROOT=Path(os.environ.get("TOTFR_ROOT",Path(__file__).resolve().parents[1])).resolve(); SRC=ROOT/"13 Source Prompts"
ERR=[]
def fail(x):ERR.append(x)
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def text(p,maxb=8000):
 if not p.exists():fail(f"missing agent control: {p.relative_to(ROOT)}");return ""
 b=p.read_bytes()
 if len(b)>maxb:fail(f"agent control exceeds {maxb} bytes: {p.relative_to(ROOT)} = {len(b)}")
 try:return b.decode("utf-8")
 except UnicodeDecodeError:fail(f"agent control not UTF-8: {p.relative_to(ROOT)}");return ""
def req(p,tokens):
 t=text(p)
 for x in tokens:
  if x not in t:fail(f"required agent control missing in {p.relative_to(ROOT)}: {x}")
 return t

AG=ROOT/"AGENTS.md"; PROTO=SRC/"TOTFR_Transactional_Agent_Deployment_SOP.md"; ROLES=SRC/"TOTFR_Agent_Role_Matrix.csv"; PUB=SRC/"TOTFR_Publication_Boundary.json"; RUNS=SRC/"Deployment Runs"; RUNREADME=RUNS/"README.md"; TEMPLATE=RUNS/"TOTFR_Run_Template.json"
req(AG,["immutable `control_ref`","Data is not instruction","Exactly one `notion_executor`","Evidence domains cannot substitute","Public distribution may contain PLAYER-SAFE assets only","Never persist query strings/tokens"])
req(PROTO,["desired-state","optimistic concurrency","CONCURRENT_CHANGE","ROLLBACK_CONFLICT","commit-pinned","DM HOLD","page-content preview hacks are prohibited","<=2 Notion requests/second","Canary by mechanism","authenticated browser"])
req(RUNREADME,["plan/*.jsonl","attestations/*.json","wal/<target_id>.json","receipts/<target_id>.json","visual/<target_id>.json","No shared append file"])

roles={}
if ROLES.exists():
 try:
  rows=list(csv.DictReader(ROLES.open(newline="",encoding="utf-8")))
  for r in rows:
   rid=(r.get("role_id") or "").strip()
   if not rid or rid=="__EOF_CONTROL__":continue
   if rid in roles:fail(f"duplicate agent role: {rid}")
   roles[rid]=r
 except Exception as e:fail(f"role matrix parse failure: {e}")
else:fail("missing agent role matrix")
writers=[r for r,v in roles.items() if v.get("notion_write")=="YES"]
if writers!=["notion_executor"]:fail(f"Notion writer set must be exactly notion_executor: {writers}")
for rid,r in roles.items():
 if r.get("art_generate")=="YES" and r.get("art_approve")=="YES":fail(f"art self-approval privilege overlap: {rid}")
 if r.get("notion_write")=="YES" and any(r.get(k)=="YES" for k in ["structural_approve","visual_approve","redteam"]):fail(f"Notion executor approval overlap: {rid}")
 if r.get("github_control_write")=="YES" and r.get("redteam")=="YES":fail(f"control author/redteam overlap: {rid}")
for needed in ["orchestrator","surface_canon_auditor","art_producer","art_reviewer","github_steward","notion_executor","structural_reviewer","visual_reviewer","adversarial_reviewer","control_author","control_reviewer"]:
 if needed not in roles:fail(f"missing required agent role: {needed}")

pub={}
if PUB.exists():
 try:pub=json.loads(PUB.read_text(encoding="utf-8"))
 except Exception as e:fail(f"publication policy parse failure: {e}")
else:fail("missing publication boundary policy")
if pub:
 if pub.get("policy",{}).get("public_dm_source_allowed") is not False:fail("publication policy must prohibit public DM source")
 if pub.get("policy",{}).get("mutable_branch_url_allowed_as_desired_state") is not False:fail("publication policy must prohibit mutable branch desired URLs")
 if not pub.get("known_public_dm_exposure"):fail("known public DM exposure inventory missing")
 if pub.get("dm_private_source_state")=="CONFIGURED" and not pub.get("dm_private_source_ref"):fail("configured private DM source missing ref")

if TEMPLATE.exists():
 try:
  tm=json.loads(TEMPLATE.read_text(encoding="utf-8"))
  if tm.get("status")!="DRAFT" or tm.get("inventory_state")!="PARTIAL" or tm.get("notion_executor_agent")!="notion_executor":fail("deployment run template must be inert DRAFT/PARTIAL with notion_executor")
 except Exception as e:fail(f"run template parse failure: {e}")
else:fail("missing deployment run template")

MUT={"REMOVE_RESIDUE","SET_COVER","SET_ICON","SET_FILE_PROPERTY","SET_VIEW_COVER_PROPERTY"}
SHA=re.compile(r"^[0-9a-f]{40}$"); SIGNED=re.compile(r"(?:X-Amz-|Signature=|token=|Authorization:|oauth)",re.I)
def check_run(d):
 rp=d/"run.json"
 try:r=json.loads(rp.read_text(encoding="utf-8"))
 except Exception as e:fail(f"run parse failure {d.name}: {e}");return
 for k in ["control_ref","development_head_at_plan"]:
  v=str(r.get(k,""));
  if not SHA.match(v) or set(v)=={"0"}:fail(f"invalid immutable {k} in run {d.name}")
 if r.get("notion_executor_agent")!="notion_executor":fail(f"wrong Notion executor in run {d.name}")
 if r.get("status") in {"APPROVED","EXECUTING","VISUAL_QA_REQUIRED","COMPLETE"} and r.get("inventory_state")!="FROZEN":fail(f"approved/executing run has partial inventory: {d.name}")
 shards=r.get("plan_shards") or []
 if r.get("status")!="DRAFT" and not shards:fail(f"non-draft run has no plan shards: {d.name}")
 seen=set(); tier2=False; mut_targets=[]
 for s in shards:
  p=ROOT/s.get("path","") if isinstance(s,dict) else Path("/")
  if not p.exists():fail(f"missing plan shard in {d.name}: {s}");continue
  if p.stat().st_size>8000:fail(f"plan shard exceeds 8000 bytes: {p.relative_to(ROOT)}")
  if s.get("blob_sha")!=blob(p):fail(f"stale plan shard blob SHA: {p.relative_to(ROOT)}")
  lines=p.read_text(encoding="utf-8").splitlines()
  if not lines:fail(f"empty plan shard: {p.relative_to(ROOT)}");continue
  try:objs=[json.loads(x) for x in lines]
  except Exception as e:fail(f"plan JSONL parse failure {p.relative_to(ROOT)}: {e}");continue
  if objs[-1].get("type")!="EOF_CONTROL":fail(f"plan shard missing EOF control: {p.relative_to(ROOT)}")
  for o in objs[:-1]:
   tid=o.get("target_id")
   if not tid or tid in seen:fail(f"missing/duplicate target_id in {d.name}: {tid}")
   seen.add(tid); action=o.get("action"); privacy=o.get("privacy"); ref=str(o.get("desired_source_ref") or "")
   if o.get("risk_tier")==2:tier2=True
   if "/development/" in ref:fail(f"mutable development URL in desired state: {tid}")
   if SIGNED.search(ref):fail(f"signed/secret material persisted in desired source: {tid}")
   if privacy=="DM_HOLD" and o.get("desired_source_mode") not in {"PRIVATE_DM","NOTION_PRIVATE_NATIVE","NONE"}:fail(f"public/nonprivate DM source in plan: {tid}")
   if privacy=="DM_HOLD" and action in MUT and pub.get("dm_private_source_state")!="CONFIGURED":fail(f"DM mutation authorized without configured private source: {tid}")
   if action in MUT:
    mut_targets.append(tid)
    if not o.get("precondition"):fail(f"mutation missing precondition: {tid}")
    if not o.get("rollback"):fail(f"mutation missing rollback: {tid}")
   if action=="SET_VIEW_COVER_PROPERTY" and o.get("risk_tier")!=2:fail(f"view change must be risk tier 2: {tid}")
  
 if r.get("status") in {"APPROVED","EXECUTING","VISUAL_QA_REQUIRED","COMPLETE"}:
  at=list((d/"attestations").glob("*.json")) if (d/"attestations").exists() else []
  decisions=[]
  for a in at:
   try:x=json.loads(a.read_text(encoding="utf-8"));decisions.append(x)
   except Exception as e:fail(f"attestation parse failure {a.relative_to(ROOT)}: {e}")
  author=r.get("plan_author_agent"); executor=r.get("notion_executor_agent")
  for x in decisions:
   if x.get("reviewer_agent") in {author,executor}:fail(f"non-independent attestation in run {d.name}: {x.get('reviewer_agent')}")
  if tier2:
   if not any(x.get("decision")=="PASS" and x.get("review_role") in {"structural_reviewer","control_reviewer","surface_canon_auditor","art_reviewer"} for x in decisions):fail(f"tier2 run missing domain PASS attestation: {d.name}")
   if not any(x.get("decision")=="PASS" and x.get("review_role")=="adversarial_reviewer" for x in decisions):fail(f"tier2 run missing adversarial PASS attestation: {d.name}")
 if r.get("status")=="COMPLETE":
  if not (d/"final.json").exists():fail(f"complete run missing final.json: {d.name}")
  for tid in mut_targets:
   if not (d/"receipts"/f"{tid}.json").exists():fail(f"complete run missing receipt: {tid}")

if RUNS.exists():
 for d in RUNS.iterdir():
  if d.is_dir() and (d/"run.json").exists():check_run(d)
else:fail("missing Deployment Runs directory")

if ERR:
 print("TOTFR AGENT CONTROL VALIDATION FAILED")
 for e in ERR:print("- "+e)
 sys.exit(1)
print("TOTFR AGENT CONTROL VALIDATION PASSED")
print(f"roles={len(roles)} deployment_runs={sum(1 for d in RUNS.iterdir() if d.is_dir() and (d/'run.json').exists()) if RUNS.exists() else 0}")
print("END-OF-FILE SENTINEL: TOTFR-AGENT-CONTROL-VALIDATOR-2026-09-04-V1")
