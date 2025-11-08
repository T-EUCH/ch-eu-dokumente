#!/usr/bin/env python3
# generate_indexes.py
# Erzeugt in jedem Ordner eine einfache index.html, die alle .txt-Dateien verlinkt.
# Leg diese Datei ins Root deines GitHub-Repo (z. B. ch-eu-dokumente) und führe sie aus.

import os
from pathlib import Path
from datetime import datetime
import html

ROOT = Path('.').resolve()  # Repo-Root, dort wo du das Script speicherst
EXTS = ['.txt', '.md']      # Dateitypen, die verlinkt werden sollen
IGNORES = {'.git', '.github', '.gitignore', '.nojekyll', 'generate_indexes.py'}

TEMPLATE_ROOT = """<!doctype html>
<html lang="de">
<meta charset="utf-8">
<title>CH-EU Dokumente — Index</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 980px; margin: 2rem auto; padding: 0 1rem; color: #111; }}
  h1 {{ margin-bottom: 0.25rem; }}
  .meta {{ color: #666; font-size: 0.95rem; margin-bottom: 1rem; }}
  ul {{ line-height: 1.6; }}
  .folder {{ margin-top: 1.2rem; border-top: 1px solid #eee; padding-top: 0.8rem; }}
  a.file {{ display:inline-block; padding: 2px 4px; }}
  footer {{ margin-top: 2rem; color:#666; font-size:0.9rem; }}
</style>
<h1>CH-EU Dokumente</h1>
<p class="meta">Index erstellt am {now}. Klicke eine Kategorie oder Datei an.</p>
<ul>
{folders}
</ul>
<footer>Auto-generated index — lege neue .txt in die Unterordner und führe das Script erneut aus.</footer>
</html>
"""

TEMPLATE_FOLDER = """<li class="folder">
  <strong>{folder_name}/</strong>
  <ul>
    {files}
  </ul>
</li>"""

TEMPLATE_FILE = '<li><a class="file" href="{href}" target="_blank">{label}</a></li>'

TEMPLATE_INDEX = """<!doctype html>
<html lang="de">
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; color: #111; }}
  h1 {{ margin-bottom: 0.25rem; }}
  .meta {{ color: #666; font-size: 0.95rem; margin-bottom: 1rem; }}
  ul {{ line-height: 1.6; }}
  .back {{ margin-bottom: 1rem; display:block; }}
  footer {{ margin-top: 2rem; color:#666; font-size:0.9rem; }}
</style>
<a class="back" href="{root_link}">← Zur Startseite</a>
<h1>{title}</h1>
<p class="meta">Index für <code>{relpath}</code> — erstellt am {now}.</p>
<ul>
{files}
</ul>
<footer>Auto-generated index — erneuern: führen Sie <code>generate_indexes.py</code> im Repo-Root aus.</footer>
</html>
"""

def safe_label(p: Path) -> str:
    return html.escape(p.name)

def make_index_for_folder(folder: Path, root_link: str = "../") -> None:
    rel = folder.relative_to(ROOT)
    files_html = []
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix.lower() in EXTS:
            href = os.path.join('.', p.name)  # relative
            files_html.append(TEMPLATE_FILE.format(href=href, label=safe_label(p)))
    title = f"Dokumente in {rel}" if str(rel) != '.' else "CH-EU Dokumente – Start"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    content = TEMPLATE_INDEX.format(title=html.escape(title),
                                    relpath=str(rel),
                                    now=now,
                                    files="\n".join(files_html),
                                    root_link=root_link)
    idx_path = folder / "index.html"
    idx_path.write_text(content, encoding="utf-8")
    print("Wrote:", idx_path)

def make_root_index(all_folders):
    # build folders list
    folders_html = []
    for fld in all_folders:
        name = fld.name
        link = f"./{name}/index.html"
        # count files
        cnt = sum(1 for p in fld.iterdir() if p.is_file() and p.suffix.lower() in EXTS)
        label = f'{html.escape(name)}/ ({cnt} Dateien)'
        folders_html.append(f'<li><a href="{link}">{label}</a></li>')
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    content = TEMPLATE_ROOT.format(now=now, folders="\n".join(folders_html))
    (ROOT / "index.html").write_text(content, encoding="utf-8")
    print("Wrote root index:", ROOT / "index.html")

def collect_top_level_folders():
    candidates = []
    for p in sorted(ROOT.iterdir()):
        if p.name in IGNORES:
            continue
        if p.is_dir():
            # only include folders that contain at least one .txt (or md)
            has = any((f.suffix.lower() in EXTS) for f in p.iterdir() if f.is_file())
            # also include empty folders (you might want them visible)
            candidates.append(p)
    return candidates

def main():
    folders = collect_top_level_folders()
    # For each top-level folder, create index.html inside it
    for fld in folders:
        # Create index listing files using relative root link
        make_index_for_folder(fld, root_link="../index.html")
    # Root index
    make_root_index(folders)
    # .nojekyll to avoid Jekyll processing
    nj = ROOT / ".nojekyll"
    if not nj.exists():
        nj.write_text("", encoding="utf-8")
        print("Wrote .nojekyll")
    print("Done. Commit and push the generated index.html files (and .nojekyll) to enable GitHub Pages.")

if __name__ == "__main__":
    main()
