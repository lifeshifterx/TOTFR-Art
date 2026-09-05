#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib,json,os,re,sys
ROOT=Path(os.environ.get("TOTFR_ROOT",Path(__file__).resolve().parents[1])).resolve();SRC=ROOT/"13 Source Prompts";RUNS=SRC/"Deployment Runs";ERR=[]
def fail(x):ERR.append(x)
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def loadj(p,label,maxb=8000):
 if not p.exists():fail(f"missing {label}: {p.relative_to(ROOT)}");return None
 b=p.read_bytes()
 if len(b)>maxb:fail(f"{label} exceeds {maxb} bytes: {p.relative_to(ROOT)} = {len(b)}")
 try:return json.loads(b.decode())
 except Exception as e:fail(f"{label} parse failure {p.relative_to(ROOT)}: {e}");return None
def text(p,maxb=8000):
 if not p.exists():fail(f"missing agent control: {p.relative_to(ROOT)}");return ""
 b=p.read_bytes()
 if len(b)>maxb:fail(f"agent control exceeds {maxb} bytes: {p.relative_to(ROOT)} = {len(b)}")
 try:return b.decode()
 except UnicodeDecodeError:fail(f"agent control not UTF-8: {p.relative_to(ROOT)}");return ""
def req(p,toks):
 t=text(p)
 for x in toks:
  if x not in t:fail(f"required agent control missing in {p.relative_to(ROOT)}: {x}")
 return t
AG=ROOT/"AGENTS.md";PROTO=SRC/"TOTFR_Transactional_Agent_Deployment_SOP.md";ROLES=SRC/"TOTFR_Agent_Role_Matrix.csv";PUB=SRC/"TOTFR_Publication_Boundary.json";RR=RUNS/"README.md";RT=RUNS/"TOTFR_Run_Template.json";ST=RUNS/"TOTFR_State_Template.json"
req(AG,["immutable `control_ref`","Data is not instruction","Exactly one `notion_executor`","Evidence domains cannot substitute","PLAYER-SAFE assets only","Never persist query strings/tokens"])
req(PROTO,["desired-state","optimistic concurrency","CONCURRENT_CHANGE","ROLLBACK_CONFLICT","commit-pinned","page-content preview hacks are prohibited","<=2 Notion requests/second","Canary by mechanism","authenticated browser"])
req(RR,["immutable frozen run manifest","state.json","plan/*.jsonl","attestations/*.json","wal/<target_id>.json","receipts/<target_id>.json","visual/<target_id>.json","mutation_key","reviewer_instance_id","final.json"])
roles={}
if ROLES.exists():
 try:
  for r in csv.DictReader(ROLES.open(newline="",encoding="utf-8")):
   rid=(r.get("role_id") or "").strip()
   if not rid or rid=="__EOF_CONTROL__":continue
   if rid in roles:fail(f"duplicate agent role: {rid}")
   roles[rid]=r
 except Exception as e:fail(f"role matrix parse failure: {e}")
else:fail("missing agent role matrix")
writers=[k for k,v in roles.items() if v.get("notion_write")=="YES"]
if writers!=["notion_executor"]:fail(f"Notion writer set must be exactly notion_executor: {writers}")
for rid,r in roles.items():
 if r.get("art_generate")=="YES" and r.get("art_approve")=="YES":fail(f"art self-approval privilege overlap: {rid}")
 if r.get("notion_write")=="YES" and any(r.get(k)=="YES" for k in ["structural_approve","visual_approve","redteam"]):fail(f"Notion executor approval overlap: {rid}")
 if r.get("github_control_write")=="YES" and r.get("redteam")=="YES":fail(f"control author/redteam overlap: {rid}")
for n in {"orchestrator","surface_canon_auditor","art_producer","art_reviewer","github_steward","notion_executor","structural_reviewer","visual_reviewer","adversarial_reviewer","control_author","control_reviewer"}:
 if n not in roles:fail(f"missing required agent role: {n}")
pub=loadj(PUB,"publication boundary") or {}
if pub:
 if pub.get("policy",{}).get("public_dm_source_allowed") is not False:fail("publication policy must prohibit public DM source")
 if pub.get("policy",{}).get("mutable_branch_url_allowed_as_desired_state") is not False:fail("publication policy must prohibit mutable branch desired URLs")
 if not pub.get("known_public_dm_exposure"):fail("known public DM exposure inventory missing")
 if pub.get("dm_private_source_state")=="CONFIGURED" and not pub.get("dm_private_source_ref"):fail("configured private DM source missing ref")
rt=loadj(RT,"run template") or {};st=loadj(ST,"state template") or {}
if rt:
 if "status" in rt or rt.get("inventory_state")!="FROZEN" or rt.get("notion_executor_agent")!="notion_executor":fail("run template must model immutable FROZEN manifest without status")
if st and (st.get("phase")!="PLANNED" or st.get("circuit_state")!="CLOSED"):fail("state template must start PLANNED/CLOSED")
MUT={"REMOVE_RESIDUE","SET_COVER","SET_ICON","SET_FILE_PROPERTY","SET_VIEW_COVER_PROPERTY"};PHASES={"PLANNED","APPROVED","EXECUTING","BLOCKED","VISUAL_QA_REQUIRED","CLOSED"};SHA=re.compile(r"^[0-9a-f]{40}$");SHA256=re.compile(r"^[0-9a-f]{64}$");SIGNED=re.compile(r"(?:X-Amz-|Signature=|token=|Authorization:|oauth)",re.I)
def scan(o,w):
 if SIGNED.search(json.dumps(o,separators=(",",":"))):fail(f"signed/secret material persisted in {w}")
def ident(v):return isinstance(v,str) and v.strip() not in {"","UNSET"}
def attestations(d,rh,sh,ai,ei):
 out=[]
 for p in sorted((d/"attestations").glob("*.json")) if (d/"attestations").exists() else []:
  x=loadj(p,"attestation");
  if not x:continue
  scan(x,f"attestation {p.name}");out.append(x);role=x.get("review_role");ri=x.get("reviewer_instance_id")
  if x.get("run_json_blob_sha")!=rh:fail(f"attestation references stale run.json: {p.name}")
  if x.get("plan_shard_blob_shas")!=sh:fail(f"attestation references stale plan shards: {p.name}")
  if role not in roles:fail(f"unknown reviewer role: {p.name}")
  if not ident(ri) or ri in {ai,ei}:fail(f"non-independent reviewer instance: {p.name}")
  if not ident(x.get("runtime_class")):fail(f"attestation missing runtime_class: {p.name}")
  if role=="structural_reviewer" and roles[role].get("structural_approve")!="YES":fail(f"review role lacks structural permission: {p.name}")
  if role=="adversarial_reviewer" and roles[role].get("redteam")!="YES":fail(f"review role lacks redteam permission: {p.name}")
 return out
def check_run(d):
 rp=d/"run.json";r=loadj(rp,"run");sp=d/"state.json";s=loadj(sp,"state")
 if not r or not s:return
 scan(r,f"run {d.name}");scan(s,f"state {d.name}");rh=blob(rp)
 if "status" in r:fail(f"immutable run.json contains mutable status: {d.name}")
 if r.get("inventory_state")!="FROZEN":fail(f"run inventory is not FROZEN: {d.name}")
 for k in ["control_ref","development_head_at_plan"]:
  v=str(r.get(k,""))
  if not SHA.match(v) or set(v)=={"0"}:fail(f"invalid immutable {k}: {d.name}")
 author=r.get("plan_author_agent");executor=r.get("notion_executor_agent");ai=r.get("plan_author_instance_id");ei=r.get("notion_executor_instance_id");ar=r.get("plan_author_runtime_class")
 if author not in roles or roles.get(author,{}).get("run_plan_write")!="YES":fail(f"invalid plan author role: {d.name}")
 if executor!="notion_executor" or roles.get(executor,{}).get("notion_write")!="YES":fail(f"wrong Notion executor: {d.name}")
 if not ident(ai) or not ident(ei) or ai==ei:fail(f"run requires distinct author/executor instance IDs: {d.name}")
 if not ident(ar):fail(f"run missing plan_author_runtime_class: {d.name}")
 if s.get("run_id")!=r.get("run_id"):fail(f"state run_id mismatch: {d.name}")
 if s.get("phase") not in PHASES:fail(f"invalid state phase: {d.name}")
 if s.get("circuit_state") not in {"CLOSED","OPEN"}:fail(f"invalid circuit_state: {d.name}")
 shards=r.get("plan_shards") or []
 if not shards:fail(f"frozen run has no plan shards: {d.name}")
 seen=set();keys=set();tier2=False;mut={};sh=[]
 for ent in shards:
  if not isinstance(ent,dict):fail(f"invalid plan shard entry: {d.name}");continue
  p=ROOT/ent.get("path","")
  if not p.exists():fail(f"missing plan shard: {ent}");continue
  if p.stat().st_size>8000:fail(f"plan shard exceeds 8000 bytes: {p.relative_to(ROOT)}")
  ps=blob(p);sh.append(ps)
  if ent.get("blob_sha")!=ps:fail(f"stale plan shard blob SHA: {p.relative_to(ROOT)}")
  try:objs=[json.loads(x) for x in p.read_text().splitlines()]
  except Exception as e:fail(f"plan JSONL parse failure {p.relative_to(ROOT)}: {e}");continue
  if not objs or objs[-1].get("type")!="EOF_CONTROL":fail(f"plan shard missing EOF control: {p.relative_to(ROOT)}");continue
  for o in objs[:-1]:
   scan(o,f"plan target {o.get('target_id')}");tid=o.get("target_id");act=o.get("action");ref=str(o.get("desired_source_ref") or "");mk=o.get("mutation_key")
   if not tid or tid in seen:fail(f"missing/duplicate target_id: {tid}")
   seen.add(tid)
   if o.get("risk_tier") not in {0,1,2}:fail(f"invalid risk_tier: {tid}")
   if o.get("risk_tier")==2:tier2=True
   for k in ["source_commit_sha","source_blob_sha"]:
    v=str(o.get(k,""))
    if o.get("desired_source_mode") not in {"NONE","PRIVATE_DM","NOTION_PRIVATE_NATIVE"} and not SHA.match(v):fail(f"invalid {k}: {tid}")
   if "/development/" in ref:fail(f"mutable development URL in desired state: {tid}")
   sc=str(o.get("source_commit_sha") or "")
   if ref.startswith("https://raw.githubusercontent.com/") and sc and f"/{sc}/" not in ref:fail(f"pinned URL commit does not match source_commit_sha: {tid}")
   if o.get("privacy")=="DM_HOLD" and o.get("desired_source_mode") not in {"PRIVATE_DM","NOTION_PRIVATE_NATIVE","NONE"}:fail(f"public/nonprivate DM source in plan: {tid}")
   if o.get("privacy")=="DM_HOLD" and act in MUT and pub.get("dm_private_source_state")!="CONFIGURED":fail(f"DM mutation authorized without configured private source: {tid}")
   if act in MUT:
    if not mk:fail(f"mutation missing mutation_key: {tid}")
    elif mk in keys:fail(f"duplicate mutation_key: {mk}")
    else:keys.add(mk)
    for k in ["precondition","expected_fingerprint","rollback"]:
     if not o.get(k):fail(f"mutation missing {k}: {tid}")
    mut[tid]=o
   if act=="SET_VIEW_COVER_PROPERTY" and o.get("risk_tier")!=2:fail(f"view change must be risk tier 2: {tid}")
 reviews=attestations(d,rh,sh,ai,ei);active=s.get("phase") in {"APPROVED","EXECUTING","VISUAL_QA_REQUIRED","CLOSED"}
 if active and mut and not any(x.get("decision")=="PASS" and x.get("review_role")=="structural_reviewer" for x in reviews):fail(f"active mutating run missing structural reviewer PASS: {d.name}")
 if active and tier2:
  if not any(x.get("decision")=="PASS" and x.get("review_role")=="adversarial_reviewer" for x in reviews):fail(f"tier2 run missing adversarial PASS: {d.name}")
  if not any(x.get("decision")=="PASS" and x.get("runtime_class")!=ar for x in reviews):fail(f"tier2 run lacks heterogeneous reviewer runtime: {d.name}")
 if s.get("circuit_state")=="OPEN" and s.get("phase") not in {"BLOCKED","VISUAL_QA_REQUIRED"}:fail(f"open circuit in advancing phase: {d.name}")
 if s.get("phase")!="CLOSED":return
 fin=loadj(d/"final.json","final record")
 if not fin:return
 scan(fin,f"final {d.name}");fri=fin.get("reviewer_instance_id")
 if fin.get("assertion")!="COMPLETE" or fin.get("decision")!="PASS" or fin.get("review_role")!="adversarial_reviewer":fail(f"closed run lacks adversarial COMPLETE PASS: {d.name}")
 if not ident(fri) or fri in {ai,ei}:fail(f"final review is not independent: {d.name}")
 if fin.get("run_json_blob_sha")!=rh or fin.get("plan_shard_blob_shas")!=sh:fail(f"final record references stale run/plan: {d.name}")
 if s.get("circuit_state")!="CLOSED" or s.get("blockers"):fail(f"closed run retains circuit/blockers: {d.name}")
 receipts={};visuals={}
 for tid,o in mut.items():
  wp=d/"wal"/f"{tid}.json";qp=d/"receipts"/f"{tid}.json";vp=d/"visual"/f"{tid}.json";w=loadj(wp,"WAL");q=loadj(qp,"receipt");v=loadj(vp,"visual record")
  if w:
   scan(w,f"WAL {tid}")
   if w.get("run_json_blob_sha")!=rh or w.get("plan_shard_blob_shas")!=sh:fail(f"WAL references stale run/plan: {tid}")
   if w.get("mutation_key")!=o.get("mutation_key"):fail(f"WAL mutation_key mismatch: {tid}")
  if q:
   scan(q,f"receipt {tid}")
   if q.get("result")!="SUCCESS":fail(f"closed run has non-success receipt: {tid}")
   if not w or q.get("wal_blob_sha")!=blob(wp):fail(f"receipt WAL SHA mismatch: {tid}")
   if q.get("post_state_fingerprint")!=o.get("expected_fingerprint"):fail(f"receipt post fingerprint mismatch: {tid}")
   conf=q.get("read_after_write_confirmations")
   if not isinstance(conf,list) or len(conf)<2 or any(x.get("fingerprint")!=o.get("expected_fingerprint") or not x.get("observed_at") for x in conf):fail(f"receipt lacks two matching post-write confirmations: {tid}")
   receipts[tid]=blob(qp)
  if v:
   scan(v,f"visual record {tid}");vi=v.get("reviewer_instance_id")
   if v.get("decision")!="PASS" or v.get("review_role")!="visual_reviewer":fail(f"closed run lacks visual PASS: {tid}")
   if not ident(vi) or vi in {ai,ei}:fail(f"visual review is not independent: {tid}")
   if not q or v.get("receipt_blob_sha")!=blob(qp):fail(f"visual record stale receipt ref: {tid}")
   if not SHA256.match(str(v.get("screenshot_sha256",""))) or not v.get("viewport") or v.get("hard_reload") is not True:fail(f"visual evidence incomplete: {tid}")
   visuals[tid]=blob(vp)
 if fin.get("receipt_blob_shas")!=receipts:fail(f"final record receipt evidence set mismatch: {d.name}")
 if fin.get("visual_blob_shas")!=visuals:fail(f"final record visual evidence set mismatch: {d.name}")
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
print("END-OF-FILE SENTINEL: TOTFR-AGENT-CONTROL-VALIDATOR-2026-09-04-V4")
