import unittest
from pathlib import Path

from herramientas import compilacion as compilar

ROOT = Path(__file__).resolve().parents[1]


class CasosExigentesYRobustez(unittest.TestCase):
    def test_muchos_integrantes_y_titulo_largo(self):
        fields = {
            "Título": "Análisis comparativo de algoritmos distribuidos de consenso en redes de computadores de alta disponibilidad con tolerancia a fallas bizantinas",
            "Subtítulo": "Una propuesta de optimización mediante canales seguros asíncronos para sistemas tolerantes a particiones de red",
            "Título corto": "Consenso distribuido",
            "Institución": "Universidad Dr. Andrés Bello",
            "Facultad": "Facultad de Tecnología e Innovación",
            "Asignatura": "Sistemas Distribuidos Avanzados",
            "Docente": "Ing. Carlos Mendoza",
            "Grupo": "Grupo 01",
            "Lugar y fecha": "San Miguel, 16 de octubre de 2026",
            "Firma": "Jaime Berrios",
        }
        members = [
            ["Ana María Rodríguez Flores", "RF202201"],
            ["Carlos Eduardo Gómez Pérez", "GP202202"],
            ["Diana Beatriz Martínez Cruz", "MC202203"],
            ["Eduardo Antonio Hernández Ramos", "HR202204"],
            ["Flor de María López Sánchez", "LS202205"],
            ["Gerardo José Castillo Peña", "CP202206"],
            ["Héctor Manuel Navarro Rivas", "NR202207"],
        ]
        tex_output = compilar.render_tex(fields, members)
        self.assertIn(r"\newcommand{\TituloTrabajo}", tex_output)
        self.assertIn("Ana María Rodríguez Flores & RF202201", tex_output)
        self.assertIn("Héctor Manuel Navarro Rivas & NR202207", tex_output)

        refs = {
            "lamport": {
                "id": "lamport",
                "orden": "Lamport, L.",
                "autor_parentetico": "Lamport",
                "autor_narrativo": "Lamport",
                "anio": "1982",
                "referencia": "Lamport, L. (1982). *The Byzantine Generals Problem*. ACM.",
                "ejemplo": False,
            }
        }
        pendientes = compilar.detectar_pendientes(fields, members, refs)
        self.assertEqual(pendientes, [], "No debería haber pendientes con datos reales")

    def test_deteccion_pendientes_con_datos_ejemplo(self):
        fields, members = compilar.read_data()
        refs = compilar.leer_referencias(ROOT / "datos/referencias.json")
        pendientes = compilar.detectar_pendientes(fields, members, refs)
        self.assertTrue(len(pendientes) > 0)
        self.assertTrue(any("Título" in p for p in pendientes))
        self.assertTrue(any("Docente" in p for p in pendientes))
        self.assertTrue(any("Integrante" in p for p in pendientes))
        self.assertTrue(any("Bibliografía" in p for p in pendientes))

    def test_colortbl_cajanota_en_reporte(self):
        sty = (ROOT / "plantilla/latex/unab_reporte.sty").read_text(encoding="utf-8")
        self.assertIn(r"\RequirePackage{colortbl}", sty)
        self.assertIn(r"\newenvironment{cajanota}", sty)
        self.assertIn(r"\cellcolor{softgray}", sty)

    def test_listings_en_ambos_estilos(self):
        reporte_sty = (ROOT / "plantilla/latex/unab_reporte.sty").read_text(encoding="utf-8")
        pres_sty = (ROOT / "plantilla/latex/unab_presentacion.sty").read_text(encoding="utf-8")
        self.assertIn(r"\RequirePackage{listings}", reporte_sty)
        self.assertIn(r"\RequirePackage{listings}", pres_sty)
        self.assertIn("unabcode", reporte_sty)
        self.assertIn("unabcode", pres_sty)


if __name__ == "__main__":
    unittest.main()
