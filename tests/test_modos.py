import contextlib
import io
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from herramientas import compilacion as compilar


class ModosCompilacion(unittest.TestCase):
    def ejecutar(self, args, presentacion=False, fallo=False):
        original = compilar.ROOT
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('datos/datos.md', 'datos/referencias.json', 'documentos/reporte.tex'):
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original / name, root / name)
            (root / 'pdf').mkdir()
            (root / 'web/presentacion').mkdir(parents=True)
            (root / 'pdf/reporte.pdf').write_bytes(b'%PDF-reporte anterior')
            (root / 'pdf/presentacion.pdf').write_bytes(b'%PDF-presentacion anterior')
            (root / 'web/presentacion/index.html').write_text('HTML incompleto', encoding='utf-8')
            if presentacion:
                shutil.copy2(original / 'documentos/presentacion.tex', root / 'documentos/presentacion.tex')
                shutil.copy2(original / 'web/presentacion/index.html', root / 'web/presentacion/index.html')
            before = {name: (root / name).read_bytes() for name in ('pdf/presentacion.pdf', 'pdf/reporte.pdf', 'web/presentacion/index.html')}
            for name in ('isotipo-azul.png', 'logo-facultad.png', 'acreditacion.png'):
                p = root / 'assets/institucional' / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.touch()
            (root / 'assets/fuentes').mkdir(parents=True)
            (root / 'assets/fuentes/firma.otf').touch()
            compiled = []

            def fake_compile(command, **kwargs):
                name = Path(command[-1]).stem
                compiled.append(name)
                if fallo:
                    return SimpleNamespace(returncode=1)
                staging = Path(command[command.index('--outdir') + 1])
                (staging / f'{name}.pdf').write_bytes(b'%PDF-nuevo')
                return SimpleNamespace(returncode=0)

            with patch.object(compilar, 'ROOT', root), patch.object(compilar, 'get_compiler', return_value='tectonic'), patch.object(compilar.subprocess, 'run', side_effect=fake_compile), patch('sys.argv', ['compilar.py'] + args), contextlib.redirect_stdout(io.StringIO()):
                if fallo:
                    with self.assertRaises(RuntimeError):
                        compilar.main()
                else:
                    compilar.main()
            after = {name: (root / name).read_bytes() for name in before}
            if not presentacion:
                self.assertFalse((root / '.build/referencias-presentacion.tex').exists())
            return compiled, before, after

    def test_por_defecto_no_requiere_fuentes_presentacion_y_conserva_salidas(self):
        compiled, before, after = self.ejecutar([])
        self.assertEqual(compiled, ['reporte'])
        self.assertNotEqual(before['pdf/reporte.pdf'], after['pdf/reporte.pdf'])
        for name in ('pdf/presentacion.pdf', 'web/presentacion/index.html'):
            self.assertEqual(before[name], after[name])

    def test_verificar_reporte_no_compila_ni_modifica(self):
        compiled, before, after = self.ejecutar(['--verificar'])
        self.assertEqual(compiled, [])
        self.assertEqual(before, after)

    def test_presentacion_requiere_opcion_explicita(self):
        compiled, before, after = self.ejecutar(['--con-presentacion'], presentacion=True)
        self.assertEqual(compiled, ['presentacion', 'reporte'])
        self.assertNotEqual(before['pdf/presentacion.pdf'], after['pdf/presentacion.pdf'])
        self.assertIn(b'referencias:inicio', after['web/presentacion/index.html'])

    def test_fallo_conserva_los_entregables(self):
        _, before, after = self.ejecutar([], fallo=True)
        self.assertEqual(before, after)

    def test_solo_presentacion(self):
        compiled, before, after = self.ejecutar(['--solo-presentacion'], presentacion=True)
        self.assertEqual(compiled, ['presentacion'])
        self.assertNotEqual(before['pdf/presentacion.pdf'], after['pdf/presentacion.pdf'])
        self.assertEqual(before['pdf/reporte.pdf'], after['pdf/reporte.pdf'])
        self.assertIn(b'referencias:inicio', after['web/presentacion/index.html'])

    def test_limpiar_elimina_build(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / '.build'
            build.mkdir()
            (build / 'temp.txt').write_text('temp', encoding='utf-8')
            with patch.object(compilar, 'ROOT', root), patch('sys.argv', ['compilar.py', '--limpiar']), contextlib.redirect_stdout(io.StringIO()):
                compilar.main()
            self.assertFalse(build.exists())

    def test_verificar_falla_si_falta_recurso(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('datos/datos.md', 'datos/referencias.json', 'documentos/reporte.tex'):
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(compilar.ROOT / name, root / name)
            with patch.object(compilar, 'ROOT', root), patch('sys.argv', ['compilar.py', '--verificar']), self.assertRaises(FileNotFoundError):
                compilar.main()

    def test_modo_entrega_detecta_pendientes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('datos/datos.md', 'datos/referencias.json', 'documentos/reporte.tex'):
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(compilar.ROOT / name, root / name)
            for name in ('isotipo-azul.png', 'logo-facultad.png', 'acreditacion.png'):
                p = root / 'assets/institucional' / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.touch()
            (root / 'assets/fuentes').mkdir(parents=True, exist_ok=True)
            (root / 'assets/fuentes/firma.otf').touch()
            with patch.object(compilar, 'ROOT', root), patch('sys.argv', ['compilar.py', '--modo-entrega']), self.assertRaisesRegex(ValueError, 'Modo entrega activado'):
                compilar.main()
