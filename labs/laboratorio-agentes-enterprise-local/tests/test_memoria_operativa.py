import unittest

from memoria.memoria_operativa import MemoriaOperativa


class TestMemoriaOperativa(unittest.TestCase):
    def test_registra_eventos(self):
        m = MemoriaOperativa()
        m.registrar({"tipo": "x"})
        self.assertEqual(len(m.consultar()), 1)


if __name__ == "__main__":
    unittest.main()
