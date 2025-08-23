# Reglas de Cursor para AuditE

Este directorio contiene las reglas de Cursor que explican cómo trabajar en el proyecto AuditE.

## 📋 Reglas Creadas

### 1. `00-overview-rapido.mdc` (Siempre aplicada)
**Resumen rápido** del proyecto completo. Lee esto primero.

### 2. `01-proyecto-estructura.mdc` (Siempre aplicada)  
**Estructura detallada** del proyecto, qué está activo vs experimentos.

### 3. `02-apis-funcionales.mdc` (Siempre aplicada)
**Lista completa de APIs** que funcionan vs las que están rotas.

### 4. `03-desarrollo-guidelines.mdc` (Siempre aplicada)
**Guías de desarrollo** y buenas prácticas para trabajar seguro.

### 5. `04-autodiagnostico-core.mdc` (Siempre aplicada)
**Documentación específica** del módulo principal del proyecto.

### 6. `05-plan-implementacion-workflow.mdc` (Siempre aplicada)
**Workflow obligatorio** para seguir el plan de implementación paso a paso.

### 7. `06-reglas-desarrollo-audite.mdc` (Siempre aplicada)
**Reglas específicas** de desarrollo que deben cumplirse en AuditE.

### 8. `07-marcado-tareas-obligatorio.mdc` (Manual)
**Protocolo obligatorio** para marcar tareas como completadas en el plan.

## 🎯 Objetivo de las Reglas

Estas reglas aseguran que cualquier IA que trabaje en este proyecto entienda:

1. **Lo que realmente funciona** vs experimentos
2. **Cómo está estructurado** el código y las APIs
3. **Qué se puede modificar** sin romper el sistema
4. **Cuáles son las mejores prácticas** para este proyecto específico
5. **Cómo seguir el plan** de implementación paso a paso
6. **Cómo marcar correctamente** las tareas completadas

## 🚀 Workflow de Desarrollo OBLIGATORIO

### ANTES de cualquier tarea:
1. ✅ Leer el [plan de implementación](../PLAN_IMPLEMENTACION_FORMULARIOS_INDUSTRIA.md)
2. ✅ Identificar la tarea específica y sus prerequisitos
3. ✅ Verificar que se puede proceder
4. ✅ Entender las especificaciones técnicas

### DESPUÉS de cualquier implementación:
1. ✅ Probar la funcionalidad completamente
2. ✅ Verificar compatibilidad con sistema actual
3. ✅ Marcar tarea como `[x]` en el plan
4. ✅ Documentar observaciones

## 🚫 Reglas Críticas

- **NUNCA** saltar tareas sin completar prerequisitos
- **NUNCA** marcar como completa una tarea que no funciona
- **SIEMPRE** consultar el plan antes de implementar
- **SIEMPRE** mantener compatibilidad con sistema actual

## ✅ Flujo Principal Funcional

```
Home → /diagnostico → AutodiagnosticoPage → Sugerencias
      ↓
Panel Admin (/admin) → Gestión de preguntas/respuestas
      ↓
🆕 NUEVO: Formularios por Industria (según plan)
```

## 🔗 Referencias Clave

- **Plan principal:** [PLAN_IMPLEMENTACION_FORMULARIOS_INDUSTRIA.md](../PLAN_IMPLEMENTACION_FORMULARIOS_INDUSTRIA.md)
- **Sistema actual funcional:** [src/config/api.ts](../audite-frontend-explorer/src/config/api.ts)
- **Regla de oro:** Si no está enlazado desde Home.tsx o no usa APIs de config/api.ts, probablemente es un experimento 