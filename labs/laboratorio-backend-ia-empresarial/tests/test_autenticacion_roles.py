import unittest

from seguridad.autenticacion_ficticia import autenticar
from seguridad.autorizacion_roles import autorizar


class TestAuthRoles(unittest.TestCase):
    def test_permite_y_bloquea(self):
        usuarios = [{"usuario": "u", "rol": "tecnico_ia", "token_ficticio": "t"}]
        a = autenticar("u", "t", usuarios)
        self.assertTrue(a["ok"])
        self.assertFalse(autorizar("tecnico_ia", "privacidad")["ok"])


if __name__ == "__main__":
    unittest.main()
