import os
import sys
from pathlib import Path

try:
    import markdown
except Exception:
    print("ERROR: package 'markdown' not found. Please run: pip install markdown")
    sys.exit(1)

BASE = Path(__file__).resolve().parents[1]
MANUAL = BASE / 'manual'
OUT = MANUAL / 'html'

TEMPLATE = '''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <style>
    body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:900px;margin:28px auto;padding:0 18px;color:#222}}
    header{{border-bottom:1px solid #eee;padding-bottom:12px;margin-bottom:20px}}
    pre{{background:#f6f8fa;padding:12px;border-radius:6px;overflow:auto}}
    code{{background:#f6f8fa;padding:2px 4px;border-radius:4px}}
    table{{border-collapse:collapse;width:100%}}
    table,th,td{{border:1px solid #ddd;padding:8px}}
    a.button{{display:inline-block;margin-top:10px;padding:8px 10px;background:#0b5ed7;color:#fff;border-radius:6px;text-decoration:none}}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p><a class="button" href="../index.html">Volver al índice</a></p>
  </header>

  <main>
  {content}
  </main>

  <footer style="margin-top:28px;color:#666">Generado automáticamente desde Markdown</footer>
</body>
</html>'''


def convert(md_path: Path, out_path: Path):
    text = md_path.read_text(encoding='utf-8')
    html = markdown.markdown(text, extensions=['fenced_code', 'tables', 'toc', 'nl2br'])
    title = md_path.stem.replace('_', ' ').title()
    out_path.write_text(TEMPLATE.format(title=title, content=html), encoding='utf-8')


def main():
    if not MANUAL.exists():
        print('manual/ directory not found')
        sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    md_files = list(MANUAL.glob('*.md'))
    if not md_files:
        print('No .md files found in manual/')
        return
    for md in md_files:
        out = OUT / (md.stem + '.html')
        print(f'Converting {md.name} -> {out.relative_to(BASE)}')
        convert(md, out)

    print('Done. Generated HTML files in', OUT)


if __name__ == '__main__':
    main()
