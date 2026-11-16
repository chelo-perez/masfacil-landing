# Genera las páginas legales de Trabajo Más Fácil a partir de los .md del repo de la app.
# Uso: python3 scripts/legal.py <carpeta docs/play-store de la app>
import html, os, re, sys
SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'trabajo')
PAGES = [('politica-de-privacidad.md', 'privacidad', 'Política de privacidad'),
         ('terminos-y-condiciones.md', 'terminos', 'Términos y condiciones'),
         ('eliminar-cuenta.md', 'eliminar-cuenta', 'Eliminar tu cuenta')]

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    t = re.sub(r'(?<![">])(https?://[^\s<)]+)', r'<a href="\1">\1</a>', t)
    t = re.sub(r'(?<![:\w/>"])([\w.+-]+@[\w-]+\.[\w.]+\w)', r'<a href="mailto:\1">\1</a>', t)
    return t

def convert(md):
    out, para, lists = [], [], []
    def flush():
        if para: out.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
    def close_lists(level=0):
        while len(lists) > level: out.append('</ul>' if lists.pop() == 'ul' else '</ol>')
    for raw in md.split('\n'):
        line = raw.rstrip()
        if line.startswith('> '):
            # El aviso de borrador no se publica; la fecha sí
            if 'Última actualización' in line: flush(); close_lists(); out.append('<p class="updated">' + inline(line[2:]) + '</p>')
            continue
        m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', line)
        if m:
            flush(); level = len(m.group(1)) // 2 + 1; kind = 'ol' if m.group(2)[0].isdigit() else 'ul'
            while len(lists) < level: lists.append(kind); out.append(f'<{kind}>')
            close_lists(level); out.append('<li>' + inline(m.group(3)) + '</li>'); continue
        if not line.strip(): flush(); close_lists(); continue
        if line.startswith('## '): flush(); close_lists(); out.append('<h2>' + inline(line[3:]) + '</h2>'); continue
        if line.startswith('# '): flush(); close_lists(); continue  # el título va en la cabecera
        para.append(line.strip())
    flush(); close_lists()
    return '\n'.join(out)

TEMPLATE = '''<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Trabajo Más Fácil</title>
<meta name="description" content="{title} de Trabajo Más Fácil, de Tecnología Más Fácil S.A.S.">
<link rel="icon" href="/logo-trabajo.png">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--ink:#172322;--mid:#566362;--light:#93A09F;--sage:#2C6566;--deep:#163235;--bg:#F4F7F7;--line:#E2EAE9}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Nunito,system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}}
header{{background:var(--deep);color:#fff;padding:28px 20px 40px}}
.wrap{{max-width:780px;margin:0 auto}}
.top{{display:flex;align-items:center;justify-content:space-between;gap:12px}}
.top img{{height:46px}}.top a{{color:#cfe7e3;text-decoration:none;font-weight:700;font-size:14px}}
h1{{font-size:clamp(28px,5vw,40px);margin:28px 0 0;letter-spacing:-.5px}}
nav.tabs{{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}}
nav.tabs a{{color:#fff;text-decoration:none;font-size:13px;font-weight:700;padding:7px 14px;border-radius:999px;background:rgba(255,255,255,.12)}}
nav.tabs a.on{{background:#fff;color:var(--deep)}}
main{{padding:0 20px 60px}}
article{{background:#fff;border:1px solid var(--line);border-radius:18px;padding:32px clamp(20px,5vw,44px);margin-top:-22px}}
h2{{font-size:20px;margin:30px 0 8px;color:var(--deep)}}p,li{{color:#2a3534;font-size:15.5px}}
ul,ol{{padding-left:22px}}li{{margin:4px 0}}a{{color:var(--sage);font-weight:700}}
.updated{{color:var(--light);font-size:13px;margin-top:0}}code{{background:#EEF4F3;padding:1px 6px;border-radius:6px}}
footer{{text-align:center;color:var(--light);font-size:13px;padding:0 20px 40px}}footer a{{color:var(--mid)}}
</style></head>
<body>
<header><div class="wrap">
  <div class="top"><a href="/trabajo"><img src="/logo-trabajo-blanco.png" alt="Trabajo Más Fácil"></a><a href="/trabajo">Volver al inicio</a></div>
  <h1>{title}</h1>
  <nav class="tabs">{tabs}</nav>
</div></header>
<main><div class="wrap"><article>
{body}
</article></div></main>
<footer>Tecnología Más Fácil S.A.S. · <a href="mailto:info@masfacil.com.ar">info@masfacil.com.ar</a> · <a href="/trabajo">masfacil.com.ar/trabajo</a></footer>
</body></html>
'''

for src, slug, title in PAGES:
    md = open(os.path.join(SRC, src), encoding='utf-8').read()
    tabs = ''.join(f'<a href="/trabajo/{s}"{" class=\"on\"" if s == slug else ""}>{t}</a>' for _, s, t in PAGES)
    open(os.path.join(OUT, f'{slug}.html'), 'w', encoding='utf-8').write(TEMPLATE.format(title=title, tabs=tabs, body=convert(md)))
    print('trabajo/' + slug + '.html')
