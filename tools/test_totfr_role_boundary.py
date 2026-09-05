#!/usr/bin/env python3
from pathlib import Path
import csv,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];VAL=ROOT/'tools/validate_totfr_role_boundary.py'
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
def mutate(r,role,col,val):
 p=r/'13 Source Prompts/TOTFR_Agent_Role_Matrix.csv';rows=list(csv.DictReader(p.open(newline='',encoding='utf-8')));fields=list(rows[0].keys())
 for x in rows:
  if x.get('role_id')==role:x[col]=val
 with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def dropcol(r,col):
 p=r/'13 Source Prompts/TOTFR_Agent_Role_Matrix.csv';rows=list(csv.DictReader(p.open(newline='',encoding='utf-8')));fields=[x for x in rows[0].keys() if x!=col]
 with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
cases=[
 ('orchestrator merge authority',lambda r:mutate(r,'orchestrator','github_merge','YES'),'agent merge authority prohibited'),
 ('control author merge authority',lambda r:mutate(r,'control_author','github_merge','YES'),'agent merge authority prohibited'),
 ('second Notion writer',lambda r:mutate(r,'orchestrator','notion_write','YES'),'Notion writer set must be exactly notion_executor'),
 ('art producer self approval',lambda r:mutate(r,'art_producer','art_approve','YES'),'art self-approval prohibited'),
 ('control author redteam overlap',lambda r:mutate(r,'control_author','redteam','YES'),'control author/redteam overlap prohibited'),
 ('executor reviewer overlap',lambda r:mutate(r,'notion_executor','structural_approve','YES'),'Notion writer/reviewer overlap prohibited'),
 ('merge column deleted',lambda r:dropcol(r,'github_merge'),'missing permission column: github_merge')]
def main():
 clean()
 for n,m,s in cases:reject(n,m,s)
 clean();print(f'TOTFR ROLE BOUNDARY TESTS PASSED: rejected={len(cases)} clean_baselines=2');print('END-OF-FILE SENTINEL: TOTFR-ROLE-BOUNDARY-TESTS-2026-09-04-V1')
if __name__=='__main__':raise SystemExit(main())
