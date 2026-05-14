# 06 - Políticas de Uso de Agente (V1 local funcional mínima)

## Objetivo
Evaluar casos sintéticos de uso de agentes contra políticas internas ficticias de seguridad defensiva.

## Funcionalidad implementada en V1
- Validación de casos y políticas en formato JSON.
- Activación de política aplicable por reglas locales.
- Decisión defensiva: permitir, bloquear o revisar.
- Detección de incumplimientos simulados.
- Generación de registros JSON por caso.
- Resúmenes por política y por decisión.
- Generación de informe Markdown y JSON consolidado.

## Ejecución
```powershell
python .\proyectos\06-politicas-uso-agente\src\evaluador_politicas_uso.py --cases .\proyectos\06-politicas-uso-agente\datos_ejemplo\casos_uso_agente_sinteticos.json --policies .\proyectos\06-politicas-uso-agente\datos_ejemplo\politicas_uso_agente.json --output-md .\proyectos\06-politicas-uso-agente\informes\informe_politicas_uso_agente.md --output-json .\proyectos\06-politicas-uso-agente\informes\resultado_politicas_uso_agente.json --registry-dir .\proyectos\06-politicas-uso-agente\registros
```

## Separación V1 y V2
- V1: evaluación local sin IA real, sin APIs externas y sin cloud.
- V2 futura (no implementada): APIs gratuitas opcionales gestionadas por `.env`, con fallback local.

## 🪪 Licencia y Autoría
Publicado bajo licencia Creative Commons CC BY-SA 4.0 International.  
© 2025 – Txema Ríos. Todos los derechos compartidos.
