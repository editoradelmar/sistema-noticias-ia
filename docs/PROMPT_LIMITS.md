PROMPT LIMITS

Resumen

Este documento explica la configuración `MAX_PROMPT_CHARS` y la recomendación por defecto usada por el servicio de generación IA.

Configuración

- Variable: `MAX_PROMPT_CHARS`
- Archivo: `backend/config.py` (expuesta como Pydantic setting `MAX_PROMPT_CHARS`)
- Valor por defecto en el repositorio: 50000 caracteres

Motivación

1. Protección contra prompts excesivamente largos
   - Algunos proveedores de LLM rechazan o fallan con prompts muy largos.
   - Prompts largos implican mayor consumo de tokens (costos) y mayor latencia.

2. Evitar pérdida de contexto accidental
   - En lugar de eliminar silenciosamente items, el sistema concatena todos los `PromptItem` y `EstiloItem` (ordenados) y aplica truncado controlado al final.

Recomendación

- Mantener el valor por defecto (50000) en entornos de desarrollo y pruebas.
- En producción, ajustar según el modelo y plan de tokens:
  - Modelos con límites de contexto pequeños (ej. 8k tokens): usar valores más conservadores (10k-20k chars).
  - Modelos con contextos grandes (32k+ tokens): 50k-100k puede ser razonable, pero monitorizar consumo de tokens.

Operación y alertas

- Cuando el prompt exceda `MAX_PROMPT_CHARS`, el sistema truncará el prompt final y emitirá un log de advertencia con la longitud original.
- Se recomienda instrumentar alertas (logs/monitor) para detectar truncados frecuentes — esto indica que los items configurados son demasiado largos o que hace falta dividir el prompt.

Siguientes pasos

- Exponer `MAX_PROMPT_CHARS` vía variable de entorno en desplegables/CI para entornos de staging/production.
- Añadir métricas y contadores que lleven la cuenta de prompts truncados por semana para ajustar el valor según uso real.
