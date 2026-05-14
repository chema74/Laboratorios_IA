import unittest

from privacidad.minimizador_contexto import minimizar_contexto


class TestMinimizadorContexto(unittest.TestCase):
    def test_elimina_campos_sensibles(self):
        p = {"caso_uso": "x", "texto": "ok", "email": "a@x.local"}
        r = minimizar_contexto(p)
        self.assertNotIn("email", r["contexto_minimizado"])


if __name__ == "__main__":
    unittest.main()
