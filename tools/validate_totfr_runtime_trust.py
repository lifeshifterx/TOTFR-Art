#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'13 Source Prompts';ERR=[]
def fail(x):ERR.append(x)
def load(p,label):
 if not p.exists():fail(f'missing {label}: {p.relative_to(ROOT)}');return None
 try:return json.loads(p.read_text(encoding='utf-8'))
 except Exception as e:fail(f'{label} parse failure: {e}');return None
trust=load(SRC/'TOTFR_Agent_Trust_Boundary.json','agent trust boundary') or {}
evp=load(SRC/'TOTFR_Runtime_Evidence_Policy.json','runtime evidence policy') or {}
if trust:
 if trust.get('verification_doctrine')!='VERIFY_THEN_TRUST_EXACT_STATE':fail('trust boundary doctrine mismatch')
 if trust.get('self_declared_instance_ids_are_security_identity') is not False:fail('self-declared instance IDs cannot be security identity')
 if trust.get('human_file_attestation_is_security_identity') is not False:fail('file attestation cannot be human security identity')
 if trust.get('agent_identity_enforcement_state')=='UNCONFIGURED' and trust.get('tier2_agent_execution_allowed_when_identity_unconfigured') is not False:fail('Tier-2 must be blocked while identity enforcement is unconfigured')
if evp:
 if evp.get('verification_doctrine')!='VERIFY_THEN_TRUST_EXACT_STATE':fail('evidence policy doctrine mismatch')
 if evp.get('visual_artifact_required') is not True or evp.get('visual_artifact_ref_must_be_durable') is not True:fail('durable visual artifact requirement missing')
 if evp.get('ephemeral_signed_url_allowed') is not False:fail('ephemeral signed URLs must be prohibited as evidence')
ag=(ROOT/'AGENTS.md').read_text(encoding='utf-8') if (ROOT/'AGENTS.md').exists() else ''
for token in ['VERIFY THEN TRUST','Self-declared instance IDs are not security identities']:
 if token not in ag:fail(f'AGENTS.md missing verification/trust control: {token}')
SIGNED=re.compile(r'(?:X-Amz-|Signature=|token=|Authorization:|oauth)',re.I);HEX64=re.compile(r'^[0-9a-f]{64}$')
req=set(evp.get('required_visual_fields',[]));player=tuple(evp.get('player_safe_artifact_ref_prefixes',[]));dm=tuple(evp.get('dm_artifact_ref_prefixes',[]))
runs=SRC/'Deployment Runs'
if runs.exists():
 for d in runs.iterdir():
  if not d.is_dir() or not (d/'run.json').exists():continue
  state=load(d/'state.json',f'state {d.name}');run=load(d/'run.json',f'run {d.name}')
  if not state or not run:continue
  tier2=False
  for ent in run.get('plan_shards',[]):
   p=ROOT/str(ent.get('path',''))
   if not p.exists():continue
   for line in p.read_text(encoding='utf-8').splitlines():
    try:o=json.loads(line)
    except Exception:continue
    if o.get('type')=='EOF_CONTROL':continue
    if o.get('risk_tier')==2:tier2=True
  if tier2 and trust.get('agent_identity_enforcement_state')=='UNCONFIGURED' and state.get('phase') not in {'PLANNED','BLOCKED'}:
   fail(f'Tier-2 agent run advanced while identity enforcement is UNCONFIGURED: {d.name}')
  vdir=d/'visual'
  if vdir.exists():
   for p in vdir.glob('*.json'):
    v=load(p,f'visual {p.name}')
    if not v:continue
    missing=[k for k in req if k not in v or v.get(k) in {'',None}]
    if missing:fail(f'visual evidence missing fields {p.name}: {sorted(missing)}');continue
    ref=str(v.get('artifact_ref',''))
    if SIGNED.search(ref):fail(f'signed/secret visual artifact ref persisted: {p.name}')
    if not HEX64.match(str(v.get('artifact_sha256',''))):fail(f'invalid visual artifact SHA-256: {p.name}')
    privacy=v.get('privacy')
    if privacy=='DM_HOLD':
     if not ref.startswith(dm):fail(f'DM visual evidence is not in private durable storage: {p.name}')
    elif privacy=='PLAYER_SAFE':
     if not ref.startswith(player):fail(f'PLAYER_SAFE visual evidence has unsupported durable ref: {p.name}')
    else:fail(f'invalid visual evidence privacy: {p.name}')
if ERR:
 print('TOTFR RUNTIME TRUST VALIDATION FAILED')
 for e in ERR:print('- '+e)
 sys.exit(1)
print('TOTFR RUNTIME TRUST VALIDATION PASSED')
print('END-OF-FILE SENTINEL: TOTFR-RUNTIME-TRUST-VALIDATOR-2026-09-04-V1')
