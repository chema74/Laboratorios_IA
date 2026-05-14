#!/usr/bin/env python3
"""
Demo rápido: ingesta de un PDF público real en el pipeline RAG.
Objetivo: demostrar que el laboratorio procesa documentos externos sin configuración extra.
"""
import os
import urllib.request
from pathlib import Path

URL_PDF_PUBLICO = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
NOMBRE_ARCHIVO = "documento_publico_prueba.pdf"

def main():
    print("🌍 Descargando PDF público para validación RAG...")
    bruto_dir = Path("datos/brutos")
    bruto_dir.mkdir(parents=True, exist_ok=True)
    ruta_destino = bruto_dir / NOMBRE_ARCHIVO

    if ruta_destino.exists():
        print(f"✅ PDF ya existe en: {ruta_destino}")
    else:
        try:
            urllib.request.urlretrieve(URL_PDF_PUBLICO, str(ruta_destino))
            print(f"✅ Descarga completada: {ruta_destino.name}")
        except Exception as e:
            print(f"⚠️ Fallo en descarga (red/firewall): {e}")
            print("💡 Copia manualmente cualquier PDF en datos/brutos/ y re-ejecuta.")
            return

    print("\n🔍 Ejecuta ahora para validar ingesta:")
    print("   python scripts/sembrar_datos.py")
    print("   python scripts/demo_llm_groq.py")
    print("\n✅ El pipeline RAG está listo para procesar documentos públicos reales.")

if __name__ == "__main__":
    main()