import unittest

from colas.jobs_locales import ejecutar_job


class TestJobsLocales(unittest.TestCase):
    def test_procesa_tarea(self):
        r = ejecutar_job("revision_privacidad", {"traza_id": "T1"})
        self.assertEqual(r["resultado"], "ok")


if __name__ == "__main__":
    unittest.main()
