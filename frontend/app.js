const API_BASE = "http://127.0.0.1:8000/api/v1";
const INSTITUTION_ID = "BANK-RIO-SUR";
const ANALYST_ID = "ANA-0091";

let currentAlerts = [];
let selectedAlert = null;
let currentInvestigation = null;
let pendingDecision = "APPROVED";

document.addEventListener("DOMContentLoaded", () => {
  initApp();
});

async function initApp() {
  await fetchAlerts();
  setupEventListeners();
}

function setupEventListeners() {
  document.getElementById("btnInvestigateAlert").addEventListener("click", () => {
    if (selectedAlert) {
      triggerInvestigation(selectedAlert.id);
    }
  });

  document.getElementById("btnApproveAction").addEventListener("click", () => {
    openDecisionModal("APPROVED");
  });

  document.getElementById("btnRejectAction").addEventListener("click", () => {
    openDecisionModal("REJECTED");
  });

  document.getElementById("btnCloseModal").addEventListener("click", closeDecisionModal);
  document.getElementById("btnCancelModal").addEventListener("click", closeDecisionModal);

  document.getElementById("btnConfirmExecution").addEventListener("click", () => {
    confirmAndExecuteDecision();
  });

  document.getElementById("searchAlertInput").addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase();
    const filtered = currentAlerts.filter(a => 
      a.id.toLowerCase().includes(term) || a.customer_name.toLowerCase().includes(term)
    );
    renderAlertList(filtered);
  });
}

async function fetchAlerts() {
  try {
    const res = await fetch(`${API_BASE}/alerts`, {
      headers: { "X-Institution-Id": INSTITUTION_ID, "X-Analyst-Id": ANALYST_ID }
    });
    if (res.ok) {
      const body = await res.json();
      currentAlerts = body.data || [];
      document.getElementById("alertCount").textContent = currentAlerts.length;
      renderAlertList(currentAlerts);
      if (currentAlerts.length > 0) {
        selectAlert(currentAlerts[0]);
      }
    }
  } catch (err) {
    console.error("Error fetching alerts:", err);
    document.getElementById("alertListContainer").innerHTML = `
      <div class="loading-state" style="color: var(--danger)">
        ⚠️ No se pudo conectar con la API de FastAPI. Asegúrese de que el servidor esté activo.
      </div>
    `;
  }
}

function renderAlertList(alerts) {
  const container = document.getElementById("alertListContainer");
  if (!alerts.length) {
    container.innerHTML = `<div class="loading-state">No se encontraron alertas.</div>`;
    return;
  }

  container.innerHTML = alerts.map(a => {
    const isSelected = selectedAlert && selectedAlert.id === a.id;
    const riskCls = a.risk_score >= 70 ? "high" : (a.risk_score >= 40 ? "medium" : "low");
    return `
      <div class="alert-card-item ${isSelected ? 'active' : ''}" onclick="onAlertClick('${a.id}')">
        <div class="alert-card-top">
          <span class="alert-card-id">${a.id}</span>
          <span class="risk-chip ${riskCls}">${a.risk_score}/100</span>
        </div>
        <div class="alert-card-name">${a.customer_name}</div>
        <div class="alert-card-trigger">${a.trigger_reason}</div>
      </div>
    `;
  }).join("");
}

window.onAlertClick = function(alertId) {
  const alert = currentAlerts.find(a => a.id === alertId);
  if (alert) {
    selectAlert(alert);
  }
};

function selectAlert(alert) {
  selectedAlert = alert;
  renderAlertList(currentAlerts);

  // Update Top Banner
  document.getElementById("selectedAlertId").textContent = alert.id;
  document.getElementById("selectedCustomerName").textContent = alert.customer_name;
  document.getElementById("selectedCustomerId").textContent = alert.customer_id;
  document.getElementById("selectedRiskScore").textContent = `${alert.risk_score} / 100`;
  document.getElementById("selectedAlertStatus").textContent = alert.status;

  const riskBadge = document.getElementById("selectedRiskBadge");
  riskBadge.className = `risk-score-badge ${alert.risk_score >= 70 ? 'high' : 'medium'}`;

  // Reset or prefill context
  resetInvestigationView();
}

function resetInvestigationView() {
  document.getElementById("invSummaryText").textContent = "Seleccione 'Investigar con Copilot' para iniciar la recolección autónoma de evidencia y el contraste de políticas.";
  document.getElementById("findingsList").innerHTML = `<div style="font-size: 0.8rem; color: var(--text-muted);">Sin hallazgos generados aún.</div>`;
  document.getElementById("missingInfoList").innerHTML = `<li>Ninguna información faltante identificada aún.</li>`;
  document.getElementById("policyTagsContainer").innerHTML = `<span class="policy-chip">P-001</span><span class="policy-chip">P-004</span>`;
  document.getElementById("recActionBadge").textContent = "PENDIENTE DE ANÁLISIS";
  document.getElementById("recRationaleText").textContent = "El Copilot evaluará la actividad frente a las políticas configuradas.";
}

async function triggerInvestigation(alertId) {
  const btn = document.getElementById("btnInvestigateAlert");
  btn.disabled = true;
  btn.innerHTML = `<span>⏳ Investigando...</span>`;

  try {
    const res = await fetch(`${API_BASE}/investigations/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Institution-Id": INSTITUTION_ID,
        "X-Analyst-Id": ANALYST_ID,
      },
      body: JSON.stringify({ alert_id: alertId }),
    });

    if (res.ok) {
      const body = await res.json();
      currentInvestigation = body.data;
      renderInvestigationReport(currentInvestigation);
    } else {
      const errBody = await res.json();
      alert(`Error en investigación: ${errBody.detail || 'Fallo desconocido'}`);
    }
  } catch (err) {
    console.error("Error running investigation:", err);
    alert("Error de conexión al ejecutar la investigación.");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>⚡ Investigar con Copilot</span>`;
  }
}

function renderInvestigationReport(inv) {
  document.getElementById("invStatusLabel").textContent = inv.status;
  document.getElementById("confidenceLabel").textContent = `${Math.round((inv.confidence_score || 0.85) * 100)}%`;
  document.getElementById("invSummaryText").textContent = inv.summary;

  const rec = inv.recommendation || {};
  document.getElementById("recActionBadge").textContent = rec.action || "REVISIÓN REQUERIDA";
  document.getElementById("recRationaleText").textContent = rec.rationale || "";

  // Render Findings
  const findingsContainer = document.getElementById("findingsList");
  if (rec.findings && rec.findings.length > 0) {
    findingsContainer.innerHTML = rec.findings.map(f => `
      <div class="finding-item">
        <div class="finding-text">📌 ${f.finding}</div>
        <div class="evidence-tags">
          ${(f.evidence || []).map(e => `
            <span class="evidence-pill">🔍 ${e.source_type}: ${e.field || ''} ${e.value ? `(${e.value})` : ''}</span>
          `).join("")}
        </div>
      </div>
    `).join("");
  }

  // Render Missing Info
  const missingContainer = document.getElementById("missingInfoList");
  if (rec.missing_information && rec.missing_information.length > 0) {
    missingContainer.innerHTML = rec.missing_information.map(m => `<li>${m}</li>`).join("");
  }

  // Render Policies
  const policiesContainer = document.getElementById("policyTagsContainer");
  if (rec.applicable_policies && rec.applicable_policies.length > 0) {
    policiesContainer.innerHTML = rec.applicable_policies.map(p => `
      <span class="policy-chip">${p}</span>
    `).join("");
  }
}

function openDecisionModal(decision) {
  if (!currentInvestigation) {
    alert("Por favor ejecute primero la investigación del Copilot.");
    return;
  }
  pendingDecision = decision;
  document.getElementById("modalAlertId").textContent = selectedAlert.id;
  document.getElementById("modalActionName").textContent = `${pendingDecision}: ${currentInvestigation.recommendation.action}`;
  document.getElementById("decisionModal").style.display = "flex";
}

function closeDecisionModal() {
  document.getElementById("decisionModal").style.display = "none";
}

async function confirmAndExecuteDecision() {
  const notes = document.getElementById("analystNotesInput").value;
  const invId = currentInvestigation.investigation_id;

  try {
    // 1. Submit analyst decision
    const decideRes = await fetch(`${API_BASE}/investigations/${invId}/decide`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Institution-Id": INSTITUTION_ID,
        "X-Analyst-Id": ANALYST_ID,
      },
      body: JSON.stringify({ decision: pendingDecision, notes: notes }),
    });

    if (!decideRes.ok) {
      const err = await decideRes.json();
      throw new Error(err.detail || "Fallo en registro de decisión");
    }

    // 2. Execute the approved action (INV-002)
    const execRes = await fetch(`${API_BASE}/investigations/${invId}/execute`, {
      method: "POST",
      headers: {
        "X-Institution-Id": INSTITUTION_ID,
        "X-Analyst-Id": ANALYST_ID,
      },
    });

    if (!execRes.ok) {
      const err = await execRes.json();
      throw new Error(err.detail || "Fallo en ejecución de acción");
    }

    const execData = await execRes.json();
    alert(`✅ Acción ejecutada con éxito!\nEstado final de alerta: ${execData.data.resulting_alert_status}\nRegistro de auditoría generado.`);
    closeDecisionModal();
    await fetchAlerts();
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}
