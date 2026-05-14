# Guía de Revisión Técnica

Documento operativo para revisar la V1 local integradora del repositorio `laboratorio-empresa-sintetica-ia` desde una perspectiva técnica de portfolio.

## 1. Validación inicial
Ejecutar desde la raíz del repositorio:

```powershell
python -m pytest .\proyectos -q
```

Interpretación esperada: la suite global valida consistencia funcional interna de los 10 proyectos en entorno local.

## 2. Ejecución de la demo final integradora
Ejecutar desde la raíz del repositorio:

```powershell
python .\proyectos\10-demo-narrativa-empresa-completa\ejecutar_demo.py --seed 42 --dias 7
```

## 3. Rutas clave de revisión
- Expediente final: `datos_ejemplo/demo_narrativa_empresa_completa/expediente_demo_empresa_completa.md`
- Guion de demo: `datos_ejemplo/demo_narrativa_empresa_completa/guion_demo.md`

## 4. Orden recomendado de revisión
1. Confirmar estado técnico global (tests).
2. Revisar expediente final de la demo integradora.
3. Revisar guion de demo para entender la secuencia narrativa.
4. Contrastar artefactos por módulo con `evidencias/INDICE_ARTEFACTOS_V1.md`.
5. Verificar coherencia entre entradas sintéticas, simulaciones y salidas documentales.

## 5. Cómo interpretar las evidencias
- Como evidencia de arquitectura modular y capacidad de integración local.
- Como demostración de reproducibilidad técnica en entorno controlado.
- Como material de portfolio para evaluación de diseño de sistemas sintéticos.
- Como base de discusión para futuras evoluciones V2, no como despliegue final.

## 6. Qué no debe interpretarse como real
- No son datos reales ni actividad de cliente real.
- No existe IA real operativa en producción.
- No existe API productiva ni dashboard productivo.
- No existe integración real con Google Workspace o Microsoft 365.
- No constituye auditoría legal real, predicción real, benchmark real ni recomendación empresarial real.
- No representa un sistema productivo.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
