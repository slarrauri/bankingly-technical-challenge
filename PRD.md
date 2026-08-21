# 📋 Product Requirements Document (PRD) — AML Alert Investigation Copilot

> **Producto:** AML Alert Investigation Copilot (Copiloto Agéntico de Cumplimiento)  
> **Cliente / Entorno de Referencia:** Banco Río Sur (Banca Múltiple, LATAM) y Plataforma Multi-Entidad Bankingly  
> **Autor:** Sebastián Larrauri — Technical Product Manager  
> **Versión:** 1.0 (PoC Baselined)  
> **Metodología:** Spec-Driven Development (SDD) & Enterprise AI Governance

---

## 1. Elección del Caso de Uso y Justificación Estratégica

### 1.1 El Problema en el Contexto Bancario Latinoamericano
Las más de 100 instituciones financieras atendidas por Bankingly en América Latina (bancos medianos, cooperativas de crédito y microfinancieras) enfrentan un crecimiento exponencial en el volumen de transacciones digitales y un endurecimiento de la regulación de Prevención de Lavado de Activos y Financiamiento del Terrorismo (AML/CFT).

Hoy, el proceso de investigación de alertas de monitoreo transaccional es **manual, lento y fragmentado**:
- Un analista de cumplimiento humano invierte entre **15 y 25 minutos por alerta**, consultando manualmente de 4 a 6 pantallas distintas (Core bancario, CRM/KYC, buró de crédito, historial de alertas previas y manuales de políticas internas).
- El **90% al 95% de las alertas resultan ser falsos positivos** legítimos (ej. importadores que estacionalmente compran inventario, profesionales con consultorías del exterior, transferencias familiares justificadas).
- La fatiga de alertas genera **riesgo de omisión de casos reales graves (falsos negativos)**, exponiendo a la entidad a sanciones regulatorias millonarias y daño reputacional.

### 1.2 Por qué este caso primero: Impacto, Esfuerzo y Riesgo
Evaluamos el caso bajo una matriz de decisión rigurosa:

```
┌────────────────────────────────────────────────────────────────────────┐
│             MATRIZ DE EVALUACIÓN DE CASOS DE USO AGÉNTICOS              │
│                                                                        │
│  Caso de Uso        Impacto   Esfuerzo   Riesgo Reg.   Ajuste Agéntico │
│  ────────────────────────────────────────────────────────────────────  │
│  ⭐ AML Copilot       ALTO      MEDIO     CONTROLADO     EXCELENTE      │
│  • Solicitud Crédito ALTO      ALTO      ALTO           MEDIO (Scoring)│
│  • Verificación KYC  MEDIO     MEDIO     MEDIO          BAJO (Doc OCR) │
│  • Cobranza Temprana MEDIO     MEDIO     ALTO (Cliente) MEDIO (Outbound)│
│  • Riesgo Portafolio ALTO      MUY ALTO  MEDIO          BAJO (BI/Dash) │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Impacto de Negocio Inmediato:** Reducción del tiempo de investigación de 15 minutos a <2 minutos por alerta (**85% de ahorro de tiempo operativo**), permitiendo a instituciones financieras medianas multiplicar su capacidad de procesamiento sin incrementar plantilla linealmente.
2. **Ajuste Agéntico Ideal:** A diferencia de una simple consulta conversacional, investigar una alerta requiere que el agente determine qué fuentes consultar, invoque herramientas de lectura estructuradas, correlacione variables dispersas, detecte inconsistencias y emita un dictamen fundamentado en políticas.
3. **Frontera de Seguridad y Human-in-the-Loop:** Permite una separación física limpia entre la propuesta investigativa del agente y la decisión final de la persona humana. El riesgo regulatorio es mitigado porque la IA **nunca cierra, congela ni reporta una cuenta de forma autónoma**.
4. **Despliegue a Decenas de Instituciones (Multi-Tenant):** La arquitectura desacopla el motor agéntico del esquema de políticas y fuentes de cada entidad mediante el identificador `institution_id` y contratos de herramientas estandarizados.

### 1.3 Alternativas Descartadas y Trade-offs
- **Revisión de Solicitudes de Crédito:** Descartada porque frecuentemente deriva en un modelo tradicional de *Credit Scoring* o reglas de motor de decisión, reduciendo el valor de la arquitectura agéntica e introduciendo alta sensibilidad en modelos de discriminación no explicable.
- **Verificación de KYC:** Descartada porque tiende a convertirse en un ejercicio de procesamiento de documentos y OCR de cédulas/pasaportes, desviando el foco de la capacidad de razonamiento e investigación multi-herramienta.
- **Cobranza Temprana (*Early Collections*):** Descartada por implicar interacción directa de cara al cliente final (*customer-facing*), incrementando el riesgo de reputación y fricción comunicacional para un primer PoC interno.
- **Monitoreo de Riesgo de Portafolio:** Descartada por su excesiva amplitud macroeconómica, corriendo el riesgo de construir un *dashboard* analítico con resúmenes en texto en vez de un flujo operativo transaccional.

### 1.4 Justificación de No-Contrapropuesta
La directriz estratégica ejecutiva de Bankingly (*"Banca agéntica interna con aprobación humana obligatoria"*) es óptima. Presentar una contrapropuesta exótica habría sacrificado la profundidad del arnés de seguridad, la calidad del benchmark y la robustez del prototipo a cambio de originalidad superficial.

---

## 2. Usuarios y Personas

### Persona Principal: Analista de Cumplimiento / AML
- **Nombre:** Andrea Silva (32 años).
- **Rol:** Analista Senior de Prevención de Lavado de Activos en Banco Río Sur.
- **Responsabilidades:** Revisar 40 a 60 alertas diarias en cola; recopilar antecedentes; contrastar con políticas del Banco Central; redactar justificaciones de cierre por falso positivo o elaborar Reportes de Operación Sospechosa (ROS/SAR).
- **Puntos de Dolor:** Fatiga visual por saltar entre aplicaciones legado; pérdida de tiempo calculando ratios financieros; estrés por el riesgo de firmar un falso positivo que resulte ser lavado real.
- **Necesidad Clave:** Un asistente inteligente que le presente el expediente sintetizado con toda la evidencia probatoria ya organizada y una sugerencia de acción clara, requiriendo únicamente su validación experta.

### Roles Secundarios
- **Oficial de Cumplimiento (Compliance Officer / Auditor):** Requiere trazabilidad absoluta (`audit_events`) de por qué se tomó cada decisión y qué evidencias sustentaron la recomendación de la IA.
- **Administrador de TI / Seguridad:** Requiere garantías de que el LLM no tiene acceso de escritura directo a la base de datos y que cada institución está aislada lógicamente (`institution_id`).

---

## 3. Alcance del Producto (Scope)

```
┌────────────────────────────────────────────────────────────────────────┐
│                         ALCANCE DEL MVP vs. ROADMAP                    │
│                                                                        │
│  [ DENTRO DEL ALCANCE - MVP PoC ]                                      │
│  ✔ Investigación automatizada de alerta individual mediante 6 tools    │
│  ✔ Correlación de perfil KYC vs. volumen transaccional histórico (30d) │
│  ✔ Evaluación determinista de 4 políticas institucionales (P-001..P-004)│
│  ✔ Generación de recomendación estructurada Pydantic v2 (CLOSE/ESCALATE)│
│  ✔ Detección explícita de información faltante y limitaciones           │
│  ✔ Aprobación humana obligatoria en código antes de ejecución (INV-002)│
│  ✔ Consola analista web interactiva con confirmación modal             │
│  ✔ Benchmark de 25 casos con métricas de exactitud y seguridad         │
│                                                                        │
│  [ FUERA DEL ALCANCE - VERSIONES FUTURAS ]                             │
│  ✖ Cierre autónomo o bloqueo de cuentas sin intervención humana        │
│  ✖ Integración en reales                 │
│  ✖ Consulta en tiempo real a listas de sanciones internacionales OFAC  │
│  ✖ Triage desatendido de colas masivas sin supervisión                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Requisitos Priorizados

### Requisitos Funcionales (FR)
- **FR-01 (Investigación Guiada por Herramientas - P1):** El sistema debe orquestar la llamada secuencial a 6 herramientas de lectura (`get_alert`, `get_customer_profile`, `get_transactions`, `get_transaction_summary`, `get_previous_alerts`, `get_aml_policies`).
- **FR-02 (Cálculo Financiero Determinista - P1):** Las sumatorias, variaciones porcentuales y ratios de ingresos deben ser calculados exclusivamente por código determinista Python/SQL, nunca por el LLM.
- **FR-03 (Esquema Estructurado Pydantic - P1):** La salida del agente debe conformarse estrictamente al esquema `InvestigationResult` (resumen ejecutivo, nivel de riesgo, score de confianza, findings con fuentes, información faltante, políticas aplicadas y acción sugerida).
- **FR-04 (Compuerta de Aprobación Humana - P1):** Ninguna acción con efectos (`CLOSE_ALERT`, `ESCALATE_ALERT`, `REQUEST_INFORMATION`) podrá ejecutarse sin la previa persistencia de un registro `Approval` firmado por un analista autorizado (`ANA-xxxx`).
- **FR-05 (Máquina de Estados Finita - P1):** El ciclo de vida de la investigación debe transitar legalmente por: `CREATED → INVESTIGATING → RECOMMENDATION_READY → AWAITING_APPROVAL → APPROVED/REJECTED → EXECUTED`.
- **FR-06 (Manejo de Incertidumbre y Datos Faltantes - P2):** Si el expediente carece de documentos indispensables (ej. facturas o KYC desactualizado), el agente debe declarar explícitamente la limitación y sugerir `REQUEST_INFORMATION`.
- **FR-07 (Inmunidad a Inyecciones de Prompt - P2):** Cualquier texto ingresado en el concepto de una transacción debe ser tratado como dato literal inerte sin capacidad de alterar el flujo de ejecución.
- **FR-08 (Auditoría Inmutable - P2):** Todo evento (inicio, llamado de tools, recomendación, aprobación y ejecución) debe persistirse en la tabla `audit_events`.

### Requisitos No Funcionales (NFR)
- **NFR-01 (Seguridad y Confinamiento):** Tasa de ejecuciones no autorizadas igual a **0.0%** bajo cualquier circunstancia.
- **NFR-02 (Aislamiento Multi-Tenant):** Toda consulta a la base de datos debe filtrar obligatoriamente por el encabezado `X-Institution-Id`.
- **NFR-03 (Tiempo de Respuesta):** La investigación completa y generación del informe debe completarse en **< 5 segundos** para la experiencia interactiva del analista.
- **NFR-04 (Confiabilidad y Reintentos):** En caso de error de validación JSON del LLM, el arnés debe reintentar hasta 2 veces con feedback del error antes de fallar de manera controlada.

---

## 5. Criterios de Aceptación (Given-When-Then)

```gherkin
Escenario 1: Flujo Exitoso de Investigación y Aprobación
  Dado que existe una alerta abierta "AML-0012" del cliente Martín Pereira en Banco Río Sur
  Cuando el analista hace clic en "Investigar con Copilot"
  Entonces el arnés recolecta la evidencia desde las 6 herramientas de lectura
  Y el agente produce un informe con nivel de riesgo ALTO, recomendación ESCALATE_ALERT y hallazgos fundamentados
  Y el estado de la investigación pasa a AWAITING_APPROVAL sin alterar el estado de la alerta en la base de datos
  Cuando el analista revisa el informe y hace clic en "Aprobar y Ejecutar"
  Entonces el sistema registra la firma del analista y actualiza la alerta a ESCALATED_SAR con evento de auditoría.

Escenario 2: Intento de Ejecución No Autorizada Bloqueado por Código
  Dado que una investigación se encuentra en estado RECOMMENDATION_READY o AWAITING_APPROVAL
  Cuando se envía una petición POST /api/v1/investigations/{id}/execute sin registro previo de aprobación
  Entonces el sistema rechaza la petición con código HTTP 400 y mensaje UnapprovedExecutionError
  Y el estado de la alerta en base de datos permanece intacto.
```

---

## 6. Cierre de Producto

### 6.1 Visión a 12 Meses
Convertir al Copiloto de AML en el **estándar de la industria para las más de 100 instituciones de la red Bankingly**, evolucionando desde un asistente de investigación reactivo hacia un **Centro de Operaciones de Cumplimiento Agéntico** capaz de realizar triage continuo, detección predictiva de redes de lavado y generación automática de expedientes regulatorios oficiales.

### 6.2 Roadmap en 3 Etapas

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ROADMAP DE PRODUCTO (12 MESES)                  │
│                                                                        │
│  [ ETAPA 1: MESES 1 - 3 ]  ──▶ PoC a Piloto Productivo                 │
│  • Conexión de conectores Core Bancario estándar de Bankingly (REST).  │
│  • Piloto controlado con 3 bancos seleccionados (10 analistas).        │
│  • Calibración fina de políticas institucionales y umbrales por país.  │
│                                                                        │
│  [ ETAPA 2: MESES 4 - 7 ]  ──▶ Triage Inteligente & Multi-Entidad      │
│  • Pre-clasificación y priorización automática de colas de alertas.    │
│  • Módulo de generación automática de borradores de ROS/SAR regulatorios.│
│  • Soporte multi-jurisdicción (Uruguay, México, Colombia, Perú).       │
│                                                                        │
│  [ ETAPA 3: MESES 8 - 12 ] ──▶ Ecosistema Agéntico Autónomo Supervisado│
│  • Agente de Monitoreo Continuo y Detección de Redes Complejas (Grafos)│
│  • Copiloto de Auditoría para reguladores e inspectores externos.      │
│  • Despliegue masivo en el SaaS multi-tenant de Bankingly.             │
└────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Esqueleto de Business Case & ROI

```
┌────────────────────────────────────────────────────────────────────────┐
│                       MODELO FINANCIERO ESTIMADO                       │
│                                                                        │
│  Parámetros de una Institución Financiera Mediana (LATAM):             │
│  • Volumen de alertas mensuales: 2,500 alertas.                        │
│  • Tiempo promedio actual por investigación: 18 minutos.               │
│  • Costo analista cumplimiento: USD 22.00 / hora.                      │
│                                                                        │
│  Situación Actual (Sin Copiloto):                                      │
│  • 2,500 alertas * 0.30 hs = 750 horas-hombre mensuales.               │
│  • Costo operativo mensual: 750 hs * USD 22 = USD 16,500 / mes.        │
│                                                                        │
│  Situación con AML Copilot (85% Ahorro de Tiempo):                     │
│  • Tiempo por alerta con IA: 2.5 minutos (0.041 hs).                   │
│  • 2,500 alertas * 0.041 hs = 104 horas-hombre mensuales.              │
│  • Costo operativo mensual de analistas: USD 2,288 / mes.              │
│  • Costo de inferencia LLM / Servidor: ~USD 120 / mes (USD 0.048/caso).│
│  • AHORRO NETO MENSUAL POR BANCO: USD 14,092 / mes (USD 169,104 / año) │
│                                                                        │
│  Oportunidad para Bankingly (Pricing SaaS):                             │
│  • Tarifa SaaS: USD 3,500 / mes por institución financiera.            │
│  • Con 25 instituciones en Año 1: ARR de USD 1,050,000.                │
│  • ROI para el banco: 302% anual (Payback < 3 meses).                  │
└────────────────────────────────────────────────────────────────────────┘
```

### 6.4 Matriz de Riesgos y Mitigaciones

| Riesgo Identificado | Nivel | Mitigación Arquitectónica / de Producto |
|---|:---:|---|
| **Alucinación de datos financieros en el dictamen** | Crítico | Cálculos numéricos delegados 100% a servicios deterministas en Python/SQL (ADR-005). Extracción forzada contra Pydantic con validación de fuentes. |
| **Aprobación descuidada ("Automation Bias")** | Alto | El frontend exige al analista abrir el modal de confirmación con el resumen de hallazgos y permite agregar notas de discrepancia antes de firmar. |
| **Inyección de instrucciones en transferencias** | Alto | Sanitización de entradas, paso de variables desacopladas en el prompt y ausencia total de herramientas de mutación para el LLM. |
| **Rechazo o desconfianza de inspectores regulatorios** | Medio | Explicabilidad completa: cada hallazgo cita IDs de transacción y artículos de política aplicables; registro inmutable en `AuditEvent`. |

### 6.5 Criterios Go / No-Go y Protocolo de Reversión (Rollback)

#### Criterios Go / No-Go para Fase Productiva
1. **Seguridad (No-Go Bloqueante):** Tasa de acciones no autorizadas = 0.0% en suite de pruebas automatizadas.
2. **Precisión de Recomendaciones:** Accuracy ≥ 85% y Grounding de evidencia ≥ 95% sobre el benchmark extendido de 100 casos.
3. **Disponibilidad y Latencia:** p95 de respuesta de investigación < 4 segundos.
4. **Validación de Compliance:** Aprobación formal del Oficial de Cumplimiento del banco piloto sobre la estructura de explicabilidad de los reportes.

#### Protocolo de Reversión y Fallback Seguro
- **Feature Flag Instantáneo:** En caso de degradación del proveedor de LLM o anomalía de servicio, la plataforma conmuta mediante un *feature toggle* al modo tradicional de revisión manual sin interrumpir el acceso a la cola de alertas del Core bancario.
- **Rollback de Esquemas:** Migraciones de base de datos idempotentes y desacopladas; los estados de auditoría histórica permanecen preservados sin afectar la continuidad operativa.
