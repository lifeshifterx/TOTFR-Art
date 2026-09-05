#!/usr/bin/env python3
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];VAL=ROOT/'tools/validate_totfr_runtime_trust.py'
def runv(r):
 e=os.environ.copy();e['TOTFR_ROOT']=str(r);p=subprocess.run([sys.executable,str(VAL)],text=True,capture_output=True,env=e);return p.returncode,(p.stdout or '')+(p.stderr or '')
def clone():
 t=tempfile.TemporaryDirectory();d=Path(t.name)/'repo';shutil.copytree(ROOT,d,ignore=shutil.ignore_patterns('.git','__pycache__'));return t,d
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
  if rc==0:raise AssertionError(f'{name}: validator accepted bad state')
  if needle not in o:raise AssertionError(f'{name}: expected {needle!r}\n{o}')
  print('PASS reject:',name)
 finally:t.cleanup()
def jedit(p,fn):
 x=json.loads(p.read_text());fn(x);p.write_text(json.dumps(x,indent=2)+'\n')
def mk_run(r,tier=1,phase='PLANNED',visual=None):
 d=r/'13 Source Prompts/Deployment Runs/TEST-RUNTIME';(d/'plan').mkdir(parents=True);p=d/'plan/01.jsonl'
 row={'target_id':'T1','risk_tier':tier};p.write_text(json.dumps(row)+'\n'+json.dumps({'type':'EOF_CONTROL'})+'\n')
 run={'run_id':'TEST-RUNTIME','plan_shards':[{'path':str(p.relative_to(r))}]};(d/'run.json').write_text(json.dumps(run))
 (d/'state.json').write_text(json.dumps({'run_id':'TEST-RUNTIME','phase':phase}))
 if visual is not None:
  (d/'visual').mkdir();(d/'visual/T1.json').write_text(json.dumps(visual))
 return d,p
def good_visual(privacy='PLAYER_SAFE',ref='library://visual/T1.png'):
 return {'target_id':'T1','destination_id':'page-1','receipt_blob_sha':'1'*40,'artifact_ref':ref,'artifact_sha256':'a'*64,'captured_at':'2026-09-05T00:00:00Z','privacy':privacy,'browser_runtime':'browser','viewport':'1440x900','hard_reload':True,'decision':'PASS'}
cases=[]
def add(n,m,s):cases.append((n,m,s))
add('self IDs promoted to security identity',lambda r:jedit(r/'13 Source Prompts/TOTFR_Agent_Trust_Boundary.json',lambda x:x.update({'self_declared_instance_ids_are_security_identity':True})),'self-declared instance IDs cannot be security identity')
add('Tier2 execution enabled without identity enforcement',lambda r:jedit(r/'13 Source Prompts/TOTFR_Agent_Trust_Boundary.json',lambda x:x.update({'tier2_agent_execution_allowed_when_identity_unconfigured':True})),'Tier-2 must be blocked')
add('verification doctrine removed',lambda r:(r/'AGENTS.md').write_text((r/'AGENTS.md').read_text().replace('VERIFY THEN TRUST','REMOVED')),'AGENTS.md missing verification/trust control')
add('Tier2 run advances while identity unconfigured',lambda r:mk_run(r,tier=2,phase='APPROVED'),'Tier-2 agent run advanced')
def missing_artifact(r):
 v=good_visual();v.pop('artifact_ref');mk_run(r,visual=v)
add('visual missing durable artifact ref',missing_artifact,'visual evidence missing fields')
def signed_visual(r):mk_run(r,visual=good_visual(ref='library://x?X-Amz-Signature=secret'))
add('signed URL persisted as visual evidence',signed_visual,'signed/secret visual artifact ref persisted')
def public_dm(r):mk_run(r,visual=good_visual('DM_HOLD','github://public/evidence.png'))
add('DM visual stored publicly',public_dm,'DM visual evidence is not in private durable storage')
def bad_hash(r):
 v=good_visual();v['artifact_sha256']='bad';mk_run(r,visual=v)
add('invalid visual artifact hash',bad_hash,'invalid visual artifact SHA-256')
def bad_plan(r):
 d,p=mk_run(r);p.write_text('{not-json}\n')
add('malformed plan hidden from trust scan',bad_plan,'plan parse failure during runtime trust scan')
def missing_plan(r):
 d,p=mk_run(r);p.unlink()
add('missing plan hidden from trust scan',missing_plan,'missing plan shard during runtime trust scan')
def main():
 clean()
 for n,m,s in cases:reject(n,m,s)
 clean();print(f'TOTFR RUNTIME TRUST TESTS PASSED: rejected={len(cases)} clean_baselines=2');print('END-OF-FILE SENTINEL: TOTFR-RUNTIME-TRUST-TESTS-2026-09-04-V1')
if __name__=='__main__':raise SystemExit(main())
