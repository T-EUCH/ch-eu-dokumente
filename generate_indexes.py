#!/usr/bin/env python3
# generate_indexes.py – erweitert für 02_Bereinigt_PY & 04_Frontend_PDF
# - durchsucht rekursiv alle .txt-Dateien (auch in Unterordnern)
# - ignoriert PDFs, JSONs usw.
# - baut manifest.json & Indexseiten

import os, json, html
from pathlib import Path
from datetime import datetime

ROOT = Path(".").resolve()

IGNORES = {
    ".git", ".github", ".gitignore", ".nojekyll", "generate_indexes.py"
}

# welche Dateiendungen sollen aufgenommen werden
VALID_EXTS = {".txt"}

def is_valid_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in VALID_EXTS

def iter_all_txt(root: Path):
    for p in root.rglob("*"):
        if any(part in IGNORES for part in p.parts):
            continue
        if is_valid_file(p):
            yield p

def write_manifest():
    rows = []
    for p in iter_all_txt(ROOT):
        rel = p.relative_to(ROOT).as_posix()
        parts = rel.split("/")
        # Kategorie ist zweite Ebene, wenn z.B. 02_Bereinigt_PY/a_Offiziell
        if len(parts) > 1 and parts[0].startswith("0"):
            category = parts[1]
        else:
            category = parts[0] if parts else ""
        rows.append({
            "category": category,
            "source_folder": parts[0] if parts else "",
            "filename": p.name,
            "path": rel
        })
    rows.sort(key=lambda r: (r["source_folder"], r["category"], r["path"]))
    out = ROOT / "manifest.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} entries to manifest.json")

def write_root_index():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    html_doc = f"""<!doctype html>
<html lang="de">
<meta charset="utf-8">
<title>CH–EU Dokumente</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 980px; margin: 2rem auto; padding: 0 1rem; }}
  ul {{ line-height: 1.6; }}
  footer {{ color:#666; font-size:.9rem; margin-top:1rem; font-size:0.9rem; }}
</style>
<h1>CH–EU Dokumente</h1>
<p>Manifest neu erstellt am {now}.</p>
<p><a href="./manifest.json" target="_blank">→ manifest.json anzeigen</a></p>
<footer>Ordnerstruktur bleibt vollständig (01–04).</footer>
</html>"""
    (ROOT / "index.html").write_text(html_doc, encoding="utf-8")
    print("Wrote index.html")

def main():
    # Root-Dateien erzeugen
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    write_manifest()
    write_root_index()
    print("Done.")

if __name__ == "__main__":
    main()
