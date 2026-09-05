#!/usr/bin/env python3
from pathlib import Path
import csv,os,sys
ROOT=Path(os.environ.get('TOTFR_ROOT',Path(__file__).resolve().parents[1])).resolve();P=ROOT/'13 Source Prompts/TOTFR_Agent_Role_Matrix.csv';ERR=[]
def fail(x):ERR.append(x)
if not P.exists():fail('missing agent role matrix');rows=[]
else:
 try:rows=list(csv.DictReader(P.open(newline='',encoding='utf-8')))
 except Exception as e:fail(f'role matrix parse failure: {e}');rows=[]
if rows:
 fields=set(rows[0].keys())
 for k in ['role_id','notion_write','github_prod_write','github_control_write','github_merge','art_generate','art_approve','structural_approve','visual_approve','redteam']:
  if k not in fields:fail(f'role matrix missing permission column: {k}')
 active=[r for r in rows if r.get('role_id') and r.get('role_id')!='__EOF_CONTROL__']
 mergers=[r['role_id'] for r in active if r.get('github_merge')=='YES']
 if mergers:fail(f'agent merge authority prohibited: {mergers}')
 writers=[r['role_id'] for r in active if r.get('notion_write')=='YES']
 if writers!=['notion_executor']:fail(f'Notion writer set must be exactly notion_executor: {writers}')
 for r in active:
  rid=r['role_id']
  if r.get('art_generate')=='YES' and r.get('art_approve')=='YES':fail(f'art self-approval prohibited: {rid}')
  if r.get('github_control_write')=='YES' and r.get('redteam')=='YES':fail(f'control author/redteam overlap prohibited: {rid}')
  if r.get('notion_write')=='YES' and any(r.get(k)=='YES' for k in ['structural_approve','visual_approve','redteam']):fail(f'Notion writer/reviewer overlap prohibited: {rid}')
if ERR:
 print('TOTFR ROLE BOUNDARY VALIDATION FAILED')
 for e in ERR:print('- '+e)
 sys.exit(1)
print('TOTFR ROLE BOUNDARY VALIDATION PASSED')
print('END-OF-FILE SENTINEL: TOTFR-ROLE-BOUNDARY-VALIDATOR-2026-09-04-V1')
