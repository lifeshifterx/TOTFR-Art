#!/usr/bin/env python3
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "13 Source Prompts"
MAX_SOP = 8000
MAX_DIRECT = 10000
MAX_SHARD = 8000

CONTROLLED = {
    ROOT / "README.md": "END-OF-FILE SENTINEL:",
    SRC / "TOTFR_Art_Notion_Deployment_Guardrails.md": "END-OF-FILE SENTINEL:",
    SRC / "TOTFR_App_Tool_Execution_Safety_SOP.md": "END-OF-FILE SENTINEL:",
    SRC / "TOTFR_Art_Generation_Remaster_QA_SOP.md": "END-OF-FILE SENTINEL:",
    SRC / "TOTFR_GitHub_Upload_Safety_Plan.md": "END-OF-FILE SENTINEL:",
    SRC / "TOTFR_Guardrail_Coverage_Matrix.md": "END-OF-FILE SENTINEL:",
    SRC / "TOTFR_Surface_Matrix_Index.md": "END-OF-FILE SENTINEL:",
    SRC / "TOTFR_Production_Manifest.md": "END-OF-FILE SENTINEL:",
}
SOP_TARGETS = {
    SRC / "TOTFR_Art_Notion_Deployment_Guardrails.md",
    SRC / "TOTFR_App_Tool_Execution_Safety_SOP.md",
    SRC / "TOTFR_Art_Generation_Remaster_QA_SOP.md",
    SRC / "TOTFR_GitHub_Upload_Safety_Plan.md",
    SRC / "TOTFR_Guardrail_Coverage_Matrix.md",
    SRC / "TOTFR_Surface_Matrix_Index.md",
}

errors = []

def fail(msg):
    errors.append(msg)

def check_text(path, sentinel):
    if not path.exists():
        fail(f"missing controlled file: {path.relative_to(ROOT)}")
        return
    raw = path.read_bytes()
    size = len(raw)
    if size > MAX_DIRECT:
        fail(f"controlled text exceeds {MAX_DIRECT} bytes: {path.relative_to(ROOT)} = {size}")
    if path in SOP_TARGETS and size > MAX_SOP:
        fail(f"SOP target exceeds {MAX_SOP} bytes: {path.relative_to(ROOT)} = {size}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        fail(f"not UTF-8: {path.relative_to(ROOT)}")
        return
    lines = text.rstrip("\n").splitlines()
    if not lines or not lines[-1].startswith(sentinel):
        fail(f"missing tail sentinel: {path.relative_to(ROOT)}")

for path, sentinel in CONTROLLED.items():
    check_text(path, sentinel)

readme = ROOT / "README.md"
if readme.exists():
    text = readme.read_text(encoding="utf-8")
    for required in [
        "TOTFR_Art_Notion_Deployment_Guardrails.md",
        "TOTFR_App_Tool_Execution_Safety_SOP.md",
        "TOTFR_Art_Generation_Remaster_QA_SOP.md",
        "TOTFR_GitHub_Upload_Safety_Plan.md",
        "TOTFR_Surface_Matrix.csv",
        "TOTFR_Surface_Matrix_Index.md",
    ]:
        if required not in text:
            fail(f"README missing authority reference: {required}")

legacy = SRC / "TOTFR_Production_Manifest.md"
if legacy.exists():
    txt = legacy.read_text(encoding="utf-8")
    if "SUPERSEDED FOR CURRENT REMASTER / DEPLOYMENT" not in txt:
        fail("legacy production manifest is not explicitly superseded")

schema_path = SRC / "TOTFR_Surface_Matrix.csv"
schema = None
if not schema_path.exists():
    fail("missing Surface Matrix schema")
else:
    if schema_path.stat().st_size > MAX_SHARD:
        fail("Surface Matrix schema exceeds 8000 bytes")
    try:
        with schema_path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        if len(rows) < 2:
            fail("Surface Matrix schema missing EOF control row")
        else:
            schema = rows[0]
            if not schema or schema[0] != "asset_id" or "source_path" not in schema:
                fail("Surface Matrix schema header is invalid")
            if rows[-1][0] != "__EOF_CONTROL__":
                fail("Surface Matrix schema missing EOF control at tail")
    except Exception as e:
        fail(f"Surface Matrix schema parse failure: {e}")

index_path = SRC / "TOTFR_Surface_Matrix_Index.md"
if index_path.exists():
    idx = index_path.read_text(encoding="utf-8")
    if "schema only" not in idx.lower() or "Surface Matrix/" not in idx:
        fail("Surface Matrix index does not enforce schema-only + shard routing")

seen_ids = {}
seen_paths = {}
shard_dir = SRC / "Surface Matrix"
if shard_dir.exists():
    for shard in sorted(shard_dir.glob("*.csv")):
        size = shard.stat().st_size
        if size > MAX_SHARD:
            fail(f"matrix shard exceeds {MAX_SHARD} bytes: {shard.name} = {size}")
            continue
        try:
            with shard.open(newline="", encoding="utf-8") as f:
                rows = list(csv.reader(f))
        except Exception as e:
            fail(f"CSV parse failure {shard.name}: {e}")
            continue
        if not rows:
            fail(f"empty shard prohibited: {shard.name}")
            continue
        if schema and rows[0] != schema:
            fail(f"schema mismatch: {shard.name}")
        if len(rows) < 2 or rows[-1][0] != "__EOF_CONTROL__":
            fail(f"missing EOF control row: {shard.name}")
        for i, row in enumerate(rows[1:-1], start=2):
            if schema and len(row) != len(schema):
                fail(f"column-count mismatch {shard.name}:{i} ({len(row)} != {len(schema)})")
                continue
            if not row:
                fail(f"blank row {shard.name}:{i}")
                continue
            aid = row[0].strip()
            spath = row[1].strip() if len(row) > 1 else ""
            if not aid or not spath:
                fail(f"asset_id/source_path required {shard.name}:{i}")
                continue
            if aid in seen_ids:
                fail(f"duplicate asset_id {aid}: {seen_ids[aid]} and {shard.name}:{i}")
            else:
                seen_ids[aid] = f"{shard.name}:{i}"
            if spath in seen_paths:
                fail(f"duplicate source_path {spath}: {seen_paths[spath]} and {shard.name}:{i}")
            else:
                seen_paths[spath] = f"{shard.name}:{i}"

spec_dir = SRC / "Art Specs"
if spec_dir.exists():
    for spec in spec_dir.glob("*.md"):
        check_text(spec, "END-OF-FILE SENTINEL:")
        if spec.stat().st_size > MAX_SOP:
            fail(f"art spec exceeds {MAX_SOP} bytes: {spec.name}")

if errors:
    print("TOTFR GUARDRAIL VALIDATION FAILED")
    for e in errors:
        print(f"- {e}")
    sys.exit(1)

print("TOTFR GUARDRAIL VALIDATION PASSED")
print(f"controlled_files={len(CONTROLLED)} matrix_shards={len(list(shard_dir.glob('*.csv'))) if shard_dir.exists() else 0} active_rows={len(seen_ids)}")
print("END-OF-FILE SENTINEL: TOTFR-GUARDRAIL-VALIDATOR-2026-09-04-HARDENED")
