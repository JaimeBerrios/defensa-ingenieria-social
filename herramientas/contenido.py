"""Bibliografía compartida y comprobaciones estructurales, sin dependencias externas."""
import html
from html.parser import HTMLParser
import json
import re
import unicodedata


def normalizar(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())


class DiapositivasHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
        self.stack = []
        self.heading = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section':
            self.stack.append({'expositor': attrs.get('data-expositor', ''), 'title': '', 'has_children': False})
            if len(self.stack) > 1:
                self.stack[-2]['has_children'] = True
        if self.stack and tag in ('h1', 'h2'):
            self.heading = True

    def handle_endtag(self, tag):
        if tag in ('h1', 'h2'):
            self.heading = False
        if tag == 'section' and self.stack:
            info = self.stack.pop()
            if not info['has_children'] or info['title'].strip():
                self.slides.append([info['expositor'], info['title']])

    def handle_data(self, data):
        if self.stack and self.heading:
            self.stack[-1]['title'] += data


def sin_comentarios(tex):
    return re.sub(r'(?<!\\)%[^\n]*', '', tex)


def verificar_laminas(tex, web, fields):
    """Formato admitido: portada, frame con título simple, expositor y cierre."""
    tex = sin_comentarios(tex)
    token = re.compile(r'\\portadainstitucional|\\expositor\{([^{}]*(?:\\Grupo)?[^{}]*)\}|\\begin\{frame\}(?:\[[^\]]*\])?\{([^{}]*)\}|\\cierreinstitucional(?:\[([^\]]*)\])?')
    slides, expositor = [], ''
    for match in token.finditer(tex):
        value = match.group(0)
        if value.startswith(r'\portadainstitucional'):
            slides.append(['', fields['Título']])
        elif value.startswith(r'\expositor'):
            expositor = match.group(1).replace(r'\Grupo', fields['Grupo'])
        elif value.startswith(r'\begin'):
            title = re.sub(r'\\fa[A-Za-z]+\s*', '', match.group(2)).replace('\\ ', ' ')
            if '\\' in title:
                raise ValueError('Título LaTeX no verificable: usa texto simple e iconos sin argumentos.')
            slides.append([expositor, title])
        else:
            slides.append(['', match.group(3) or 'Muchas gracias por su atención'])
    if len(re.findall(r'\\begin\{frame\}', tex)) != sum(1 for m in token.finditer(tex) if m.group(0).startswith(r'\begin')):
        raise ValueError('Hay frames sin título verificable. Usa \\begin{frame}{Título} con texto simple.')
    parser = DiapositivasHTML()
    parser.feed(web)
    errors = []
    if len(slides) != len(parser.slides):
        errors.append(f'Cantidad de láminas: LaTeX={len(slides)}, HTML={len(parser.slides)}.')
    for i, (left, right) in enumerate(zip(slides, parser.slides), 1):
        right[0] = fields['Grupo'] if right[0] == 'grupo' else right[0]
        for column, label in enumerate(('expositor', 'título')):
            if normalizar(left[column]) != normalizar(right[column]):
                errors.append(f'Lámina {i}, {label}: LaTeX="{left[column]}" / HTML="{right[column]}".')
    if errors:
        raise ValueError('Presentaciones incoherentes:\n' + '\n'.join(errors))
    return len(slides)


def leer_referencias(path):
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    if data.get('estilo') != 'APA 7' or not isinstance(data.get('referencias'), list):
        raise ValueError('datos/referencias.json debe declarar estilo APA 7 y una lista referencias.')
    refs = {}
    for entry in data['referencias']:
        for key in ('id', 'orden', 'autor_parentetico', 'autor_narrativo', 'anio', 'referencia'):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                raise ValueError(f'Referencia incompleta: falta {key}.')
        key = entry['id']
        if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_-]*', key) or key in refs:
            raise ValueError(f'Identificador de referencia inválido o repetido: {key}')
        if entry['referencia'].count('*') % 2:
            raise ValueError(f'Cursivas sin cerrar en la referencia {key}.')
        refs[key] = entry
    return refs


def referencia_formateada(entry, escape, italic):
    parts = entry['referencia'].split('*')
    text = ''.join(italic(escape(part)) if i % 2 else escape(part) for i, part in enumerate(parts))
    if entry.get('ejemplo'):
        text += escape(' [Referencia de ejemplo: reemplazar con una fuente real.]')
    return text


def cita(entry, narrativa=False, localizador=''):
    autor = entry['autor_narrativo' if narrativa else 'autor_parentetico']
    suffix = ', ' + localizador if localizador else ''
    return f'{autor} ({entry["anio"]}{suffix})' if narrativa else f'({autor}, {entry["anio"]}{suffix})'


def preparar_referencias(refs, tex_sources, web, escape):
    ordered = sorted(refs, key=lambda key: unicodedata.normalize('NFKD', refs[key]['orden']).casefold())
    cited_tex = []
    for source in tex_sources:
        used = set()
        for key_str in re.findall(r'\\cita(?:s|texto)?(?:\[[^\]]*\])?\{([^{}]+)\}', sin_comentarios(source)):
            for key in [k.strip() for k in key_str.split(',') if k.strip()]:
                if key not in refs:
                    raise ValueError(f'Cita LaTeX desconocida: {key}')
                used.add(key)
        if re.search(r'\\cite(?:\[|\{)', sin_comentarios(source)):
            raise ValueError('Usa \\cita o \\citatexto para las citas APA compartidas, en lugar de \\cite.')
        cited_tex.append(used)
    cited_web = set()
    def web_cita(match):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', match.group(1)))
        raw_keys = html.unescape(attrs['data-cita'])
        keys = [k.strip() for k in raw_keys.split(',') if k.strip()]
        for k in keys:
            if k not in refs:
                raise ValueError(f'Cita HTML desconocida: {k}')
            cited_web.add(k)
        if len(keys) == 1:
            text = cita(refs[keys[0]], attrs.get('data-tipo') == 'narrativa', html.unescape(attrs.get('data-localizador', '')))
        else:
            parts = [f"{refs[k]['autor_parentetico']}, {refs[k]['anio']}" for k in keys]
            text = f"({'; '.join(parts)})"
        return '<span' + match.group(1) + '>' + html.escape(text) + '</span>'
    if web is not None:
        web = re.sub(r'<span(\s[^>]*data-cita="[^"]+"[^>]*)>.*?</span>', web_cita, web, flags=re.DOTALL)
    if web is not None and cited_tex[0] != cited_web:
        raise ValueError(f'Citas diferentes entre presentación y web: LaTeX={sorted(cited_tex[0])}, HTML={sorted(cited_web)}')
    lines = [
        r'\makeatletter',
        r'\newcommand{\cita}[2][]{(\csname autorp@#2\endcsname, \csname anio@#2\endcsname\if\relax\detokenize{#1}\relax\else, #1\fi)}',
        r'\newcommand{\citatexto}[2][]{\csname autorn@#2\endcsname\ (\csname anio@#2\endcsname\if\relax\detokenize{#1}\relax\else, #1\fi)}',
        r'\newcommand{\citas}[1]{(%',
        r'  \def\citassep{}%',
        r'  \@for\@tmp:=#1\do{%',
        r'    \citassep\csname autorp@\@tmp\endcsname,~\csname anio@\@tmp\endcsname%',
        r'    \def\citassep{;~}%',
        r'  }%',
        r')}',
        r'\makeatother',
    ]
    for key in ordered:
        for macro, field in [('autorp', 'autor_parentetico'), ('autorn', 'autor_narrativo'), ('anio', 'anio')]:
            lines.append(r'\expandafter\def\csname ' + macro + '@' + key + r'\endcsname{' + escape(refs[key][field]) + '}')
    selected = [key for key in ordered if key in cited_tex[0]]
    report_entries = [referencia_formateada(refs[key], escape, lambda s: r'\textit{' + s + '}') for key in ordered if key in cited_tex[1]]
    slide_entries = [referencia_formateada(refs[key], escape, lambda s: r'\textit{' + s + '}') for key in selected]
    report = '\n'.join(r'\noindent\hangindent=1.27cm\hangafter=1 ' + entry + r'\par' for entry in report_entries)
    slides = '\n'.join(r'\item ' + entry for entry in slide_entries)
    if not report_entries:
        report = 'No hay fuentes citadas. Agrega referencias reales antes de entregar.'
    if not slide_entries:
        slides = r'\item No hay fuentes citadas. Agrega referencias reales antes de entregar.'
    bibliography = '<ul class="referencias-apa">' + ''.join('<li>' + referencia_formateada(refs[key], html.escape, lambda s: '<em>' + s + '</em>') + '</li>' for key in selected) + '</ul>'
    if not selected:
        bibliography = '<p>No hay fuentes citadas. Agrega referencias reales antes de entregar.</p>'
    if web is not None:
        web, count = re.subn(r'<!-- referencias:inicio -->.*?<!-- referencias:fin -->', lambda _: '<!-- referencias:inicio -->\n' + bibliography + '\n<!-- referencias:fin -->', web, flags=re.DOTALL)
        if count != 1:
            raise ValueError('Conserva un bloque referencias:inicio / referencias:fin en el HTML.')
    return web, '\n'.join(lines), report, r'\begin{itemize}' + slides + r'\end{itemize}'
