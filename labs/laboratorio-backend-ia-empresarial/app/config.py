from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_CONTRATOS = RAIZ / "datos" / "contratos_api.json"
RUTA_USUARIOS = RAIZ / "datos" / "usuarios_roles.json"
RUTA_PETICIONES = RAIZ / "datos" / "peticiones_backend.json"
RUTA_TAREAS = RAIZ / "datos" / "tareas_cola.json"
RUTA_MODULOS = RAIZ / "datos" / "modulos_ia_empresarial.json"
RUTA_INFORME = RAIZ / "informes" / "informe_backend_ia_empresarial.md"
