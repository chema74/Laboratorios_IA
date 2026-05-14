import unittest

from evaluacion.evaluador_resultados import evaluar_resultado
from evaluacion.evaluador_trazabilidad import evaluar_trazabilidad


class TestEvaluacionResultados(unittest.TestCase):
    def test_evalua_resultado_trazabilidad_y_limites(self):
        r = {
            "ejecucion": {"resultados": [{}, {}, {}], "bloqueos": []},
            "trazas": [{}, {}, {}],
            "memoria": [{}, {}, {}],
        }
        ev = evaluar_resultado(r)
        tr = evaluar_trazabilidad(r)
        self.assertTrue(ev["resuelto"])
        self.assertTrue(ev["limites_respetados"])
        self.assertTrue(tr["suficiente"])


if __name__ == "__main__":
    unittest.main()
