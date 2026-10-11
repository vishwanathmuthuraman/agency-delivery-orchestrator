"""Render the repository's Markdown documentation as one offline reading view."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import html
import re
try:
    import markdown
except ImportError:
    raise SystemExit('Install the documentation dependencies from requirements-blueprint.txt first.')

ROOT = Path(__file__).resolve().parents[1]
DOCS = [ROOT / 'README.md', *sorted((ROOT / 'docs').glob('[0-9][0-9]-*.md')), ROOT / 'examples/README.md']
IDS = {path.resolve(): ('overview' if path == ROOT / 'README.md' else 'examples' if path.parent.name == 'examples' else path.stem) for path in DOCS}
CSS = '''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f3f6f2;color:#183b34;font:17px/1.65 system-ui,sans-serif}header{background:#075345;color:white;padding:44px max(24px,calc((100vw - 1080px)/2))}header p{max-width:850px}h1{font:600 42px/1.15 Georgia,serif}main,nav{max-width:1140px;margin:auto;padding:24px}nav{display:flex;flex-wrap:wrap;gap:14px}section{background:white;border:1px solid #d6e1da;padding:28px;border-radius:12px;margin-bottom:22px;overflow:auto}h2{font:600 28px/1.2 Georgia,serif}h3{font-size:21px}a{color:#075d53;text-underline-offset:3px}header a{color:white}li{margin:9px 0}td,th{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #d6e1da;min-width:130px}table{border-collapse:collapse;width:100%;font-size:15px}code{font-size:.86em;overflow-wrap:anywhere}pre{padding:16px;background:#edf2eb;overflow:auto}pre code{white-space:pre}blockquote{border-left:4px solid #98aa56;margin:16px 0;padding:8px 18px;background:#f2f5e8}.quiet{font-size:14px;color:#596a63}a:focus-visible{outline:3px solid #b19b59;outline-offset:4px}@media(max-width:760px){main,nav{padding:12px}section{padding:20px}h1{font-size:34px}header{padding:30px 24px}}@media print{header{background:white;color:#183b34;padding:10px}body{font-size:10pt;background:white}section{border:0;padding:12px;overflow:visible}nav{display:none}h2,h3{break-after:avoid}tr{break-inside:avoid}}'''

def content(path):
    rendered = markdown.markdown(path.read_text(), extensions=['tables', 'fenced_code', 'sane_lists'])
    def link(match):
        target = html.unescape(match.group(1))
        parsed = urlparse(target)
        if parsed.scheme or not parsed.path:
            return match.group(0)
        resolved = (path.parent / unquote(parsed.path)).resolve()
        if resolved in IDS:
            new = '#' + IDS[resolved]
        else:
            new = str(resolved.relative_to(ROOT)) + ('#' + parsed.fragment if parsed.fragment else '')
        return 'href="' + html.escape(new, quote=True) + '"'
    return re.sub(r'href="([^"]+)"', link, rendered)

nav=''.join('<a href="#'+IDS[p.resolve()]+'">'+html.escape(p.stem.replace('-', ' '))+'</a>' for p in DOCS)
body=''.join('<section id="'+IDS[p.resolve()]+'">'+content(p)+'</section>' for p in DOCS)
page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Agency Delivery Orchestrator — complete blueprint</title><style>'+CSS+'</style></head><body><header><p>PUBLIC-INTENDED DOCUMENTATION BLUEPRINT · 11 OCTOBER 2026</p><h1>Agency Delivery Orchestrator</h1><p>From the approved brief to completed delivery: plan work, collect inputs, coordinate production, handle changes, obtain reviews and prepare billing evidence.</p><p>Blueprint only. Application implementation and benchmark execution have not started.</p></header><nav aria-label="Blueprint sections">'+nav+'</nav><main>'+body+'</main></body></html>'
(ROOT / 'BLUEPRINT.html').write_text(page)
print('Rendered BLUEPRINT.html from '+str(len(DOCS))+' Markdown documents.')
