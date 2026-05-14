import unittest

from privacidad.detector_pii import detectar_pii


class TestDetectorPII(unittest.TestCase):
    def test_detecta_email_telefono_identificador(self):
        t = "correo a@b.local telefono 612345678 id A12345678Z"
        out = detectar_pii(t)
        tipos = {x["tipo"] for x in out}
        self.assertIn("email", tipos)
        self.assertIn("telefono", tipos)
        self.assertIn("identificador", tipos)


if __name__ == "__main__":
    unittest.main()
