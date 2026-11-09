#!/usr/bin/env python3
"""Genera index.html con un listado de todas las webs HTML del repositorio.

Estilo basado en el Plan de Digitalización de Vedruna María Inmaculada Vigo.
Edita la sección CONFIGURACIÓN para cambiar los textos de la portada.
"""
import html
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

# ───────────── CONFIGURACIÓN ─────────────
INICIAL = "V"                                   # letra del logo circular
LOGO_L1 = "VEDRUNA EDUCACIÓN"
LOGO_L2 = "María Inmaculada Vigo"
EYEBROW = "Recursos digitales"
TITULO = "Nuestras"                             # parte en blanco del título
TITULO_VERDE = "webs"                           # parte en verde del título
LEAD = ("Materiales, planes y herramientas digitales del centro, "
        "reunidos en un único lugar.")
SMALL = ("Cada recurso se publica en su propia página. "
         "Esta lista se actualiza sola cada vez que se añade uno nuevo.")
PIE = "Colegio Vedruna María Inmaculada Vigo"
SKIP_DIRS = {"node_modules", "assets", "static"}  # carpetas que no se listan
# ─────────────────────────────────────────

ROOT = Path(__file__).parent


def read_meta(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    t = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    d = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
        text, re.I | re.S,
    )
    title = html.unescape(re.sub(r"\s+", " ", t.group(1)).strip()) if t else ""
    desc = html.unescape(re.sub(r"\s+", " ", d.group(1)).strip()) if d else ""
    return title, desc


def pretty(name):
    return name.replace("-", " ").replace("_", " ").strip().capitalize()


def collect():
    items = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if rel.as_posix() == "index.html":
            continue
        if any(part.startswith(".") or part in SKIP_DIRS for part in rel.parts):
            continue
        if p.name == "index.html":          # carpeta/index.html -> enlace a carpeta/
            href = quote(rel.parent.as_posix()) + "/"
            fallback = pretty(rel.parent.name)
            shown = rel.parent.as_posix() + "/"
        else:                               # fichero suelto
            href = quote(rel.as_posix())
            fallback = pretty(p.stem)
            shown = rel.as_posix()
        title, desc = read_meta(p)
        items.append({
            "href": href,
            "title": title or fallback,
            "desc": desc,
            "path": shown,
        })
    items.sort(key=lambda i: i["title"].lower())
    return items


PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%%TITLE_PLAIN%%</title>
<style>
:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);
--bg:#fff;--tx:#383836;--mut:#5d5d58;--dk:#3b3b39;--gr:#a4c639;--gr-l:#c4dc72;--gr-d:#5f7a1f;--soft:#f1f5e1;--line:#dde6bd;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1d1d1c;--tx:#ececea;--mut:#b4b4ae;--dk:#2b2b2a;--soft:#2a2e1d;--line:#454c2c;--card:#242423;--gr-d:#b5d35a}}
html{scroll-padding-top:env(safe-area-inset-top,0px);scroll-behavior:smooth}
*,*::before,*::after{box-sizing:inherit}
body{margin:0;background:var(--bg);color:var(--tx);font:17px/1.65 "Helvetica Neue",Arial,sans-serif}
h1,h2,h3{font-weight:400;line-height:1.1;margin:0 0 .5em;letter-spacing:-.02em}
h2{font-size:clamp(1.8rem,4vw,2.6rem)}h3{font-size:1.15rem;font-weight:700;letter-spacing:0;line-height:1.25}
p{margin:0 0 1em}.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
header{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:72px;flex-wrap:wrap}
.logo{font-size:.78rem;line-height:1.2;font-weight:700;display:flex;gap:10px;align-items:center;color:var(--tx);text-decoration:none}
.logo b{display:grid;place-items:center;width:40px;height:40px;background:var(--dk);color:var(--gr);border-radius:50%;font-size:1.3rem}
.logo small{font-weight:400;font-size:.78rem}
nav a{padding:8px 14px;color:var(--tx);text-decoration:none;font-weight:600;border-bottom:3px solid var(--gr)}
a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--gr-d);outline-offset:2px}
.hero{background:var(--dk);color:#fff;padding:72px 0}
.hero .wrap{display:grid;grid-template-columns:1.1fr 1fr;gap:48px;align-items:center}
.eye{font-size:.8rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gr-d);margin-bottom:.8em}
.hero .eye{color:var(--gr-l)}
.hero h1{font-size:clamp(2.8rem,7vw,5.2rem);margin:.2em 0 .3em}.hero h1 span{color:var(--gr)}
.hero .lead{font-size:1.6rem;line-height:1.35;margin:1em 0}
.hero p.small{color:#d8d8d3;font-size:1rem}
.btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.btn{display:inline-block;padding:14px 22px;border:1px solid var(--gr);border-radius:8px;color:#fff;font-weight:700;text-decoration:none;font-size:1rem}
.btn.fill{background:var(--gr);color:#2b2b2a}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.tile{border:1px solid #5c6340;background:rgba(255,255,255,.06);border-radius:20px;padding:24px}
.tile h3{font-size:2.4rem;font-weight:400;margin-bottom:.2em;letter-spacing:-.02em}
.tile p{font-size:.95rem;margin:0;color:#e6e6e1}
.tile.wide{grid-column:1/-1;background:var(--gr);color:#2b2b2a}.tile.wide p{color:#2b2b2a}
.tile.wide h3{font-size:3.4rem}
section.s{padding:72px 0}
.bar{display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin:8px 0 32px}
.bar h2{margin:0}
.search{font:inherit;padding:12px 16px;border-radius:10px;border:1px solid var(--gr-d);background:var(--card);color:var(--tx);min-width:min(100%,300px)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
a.card{display:flex;flex-direction:column;gap:12px;background:var(--soft);border:1px solid var(--line);border-top:6px solid var(--gr);border-radius:20px;padding:24px;color:inherit;text-decoration:none;transition:transform .15s,border-color .15s}
a.card:hover{transform:translateY(-3px);border-color:var(--gr-d)}
a.card[hidden]{display:none}
.card .top{display:flex;gap:14px;align-items:flex-start}
.ico{flex:none;width:44px;height:44px;border-radius:12px;background:var(--card);color:var(--gr-d);display:grid;place-items:center;font-weight:700;font-size:1.15rem}
.card h3{margin:0}
.card p{margin:0;color:var(--mut);font-size:.95rem}
.card .go{margin-top:auto;padding-top:8px;display:flex;justify-content:space-between;align-items:center;gap:10px;border-top:1px solid var(--line)}
.card code{font-size:.78rem;color:var(--mut);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.card .open{flex:none;background:var(--dk);color:#fff;border-radius:8px;padding:6px 14px;font-weight:700;font-size:.9rem}
.pend{border:2px dashed var(--line);border-radius:20px;padding:28px;color:var(--mut)}
footer{background:var(--dk);color:#d8d8d3;padding:32px 0;font-size:.9rem;border-top:6px solid var(--gr)}
footer .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media(max-width:860px){.hero{padding:48px 0}.hero .wrap{grid-template-columns:1fr;gap:32px}.hero .lead{font-size:1.3rem}.tile h3{font-size:1.7rem}.tile.wide h3{font-size:2.6rem}}
</style>
</head>
<body>
<header><div class="wrap">
<a class="logo" href="./"><b>%%INICIAL%%</b><span>%%LOGO_L1%%<br><small>%%LOGO_L2%%</small></span></a>
<nav aria-label="Principal"><a href="#webs">Todas las webs</a></nav>
</div></header>

<main>
<div class="hero"><div class="wrap">
<div>
<div class="eye">%%EYEBROW%%</div>
<h1>%%TITULO%% <span>%%TITULO_VERDE%%</span></h1>
<p class="lead">%%LEAD%%</p>
<p class="small">%%SMALL%%</p>
<div class="btns"><a class="btn fill" href="#webs">Ver todas las webs ↓</a></div>
</div>
<div class="tiles">
<div class="tile wide"><h3>%%COUNT%%</h3><p>%%COUNT_LABEL%% publicadas</p></div>
<div class="tile"><h3>Buscar</h3><p>Filtra por título o descripción al instante.</p></div>
<div class="tile"><h3>%%FECHA%%</h3><p>Última actualización del índice.</p></div>
</div>
</div></div>

<section class="s" id="webs"><div class="wrap">
<div class="eye">Biblioteca</div>
<div class="bar">
<h2>Todas las webs</h2>
<input class="search" id="q" type="search" placeholder="Buscar una web…" aria-label="Buscar una web">
</div>
<div class="grid" id="grid">
%%CARDS%%
</div>
<p class="pend" id="empty" hidden>No hay ninguna web que coincida con la búsqueda.</p>
</div></section>
</main>

<footer><div class="wrap"><span>%%PIE%%</span><span>Índice generado automáticamente</span></div></footer>

<script>
const q=document.getElementById('q'),cards=[...document.querySelectorAll('.card')],empty=document.getElementById('empty');
q.addEventListener('input',()=>{const s=q.value.toLowerCase().trim();let n=0;
cards.forEach(c=>{const show=c.textContent.toLowerCase().includes(s);c.hidden=!show;if(show)n++});
empty.hidden=n>0||cards.length===0});
</script>
</body>
</html>
"""

CARD = """<a class="card" href="%%HREF%%">
<div class="top"><span class="ico" aria-hidden="true">%%INI%%</span><h3>%%TITLE%%</h3></div>
%%DESC%%<div class="go"><code>%%PATH%%</code><span class="open">Abrir →</span></div>
</a>"""

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def fill(template, values):
    for k, v in values.items():
        template = template.replace(f"%%{k}%%", v)
    return template


def main():
    items = collect()
    esc = html.escape
    if items:
        cards = "\n".join(
            fill(CARD, {
                "HREF": i["href"],
                "INI": esc(next((c for c in i["title"] if c.isalnum()), "·").upper()),
                "TITLE": esc(i["title"]),
                "DESC": f'<p>{esc(i["desc"])}</p>\n' if i["desc"] else "",
                "PATH": esc(i["path"]),
            })
            for i in items
        )
    else:
        cards = '<p class="pend">Todavía no hay webs. Sube una carpeta con su index.html y aparecerá aquí.</p>'

    n = len(items)
    hoy = datetime.now(timezone.utc)
    page = fill(PAGE, {
        "TITLE_PLAIN": esc(f"{TITULO} {TITULO_VERDE} · {LOGO_L1}"),
        "INICIAL": esc(INICIAL),
        "LOGO_L1": esc(LOGO_L1),
        "LOGO_L2": esc(LOGO_L2),
        "EYEBROW": esc(EYEBROW),
        "TITULO": esc(TITULO),
        "TITULO_VERDE": esc(TITULO_VERDE),
        "LEAD": esc(LEAD),
        "SMALL": esc(SMALL),
        "PIE": esc(PIE),
        "COUNT": str(n),
        "COUNT_LABEL": "web" if n == 1 else "webs",
        "FECHA": f"{hoy.day} {MESES[hoy.month - 1][:3]}.",
        "CARDS": cards,
    })
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print(f"index.html generado con {n} webs")


if __name__ == "__main__":
    main()
