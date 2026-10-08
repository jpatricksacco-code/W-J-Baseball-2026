import re, sys

HTML = sys.argv[1] if len(sys.argv) > 1 else "index.html"
TITLE = "Red Black World Series 2026"

CSS = """<style>
:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);
--bg:#f4f2f2;--card:#fff;--tx:#1a1a1a;--mu:#6b6465;--hd:#111;--ac:#b3121f;--ac2:#e03a47;--ln:#e0dada;--st:#faf6f6;--hov:#f8e4e6;--mu-hd:#c9c1c2}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0e0e0e;--card:#1a1a1a;--tx:#ece8e8;--mu:#a29a9b;--hd:#050505;--ac:#ff4d5a;--ac2:#ff4d5a;--ln:#2e2a2a;--st:#201d1d;--hov:#3a1a1e}}
:root[data-theme="dark"]{--bg:#0e0e0e;--card:#1a1a1a;--tx:#ece8e8;--mu:#a29a9b;--hd:#050505;--ac:#ff4d5a;--ac2:#ff4d5a;--ln:#2e2a2a;--st:#201d1d;--hov:#3a1a1e}
html{scroll-padding-top:env(safe-area-inset-top,0px)}*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:14px/1.4 -apple-system,"Segoe UI",Roboto,Arial,sans-serif}
header{background:linear-gradient(180deg,#1c1c1c 0%,var(--hd) 100%);color:#fff;padding:20px 20px 0;border-bottom:4px solid #c8102e}
.eyebrow{display:block;font-size:11px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#ff6b77;margin-bottom:4px}
h1{margin:0;font-size:30px;font-weight:800;letter-spacing:.02em;text-transform:uppercase;line-height:1.1}
h1 em{font-style:normal;color:#e8202f}
header p{margin:6px 0 14px;color:#b8afb0;font-size:13px;letter-spacing:.03em}
nav{display:flex;gap:2px;flex-wrap:wrap}
nav button{background:none;border:0;color:#b8afb0;padding:11px 18px;font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;border-bottom:3px solid transparent;transition:color .15s,background .15s}
nav button:hover{color:#fff;background:rgba(255,255,255,.06)}
nav button.on{color:#fff;border-color:#e8202f}
main{max-width:1200px;margin:0 auto;padding:16px}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.bar label{font-weight:600;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mu)}
select{background:var(--card);color:var(--tx);border:1px solid var(--ln);border-radius:4px;padding:6px 8px;font-size:14px}
select:focus{outline:2px solid var(--ac);outline-offset:1px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin-bottom:16px}
.c{background:var(--card);border:1px solid var(--ln);border-top:3px solid var(--ac);border-radius:6px;padding:8px 10px}
.c b{display:block;font-size:22px;font-weight:800}.c span{color:var(--mu);font-size:11px;text-transform:uppercase;letter-spacing:.06em}
.box{background:var(--card);border:1px solid var(--ln);border-radius:6px;margin-bottom:16px;overflow:hidden}
.box h2{margin:0;padding:10px 14px;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;background:var(--hd);color:#fff;border-left:5px solid #e8202f}
.sc{overflow-x:auto}table{border-collapse:collapse;width:100%;white-space:nowrap}
th,td{padding:6px 10px;text-align:right;border-bottom:1px solid var(--ln)}th:first-child,td:first-child{text-align:left}
th{cursor:pointer;background:var(--st);font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--mu);position:sticky;top:0;user-select:none}
th:hover{color:var(--ac)}th.s{color:var(--ac);box-shadow:inset 0 -2px 0 var(--ac)}
tbody tr:nth-child(even){background:var(--st)}tbody tr:hover{background:var(--hov)}
td.n{font-weight:600}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
svg{display:block;width:100%;height:auto}svg text{fill:var(--mu);font-size:10px}
.lg{display:flex;gap:12px;flex-wrap:wrap;padding:8px 12px;font-size:12px}.lg i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px}
footer{color:var(--mu);font-size:12px;padding:8px 0 24px}
@media (max-width:520px){h1{font-size:23px}nav button{padding:10px 12px}}
</style>"""

HEADER = ('<header><span class="eyebrow">WAS_AND · Ross Memorial Park</span>'
          '<h1>Red Black <em>World Series</em> 2026</h1>')

html = open(HTML, encoding="utf-8").read()

# <title>
html, n1 = re.subn(r"<title>.*?</title>", f"<title>{TITLE}</title>", html, count=1, flags=re.S)
# stylesheet
html, n2 = re.subn(r"<style>.*?</style>", lambda m: CSS, html, count=1, flags=re.S)
# header + h1 (keeps <p id="sub"> and <nav id="nav"> intact)
html, n3 = re.subn(r"<header>(?:<span class=\"eyebrow\">.*?</span>)?<h1>.*?</h1>", lambda m: HEADER, html, count=1, flags=re.S)

if not (n1 and n2 and n3):
    sys.exit(f"Pattern not found (title={n1}, style={n2}, header={n3}) - nothing written.")

# ---- Game labels: dates are M/D/YY, so label them Game 1..N in chronological order
html, n4 = re.subn(
    r"(?:const pd=[^\n]*\n)?const dates=[^\n]*\nconst fm=[^\n]*\n",
    lambda m: ("const pd=s=>{const[m,d,y]=s.split('/');return new Date(2000+ +y,m-1,d)};\n"
               "const dates=[...new Set(D.map(r=>r.d))].sort((a,b)=>pd(a)-pd(b));\n"
               "const fm=d=>'Game '+(dates.indexOf(d)+1);\n"),
    html, count=1)
html, n5 = re.subn(r"\$\{fm\(d\)\}(?:/\$\{dates\[0\]\.slice\(0,4\)\})?", lambda m: "${fm(d)}", html, count=1)
if not (n4 and n5):
    sys.exit(f"Game-label pattern not found ({n4},{n5}) - nothing written.")

open(HTML, "w", encoding="utf-8").write(html)
print(f"Restyled {HTML}")
