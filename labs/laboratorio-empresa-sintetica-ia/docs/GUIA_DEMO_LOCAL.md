# Guía de Demo Local

## Estado actual del laboratorio
- V1 local integradora completada.
- 10 proyectos internos implementados.
- 70 tests pasando.
- Demo narrativa final disponible.
- Funciona en local.
- Sin datos reales.
- Sin APIs externas obligatorias.
- Sin claves.
- Sin servicios de pago.
- Sin IA funcional real todavía.
- Sin sistema productivo.

## Módulos incluidos
- `01-generador-empresa-sintetica`
- `02-simulador-eventos-negocio`
- `03-fabrica-documentos-sinteticos`
- `04-generador-escenarios-prueba-agentes`
- `05-motor-simulacion-crisis`
- `06-simulador-revision-humana`
- `07-gemelo-digital-operativo-ligero`
- `08-laboratorio-privacidad-datos-sinteticos`
- `09-comparador-agente-proceso`
- `10-demo-narrativa-empresa-completa`

## Comandos principales (PowerShell)
Ejecutar desde la raíz del repositorio:

```powershell
python -m pytest .\proyectos -q
python .\proyectos\10-demo-narrativa-empresa-completa\ejecutar_demo.py --seed 42 --dias 7
```

## Comandos de demo por proyecto (PowerShell)
```powershell
python .\proyectos\01-generador-empresa-sintetica\ejecutar_demo.py --seed 42 --empleados 12 --clientes 20 --productos 8
python .\proyectos\02-simulador-eventos-negocio\ejecutar_demo.py --seed 42 --dias 7 --eventos-por-dia 8
python .\proyectos\03-fabrica-documentos-sinteticos\ejecutar_demo.py --seed 42 --documentos-por-tipo 3
python .\proyectos\04-generador-escenarios-prueba-agentes\ejecutar_demo.py --seed 42 --escenarios-por-tipo 3
python .\proyectos\05-motor-simulacion-crisis\ejecutar_demo.py --seed 42 --crisis 5 --dias 10
python .\proyectos\06-simulador-revision-humana\ejecutar_demo.py --seed 42 --revisiones 20 --porcentaje-escalado 25
python .\proyectos\07-gemelo-digital-operativo-ligero\ejecutar_demo.py --seed 42 --dias 10
python .\proyectos\08-laboratorio-privacidad-datos-sinteticos\ejecutar_demo.py --seed 42 --max-datos 80
python .\proyectos\09-comparador-agente-proceso\ejecutar_demo.py --seed 42 --procesos 7
python .\proyectos\10-demo-narrativa-empresa-completa\ejecutar_demo.py --seed 42 --dias 7
```

## Salidas principales del proyecto 10
- `datos_ejemplo/demo_narrativa_empresa_completa/expediente_demo_empresa_completa.md`
- `datos_ejemplo/demo_narrativa_empresa_completa/guion_demo.md`

## Límites de esta demo
- No hay IA real ejecutándose en producción.
- No hay API productiva ni dashboard productivo.
- No hay datos reales ni cliente real.
- No hay integración real con Google Workspace o Microsoft 365.
- No hay benchmark real, predicción real ni recomendación empresarial real.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
