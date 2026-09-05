#!/usr/bin/env python3
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];VAL=ROOT/'tools/validate_totfr_meta_controls.py'
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
def repl(p,a,b):p.write_text(p.read_text().replace(a,b),encoding='utf-8')
SRC=lambda r:r/'13 Source Prompts'
cases=[]
def add(n,m,s):cases.append((n,m,s))
add('status source binding disabled',lambda r:jedit(SRC(r)/'TOTFR_Required_GitHub_Protection.json',lambda x:x.update({'require_status_source_binding':False})),'source-bound')
add('strict checks disabled',lambda r:jedit(SRC(r)/'TOTFR_Required_GitHub_Protection.json',lambda x:x.update({'strict_required_status_checks_policy':False})),'strict status checks')
add('always bypass enabled',lambda r:jedit(SRC(r)/'TOTFR_Required_GitHub_Protection.json',lambda x:x.update({'allow_always_bypass':True})),'always-bypass')
add('integration target widened',lambda r:jedit(SRC(r)/'TOTFR_Required_GitHub_Protection.json',lambda x:x.update({'integration_branch':'~ALL'})),'default branch specifically')
add('required check removed',lambda r:jedit(SRC(r)/'TOTFR_Required_GitHub_Protection.json',lambda x:x.update({'required_status_contexts':['validate']})),'required status contexts')
add('self IDs promoted',lambda r:jedit(SRC(r)/'TOTFR_Agent_Trust_Boundary.json',lambda x:x.update({'self_declared_instance_ids_are_security_identity':True})),'self-declared security identity')
add('file attestation promoted',lambda r:jedit(SRC(r)/'TOTFR_Agent_Trust_Boundary.json',lambda x:x.update({'human_file_attestation_is_security_identity':True})),'file attestation')
add('Tier2 agent execution opened',lambda r:jedit(SRC(r)/'TOTFR_Agent_Trust_Boundary.json',lambda x:x.update({'tier2_agent_execution_allowed_when_identity_unconfigured':True})),'Tier-2 is not fail-closed')
add('durable visual evidence disabled',lambda r:jedit(SRC(r)/'TOTFR_Runtime_Evidence_Policy.json',lambda x:x.update({'visual_artifact_ref_must_be_durable':False})),'durable visual evidence')
add('signed visual URLs allowed',lambda r:jedit(SRC(r)/'TOTFR_Runtime_Evidence_Policy.json',lambda x:x.update({'ephemeral_signed_url_allowed':True})),'ephemeral signed evidence')
add('internal repo privacy weakened',lambda r:jedit(SRC(r)/'TOTFR_Publication_Boundary.json',lambda x:x.update({'internal_control_repository_required_visibility':'PUBLIC'})),'PRIVATE visibility')
add('history contamination erased',lambda r:jedit(SRC(r)/'TOTFR_Publication_Boundary.json',lambda x:x.update({'current_public_history_is_spoiler_contaminated':False})),'contamination')
def pubflag(r,k):jedit(SRC(r)/'TOTFR_Publication_Boundary.json',lambda x:x['policy'].update({k:True}))
add('public control plane allowed',lambda r:pubflag(r,'control_plane_allowed_in_player_safe_public_repository'),'control plane must be prohibited')
add('public future metadata allowed',lambda r:pubflag(r,'future_or_dm_metadata_allowed_in_player_safe_public_repository'),'future/DM metadata')
add('main workflow path filtered',lambda r:repl(r/'.github/workflows/validate-totfr-guardrails.yml','  pull_request:\n','  pull_request:\n    paths: ["tools/**"]\n'),'path filters')
add('main workflow uses pull_request_target',lambda r:repl(r/'.github/workflows/validate-totfr-guardrails.yml','  pull_request:\n','  pull_request_target:\n'),'pull_request_target')
add('main workflow gets write token',lambda r:repl(r/'.github/workflows/validate-totfr-guardrails.yml','  contents: read','  contents: write'),'write privilege')
add('integrity hostile tests removed',lambda r:repl(r/'.github/workflows/validate-totfr-control-plane.yml','      - name: Prove control-plane self-protection rejects weakened states\n        run: python tools/test_totfr_meta_controls.py\n',''),'integrity workflow missing required step')
add('meta test deleted',lambda r:(r/'tools/test_totfr_meta_controls.py').unlink(),'missing required validator/test')
def main():
 clean()
 for n,m,s in cases:reject(n,m,s)
 clean();print(f'TOTFR META CONTROL TESTS PASSED: rejected={len(cases)} clean_baselines=2');print('END-OF-FILE SENTINEL: TOTFR-META-CONTROL-TESTS-2026-09-04-V1')
if __name__=='__main__':raise SystemExit(main())
