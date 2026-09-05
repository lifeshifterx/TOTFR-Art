#!/usr/bin/env python3
from pathlib import Path
import json,os,sys,urllib.request
repo=os.environ.get('GITHUB_REPOSITORY');token=os.environ.get('GITHUB_TOKEN');ERR=[]
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'13 Source Prompts';POL=SRC/'TOTFR_Required_GitHub_Protection.json';PUB=SRC/'TOTFR_Publication_Boundary.json'
def fail(x):ERR.append(x)
def get(path):
 if not repo or not token:fail('missing GITHUB_REPOSITORY/GITHUB_TOKEN');return None
 req=urllib.request.Request(f'https://api.github.com/repos/{repo}{path}',headers={'Authorization':f'Bearer {token}','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
 try:
  with urllib.request.urlopen(req,timeout=20) as r:return json.load(r)
 except Exception as e:fail(f'GitHub API read failed {path}: {e}');return None
def load(p,label):
 try:return json.loads(p.read_text(encoding='utf-8'))
 except Exception as e:fail(f'{label} load failed: {e}');return {}
policy=load(POL,'protection policy');pub=load(PUB,'publication policy')
required=set(policy.get('required_rule_types',[]));required_checks=set(policy.get('required_status_contexts',[]));strict_required=policy.get('strict_required_status_checks_policy') is True;allow_always=policy.get('allow_always_bypass') is True;source_binding=policy.get('require_status_source_binding') is True
meta=get('') or {};default=meta.get('default_branch','development')
if pub.get('internal_control_repository')==repo and pub.get('internal_control_repository_required_visibility')=='PRIVATE' and meta.get('private') is not True:
 fail(f'internal control repository must be PRIVATE; observed private={meta.get("private")}')
items=get('/rulesets') or [];found=[]
for item in items:
 if item.get('enforcement')!='active':continue
 d=get('/rulesets/'+str(item.get('id'))) or {};inc=(d.get('conditions',{}).get('ref_name',{}).get('include') or [])
 targets_default=('~DEFAULT_BRANCH' in inc or default in inc or f'refs/heads/{default}' in inc)
 if not targets_default or '~ALL' in inc:continue
 rules={r.get('type'):r for r in d.get('rules',[])};missing=required-set(rules);bypass=[b for b in d.get('bypass_actors',[]) if b.get('bypass_mode')=='always']
 params=rules.get('required_status_checks',{}).get('parameters',{});strict=params.get('strict_required_status_checks_policy') is True
 check_entries=[x for x in params.get('required_status_checks',[]) if isinstance(x,dict)];checks={x.get('context','') for x in check_entries};missing_checks=required_checks-checks
 unbound=sorted(x for x in required_checks if x in checks and not any(e.get('context')==x and isinstance(e.get('integration_id'),int) and e.get('integration_id')>0 for e in check_entries)) if source_binding else []
 result={'id':d.get('id'),'name':d.get('name'),'include':inc,'missing_rules':sorted(missing),'missing_checks':sorted(missing_checks),'unbound_checks':unbound,'always_bypass':len(bypass),'strict':strict}
 found.append(result)
 if not missing and not missing_checks and not unbound and (not strict_required or strict) and (allow_always or not bypass) and not ERR:
  print('TOTFR LIVE PROTECTION VALIDATION PASSED');print(json.dumps(result,sort_keys=True));print('END-OF-FILE SENTINEL: TOTFR-LIVE-PROTECTION-VALIDATOR-2026-09-04-V3');raise SystemExit(0)
fail(f'no active default-branch integration ruleset satisfies required controls; observed={found}')
print('TOTFR LIVE PROTECTION VALIDATION FAILED')
for e in ERR:print('- '+e)
sys.exit(1)
