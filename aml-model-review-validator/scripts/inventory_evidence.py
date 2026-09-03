#!/usr/bin/env python3
from pathlib import Path
import sys, json

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
exts = {".docx",".pdf",".pptx",".xlsx",".xls",".csv",".parquet",".py",".sql",".r",".scala",".ipynb",".json",".yaml",".yml",".xml",".ini",".md"}
rows = []
for p in sorted(root.rglob("*")):
    if p.is_file() and p.suffix.lower() in exts:
        rows.append({
            "path": str(p),
            "extension": p.suffix.lower(),
            "size_bytes": p.stat().st_size
        })
print(json.dumps(rows, indent=2))
