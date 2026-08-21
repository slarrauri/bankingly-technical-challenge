
## Decision 007 — Architecture approach

**Decisión:** implementar el PoC como un **modular monolith** con un Agent Harness explícito.

**Motivo:** priorizar velocidad, legibilidad y validación del workflow sobre complejidad operacional.

**Principio:** los límites arquitectónicos deben existir aunque todavía no sean servicios independientes.

**Trade-off:** menor aislamiento operacional que una arquitectura de microservices, a cambio de menor complejidad y mayor velocidad durante la validación.

---

## Decision 008 — LLM responsibility boundary

**Decisión:** el LLM será responsable de planificación, selección de tools, interpretación de evidencia y generación de recomendaciones.

El código será responsable de:

- autorización;
    
- validación;
    
- estado;
    
- approval gates;
    
- ejecución;
    
- audit trail.
    

**Motivo:** tratar el LLM como componente probabilístico y no como autoridad de seguridad.

---

## Decision 009 — Deterministic computation

**Decisión:** cálculos financieros y métricas transaccionales serán realizados por código/tools determinísticas, no por el LLM.

**Motivo:** reducir errores y mejorar reproducibilidad.

Ejemplo:

```text
Transaction data
      ↓
Python / SQL
      ↓
Transaction summary
      ↓
LLM reasoning
```

No:

```text
Transaction data
      ↓
LLM
      ↓
"Volume increased 347%"
```

---

## Decision 010 — Structured agent contract

**Decisión:** el agente utilizará structured outputs validados por código.

**Motivo:** permitir validación, persistencia, evaluación y trazabilidad de las recomendaciones.

---

## Decision 011 — Closed action vocabulary

**Decisión:** las acciones posibles estarán restringidas a un conjunto cerrado:

`CLOSE_ALERT`, `ESCALATE_ALERT`, `REQUEST_INFORMATION`.

**Motivo:** reducir superficie de riesgo y hacer explícito el límite funcional del PoC.

---

## Decision 012 — Evidence traceability

**Decisión:** las conclusiones del agente deberán vincularse con referencias estructuradas a los datos utilizados.

**Motivo:** permitir evaluación de grounding, auditabilidad y explicación de las recomendaciones.

---

## Decision 013 — No execution capability in the agent

**Decisión:** el LLM no tendrá acceso directo a herramientas de ejecución.

**Motivo:** separar completamente recomendación de ejecución y garantizar Human-in-the-Loop mediante arquitectura.

---

## Decision 014 — Insufficient evidence is a valid outcome

**Decisión:** el agente podrá concluir que la información disponible no permite recomendar el cierre o escalamiento.

**Motivo:** evitar que el sistema fuerce una decisión cuando la evidencia es insuficiente.

---
