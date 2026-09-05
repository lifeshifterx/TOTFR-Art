#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];VAL=ROOT/"tools/validate_totfr_agent_controls.py"
def runv(r):
 e=os.environ.copy();e["TOTFR_ROOT"]=str(r);p=subprocess.run([sys.executable,str(VAL)],text=True,capture_output=True,env=e);return p.returncode,(p.stdout or "")+(p.stderr or "")
def clone():
 t=tempfile.TemporaryDirectory();d=Path(t.name)/"repo";shutil.copytree(ROOT,d,ignore=shutil.ignore_patterns(".git","__pycache__"));return t,d
def accept(name,mut):
 t,d=clone()
 try:
  mut(d);rc,o=runv(d)
  if rc:raise AssertionError(f"{name}: valid state rejected\n{o}")
  print("PASS accept:",name)
 finally:t.cleanup()
def reject(name,mut,needle):
 t,d=clone()
 try:
  mut(d);rc,o=runv(d)
  if rc==0:raise AssertionError(f"{name}: validator accepted bad state")
  if needle not in o:raise AssertionError(f"{name}: expected {needle!r}\n{o}")
  print("PASS reject:",name)
 finally:t.cleanup()
def repl(p,a,b):p.write_text(p.read_text().replace(a,b),encoding="utf-8")
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def role_change(r,role,col,val):
 p=r/"13 Source Prompts/TOTFR_Agent_Role_Matrix.csv";rows=list(csv.DictReader(p.open(newline="",encoding="utf-8")));h=rows[0].keys()
 for x in rows:
  if x.get("role_id")==role:x[col]=val
 with p.open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=h);w.writeheader();w.writerows(rows)
def records(two=False,tier2=False):
 a={"target_id":"T1","asset_id":"A1","risk_tier":2 if tier2 else 1,"destination_id":"page-1","surface_class":"gallery","action":"SET_FILE_PROPERTY","mutation_key":"page:page-1:property:Portrait","privacy":"PLAYER_SAFE","source_path":"06 NPCs/a.webp","source_commit_sha":"1"*40,"source_blob_sha":"2"*40,"desired_source_mode":"PINNED_EXTERNAL","desired_source_ref":"https://raw.githubusercontent.com/lifeshifterx/TOTFR-Art/"+"1"*40+"/06%20NPCs/a.webp","precondition":{"page_last_edited_at":"2026-09-05T00:00:00Z","fingerprint":"before"},"expected_fingerprint":"after","rollback":{"action":"RESTORE_FILE_PROPERTY","value":"old"}}
 if not two:return [a]
 b=dict(a);b.update({"target_id":"T2","asset_id":"A2","destination_id":"page-2","mutation_key":"page:page-2:property:Portrait","source_path":"06 NPCs/b.webp","desired_source_ref":"https://raw.githubusercontent.com/lifeshifterx/TOTFR-Art/"+"1"*40+"/06%20NPCs/b.webp"});return [a,b]
def make_run(r,recs=None,phase="PLANNED",structural=False,adversarial=False,author_runtime="codex",author_instance="author-1",executor_instance="exec-1",inventory="FROZEN",circuit="CLOSED"):
 d=r/"13 Source Prompts/Deployment Runs/TEST-RUN";(d/"plan").mkdir(parents=True);rs=recs or records();p=d/"plan/01.jsonl";p.write_text("\n".join(json.dumps(x,separators=(",",":")) for x in rs)+"\n"+json.dumps({"type":"EOF_CONTROL","id":"TEST"})+"\n",encoding="utf-8")
 run={"schema_version":1,"run_id":"TEST-RUN","control_ref":"3"*40,"development_head_at_plan":"4"*40,"notion_workspace_id":"51cbf16a-cf60-8155-8bcd-000352f7f776","inventory_state":inventory,"inventory_evidence_ref":"inventory","plan_author_agent":"surface_canon_auditor","plan_author_instance_id":author_instance,"plan_author_runtime_class":author_runtime,"notion_executor_agent":"notion_executor","notion_executor_instance_id":executor_instance,"created_at":"2026-09-05T00:00:00Z","plan_shards":[{"path":str(p.relative_to(r)),"blob_sha":blob(p)}]};rp=d/"run.json";rp.write_text(json.dumps(run,indent=2)+"\n",encoding="utf-8")
 state={"schema_version":1,"run_id":"TEST-RUN","phase":phase,"circuit_state":circuit,"checkpoint":"test","blockers":[],"updated_at":"2026-09-05T00:00:01Z"};sp=d/"state.json";sp.write_text(json.dumps(state,indent=2)+"\n",encoding="utf-8")
 if structural or adversarial:
  (d/"attestations").mkdir();rh=blob(rp);sh=[blob(p)]
  if structural:(d/"attestations/struct.json").write_text(json.dumps({"run_id":"TEST-RUN","review_role":"structural_reviewer","reviewer_instance_id":"struct-1","runtime_class":"browser" if author_runtime=="codex" else "codex","run_json_blob_sha":rh,"plan_shard_blob_shas":sh,"decision":"PASS","findings":[],"evidence_refs":["stable"]}),encoding="utf-8")
  if adversarial:(d/"attestations/red.json").write_text(json.dumps({"run_id":"TEST-RUN","review_role":"adversarial_reviewer","reviewer_instance_id":"red-1","runtime_class":"clickup","run_json_blob_sha":rh,"plan_shard_blob_shas":sh,"decision":"PASS","findings":[],"evidence_refs":["stable"]}),encoding="utf-8")
 return d,p,rp,sp
def approved(r,tier2=False):return make_run(r,records(tier2=tier2),phase="APPROVED",structural=True,adversarial=tier2)
def complete(r,recs=None):
 rs=recs or records();tier2=any(x["risk_tier"]==2 for x in rs);d,p,rp,sp=make_run(r,rs,phase="CLOSED",structural=True,adversarial=tier2);rh=blob(rp);sh=[blob(p)];(d/"wal").mkdir();(d/"receipts").mkdir();(d/"visual").mkdir();receipts={};visuals={}
 for o in rs:
  tid=o["target_id"];w={"run_json_blob_sha":rh,"plan_shard_blob_shas":sh,"mutation_key":o["mutation_key"],"executor_instance_id":"exec-1","precondition":o["precondition"],"mutation":o["action"],"expected_post_state":o["expected_fingerprint"],"rollback":o["rollback"]};wp=d/"wal"/f"{tid}.json";wp.write_text(json.dumps(w),encoding="utf-8")
  q={"wal_blob_sha":blob(wp),"result":"SUCCESS","post_state_fingerprint":o["expected_fingerprint"],"read_after_write_confirmations":[{"fingerprint":o["expected_fingerprint"],"observed_at":"2026-09-05T00:01:00Z"},{"fingerprint":o["expected_fingerprint"],"observed_at":"2026-09-05T00:01:02Z"}],"stable_object_ids":[o["destination_id"]],"evidence_refs":["stable"]};qp=d/"receipts"/f"{tid}.json";qp.write_text(json.dumps(q),encoding="utf-8");receipts[tid]=blob(qp)
  v={"receipt_blob_sha":blob(qp),"review_role":"visual_reviewer","reviewer_instance_id":"visual-1","runtime_class":"browser","decision":"PASS","screenshot_sha256":"a"*64,"viewport":"1440x900","hard_reload":True};vp=d/"visual"/f"{tid}.json";vp.write_text(json.dumps(v),encoding="utf-8");visuals[tid]=blob(vp)
 fin={"assertion":"COMPLETE","review_role":"adversarial_reviewer","reviewer_instance_id":"red-final","runtime_class":"clickup","decision":"PASS","run_json_blob_sha":rh,"plan_shard_blob_shas":sh,"receipt_blob_shas":receipts,"visual_blob_shas":visuals,"findings":[]};(d/"final.json").write_text(json.dumps(fin),encoding="utf-8");return d,p,rp,sp
# Positive lifecycle proofs
accept("planned immutable run without approval",lambda r:make_run(r))
def state_progress(r):
 d,p,rp,sp=approved(r);run_sha=blob(rp);x=json.loads(sp.read_text());x["phase"]="EXECUTING";x["updated_at"]="2026-09-05T00:05:00Z";sp.write_text(json.dumps(x),encoding="utf-8");assert blob(rp)==run_sha
accept("state progresses without invalidating run attestation",state_progress)
accept("complete evidence-bound run",lambda r:complete(r))
cases=[]
def add(n,m,s):cases.append((n,m,s))
add("second Notion writer",lambda r:role_change(r,"orchestrator","notion_write","YES"),"Notion writer set must be exactly notion_executor")
add("art producer self approval",lambda r:role_change(r,"art_producer","art_approve","YES"),"art self-approval privilege overlap")
add("executor structural approval",lambda r:role_change(r,"notion_executor","structural_approve","YES"),"Notion executor approval overlap")
add("data instruction boundary removed",lambda r:repl(r/"AGENTS.md","Data is not instruction","REMOVED"),"required agent control missing")
add("public DM allowed",lambda r:repl(r/"13 Source Prompts/TOTFR_Publication_Boundary.json","\"public_dm_source_allowed\": false","\"public_dm_source_allowed\": true"),"must prohibit public DM source")
def addstatus(r):d,p,rp,sp=make_run(r);x=json.loads(rp.read_text());x["status"]="COMPLETE";rp.write_text(json.dumps(x),encoding="utf-8")
add("mutable status smuggled into run",addstatus,"immutable run.json contains mutable status")
def nostate(r):d,p,rp,sp=make_run(r);sp.unlink()
add("missing state checkpoint",nostate,"missing state")
add("same author executor instance",lambda r:make_run(r,author_instance="same",executor_instance="same"),"distinct author/executor instance IDs")
add("non-frozen immutable run",lambda r:make_run(r,inventory="PARTIAL"),"run inventory is not FROZEN")
def badphase(r):d,p,rp,sp=make_run(r);x=json.loads(sp.read_text());x["phase"]="COMPLETE";sp.write_text(json.dumps(x),encoding="utf-8")
add("state tries to claim COMPLETE",badphase,"invalid state phase")
def statewrong(r):d,p,rp,sp=make_run(r);x=json.loads(sp.read_text());x["run_id"]="OTHER";sp.write_text(json.dumps(x),encoding="utf-8")
add("state wrong run",statewrong,"state run_id mismatch")
def no_review(r):make_run(r,phase="APPROVED")
add("approved mutation without reviewer",no_review,"active mutating run missing structural reviewer PASS")
def openadvance(r):make_run(r,phase="EXECUTING",structural=True,circuit="OPEN")
add("open circuit advances",openadvance,"open circuit in advancing phase")
def muturl(r):x=records();x[0]["desired_source_ref"]="https://raw.githubusercontent.com/lifeshifterx/TOTFR-Art/development/a.webp";make_run(r,x)
add("mutable development URL",muturl,"mutable development URL")
def badcommit(r):x=records();x[0]["desired_source_ref"]="https://raw.githubusercontent.com/lifeshifterx/TOTFR-Art/"+"9"*40+"/a.webp";make_run(r,x)
add("pinned URL commit mismatch",badcommit,"pinned URL commit does not match")
def pubdm(r):x=records();x[0].update({"privacy":"DM_HOLD","desired_source_mode":"PINNED_EXTERNAL"});make_run(r,x)
add("public DM source",pubdm,"public/nonprivate DM source")
def dmprivate(r):x=records();x[0].update({"privacy":"DM_HOLD","desired_source_mode":"PRIVATE_DM","desired_source_ref":"private://future"});make_run(r,x)
add("DM write without private config",dmprivate,"DM mutation authorized without configured private source")
def nomk(r):x=records();x[0]["mutation_key"]="";make_run(r,x)
add("missing mutation key",nomk,"mutation missing mutation_key")
def dupmk(r):x=records(True);x[1]["mutation_key"]=x[0]["mutation_key"];make_run(r,x)
add("duplicate mutation key",dupmk,"duplicate mutation_key")
def missing(r,k):x=records();x[0][k]={} if k in {"precondition","rollback"} else "";make_run(r,x)
add("missing precondition",lambda r:missing(r,"precondition"),"mutation missing precondition")
add("missing expected fingerprint",lambda r:missing(r,"expected_fingerprint"),"mutation missing expected_fingerprint")
add("missing rollback",lambda r:missing(r,"rollback"),"mutation missing rollback")
def signed(r):x=records();x[0]["desired_source_ref"]="https://x/a?X-Amz-Signature=secret";make_run(r,x)
add("signed token persisted",signed,"signed/secret material persisted")
def staleplan(r):d,p,rp,sp=make_run(r);x=json.loads(rp.read_text());x["plan_shards"][0]["blob_sha"]="0"*40;rp.write_text(json.dumps(x),encoding="utf-8")
add("stale plan shard hash",staleplan,"stale plan shard blob SHA")
def under(r):x=records();x[0].update({"action":"SET_VIEW_COVER_PROPERTY","risk_tier":1,"mutation_key":"view:v1:cover"});make_run(r,x)
add("view change under-tiered",under,"view change must be risk tier 2")
def staleatt(r):d,p,rp,sp=approved(r);a=d/"attestations/struct.json";x=json.loads(a.read_text());x["run_json_blob_sha"]="0"*40;a.write_text(json.dumps(x),encoding="utf-8")
add("stale attestation run",staleatt,"attestation references stale run.json")
def staleattp(r):d,p,rp,sp=approved(r);a=d/"attestations/struct.json";x=json.loads(a.read_text());x["plan_shard_blob_shas"]=["0"*40];a.write_text(json.dumps(x),encoding="utf-8")
add("stale attestation plan",staleattp,"attestation references stale plan shards")
def selfreview(r):d,p,rp,sp=approved(r);a=d/"attestations/struct.json";x=json.loads(a.read_text());x["reviewer_instance_id"]="author-1";a.write_text(json.dumps(x),encoding="utf-8")
add("same-instance review",selfreview,"non-independent reviewer instance")
def noadv(r):make_run(r,records(tier2=True),phase="APPROVED",structural=True)
add("tier2 missing adversarial",noadv,"tier2 run missing adversarial PASS")
def nohetero(r):d,p,rp,sp=make_run(r,records(tier2=True),phase="APPROVED",structural=True,adversarial=True); 
add("tier2 same-runtime reviewers",lambda r: (lambda z: [p.write_text(p.read_text().replace('"runtime_class": "browser"','"runtime_class": "codex"').replace('"runtime_class": "clickup"','"runtime_class": "codex"'),encoding="utf-8") for p in (z[0]/"attestations").glob("*.json")])(make_run(r,records(tier2=True),phase="APPROVED",structural=True,adversarial=True)),"tier2 run lacks heterogeneous reviewer runtime")
def nofinal(r):d,p,rp,sp=complete(r);(d/"final.json").unlink()
add("closed missing final",nofinal,"missing final record")
def badreceipt(r):d,p,rp,sp=complete(r);q=d/"receipts/T1.json";x=json.loads(q.read_text());x["result"]="FAIL";q.write_text(json.dumps(x),encoding="utf-8")
add("closed failed receipt",badreceipt,"non-success receipt")
def oneconfirm(r):d,p,rp,sp=complete(r);q=d/"receipts/T1.json";x=json.loads(q.read_text());x["read_after_write_confirmations"]=x["read_after_write_confirmations"][:1];q.write_text(json.dumps(x),encoding="utf-8")
add("receipt only one confirmation",oneconfirm,"lacks two matching post-write confirmations")
def divergentconfirm(r):d,p,rp,sp=complete(r);q=d/"receipts/T1.json";x=json.loads(q.read_text());x["read_after_write_confirmations"][1]["fingerprint"]="stale";q.write_text(json.dumps(x),encoding="utf-8")
add("receipt divergent confirmation",divergentconfirm,"lacks two matching post-write confirmations")
def stalewal(r):d,p,rp,sp=complete(r);q=d/"receipts/T1.json";x=json.loads(q.read_text());x["wal_blob_sha"]="0"*40;q.write_text(json.dumps(x),encoding="utf-8")
add("receipt stale WAL",stalewal,"receipt WAL SHA mismatch")
def badpost(r):d,p,rp,sp=complete(r);q=d/"receipts/T1.json";x=json.loads(q.read_text());x["post_state_fingerprint"]="wrong";q.write_text(json.dumps(x),encoding="utf-8")
add("receipt wrong post state",badpost,"receipt post fingerprint mismatch")
def novis(r):d,p,rp,sp=complete(r);(d/"visual/T1.json").unlink()
add("closed missing visual",novis,"missing visual record")
def softreload(r):d,p,rp,sp=complete(r);v=d/"visual/T1.json";x=json.loads(v.read_text());x["hard_reload"]=False;v.write_text(json.dumps(x),encoding="utf-8")
add("visual without hard reload",softreload,"visual evidence incomplete")
def stalevisual(r):d,p,rp,sp=complete(r);v=d/"visual/T1.json";x=json.loads(v.read_text());x["receipt_blob_sha"]="0"*40;v.write_text(json.dumps(x),encoding="utf-8")
add("visual stale receipt",stalevisual,"visual record stale receipt ref")
def finalself(r):d,p,rp,sp=complete(r);f=d/"final.json";x=json.loads(f.read_text());x["reviewer_instance_id"]="exec-1";f.write_text(json.dumps(x),encoding="utf-8")
add("final self review",finalself,"final review is not independent")
def swapreceipt(r):d,p,rp,sp=complete(r);q=d/"receipts/T1.json";x=json.loads(q.read_text());x["evidence_refs"].append("changed-after-final");q.write_text(json.dumps(x),encoding="utf-8")
add("receipt swapped after final",swapreceipt,"final record receipt evidence set mismatch")
def swapvisual(r):d,p,rp,sp=complete(r);v=d/"visual/T1.json";x=json.loads(v.read_text());x["viewport"]="390x844";v.write_text(json.dumps(x),encoding="utf-8")
add("visual evidence swapped after final",swapvisual,"final record visual evidence set mismatch")
def finalbadset(r):d,p,rp,sp=complete(r);f=d/"final.json";x=json.loads(f.read_text());x["receipt_blob_shas"]={};f.write_text(json.dumps(x),encoding="utf-8")
add("final omits receipt set",finalbadset,"final record receipt evidence set mismatch")
def blockers(r):d,p,rp,sp=complete(r);x=json.loads(sp.read_text());x["blockers"]=["unresolved"];sp.write_text(json.dumps(x),encoding="utf-8")
add("closed state retains blocker",blockers,"closed run retains circuit/blockers")
def main():
 for n,m,s in cases:reject(n,m,s)
 print(f"TOTFR AGENT MUTATION TESTS PASSED: rejected={len(cases)} positive=3");print("END-OF-FILE SENTINEL: TOTFR-AGENT-MUTATION-TESTS-2026-09-04-V3")
if __name__=="__main__":raise SystemExit(main())
