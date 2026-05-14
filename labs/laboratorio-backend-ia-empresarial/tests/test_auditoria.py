import unittest

from auditoria.registro_peticiones import registrar_peticion
from auditoria.trazabilidad import resumen_trazas


class TestAuditoria(unittest.TestCase):
    def test_registra_trazabilidad(self):
        b = []
        registrar_peticion(b, {"estado": "ok"})
        resumen = resumen_trazas(b)
        self.assertEqual(resumen["total"], 1)


if __name__ == "__main__":
    unittest.main()
