#!/usr/bin/env python3
# generate_indexes.py – baut:
#  - in jedem Top-Level-Ordner eine index.html
#  - im Root: manifest.json (alle .txt) + index.html + .nojekyll

import os, json, html
from pathlib import Path
from datetime import datetime

ROOT = Path(".").resolve()
EXTS = [".txt"]  # nur Textdateien listen
IGNORES = {".git", ".github", ".gitignore", ".nojekyll", "generate_indexes.py"}

def top_level_folders():
    out = []
    for p in sorted(ROOT.iterdir()):
        if p.name in IGNORES: 
            continue
        if p.is_dir():
            out.append(p)
    return out

def list_txt(folder: Path):
    return sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in EXTS])

def write_folder_index(folder: Path):
    rel = folder.relative_to(ROOT)
    items = list_txt(folder)
    lis = []
    for f in items:
        label = html.escape(f.name)
        lis.append(f'<li><a href="./{f.name}" target="_blank">{label}</a></li>')
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    html_doc = f"""<!doctype html>
<html lang="de">
<meta charset="utf-8">
<title>Index – {html.escape(str(rel))}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; }}
  a.back {{ display:inline-block; margin-bottom: 1rem; }}
  ul {{ line-height: 1.6; }}
</style>
<a class="back" href="../index.html">← Zur Startseite</a>
<h1>{html.escape(str(rel))}</h1>
<p>Index für <code>{html.escape(str(rel))}</code> — erstellt am {now}</p>
<ul>
{''.join(lis) if lis else '<li><em>Noch keine .txt-Dateien.</em></li>'}
</ul>
</html>"""
    (folder / "index.html").write_text(html_doc, encoding="utf-8")
    print("Wrote:", folder / "index.html")

def write_manifest(folders):
    rows = []
    for fld in folders:
        for f in list_txt(fld):
            rel = f.relative_to(ROOT).as_posix()
            rows.append({
                "category": fld.name,     # z.B. a_Offiziell / b_Pro / c_Contra / d_Gemischt
                "filename": f.name,
                "path": rel               # z.B. c_Contra/c_2025-07-14_...
            })
    rows.sort(key=lambda r: (r["category"], r["filename"]))
    out = ROOT / "manifest.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote:", out)

def write_root_index(folders):
    lis = []
    for fld in folders:
        name = html.escape(fld.name)
        lis.append(f'<li><a href="./{name}/index.html">{name}</a></li>')
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    html_doc = f"""<!doctype html>
<html lang="de">
<meta charset="utf-8">
<title>CH–EU Dokumente</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 980px; margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ margin: 0 0 .5rem; }}
  ul {{ line-height: 1.6; }}
  footer {{ color:#666; font-size:.9rem; margin-top:1rem; }}
  code {{ background:#f3f3f3; padding:2px 4px; border-radius:4px; }}
</style>
<h1>CH–EU Dokumente</h1>
<p>Startseite (erstellt am {now}). Kategorien:</p>
<ul>
{''.join(lis) if lis else '<li><em>Keine Unterordner gefunden.</em></li>'}
</ul>
<p>Maschinenlese-Index: <a href="./manifest.json" target="_blank"><code>manifest.json</code></a></p>
<footer>Hinweis: Neue .txt-Dateien hochladen, dann dieses Skript erneut ausführen und committen.</footer>
</html>"""
    (ROOT / "index.html").write_text(html_doc, encoding="utf-8")
    print("Wrote:", ROOT / "index.html")

def main():
    folders = top_level_folders()
    for fld in folders:
        write_folder_index(fld)
    # Root-Dateien:
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("Wrote:", ROOT / ".nojekyll")
    write_manifest(folders)
    write_root_index(folders)
    print("Done.")

if __name__ == "__main__":
    main()
