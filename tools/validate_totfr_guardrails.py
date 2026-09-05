#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, os, sys

ROOT=Path(os.environ.get("TOTFR_ROOT",Path(__file__).resolve().parents[1])).resolve()
SRC=ROOT/"13 Source Prompts"; MAX_SOP=8000; MAX_DIRECT=10000; MAX_SHARD=8000
CONTROLLED={
 ROOT/"README.md":"END-OF-FILE SENTINEL:",
 SRC/"TOTFR_Art_Notion_Deployment_Guardrails.md":"END-OF-FILE SENTINEL:",
 SRC/"TOTFR_App_Tool_Execution_Safety_SOP.md":"END-OF-FILE SENTINEL:",
 SRC/"TOTFR_Art_Generation_Remaster_QA_SOP.md":"END-OF-FILE SENTINEL:",
 SRC/"TOTFR_GitHub_Upload_Safety_Plan.md":"END-OF-FILE SENTINEL:",
 SRC/"TOTFR_Guardrail_Coverage_Matrix.md":"END-OF-FILE SENTINEL:",
 SRC/"TOTFR_Surface_Matrix_Index.md":"END-OF-FILE SENTINEL:",
 SRC/"TOTFR_Production_Manifest.md":"END-OF-FILE SENTINEL:",
}
SOP_TARGETS=set(CONTROLLED)-{ROOT/"README.md",SRC/"TOTFR_Production_Manifest.md"}
errors=[]
def fail(x): errors.append(x)
def check_text(p,s):
    if not p.exists(): fail(f"missing controlled file: {p.relative_to(ROOT)}"); return
    raw=p.read_bytes(); n=len(raw)
    if n>MAX_DIRECT: fail(f"controlled text exceeds {MAX_DIRECT} bytes: {p.relative_to(ROOT)} = {n}")
    if p in SOP_TARGETS and n>MAX_SOP: fail(f"SOP target exceeds {MAX_SOP} bytes: {p.relative_to(ROOT)} = {n}")
    try:t=raw.decode("utf-8")
    except UnicodeDecodeError: fail(f"not UTF-8: {p.relative_to(ROOT)}"); return
    if not t.rstrip("\n").splitlines()[-1].startswith(s): fail(f"missing tail sentinel: {p.relative_to(ROOT)}")
for p,s in CONTROLLED.items(): check_text(p,s)

def require_text(p,tokens):
    if not p.exists(): return
    try:t=p.read_text(encoding="utf-8")
    except UnicodeDecodeError:return
    for x in tokens:
        if x not in t: fail(f"required control missing in {p.relative_to(ROOT)}: {x}")

readme=ROOT/"README.md"
require_text(readme,["TOTFR_Art_Notion_Deployment_Guardrails.md","TOTFR_App_Tool_Execution_Safety_SOP.md","TOTFR_Art_Generation_Remaster_QA_SOP.md","TOTFR_GitHub_Upload_Safety_Plan.md","TOTFR_Surface_Matrix.csv","TOTFR_Surface_Matrix_Index.md"])
legacy=SRC/"TOTFR_Production_Manifest.md"
if legacy.exists() and "SUPERSEDED FOR CURRENT REMASTER / DEPLOYMENT" not in legacy.read_text(encoding="utf-8"): fail("legacy production manifest is not explicitly superseded")
require_text(SRC/"TOTFR_Art_Notion_Deployment_Guardrails.md",["CLEAN BASELINE VERIFIED","VISUALLY APPROVED"])
require_text(SRC/"TOTFR_App_Tool_Execution_Safety_SOP.md",["A write/update endpoint must never be used as a substitute for a read/inspection endpoint.","exact target branch/ref","OPENS THE CIRCUIT","GLOBAL MUTATION FREEZE","EXACT LIBRARY VERIFICATION"])
require_text(SRC/"TOTFR_Art_Generation_Remaster_QA_SOP.md",["TOTFR_Surface_Matrix.csv","TOTFR_Surface_Matrix_Index.md","DESIGN APPROVED","Editing a specific existing image requires usable source pixels"])
require_text(SRC/"TOTFR_GitHub_Upload_Safety_Plan.md",["PR-first control plane","CURRENT-HEAD CI FALLBACK","another branch/ref","tools/test_totfr_guardrails.py"])
require_text(SRC/"TOTFR_Surface_Matrix_Index.md",["Evidence-bound fields","State-transition invariants","Circuit breaker / reset","approved_binary_sha"])

workflow=ROOT/".github/workflows/validate-totfr-guardrails.yml"
if not workflow.exists(): fail("missing guardrail validation workflow")
else:
    w=workflow.read_text(encoding="utf-8")
    for x in ["actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1","actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97","permissions:","contents: read","persist-credentials: false","timeout-minutes: 5","python tools/validate_totfr_guardrails.py","python tools/test_totfr_guardrails.py"]:
        if x not in w: fail(f"guardrail workflow missing required control: {x}")

schema_path=SRC/"TOTFR_Surface_Matrix.csv"; schema=None
required_cols={"asset_id","source_path","operation","audit_a","audit_b","audit_c","technical_qa","visual_qa","cross_surface_qa","design_state","remaster_path","cleanup_state","deployment_state","structural_state","visual_state","source_sha","approved_binary_sha","design_evidence_ref","rollback_ref","cleanup_evidence_ref","deployment_evidence_ref","visual_evidence_ref","failure_count","circuit_state"}
if not schema_path.exists(): fail("missing Surface Matrix schema")
else:
    if schema_path.stat().st_size>MAX_SHARD: fail("Surface Matrix schema exceeds 8000 bytes")
    try:
        rows=list(csv.reader(schema_path.open(newline="",encoding="utf-8"))); schema=rows[0] if rows else []
        if len(rows)<2 or rows[-1][0]!="__EOF_CONTROL__": fail("Surface Matrix schema missing EOF control at tail")
        missing=required_cols-set(schema)
        if missing: fail("Surface Matrix schema missing required columns: "+",".join(sorted(missing)))
    except Exception as e: fail(f"Surface Matrix schema parse failure: {e}")

def blob_sha(p):
    b=p.read_bytes(); return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
ALLOWED={
 "audit_a":{"PASS","FAIL","UNKNOWN"},"audit_b":{"PASS","FAIL","UNKNOWN"},"audit_c":{"PASS","FAIL","UNKNOWN"},
 "technical_qa":{"PASS","FAIL","NOT RUN"},"visual_qa":{"PASS","FAIL","NOT RUN"},"cross_surface_qa":{"PASS","FAIL","NOT RUN"},
 "design_state":{"UNVALIDATED","DESIGN APPROVED","DESIGN REJECTED","DM HOLD","NEEDS REVIEW"},
 "cleanup_state":{"NOT STARTED","CLEANUP REQUIRED","CLEAN BASELINE VERIFIED","NOT APPLICABLE"},
 "deployment_state":{"NOT DEPLOYED","DEPLOYMENT WRITTEN","DM HOLD","NO DESTINATION","BROKEN/MISSING"},
 "structural_state":{"NOT VALIDATED","STRUCTURALLY VERIFIED","STRUCTURAL FAILURE"},
 "visual_state":{"NOT VALIDATED","VISUAL QA REQUIRED","VISUALLY APPROVED","VISUAL FAILURE"},
 "circuit_state":{"CLOSED","OPEN"},
}
def vrow(d,where):
    for k,vals in ALLOWED.items():
        v=d.get(k,"").strip()
        if v and v not in vals: fail(f"invalid {k} {where}: {v}")
    fc=d.get("failure_count","").strip()
    if fc:
        try:
            if int(fc)<0: raise ValueError
        except ValueError: fail(f"invalid failure_count {where}: {fc}")
    sp=d.get("source_path","").strip(); source=ROOT/sp if sp else None
    if source and not source.exists(): fail(f"source_path missing {where}: {sp}")
    ss=d.get("source_sha","").strip()
    if source and ss and blob_sha(source)!=ss: fail(f"source_sha mismatch {where}")
    rp=d.get("remaster_path","").strip(); approved=ROOT/rp if rp else source
    aps=d.get("approved_binary_sha","").strip()
    if approved and aps:
        if not approved.exists(): fail(f"approved binary missing {where}: {rp or sp}")
        elif blob_sha(approved)!=aps: fail(f"approved_binary_sha mismatch {where}")
    if d.get("design_state")=="DESIGN APPROVED":
        for k in ["audit_a","audit_b","audit_c","technical_qa","visual_qa","cross_surface_qa"]:
            if d.get(k)!="PASS": fail(f"DESIGN APPROVED missing {k}=PASS {where}")
        for k in ["source_sha","approved_binary_sha","design_evidence_ref"]:
            if not d.get(k,"").strip(): fail(f"DESIGN APPROVED missing {k} {where}")
    if d.get("deployment_state")=="DEPLOYMENT WRITTEN":
        if d.get("design_state")!="DESIGN APPROVED": fail(f"DEPLOYMENT WRITTEN without DESIGN APPROVED {where}")
        if d.get("cleanup_state")!="CLEAN BASELINE VERIFIED": fail(f"DEPLOYMENT WRITTEN without CLEAN BASELINE VERIFIED {where}")
        for k in ["rollback_ref","cleanup_evidence_ref","deployment_evidence_ref"]:
            if not d.get(k,"").strip(): fail(f"DEPLOYMENT WRITTEN missing {k} {where}")
    if d.get("structural_state")=="STRUCTURALLY VERIFIED" and d.get("deployment_state")!="DEPLOYMENT WRITTEN":
        fail(f"STRUCTURALLY VERIFIED without DEPLOYMENT WRITTEN {where}")
    if d.get("visual_state")=="VISUALLY APPROVED":
        if d.get("structural_state")!="STRUCTURALLY VERIFIED": fail(f"VISUALLY APPROVED without STRUCTURALLY VERIFIED {where}")
        if not d.get("visual_evidence_ref","").strip(): fail(f"VISUALLY APPROVED missing visual_evidence_ref {where}")

seen_ids={}; seen_paths={}; shard_dir=SRC/"Surface Matrix"
if shard_dir.exists():
    for shard in sorted(shard_dir.glob("*.csv")):
        if shard.stat().st_size>MAX_SHARD: fail(f"matrix shard exceeds {MAX_SHARD} bytes: {shard.name} = {shard.stat().st_size}"); continue
        try: rows=list(csv.reader(shard.open(newline="",encoding="utf-8")))
        except Exception as e: fail(f"CSV parse failure {shard.name}: {e}"); continue
        if not rows: fail(f"empty shard prohibited: {shard.name}"); continue
        if schema and rows[0]!=schema: fail(f"schema mismatch: {shard.name}")
        if len(rows)<2 or rows[-1][0]!="__EOF_CONTROL__": fail(f"missing EOF control row: {shard.name}")
        for i,row in enumerate(rows[1:-1],2):
            if schema and len(row)!=len(schema): fail(f"column-count mismatch {shard.name}:{i}"); continue
            d=dict(zip(schema,row)); aid=d.get("asset_id","").strip(); sp=d.get("source_path","").strip()
            if not aid or not sp: fail(f"asset_id/source_path required {shard.name}:{i}"); continue
            if aid in seen_ids: fail(f"duplicate asset_id {aid}: {seen_ids[aid]} and {shard.name}:{i}")
            else: seen_ids[aid]=f"{shard.name}:{i}"
            if sp in seen_paths: fail(f"duplicate source_path {sp}: {seen_paths[sp]} and {shard.name}:{i}")
            else: seen_paths[sp]=f"{shard.name}:{i}"
            vrow(d,f"{shard.name}:{i}")

spec_dir=SRC/"Art Specs"
if spec_dir.exists():
    for spec in spec_dir.glob("*.md"): check_text(spec,"END-OF-FILE SENTINEL:")

if errors:
    print("TOTFR GUARDRAIL VALIDATION FAILED")
    for e in errors: print("- "+e)
    sys.exit(1)
print("TOTFR GUARDRAIL VALIDATION PASSED")
print(f"controlled_files={len(CONTROLLED)} matrix_shards={len(list(shard_dir.glob('*.csv'))) if shard_dir.exists() else 0} active_rows={len(seen_ids)}")
print("END-OF-FILE SENTINEL: TOTFR-GUARDRAIL-VALIDATOR-2026-09-04-HARDENED-V8")
