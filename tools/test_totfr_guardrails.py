#!/usr/bin/env python3
from pathlib import Path
import csv
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_totfr_guardrails.py"

def run_validator(root):
    env = os.environ.copy()
    env["TOTFR_ROOT"] = str(root)
    p = subprocess.run([sys.executable, str(VALIDATOR)], text=True, capture_output=True, env=env)
    return p.returncode, (p.stdout or "") + (p.stderr or "")

def clone_tree():
    td = tempfile.TemporaryDirectory()
    dst = Path(td.name) / "repo"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return td, dst

def expect_clean(name="clean baseline"):
    td, dst = clone_tree()
    try:
        rc, out = run_validator(dst)
        if rc != 0:
            raise AssertionError(f"{name} unexpectedly failed:\n{out}")
    finally:
        td.cleanup()

def expect_reject(name, mutate, needle):
    td, dst = clone_tree()
    try:
        mutate(dst)
        rc, out = run_validator(dst)
        if rc == 0:
            raise AssertionError(f"{name}: validator incorrectly accepted bad state")
        if needle not in out:
            raise AssertionError(f"{name}: failed for wrong reason; expected {needle!r}\n{out}")
    finally:
        td.cleanup()

def schema_header(root):
    with (root / "13 Source Prompts" / "TOTFR_Surface_Matrix.csv").open(newline="", encoding="utf-8") as f:
        return next(csv.reader(f))

def write_shard(root, rows, eof=True):
    d = root / "13 Source Prompts" / "Surface Matrix"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "99_Test.csv"
    header = schema_header(root)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header)
        for aid, spath in rows:
            row = [""] * len(header); row[0] = aid; row[1] = spath; w.writerow(row)
        if eof: w.writerow(["__EOF_CONTROL__"])
    return p

cases=[]
def add(name, mutate, needle): cases.append((name, mutate, needle))

add("missing controlled SOP", lambda r:(r/"13 Source Prompts"/"TOTFR_App_Tool_Execution_Safety_SOP.md").unlink(), "missing controlled file")

def missing_sentinel(r):
    p=r/"13 Source Prompts"/"TOTFR_Art_Notion_Deployment_Guardrails.md"; lines=p.read_text(encoding="utf-8").rstrip("\n").splitlines(); p.write_text("\n".join(lines[:-1])+"\n",encoding="utf-8")
add("missing tail sentinel", missing_sentinel, "missing tail sentinel")

def oversize_sop(r):
    p=r/"13 Source Prompts"/"TOTFR_Art_Notion_Deployment_Guardrails.md"; txt=p.read_text(encoding="utf-8"); lines=txt.rstrip("\n").splitlines(); p.write_text("\n".join(lines[:-1])+"\n"+("X"*1000)+"\n"+lines[-1]+"\n",encoding="utf-8")
add("oversized SOP", oversize_sop, "SOP target exceeds 8000 bytes")

def readme_drift(r):
    p=r/"README.md"; p.write_text(p.read_text(encoding="utf-8").replace("TOTFR_Surface_Matrix_Index.md","REMOVED_INDEX_REF"),encoding="utf-8")
add("README authority drift", readme_drift, "README missing authority reference")

def legacy_regression(r):
    p=r/"13 Source Prompts"/"TOTFR_Production_Manifest.md"; p.write_text(p.read_text(encoding="utf-8").replace("SUPERSEDED FOR CURRENT REMASTER / DEPLOYMENT","LEGACY"),encoding="utf-8")
add("legacy authority regression", legacy_regression, "legacy production manifest is not explicitly superseded")

def bad_schema(r):
    p=r/"13 Source Prompts"/"TOTFR_Surface_Matrix.csv"; rows=list(csv.reader(p.open(newline="",encoding="utf-8"))); rows[0][0]="asset_idx"; f=p.open("w",newline="",encoding="utf-8"); csv.writer(f).writerows(rows); f.close()
add("invalid matrix schema", bad_schema, "Surface Matrix schema header is invalid")
add("duplicate asset id", lambda r:write_shard(r,[("ASSET-1","01 Branding/a.webp"),("ASSET-1","01 Branding/b.webp")]), "duplicate asset_id ASSET-1")
add("duplicate source path", lambda r:write_shard(r,[("ASSET-1","01 Branding/a.webp"),("ASSET-2","01 Branding/a.webp")]), "duplicate source_path 01 Branding/a.webp")
add("missing shard EOF", lambda r:write_shard(r,[("ASSET-1","01 Branding/a.webp")],False), "missing EOF control row")

def oversized_shard(r):
    d=r/"13 Source Prompts"/"Surface Matrix"; d.mkdir(parents=True,exist_ok=True); (d/"99_Test.csv").write_text("asset_id,source_path\n"+("X"*8100),encoding="utf-8")
add("oversized shard", oversized_shard, "matrix shard exceeds 8000 bytes")

def empty_shard(r):
    d=r/"13 Source Prompts"/"Surface Matrix"; d.mkdir(parents=True,exist_ok=True); (d/"99_Test.csv").write_text("",encoding="utf-8")
add("empty shard", empty_shard, "empty shard prohibited")

def malformed_columns(r):
    d=r/"13 Source Prompts"/"Surface Matrix"; d.mkdir(parents=True,exist_ok=True); p=d/"99_Test.csv"; h=schema_header(r); f=p.open("w",newline="",encoding="utf-8"); w=csv.writer(f); w.writerow(h); w.writerow(["ASSET-1","01 Branding/a.webp","EXTRA"]); w.writerow(["__EOF_CONTROL__"]); f.close()
add("shard column mismatch", malformed_columns, "column-count mismatch")

def bad_art_spec(r):
    d=r/"13 Source Prompts"/"Art Specs"; d.mkdir(parents=True,exist_ok=True); (d/"bad.md").write_text("# bad\n"+("X"*8100)+"\nEND-OF-FILE SENTINEL: TEST\n",encoding="utf-8")
add("oversized art spec", bad_art_spec, "art spec exceeds 8000 bytes")
add("non UTF-8 controlled file", lambda r:(r/"13 Source Prompts"/"TOTFR_Guardrail_Coverage_Matrix.md").write_bytes(b"\xff\xfe\xfd"), "not UTF-8")

def main():
    expect_clean("initial clean baseline")
    for name,mutate,needle in cases:
        expect_reject(name,mutate,needle); print(f"PASS reject: {name}")
    expect_clean("final clean baseline")
    print(f"TOTFR MUTATION TESTS PASSED: rejected={len(cases)} clean_baselines=2")
    print("END-OF-FILE SENTINEL: TOTFR-GUARDRAIL-MUTATION-TESTS-2026-09-04-HARDENED")
    return 0

if __name__=="__main__": raise SystemExit(main())
