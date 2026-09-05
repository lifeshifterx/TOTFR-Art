#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'13 Source Prompts';ERR=[]
def fail(x):ERR.append(x)
def text(p):
 if not p.exists():fail(f'missing control-plane file: {p.relative_to(ROOT)}');return ''
 return p.read_text(encoding='utf-8')
def load(p):
 if not p.exists():fail(f'missing control policy: {p.relative_to(ROOT)}');return {}
 try:return json.loads(p.read_text(encoding='utf-8'))
 except Exception as e:fail(f'policy parse failure {p.relative_to(ROOT)}: {e}');return {}
policy=load(SRC/'TOTFR_Required_GitHub_Protection.json');trust=load(SRC/'TOTFR_Agent_Trust_Boundary.json');evidence=load(SRC/'TOTFR_Runtime_Evidence_Policy.json')
if policy:
 if policy.get('verification_doctrine')!='VERIFY_THEN_TRUST_EXACT_STATE':fail('protection policy doctrine mismatch')
 if set(policy.get('required_status_contexts',[]))!={'validate','control-plane-integrity'}:fail('required status contexts must be validate + control-plane-integrity')
 if policy.get('strict_required_status_checks_policy') is not True:fail('strict status checks must be required')
 if policy.get('allow_always_bypass') is not False:fail('always-bypass must be prohibited')
if trust:
 if trust.get('self_declared_instance_ids_are_security_identity') is not False:fail('trust boundary permits self-declared security identity')
 if trust.get('agent_identity_enforcement_state')=='UNCONFIGURED' and trust.get('tier2_agent_execution_allowed_when_identity_unconfigured') is not False:fail('Tier-2 is not fail-closed while identity is unconfigured')
if evidence and evidence.get('visual_artifact_ref_must_be_durable') is not True:fail('durable visual evidence control missing')
main=ROOT/'.github/workflows/validate-totfr-guardrails.yml';integrity=ROOT/'.github/workflows/validate-totfr-control-plane.yml';m=text(main);i=text(integrity)
for name,w in [('main',m),('integrity',i)]:
 if 'pull_request_target' in w:fail(f'{name} workflow uses pull_request_target')
 if 'paths:' in w:fail(f'{name} workflow path filters can suppress required checks')
 for tok in ['permissions:','contents: read','persist-credentials: false','actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1','actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97']:
  if tok not in w:fail(f'{name} workflow missing hardening token: {tok}')
 if 'contents: write' in w or 'pull-requests: write' in w or 'issues: write' in w:fail(f'{name} workflow has write privilege')
for tok in ['python tools/validate_totfr_guardrails.py','python tools/test_totfr_guardrails.py','python tools/validate_totfr_agent_controls.py','python tools/test_totfr_agent_controls.py','python tools/validate_totfr_runtime_trust.py','python tools/test_totfr_runtime_trust.py','python tools/validate_totfr_live_protection.py','cancel-in-progress: true']:
 if tok not in m:fail(f'main workflow missing required step/control: {tok}')
for tok in ['control-plane-integrity','python tools/validate_totfr_meta_controls.py','python tools/validate_totfr_live_protection.py','cancel-in-progress: true']:
 if tok not in i:fail(f'integrity workflow missing required step/control: {tok}')
ag=text(ROOT/'AGENTS.md')
for tok in ['VERIFY THEN TRUST','Self-declared instance IDs are not security identities','Tier-2 agent execution is prohibited']:
 if tok not in ag:fail(f'AGENTS.md missing meta-control: {tok}')
for p in [ROOT/'tools/validate_totfr_runtime_trust.py',ROOT/'tools/test_totfr_runtime_trust.py',ROOT/'tools/validate_totfr_live_protection.py',ROOT/'tools/validate_totfr_meta_controls.py']:
 if not p.exists():fail(f'missing required validator/test: {p.relative_to(ROOT)}')
if ERR:
 print('TOTFR META CONTROL VALIDATION FAILED')
 for e in ERR:print('- '+e)
 sys.exit(1)
print('TOTFR META CONTROL VALIDATION PASSED')
print('END-OF-FILE SENTINEL: TOTFR-META-CONTROL-VALIDATOR-2026-09-04-V1')
