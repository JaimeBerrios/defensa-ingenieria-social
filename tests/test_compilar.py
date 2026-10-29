import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from herramientas import compilacion as compilar


class DatosCompartidos(unittest.TestCase):
    def test_escape_tex(self):
        self.assertEqual(compilar.tex_escape('A&B_50%'), r'A\&B\_50\%')
        self.assertEqual(compilar.tex_escape('á ñ'), 'á ñ')

    def test_web_escapa_y_conserva_contenido(self):
        fields = {key: 'Dato' for key in compilar.FIELDS}
        fields['Título'] = '<script>alert("x")</script> & Ciencia'
        fields['Firma'] = 'NO PUBLICAR FIRMA'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'web/presentacion').mkdir(parents=True)
            source = '<title>Antes</title><span data-campo="Título">Antes</span><tbody id="integrantes"></tbody><section>Contenido propio</section>'
            (root / 'web/presentacion/index.html').write_text(source, encoding='utf-8')
            with patch.object(compilar, 'ROOT', root):
                result = compilar.render_web(fields, [['Ana & Luis', '<001>']])
            self.assertIn('&lt;script&gt;', result)
            self.assertNotIn('<script>', result)
            self.assertIn('<td>Ana &amp; Luis</td><td>&lt;001&gt;</td>', result)
            self.assertIn('<section>Contenido propio</section>', result)
            self.assertNotIn(fields['Firma'], result)
            self.assertEqual((root / 'web/presentacion/index.html').read_text(encoding='utf-8'), source)

    def test_rechaza_datos_incompletos(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'datos').mkdir()
            (root / 'datos/datos.md').write_text('## Datos generales\n- Título: Ejemplo\n', encoding='utf-8')
            with patch.object(compilar, 'ROOT', root), self.assertRaises(ValueError):
                compilar.read_data()

    def test_html_sin_tabla_no_se_publica(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'web/presentacion').mkdir(parents=True)
            (root / 'web/presentacion/index.html').write_text('<title>Ejemplo</title>', encoding='utf-8')
            with patch.object(compilar, 'ROOT', root), self.assertRaises(ValueError):
                compilar.render_web({'Título': 'Ejemplo'}, [])


if __name__ == '__main__':
    unittest.main()
