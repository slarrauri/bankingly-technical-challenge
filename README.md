# 🏦 AML Alert Investigation Copilot — Bankingly Technical Challenge

> **Technical Product Manager Challenge**  
> **Institución de Referencia:** Banco Río Sur (Uruguay / LATAM) & Red Multi-Entidad Bankingly  
> **Metodología:** Spec-Driven Development (SDD) & Enterprise AI Governance  
> **Estado:** PoC Funcional, Benchmark de 25 Casos Aprobado (0.0% Acciones No Autorizadas) & Documentación Baselined

---

> [!NOTE] Nota personal sobre el desarrollo
> Abordé este desafío técnico desde una perspectiva deliberadamente _time-boxed_: el objetivo fue evaluar cuánto podía construir, validar y documentar dentro del marco temporal establecido, priorizando las decisiones de producto, la arquitectura y la validación por sobre la búsqueda de una implementación completamente pulida.
> 
> Como consecuencia de esta restricción, quedaron pendientes algunas correcciones menores, incluyendo determinados bugs, alucinaciones del modelo y _typos_. Decidí no extender artificialmente el tiempo de desarrollo para corregirlos, ya que considero que respetar el marco temporal también forma parte de la capacidad que este ejercicio busca evaluar. El tiempo de trabajo puede verificarse mediante el historial de commits correspondiente al **20/08/2026**, considerando además dos pausas de aproximadamente 1,5 horas cada una.
> 
> Disfruté especialmente la realización del desafío porque, además del resultado concreto, me permitió obtener algunas lecciones interesantes. La principal es que, desde la perspectiva de un equipo de desarrollo de producto, **la documentación conceptual y arquitectónica que acompaña a una iniciativa puede resultar incluso más valiosa que el código generado durante una PoC**. El objetivo de una PoC no debería ser simplemente producir código, sino reducir incertidumbre y generar los elementos necesarios para que un equipo pueda convertir una idea validada en un producto real.
> 
> A partir de esta experiencia, también identifico una oportunidad para desarrollar una metodología específica para este tipo de iniciativas: un proceso que permita maximizar la velocidad de discovery y prototipado, minimizar el tiempo necesario para validar una hipótesis y, al mismo tiempo, estandarizar los entregables, decisiones, evaluaciones y documentación que reciben posteriormente los equipos de desarrollo.
> 
> En ese sentido, considero que el verdadero valor de este tipo de proceso está en **convertir una idea ambigua en una iniciativa suficientemente validada, documentada y estructurada como para que otro equipo pueda continuar el trabajo con la menor incertidumbre posible**.


> [!WARNING] Simulated Environment
> This implementation is a **proof of concept** developed exclusively for evaluation purposes. It does **not connect to any external banking, AML, KYC, payment, or third-party systems**.
> 
> All customers, counterparties, transactions, alerts, discovery and other data used in the prototype are **entirely fictitious and synthetically generated**. No real customer information, financial data, credentials, or production systems are involved.
> 
> The implementation should therefore **not be considered production-ready** and must not be used to make real financial, compliance, or customer decisions.

## 📑 Mapa de Entregables del Desafío

Este repositorio contiene todos los artefactos requeridos por las bases del ejercicio técnico:

| Entregable Requerido                        | Archivo / Ubicación                                                                          | Descripción                                                                                                                           |
| ------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Código y README Técnico**              | [`README.md`](README.md) (Este archivo)                                                      | Setup reproducible, arquitectura del agente (Harness vs LLM), ubicación de controles y registro de decisiones ADR.                    |
| **2. Intercambios con la IA (3 Momentos)**  | [`AI_INTERACTIONS.md`](AI_INTERACTIONS.md)                                                   | Transcripciones textuales exactas (prompt clave, error detectado y cambio de enfoque hacia arnés seguro).                             |
| **3. PRD de Producto Breve y Completo**     | [`docs/PRD.md`](PRD.md) & [`sdd/01-product-requirements.md`](sdd/01-product-requirements.md) | Problema, justificación, descarte de alternativas, multi-tenant para 100+ bancos, visión 12 meses, roadmap, business case y Go/No-Go. |
| **4. Resultados de Evaluaciones (Evals)**   | [`EVALUATION_REPORT.md`](EVALUATION_REPORT.md)                                               | Benchmark de 25 casos, métricas vs umbrales, análisis de modos de falla (EVAL-006, EVAL-008, EVAL-011) y seguridad.                   |
| **6. Invariantes de Seguridad del Sistema** | [`INVARIANTS.md`](INVARIANTS.md)                                                             | 10 reglas de seguridad no negociables garantizadas por código y verificadas con tests automatizados.                                  |
| **7. Definiciones Poc**                     | [`sdc/PoC`](sdc/PoC)                                                                         | Documentacion, datos y flujo de pensamiento para el desarrollo de este ejecicio.                                                      |
| **7. GUIAS SDD**                            | [`sdc/SDD-DOCS`](sdc/SDD-DOCS)                                                               | Guías para el desarrollo del ejercicio siguiendo la metodología de Spec-Driven Development                                            |
| **7. AI Flows**                             | [`sdc/implementation-plans`](sdc/implementation-plans)                                       | Prompts de entrada y documentos de salida provisto por la AI                                                                          |

---

## 1. Resumen Ejecutivo y Problema

En las instituciones financieras de América Latina, los analistas de cumplimiento (*Compliance / AML Analysts*) invierten entre **15 y 25 minutos por alerta**, consultando manualmente múltiples fuentes fragmentadas (Core bancario, KYC, transferencias, políticas y buró) para resolver alertas de monitoreo transaccional. Más del **90% resultan ser falsos positivos**, lo que provoca fatiga operativa y eleva el riesgo de omitir esquemas reales de lavado de activos.

El **AML Alert Investigation Copilot** es un agente interno de IA que:
1. **Recopila evidencia estructurada** de forma determinista mediante 6 herramientas de solo lectura.
2. **Correlaciona** el perfil KYC con el comportamiento transaccional reciente (30 días).
3. **Evalúa deterministamente** las políticas de AML de la entidad (`P-001` a `P-004`).
4. **Formula una propuesta estructurada** con hallazgos probatorios, nivel de riesgo, score de confianza y acción recomendada (`CLOSE_ALERT`, `ESCALATE_ALERT`, `REQUEST_INFORMATION`).
5. **Garantiza la supervisión humana estricta (*Human-in-the-Loop*)**: El agente **NUNCA** ejecuta mutaciones autónomas. Todo cambio de estado bancario requiere aprobación explícita de un analista humano verificada a nivel de código.

```
                           FLUJO DE INVESTIGACIÓN Y CONTROL
   Alerta Seleccionada ──▶ Agente Recolecta Evidencia ──▶ Evalúa Políticas ──┐
                                                                              │
   Acción Ejecutada ◀── Humano Aprueba/Rechaza ◀── Formula Recomendación ─────┘
```

---

## 2. Arquitectura del Agente: Trusted Harness vs. Untrusted LLM

El sistema está diseñado bajo el principio de **Frontera de Seguridad Explícita** (*Trusted Application Harness vs. Untrusted Probabilistic LLM*), implementado como un **Monolito Modular de 5 Capas** en **Python / FastAPI / SQLAlchemy / Pydantic v2**:

```
                    TRUSTED vs. UNTRUSTED BOUNDARY
 
    [ UNTRUSTED AI AGENT (LLM Engine) ]
    (Razonamiento probabilístico, síntesis en lenguaje natural, sugerencia de JSON)
               │ (Produce únicamente el payload estructurado InvestigationResult)
               ▼
    ════════════════════════════════════════════════════════════════
           TRUSTED AGENT HARNESS (Aplicación Python / FastAPI)
    ════════════════════════════════════════════════════════════════
               │ 1. Aislamiento de Herramientas (Solo lectura autorizada)
               │ 2. Aritmética Determinista (Python/SQL puro, nunca LLM)
               │ 3. Aislamiento Multi-Tenant (Filtro por X-Institution-Id)
               │ 4. Validación de Esquema Pydantic v2 (Máximo 2 reintentos)
               │ 5. Máquina de Estados Finita (Prohíbe salto a EXECUTED)
               │ 6. Compuerta de Aprobación Humana Obligatoria (INV-002)
               ▼
    [ CONTROLLED DATABASE MUTATION & IMMUTABLE AUDIT LOG ]
```

### ¿Qué decide el modelo y qué garantiza el código?

| Dimensión                   | Lo que decide el Modelo LLM (Untrusted)            | Lo que GARANTIZA el Código (Trusted Harness)                                                                                                                                                                                                                   |
| --------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Recolección de Datos**    | Sugiere interpretar los datos recopilados.         | El arnés ejecuta deterministamente las 6 herramientas autorizadas de solo lectura. El LLM no tiene acceso directo a la base de datos.                                                                                                                          |
| **Cálculo Financiero**      | *Nada.* No realiza operaciones aritméticas.        | Los totales, porcentajes de incremento y ratios de ingresos se calculan con exactitud en Python/SQL ([`summary_service.py`](file:///f:/documents/bankingly-technical-challenge/backend/tools/services/summary_service.py)).                                    |
| **Estructura del Dictamen** | Llena los campos del reporte en lenguaje natural.  | Validación estricta con Pydantic v2 ([`validator.py`](file:///f:/documents/bankingly-technical-challenge/backend/harness/validator.py)); si el formato es inválido, reintenta o falla de forma segura.                                                         |
| **Aprobación y Mutación**   | Puede sugerir `ESCALATE_ALERT` o `CLOSE_ALERT`.    | **Compuerta en código:** El backend bloquea físicamente cualquier ejecución si no existe un registro previo de `Approval` firmado por un analista ([`approval_gate.py`](file:///f:/documents/bankingly-technical-challenge/backend/harness/approval_gate.py)). |
| **Ciclo de Vida / Estados** | No tiene control sobre las transiciones de estado. | La máquina de estados ([`state_machine.py`](file:///f:/documents/bankingly-technical-challenge/backend/harness/state_machine.py)) prohíbe terminantemente la transición `RECOMMENDATION_READY → EXECUTED`.                                                     |
| **Inyecciones de Prompt**   | Podría ser engañado por texto malicioso.           | Los textos de transferencias son encapsulados como variables inertes; ninguna instrucción textual puede desencadenar acciones.                                                                                                                                 |

---

## 3. ¿Dónde Vive el Control en el Código? (Demostración de Seguridad)

Una de las preguntas centrales del ejercicio es: **¿Qué pasa si se le pide al agente ejecutar sin aprobación humana y dónde vive ese control en el código?**

### Ubicación Exacta de los Controles:
1. **Verificación de Aprobación Previa:** En [`backend/harness/approval_gate.py` (Líneas 120-131)](file:///f:/documents/bankingly-technical-challenge/backend/harness/approval_gate.py#L120-L131), la función `execute_approved_action()` consulta la base de datos relacional:
   ```python
   approval = recommendation.approval
   if not approval or investigation.status not in [InvestigationStatus.APPROVED.value, InvestigationStatus.REJECTED.value]:
       raise UnapprovedExecutionError(
           f"Execution denied: No valid human approval found for investigation '{investigation_id}'. "
           f"Status is '{investigation.status}' (INV-002)."
       )
   ```
2. **Validación de la Máquina de Estados:** En [`backend/harness/state_machine.py` (Líneas 22-42)](file:///f:/documents/bankingly-technical-challenge/backend/harness/state_machine.py#L22-L42), el conjunto `VALID_INVESTIGATION_TRANSITIONS` define que desde `RECOMMENDATION_READY` o `AWAITING_APPROVAL` solo se puede transitar a `APPROVED` o `REJECTED`. Intentar forzar la transición a `EXECUTED` lanza `InvalidStateTransitionError`.
3. **Endpoints REST Desacoplados:** En [`backend/api/decisions.py` (Líneas 73-109)](file:///f:/documents/bankingly-technical-challenge/backend/api/decisions.py#L73-L109), el endpoint `POST /investigations/{id}/execute` atrapa `UnapprovedExecutionError` y responde con `HTTP 400 Bad Request`, impidiendo cualquier mutación en la tabla `AMLAlert`.

### ¿Qué pasa ante un intento no autorizado?
- Si un usuario, script o atacante intenta invocar `/execute` directamente:
  - El sistema rechaza la llamada con código `HTTP 400`.
  - La alerta permanece en su estado original sin sufrir modificaciones.
  - Se registra el intento en `audit_events`.
  - Este comportamiento está verificado al 100% en los tests de seguridad: [`tests/security/test_invariants.py`](file:///f:/documents/bankingly-technical-challenge/tests/security/test_invariants.py).

---

## 4. Registro de Decisiones ante Ambigüedad (Estilo ADR Breve)

Ante dudas de alcance y diseño técnico tomamos decisiones explícitas documentadas en [`.sdd/adr/`](file:///f:/documents/bankingly-technical-challenge/.sdd/adr/) y [`DECISIONS.md`](file:///f:/documents/bankingly-technical-challenge/DECISIONS.md):

| ADR ID | Decisión Adoptada | Alternativas Consideradas | Trade-off Aceptado |
|:---:|---|---|---|
| [**ADR-001**](file:///f:/documents/bankingly-technical-challenge/.sdd/adr/ADR-001-use-case-selection.md) | **Copiloto de Alertas AML** como caso de uso central del PoC. | Revisión de Crédito, Verificación KYC, Cobranza Temprana, Monitoreo de Cartera. | Se priorizó un flujo investigativo interno profundo y medible con Human-in-the-Loop por sobre casos conversacionales o de extracción de documentos (OCR). |
| [**ADR-002**](file:///f:/documents/bankingly-technical-challenge/.sdd/adr/ADR-002-modular-monolith.md) | **Monolito Modular en Python / FastAPI** con SQLite/PostgreSQL. | Microservicios distribuidos, frameworks de agentes pesados (LangChain/CrewAI). | Se sacrificó la distribución en múltiples microservicios para eliminar latencias de red y asegurar trazabilidad y determinismo total en el PoC. |
| [**ADR-003**](file:///f:/documents/bankingly-technical-challenge/.sdd/adr/ADR-003-trusted-harness-boundary.md) | **Trusted Agent Harness & Validación Pydantic v2**. | Agente con bucle de ejecución autónomo y confirmación por chat. | Se eliminaron todas las herramientas de mutación del alcance del LLM; toda acción requiere un registro de aprobación física en base de datos. |
| [**ADR-004**](file:///f:/documents/bankingly-technical-challenge/.sdd/adr/ADR-004-evaluation-first-design.md) | **Diseño Evaluation-First con Benchmark de 25 Casos**. | Pruebas manuales ad-hoc o prompts no testeados cuantitativamente. | Se invirtió esfuerzo temprano en construir la verdad de terreno (*Ground Truth*) para garantizar que las métricas de exactitud y seguridad fueran demostrables. |
| [**ADR-005**](file:///f:/documents/bankingly-technical-challenge/.sdd/adr/ADR-005-deterministic-tool-computations.md) | **Cálculo Determinista en Python/SQL para Métricas Financieras**. | Permitir al LLM calcular sumas y porcentajes en su prompt. | Se restringió el rol del LLM exclusivamente a razonar sobre números ya calculados con precisión matemática, eliminando alucinaciones aritméticas. |

---

## 5. Resultados del Benchmark de Evaluación

El sistema fue sometido a un conjunto de evaluación de **25 casos estratificados** (`data/evaluation/aml_evaluation_ground_truth_25.csv`) cubriendo 7 categorías representativas:

| Métrica de Calidad | Umbral Exigido | Resultado Obtenido | Estado |
|---|:---:|:---:|:---:|
| **Unauthorized Action Rate (Seguridad)** | **0.0%** | **0.0%** | ✅ **PASSED** |
| **Recommendation Accuracy** | **≥ 80.0%** | **88.0% (22/25)** | ✅ **PASSED** |
| **Evidence Grounding Score** | **≥ 90.0%** | **100.0%** | ✅ **PASSED** |
| **Resistencia a Inyecciones de Prompt** | **100.0%** | **100.0%** | ✅ **PASSED** |

> *Para un desglose completo de los casos caso por caso y el análisis de los 3 casos de fallo (EVAL-006, EVAL-008, EVAL-011), consultar [`EVALUATION_REPORT.md`](file:///f:/documents/bankingly-technical-challenge/EVALUATION_REPORT.md).*

---

## 6. Guía de Instalación y Ejecución Local (Setup Reproducible)

El proyecto puede ejecutarse localmente mediante **Python directo** o utilizando **Docker Compose**.

### Opción A: Ejecución con Python Local

#### 1. Requisitos Previos
- Python 3.11 o superior instalado.
- Git.

#### 2. Clonar y Configurar Entorno Virtual
```bash
# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd bankingly-technical-challenge

# Crear y activar entorno virtual
python -m venv venv

# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 3. Inicializar Base de Datos y Semilla (Seed Data)
```bash
# Ejecuta la carga de datos sintéticos de Banco Río Sur en SQLite
python -m backend.data.seed
```

#### 4. Iniciar Servidor Backend FastAPI
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Swagger interactiva disponible en: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

#### 5. Abrir la Consola de Cumplimiento (Frontend)
El frontend es una Single Page Application (SPA) en HTML5/Vanilla JS optimizada para máxima velocidad y sin dependencias pesadas de build:
- Simplemente abre [`frontend/index.html`](file:///f:/documents/bankingly-technical-challenge/frontend/index.html) en tu navegador web (o utiliza una extensión como *Live Server* / `python -m http.server 3000` en la carpeta `frontend/`).

---

### Opción B: Ejecución con Docker Compose

```bash
# Construir y levantar contenedores
docker-compose up --build
```
- Backend disponible en: `http://localhost:8000`
- Documentación OpenAPI: `http://localhost:8000/docs`

---

## 7. Ejecución de Pruebas y Benchmark

### Correr Suite Completa de Tests (Unitarios, Integración y Seguridad)
```bash
pytest -v
```

### Correr Exclusivamente las Pruebas de Invariantes de Seguridad (INV-001 a INV-010)
```bash
pytest tests/security/test_invariants.py -v
```

### Correr el Benchmark de Evaluación de 25 Casos
```bash
python -m backend.evaluation.runner
```
Generará el reporte en consola y actualizará `data/evaluation/benchmark_report.json`.

---

## 8. Estructura del Repositorio

```
bankingly-technical-challenge/
├── README.md                          # Documento técnico principal (Setup + Arquitectura + ADRs)
├── AI_INTERACTIONS.md                 # Transcripciones textuales de los 3 momentos con IA
├── EVALUATION_REPORT.md               # Reporte exhaustivo de evals y análisis de fallas
├── INVARIANTS.md                      # 10 invariantes de seguridad del sistema
├── DECISIONS.md                       # Índice de registros de decisiones arquitectónicas
├── requirements.txt                   # Dependencias Python
├── Dockerfile                         # Contenedor Docker para despliegue
├── docker-compose.yml                 # Orquestación de servicios
│
├── docs/                              # Documentación adicional de producto y presentación
│   ├── PRD.md                         # Product Requirements Document completo consolidado
│   └── LIVE_SESSION_GUIDE.md          # Guía para la defensa en la sesión en vivo de 30 min
│
├── .sdd/                              # Especificaciones Spec-Driven Development (Capas 1 a 6)
│   ├── 00-constitution.md             # Principios no negociables del proyecto
│   ├── 01-product-requirements.md     # PRD sincronizado
│   ├── 02-data-model-spec.md          # Modelo de datos relacional y ERD
│   ├── 03-api-contract.md             # Contrato de endpoints REST y herramientas
│   ├── 04-ui-ux-spec.md               # Especificación de interfaz de analista
│   ├── 05-architecture.md             # Especificación arquitectónica del arnés
│   ├── 08-verification-spec.md        # Plan de verificación y benchmark
│   └── adr/                           # Registros de decisión individuales (ADR-001..005)
│
├── backend/                           # Aplicación Python FastAPI
│   ├── main.py                        # Punto de entrada de la API REST
│   ├── api/                           # Routers (alerts, investigations, decisions)
│   ├── harness/                       # Trusted Agent Harness (orchestrator, gate, state machine)
│   ├── agent/                         # Prompt engine, cliente LLM y esquemas Pydantic
│   ├── tools/                         # 6 herramientas deterministas de lectura
│   ├── domain/                        # Modelos SQLAlchemy y enums
│   ├── data/                          # Conexión a base de datos y script seed.py
│   └── evaluation/                    # Runner y evaluadores del benchmark
│
├── frontend/                          # Consola web del analista de cumplimiento
│   ├── index.html                     # Interfaz de usuario interactiva
│   ├── styles.css                     # Sistema de diseño y tokens visuales
│   └── app.js                         # Lógica de conexión a la API REST y modal de aprobación
│
├── data/                              # Datasets y benchmark
│   ├── seed/                          # Datos simulados de Banco Río Sur
│   └── evaluation/                    # Ground Truth de 25 casos y reportes JSON
│
└── tests/                             # Suite de pruebas automatizadas
    ├── unit/                          # Pruebas de herramientas y validadores
    ├── integration/                   # Pruebas de endpoints FastAPI
    ├── security/                      # Verificación de invariantes (INV-001..INV-010)
    └── evaluation/                    # Verificación del benchmark
```