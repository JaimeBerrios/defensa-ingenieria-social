import unittest
from pathlib import Path

from herramientas.contenido import verificar_laminas, preparar_referencias, leer_referencias, cita
from herramientas.compilacion import tex_escape


class Coherencia(unittest.TestCase):
    fields = {'Título': 'Proyecto', 'Grupo': 'Grupo 01'}
    tex = r'\portadainstitucional \expositor{Ana} \begin{frame}{\faBook \ Tema}x\end{frame}'
    web = '<section><h1>Proyecto</h1></section><section data-expositor="Ana"><h2>Tema</h2></section>'

    def test_ignora_comentarios(self):
        self.assertEqual(verificar_laminas(self.tex + '\n% \\begin{frame}{Ignorado}', self.web, self.fields), 2)

    def test_detecta_titulo_expositor_y_cantidad(self):
        for web, esperado in [(self.web.replace('Tema', 'Otro'), 'título'), (self.web.replace('Ana', 'Luis'), 'expositor'), (self.web + '<section><h2>Extra</h2></section>', 'Cantidad')]:
            with self.subTest(esperado=esperado), self.assertRaisesRegex(ValueError, esperado):
                verificar_laminas(self.tex, web, self.fields)

    def test_rechaza_titulo_no_verificable(self):
        with self.assertRaisesRegex(ValueError, 'sin título verificable'):
            verificar_laminas(r'\begin{frame}{\textbf{Tema}}', self.web, self.fields)

    def test_admite_laminas_verticales(self):
        web_vertical = '<section><h1>Proyecto</h1></section><section><section data-expositor="Ana"><h2>Tema</h2></section></section>'
        self.assertEqual(verificar_laminas(self.tex, web_vertical, self.fields), 2)



class Referencias(unittest.TestCase):
    def setUp(self):
        self.refs = leer_referencias(Path(__file__).resolve().parents[1] / 'datos/referencias.json')
        self.web = '<span data-cita="fuente"></span><!-- referencias:inicio -->viejo<!-- referencias:fin -->'

    def test_cita_narrativa_y_localizador(self):
        self.assertEqual(cita(self.refs['fuente'], True, 'p. 10'), 'Apellido (Año, p. 10)')
        self.assertEqual(cita(self.refs['fuente'], False), '(Apellido, Año)')

    def test_referencia_compartida_cursivas_y_ejemplo(self):
        web, macros, report, slides = preparar_referencias(self.refs, [r'\cita{fuente}', r'\cita{fuente}'], self.web, tex_escape)
        self.assertIn('<em>Título de la obra</em>', web)
        self.assertIn(r'\textit{Título de la obra}', report)
        self.assertIn('Referencia de ejemplo', slides)
        self.assertNotIn('viejo', web)

    def test_bibliografia_por_documento(self):
        _, _, report, slides = preparar_referencias(self.refs, [r'\cita{fuente}', ''], self.web, tex_escape)
        self.assertIn('No hay fuentes citadas', report)
        self.assertIn('Apellido', slides)

    def test_rechaza_citas_desconocidas_o_desiguales(self):
        for sources in [[r'\cita{ausente}', ''], ['', '']]:
            with self.assertRaises(ValueError):
                preparar_referencias(self.refs, sources, self.web, tex_escape)

    def test_citas_multiples(self):
        web_multiple = '<span data-cita="fuente, fuente"></span><!-- referencias:inicio -->viejo<!-- referencias:fin -->'
        web, macros, report, slides = preparar_referencias(self.refs, [r'\citas{fuente, fuente}', r'\citas{fuente}'], web_multiple, tex_escape)
        self.assertIn('(Apellido, Año; Apellido, Año)', web)
        self.assertIn(r'\newcommand{\citas}', macros)
