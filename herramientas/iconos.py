"""Descarga iconos oficiales y actualiza la selección SVG local de las diapositivas."""
import argparse
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
VERSION = '6.7.2'
CARPETA = ROOT / 'assets/iconos/fontawesome/solid'
PRESENTACION = ROOT / 'web/presentacion/index.html'


def leer_svg(texto):
    svg = ET.fromstring(texto)
    if not svg.tag.endswith('svg') or not svg.get('viewBox'):
        raise ValueError('El recurso no es un icono SVG con viewBox.')
    paths = list(svg)
    if not paths or any(not p.tag.endswith('path') or not p.get('d') for p in paths):
        raise ValueError('Solo se admiten iconos oficiales compuestos por paths.')
    return svg


def descargar(nombre):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', nombre):
        raise ValueError(f'Nombre de icono inválido: {nombre}')
    url = f'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/{VERSION}/svgs/solid/{nombre}.svg'
    with urllib.request.urlopen(url, timeout=30) as respuesta:
        texto = respuesta.read().decode('utf-8')
    leer_svg(texto)
    CARPETA.mkdir(parents=True, exist_ok=True)
    (CARPETA / f'{nombre}.svg').write_text(texto, encoding='utf-8')
    print(f'Icono oficial guardado: {nombre}')


def sincronizar():
    simbolos = []
    for archivo in sorted(CARPETA.glob('*.svg')):
        svg = leer_svg(archivo.read_text(encoding='utf-8'))
        paths = ''.join(f'<path d="{p.attrib["d"]}"/>' for p in svg)
        simbolos.append(f'<symbol id="fa-{archivo.stem}" viewBox="{svg.attrib["viewBox"]}">{paths}</symbol>')
    if not simbolos:
        raise ValueError('No hay iconos locales para sincronizar.')
    texto = PRESENTACION.read_text(encoding='utf-8')
    texto, cantidad = re.subn(r'(<svg class="biblioteca-iconos"[^>]*><defs>).*?(</defs></svg>)',
        lambda m: m[1] + ''.join(simbolos) + m[2], texto, flags=re.DOTALL)
    if cantidad != 1:
        raise ValueError('Debe existir una única biblioteca-iconos en la presentación.')
    PRESENTACION.write_text(texto, encoding='utf-8')
    print(f'Biblioteca en línea actualizada: {len(simbolos)} iconos; funciona con file:// y sin conexión.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--descargar', nargs='+', default=[], metavar='NOMBRE')
    parser.add_argument('--sincronizar', action='store_true')
    args = parser.parse_args()
    if not args.descargar and not args.sincronizar:
        parser.error('Indica --descargar NOMBRE o --sincronizar.')
    for nombre in args.descargar:
        descargar(nombre)
    if args.sincronizar:
        sincronizar()


if __name__ == '__main__':
    main()
