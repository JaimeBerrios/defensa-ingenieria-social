"""Comprueba enlaces y recursos locales del portal, las diapositivas y la demo."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class EnlacesHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rutas = []
        self.ids = set()
        self.fragmentos = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                raise ValueError(f'ID repetido: {attrs["id"]}')
            self.ids.add(attrs['id'])
        for clave in ('src', 'href', 'data-src'):
            valor = attrs.get(clave, '')
            url = urlsplit(valor)
            if url.scheme or url.netloc or not valor:
                continue
            if url.path:
                self.rutas.append(unquote(url.path))
            elif url.fragment and not url.fragment.startswith('/'):
                self.fragmentos.append(url.fragment)
            elif url.fragment.startswith('/') and not url.fragment[1:].replace('/', '').isdigit():
                self.fragmentos.append(url.fragment[1:])


def verificar_html(archivo):
    parser = EnlacesHTML()
    parser.feed(archivo.read_text(encoding='utf-8'))
    errores = [f'{archivo}: recurso inexistente {ruta}' for ruta in parser.rutas
               if not (archivo.parent / ruta).exists()]
    errores += [f'{archivo}: destino inexistente #{destino}' for destino in parser.fragmentos
                if destino not in parser.ids]
    return errores


def verificar_documentacion(root=ROOT):
    """Comprueba destinos locales de enlaces Markdown al reorganizar las guías."""
    errores = []
    archivos = [root / 'README.md', *sorted((root / 'docs').rglob('*.md'))]
    for archivo in archivos:
        texto = re.sub(r'```.*?```', '', archivo.read_text(encoding='utf-8'), flags=re.DOTALL)
        for destino in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', texto):
            url = urlsplit(destino)
            if url.scheme or url.netloc or not url.path:
                continue
            if not (archivo.parent / unquote(url.path)).exists():
                errores.append(f'{archivo}: enlace inexistente {destino}')
    return errores


def verificar_web(root=ROOT):
    errores = verificar_documentacion(root)
    for relativa in ('index.html', 'web/presentacion/index.html', 'ejemplos/reveal-demo.html'):
        errores.extend(verificar_html(root / relativa))
    carpetas_css = [root / 'web', root / 'vendor/bootstrap/css', root / 'vendor/fontawesome/css']
    for archivo in (p for carpeta in carpetas_css for p in carpeta.rglob('*.css')):
        for ruta in re.findall(r'url\([\'"]?([^\)\'"\s]+)', archivo.read_text(encoding='utf-8')):
            url = urlsplit(ruta)
            if not url.scheme and not url.netloc and url.path and not (archivo.parent / unquote(url.path)).is_file():
                errores.append(f'{archivo}: recurso CSS inexistente {ruta}')
    if errores:
        raise ValueError('\n'.join(errores))


if __name__ == '__main__':
    verificar_web()
    print('Enlaces de documentación y recursos locales del portal, presentación y demo verificados.')
