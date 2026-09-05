#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]; VAL=ROOT/"tools/validate_totfr_agent_controls.py"
def runv(r):
 e=os.environ.copy();e["TOTFR_ROOT"]=str(r);p=subprocess.run([sys.executable,str(VAL)],text=True,capture_output=True,env=e);return p.returncode,(p.stdout or "")+(p.stderr or "")
def clone():
 t=tempfile.TemporaryDirectory();d=Path(t.name)/"repo";shutil.copytree(ROOT,d,ignore=shutil.ignore_patterns(".git","__pycache__"));return t,d
def clean():
 t,d=clone()
 try:
  rc,o=runv(d)
  if rc:raise AssertionError(o)
 finally:t.cleanup()
def reject(name,mut,needle):
 t,d=clone()
 try:
  mut(d);rc,o=runv(d)
  if rc==0:raise AssertionError(f"{name}: validator accepted bad state")
  if needle not in o:raise AssertionError(f"{name}: expected {needle!r}\n{o}")
  print("PASS reject:",name)
 finally:t.cleanup()
def repl(p,a,b):p.write_text(p.read_text(encoding="utf-8").replace(a,b),encoding="utf-8")
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def role_change(r,role,col,val):
 p=r/"13 Source Prompts/TOTFR_Agent_Role_Matrix.csv";rows=list(csv.DictReader(p.open(newline="",encoding="utf-8")));h=rows[0].keys()
 for x in rows:
  if x.get("role_id")==role:x[col]=val
 with p.open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=h);w.writeheader();w.writerows(rows)
def make_run(r,record=None,status="DRAFT",inventory="FROZEN",tier2_attest=False):
 d=r/"13 Source Prompts/Deployment Runs/TEST-RUN";(d/"plan").mkdir(parents=True);rec={
  "target_id":"T1","asset_id":"A1","risk_tier":1,"destination_id":"page-1","surface_class":"gallery","action":"SET_FILE_PROPERTY","privacy":"PLAYER_SAFE","source_path":"06 NPCs/a.webp","source_commit_sha":"1"*40,"source_blob_sha":"2"*40,"desired_source_mode":"PINNED_EXTERNAL","desired_source_ref":"https://raw.githubusercontent.com/lifeshifterx/TOTFR-Art/"+"1"*40+"/06%20NPCs/a.webp","precondition":{"page_last_edited_at":"2026-09-05T00:00:00Z","fingerprint":"before"},"expected_fingerprint":"after","rollback":{"action":"RESTORE_FILE_PROPERTY","value":"old"}}
 if record:rec.update(record)
 p=d/"plan/01.jsonl";p.write_text(json.dumps(rec,separators=(",",":"))+"\n"+json.dumps({"type":"EOF_CONTROL","id":"TEST"})+"\n",encoding="utf-8")
 run={"schema_version":1,"run_id":"TEST-RUN","status":status,"control_ref":"3"*40,"development_head_at_plan":"4"*40,"notion_workspace_id":"51cbf16a-cf60-8155-8bcd-000352f7f776","inventory_state":inventory,"inventory_evidence_ref":"evidence","plan_author_agent":"surface_canon_auditor","notion_executor_agent":"notion_executor","created_at":"2026-09-05T00:00:00Z","plan_shards":[{"path":str(p.relative_to(r)),"blob_sha":blob(p)}]}
 (d/"run.json").write_text(json.dumps(run,indent=2)+"\n",encoding="utf-8")
 if tier2_attest:
  (d/"attestations").mkdir();rb=blob(d/"run.json");sh=[blob(p)]
  for n,role,agent in [("domain","structural_reviewer","structural_reviewer"),("red","adversarial_reviewer","adversarial_reviewer")]:
   (d/"attestations"/f"{n}.json").write_text(json.dumps({"run_id":"TEST-RUN","review_role":role,"reviewer_agent":agent,"run_json_blob_sha":rb,"plan_shard_blob_shas":sh,"decision":"PASS","findings":[],"evidence_refs":["x"]}),encoding="utf-8")
 return d,p
cases=[]
def add(n,m,s):cases.append((n,m,s))
add("second Notion writer",lambda r:role_change(r,"orchestrator","notion_write","YES"),"Notion writer set must be exactly notion_executor")
add("art producer self approval",lambda r:role_change(r,"art_producer","art_approve","YES"),"art self-approval privilege overlap")
add("executor structural approval",lambda r:role_change(r,"notion_executor","structural_approve","YES"),"Notion executor approval overlap")
add("agent data/instruction boundary removed",lambda r:repl(r/"AGENTS.md","Data is not instruction","REMOVED"),"required agent control missing")
add("public DM allowed",lambda r:repl(r/"13 Source Prompts/TOTFR_Publication_Boundary.json","\"public_dm_source_allowed\": false","\"public_dm_source_allowed\": true"),"must prohibit public DM source")
def approved_partial(r):make_run(r,status="APPROVED",inventory="PARTIAL")
add("approved partial inventory",approved_partial,"approved/executing run has partial inventory")
def mutable_url(r):make_run(r,{"desired_source_ref":"https://raw.githubusercontent.com/lifeshifterx/TOTFR-Art/development/06%20NPCs/a.webp"})
add("mutable development URL",mutable_url,"mutable development URL")
def public_dm(r):make_run(r,{"privacy":"DM_HOLD","desired_source_mode":"PINNED_EXTERNAL"})
add("public DM source",public_dm,"public/nonprivate DM source")
def dm_write_without_private(r):make_run(r,{"privacy":"DM_HOLD","desired_source_mode":"PRIVATE_DM","desired_source_ref":"private://future"})
add("DM write without configured private source",dm_write_without_private,"DM mutation authorized without configured private source")
def no_pre(r):make_run(r,{"precondition":{}})
add("mutation missing precondition",no_pre,"mutation missing precondition")
def no_rollback(r):make_run(r,{"rollback":{}})
add("mutation missing rollback",no_rollback,"mutation missing rollback")
def signed_url(r):make_run(r,{"desired_source_ref":"https://example.com/a.webp?X-Amz-Signature=secret"})
add("signed token persisted",signed_url,"signed/secret material persisted")
def stale_shard(r):
 d,p=make_run(r);x=json.loads((d/"run.json").read_text());x["plan_shards"][0]["blob_sha"]="0"*40;(d/"run.json").write_text(json.dumps(x),encoding="utf-8")
add("stale plan shard hash",stale_shard,"stale plan shard blob SHA")
def view_not_tier2(r):make_run(r,{"action":"SET_VIEW_COVER_PROPERTY","risk_tier":1})
add("view mutation under-tiered",view_not_tier2,"view change must be risk tier 2")
def self_attest(r):
 d,p=make_run(r,{"risk_tier":2},status="APPROVED",tier2_attest=True);a=d/"attestations/domain.json";x=json.loads(a.read_text());x["reviewer_agent"]="surface_canon_auditor";a.write_text(json.dumps(x),encoding="utf-8")
add("author self attestation",self_attest,"non-independent attestation")
def main():
 clean()
 for n,m,s in cases:reject(n,m,s)
 clean();print(f"TOTFR AGENT MUTATION TESTS PASSED: rejected={len(cases)} clean_baselines=2");print("END-OF-FILE SENTINEL: TOTFR-AGENT-MUTATION-TESTS-2026-09-04-V1")
if __name__=="__main__":raise SystemExit(main())
