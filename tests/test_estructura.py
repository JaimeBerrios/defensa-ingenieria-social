from pathlib import Path
import tempfile
import unittest

from herramientas.iconos import leer_svg
from herramientas.validacion import verificar_documentacion, verificar_html, verificar_web

ROOT = Path(__file__).resolve().parents[1]


class EstructuraRepositorio(unittest.TestCase):
    def test_enlaces_y_recursos_tras_migracion(self):
        verificar_web(ROOT)

    def test_detecta_destinos_y_recursos_rotos(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / 'index.html'
            archivo.write_text('<a href="#ausente">Ir</a><img src="falta.png">')
            errores = verificar_html(archivo)
            self.assertEqual(len(errores), 2)

    def test_documentacion_anidada_y_enlaces_rotos(self):
        with tempfile.TemporaryDirectory() as carpeta:
            root = Path(carpeta)
            (root / 'docs/uso').mkdir(parents=True)
            (root / 'README.md').write_text('[Guía](docs/uso/guia.md)')
            guia = root / 'docs/uso/guia.md'
            guia.write_text('[Inicio](../../README.md) [Externo](https://example.com)')
            self.assertEqual(verificar_documentacion(root), [])
            guia.write_text('[Ruta anterior](../guia.md)')
            errores = verificar_documentacion(root)
            self.assertEqual(len(errores), 1)
            self.assertIn('../guia.md', errores[0])

    def test_iconos_locales_validos_y_licencia(self):
        carpeta = ROOT / 'assets/iconos/fontawesome'
        self.assertTrue((carpeta / 'LICENSE.txt').is_file())
        iconos = list((carpeta / 'solid').glob('*.svg'))
        self.assertTrue(iconos)
        for archivo in iconos:
            with self.subTest(icono=archivo.name):
                leer_svg(archivo.read_text())

    def test_descarta_svg_con_elementos_ejecutables(self):
        with self.assertRaises(ValueError):
            leer_svg('<svg viewBox="0 0 1 1"><script>alert(1)</script></svg>')


if __name__ == '__main__':
    unittest.main()
