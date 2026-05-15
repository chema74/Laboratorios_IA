# Informe de Clasificación de Sensibilidad de Datos Sintéticos

Fecha de generación: 2026-05-10T20:05:09

## Resumen ejecutivo
Clasificación local de sensibilidad en registros sintéticos para aplicar minimización, enmascarado y revisión defensiva.

## Total de registros analizados
4

## Distribución por sensibilidad
- dato personal sintético: 1
- credencial ficticia: 1
- secreto ficticio: 1
- financiero sintético: 1

## Registros que requieren minimización
- DS-001 - dato personal sintético
- DS-002 - credencial ficticia
- DS-003 - secreto ficticio

## Registros que requieren enmascarado
- DS-001 - dato personal sintético
- DS-002 - credencial ficticia
- DS-003 - secreto ficticio
- DS-004 - financiero sintético

## Registros que requieren revisión humana
- DS-002 - credencial ficticia
- DS-003 - secreto ficticio

## Acciones defensivas recomendadas
- enmascarar_y_minimizar: 1
- bloquear_y_revisar: 2
- enmascarar: 1

## Lectura técnica defensiva
Los marcadores de secreto o credencial ficticia elevan criticidad y activan bloqueo con revisión humana.

## Límites del clasificador
Reglas simples por placeholders sintéticos; no aplica a datos reales ni operación productiva.

## Recomendaciones siguientes
1. Ajustar reglas por contexto de negocio sintético.
2. Integrar salida con políticas del proyecto 06.
3. Cruzar hallazgos con informe defensivo del proyecto 09.

##  Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
(c) 2026 - Txema Ríos. Todos los derechos compartidos.

