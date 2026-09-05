#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]; VALIDATOR=ROOT/"tools"/"validate_totfr_guardrails.py"
def runv(r):
    e=os.environ.copy();e["TOTFR_ROOT"]=str(r);p=subprocess.run([sys.executable,str(VALIDATOR)],text=True,capture_output=True,env=e);return p.returncode,(p.stdout or "")+(p.stderr or "")
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
        if rc==0:raise AssertionError(f"{name}: accepted bad state")
        if needle not in o:raise AssertionError(f"{name}: expected {needle!r}\n{o}")
    finally:t.cleanup()
def repl(p,a,b):p.write_text(p.read_text(encoding="utf-8").replace(a,b),encoding="utf-8")
def header(r):
    with (r/"13 Source Prompts"/"TOTFR_Surface_Matrix.csv").open(newline="",encoding="utf-8") as f:return next(csv.reader(f))
def blob(p):
    b=p.read_bytes();return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def source(r,path="01 Branding/test.webp"):
    p=r/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b"TOTFR-test-source");return p
def shard(r,dictrows,eof=True):
    d=r/"13 Source Prompts"/"Surface Matrix";d.mkdir(parents=True,exist_ok=True);p=d/"99_Test.csv";h=header(r)
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(h)
        for vals in dictrows:w.writerow([vals.get(k,"") for k in h])
        if eof:w.writerow(["__EOF_CONTROL__"])
    return p
cases=[]
def add(n,m,s):cases.append((n,m,s))
add("missing SOP",lambda r:(r/"13 Source Prompts"/"TOTFR_App_Tool_Execution_Safety_SOP.md").unlink(),"missing controlled file")
def nosentinel(r):
    p=r/"13 Source Prompts"/"TOTFR_Art_Notion_Deployment_Guardrails.md";a=p.read_text(encoding="utf-8").rstrip("\n").splitlines();p.write_text("\n".join(a[:-1])+"\n",encoding="utf-8")
add("missing sentinel",nosentinel,"missing tail sentinel")
def oversop(r):
    p=r/"13 Source Prompts"/"TOTFR_Art_Notion_Deployment_Guardrails.md";a=p.read_text(encoding="utf-8").rstrip("\n").splitlines();p.write_text("\n".join(a[:-1])+"\n"+"X"*1200+"\n"+a[-1]+"\n",encoding="utf-8")
add("oversized SOP",oversop,"SOP target exceeds 8000 bytes")
add("README authority drift",lambda r:repl(r/"README.md","TOTFR_Surface_Matrix_Index.md","REMOVED"),"README.md")
add("legacy authority regression",lambda r:repl(r/"13 Source Prompts"/"TOTFR_Production_Manifest.md","SUPERSEDED FOR CURRENT REMASTER / DEPLOYMENT","LEGACY"),"legacy production manifest")
def badschema(r):
    p=r/"13 Source Prompts"/"TOTFR_Surface_Matrix.csv";rows=list(csv.reader(p.open(newline="",encoding="utf-8")));rows[0].remove("approved_binary_sha")
    with p.open("w",newline="",encoding="utf-8") as f:csv.writer(f).writerows(rows)
add("missing evidence column",badschema,"schema missing required columns")
def dupid(r):
    p=source(r);s=blob(p);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"source_sha":s},{"asset_id":"A","source_path":"01 Branding/other.webp"}]);(r/"01 Branding/other.webp").write_bytes(b"x")
add("duplicate id",dupid,"duplicate asset_id A")
def duppath(r):
    p=source(r);s=blob(p);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"source_sha":s},{"asset_id":"B","source_path":str(p.relative_to(r)),"source_sha":s}])
add("duplicate path",duppath,"duplicate source_path")
add("missing shard EOF",lambda r:(source(r),shard(r,[{"asset_id":"A","source_path":"01 Branding/test.webp"}],False)),"missing EOF control row")
def overshard(r):
    d=r/"13 Source Prompts"/"Surface Matrix";d.mkdir(parents=True,exist_ok=True);(d/"99_Test.csv").write_text("asset_id,source_path\n"+"X"*8100,encoding="utf-8")
add("oversized shard",overshard,"matrix shard exceeds 8000 bytes")
def badvocab(r):
    p=source(r);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"audit_a":"MAYBE"}])
add("invalid vocabulary",badvocab,"invalid audit_a")
def badsource(r):
    p=source(r);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"source_sha":"deadbeef"}])
add("source SHA drift",badsource,"source_sha mismatch")
def badapprovedsha(r):
    p=source(r);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"source_sha":blob(p),"approved_binary_sha":"deadbeef"}])
add("approved binary SHA drift",badapprovedsha,"approved_binary_sha mismatch")
def designwithoutqa(r):
    p=source(r);s=blob(p);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"source_sha":s,"approved_binary_sha":s,"design_evidence_ref":"evidence","design_state":"DESIGN APPROVED","audit_a":"PASS","audit_b":"PASS","audit_c":"PASS","technical_qa":"PASS","visual_qa":"FAIL","cross_surface_qa":"PASS"}])
add("design approval missing QA",designwithoutqa,"DESIGN APPROVED missing visual_qa=PASS")
def deploywithoutclean(r):
    p=source(r);s=blob(p);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"source_sha":s,"approved_binary_sha":s,"design_evidence_ref":"e","design_state":"DESIGN APPROVED","audit_a":"PASS","audit_b":"PASS","audit_c":"PASS","technical_qa":"PASS","visual_qa":"PASS","cross_surface_qa":"PASS","deployment_state":"DEPLOYMENT WRITTEN","cleanup_state":"CLEANUP REQUIRED"}])
add("deployment without clean baseline",deploywithoutclean,"without CLEAN BASELINE VERIFIED")
def deploywithoutevidence(r):
    p=source(r);s=blob(p);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"source_sha":s,"approved_binary_sha":s,"design_evidence_ref":"e","design_state":"DESIGN APPROVED","audit_a":"PASS","audit_b":"PASS","audit_c":"PASS","technical_qa":"PASS","visual_qa":"PASS","cross_surface_qa":"PASS","deployment_state":"DEPLOYMENT WRITTEN","cleanup_state":"CLEAN BASELINE VERIFIED"}])
add("deployment without rollback evidence",deploywithoutevidence,"DEPLOYMENT WRITTEN missing rollback_ref")
def visualwithoutstruct(r):
    p=source(r);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"visual_state":"VISUALLY APPROVED","visual_evidence_ref":"shot"}])
add("visual approval without structure",visualwithoutstruct,"VISUALLY APPROVED without STRUCTURALLY VERIFIED")
def visualwithoutevidence(r):
    p=source(r);shard(r,[{"asset_id":"A","source_path":str(p.relative_to(r)),"visual_state":"VISUALLY APPROVED","structural_state":"STRUCTURALLY VERIFIED","deployment_state":"DEPLOYMENT WRITTEN"}])
add("visual approval without evidence",visualwithoutevidence,"VISUALLY APPROVED missing visual_evidence_ref")
add("app branch-local SHA rule removed",lambda r:repl(r/"13 Source Prompts"/"TOTFR_App_Tool_Execution_Safety_SOP.md","exact target branch/ref","REMOVED_BRANCH_RULE"),"required control missing")
add("app circuit breaker removed",lambda r:repl(r/"13 Source Prompts"/"TOTFR_App_Tool_Execution_Safety_SOP.md","OPENS THE CIRCUIT","REMOVED_CIRCUIT"),"required control missing")
add("PR-first rule removed",lambda r:repl(r/"13 Source Prompts"/"TOTFR_GitHub_Upload_Safety_Plan.md","PR-first control plane","REMOVED_PR_FIRST"),"required control missing")
add("matrix evidence rule removed",lambda r:repl(r/"13 Source Prompts"/"TOTFR_Surface_Matrix_Index.md","Evidence-bound fields","REMOVED_EVIDENCE"),"required control missing")
add("workflow mutation tests removed",lambda r:repl(r/".github/workflows/validate-totfr-guardrails.yml","python tools/test_totfr_guardrails.py","echo removed"),"guardrail workflow missing required control")
add("workflow checkout unpinned",lambda r:repl(r/".github/workflows/validate-totfr-guardrails.yml","actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1","actions/checkout@v7"),"guardrail workflow missing required control")
add("workflow credentials persisted",lambda r:repl(r/".github/workflows/validate-totfr-guardrails.yml","persist-credentials: false","persist-credentials: true"),"guardrail workflow missing required control")
add("workflow write privilege",lambda r:repl(r/".github/workflows/validate-totfr-guardrails.yml","contents: read","contents: write"),"guardrail workflow missing required control")
def main():
    clean()
    for n,m,s in cases:reject(n,m,s);print("PASS reject:",n)
    clean();print(f"TOTFR MUTATION TESTS PASSED: rejected={len(cases)} clean_baselines=2");print("END-OF-FILE SENTINEL: TOTFR-GUARDRAIL-MUTATION-TESTS-2026-09-04-HARDENED-V5")
if __name__=="__main__":raise SystemExit(main())
