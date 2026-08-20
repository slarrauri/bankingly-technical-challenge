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

async function selectAlert(alert) {
  selectedAlert = alert;
  currentInvestigation = null;
  renderAlertList(currentAlerts);

  // Update Top Banner
  document.getElementById("selectedAlertId").textContent = alert.id;
  document.getElementById("selectedCustomerName").textContent = alert.customer_name;
  document.getElementById("selectedCustomerId").textContent = alert.customer_id;
  document.getElementById("selectedRiskScore").textContent = `${alert.risk_score} / 100`;
  document.getElementById("selectedAlertStatus").textContent = alert.status;

  const riskBadge = document.getElementById("selectedRiskBadge");
  riskBadge.className = `risk-score-badge ${alert.risk_score >= 70 ? 'high' : 'medium'}`;

  // Reset investigation view & disable decision buttons until investigation is completed
  resetInvestigationView();

  // Fetch real KYC and transaction summary from SQLite DB
  await fetchAlertContext(alert.id);
}

async function fetchAlertContext(alertId) {
  const kycCard = document.getElementById("kycCardContainer");
  const summaryCard = document.getElementById("summaryCardContainer");

  kycCard.classList.add("loading-shimmer");
  summaryCard.classList.add("loading-shimmer");

  try {
    const res = await fetch(`${API_BASE}/alerts/${alertId}/context`, {
      headers: { "X-Institution-Id": INSTITUTION_ID, "X-Analyst-Id": ANALYST_ID }
    });

    if (res.ok) {
      const body = await res.json();
      const { customer, transaction_summary, investigation } = body.data || {};
      renderCustomerKyc(customer);
      renderTransactionSummary(transaction_summary);

      if (investigation && investigation.recommendation) {
        currentInvestigation = investigation;
        renderInvestigationReport(investigation);
      } else {
        resetInvestigationView();
      }
    } else {
      console.error("Failed to fetch alert context:", res.statusText);
      resetInvestigationView();
    }
  } catch (err) {
    console.error("Error fetching context:", err);
    resetInvestigationView();
  } finally {
    kycCard.classList.remove("loading-shimmer");
    summaryCard.classList.remove("loading-shimmer");
  }
}

function renderCustomerKyc(customer) {
  if (!customer) return;

  const statusBadge = document.getElementById("kycStatusBadge");
  statusBadge.textContent = customer.kyc_status || "VERIFIED";
  statusBadge.className = `status-chip ${customer.kyc_status === 'VERIFIED' ? 'verified' : (customer.kyc_status === 'INCOMPLETE' ? 'danger' : 'warning')}`;

  document.getElementById("kycOccupation").textContent = customer.occupation || "Desconocida";
  
  const incomeVal = Number(customer.declared_monthly_income || 0).toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  });
  document.getElementById("kycIncome").textContent = `${incomeVal} / mes`;
  document.getElementById("kycFundsSource").textContent = customer.declared_source_of_funds || "No especificado";
  document.getElementById("kycNotes").textContent = customer.kyc_notes || "Sin notas de cumplimiento registradas.";
}

function renderTransactionSummary(summary) {
  if (!summary) return;

  const volChip = document.getElementById("volChangeChip");
  const volVal = Number(summary.volume_change_percentage || 0);
  const sign = volVal > 0 ? "+" : "";
  volChip.textContent = `${sign}${volVal.toFixed(1)}% Volumen`;
  volChip.className = `metric-chip ${volVal > 100 ? 'highlight' : (volVal < 0 ? 'low' : '')}`;

  const inflowVal = Number(summary.current_period_inflow || 0).toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  });
  const outflowVal = Number(summary.current_period_outflow || 0).toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  });

  document.getElementById("recentInflow").textContent = inflowVal;
  document.getElementById("recentOutflow").textContent = outflowVal;
  document.getElementById("incomeRatio").textContent = `${Number(summary.inflow_to_declared_income_ratio || 0).toFixed(2)}x`;

  const newCps = summary.new_counterparties_detected || [];
  document.getElementById("newCounterparties").textContent = newCps.length > 0 ? newCps.join(", ") : "Ninguna detectada";
}

function resetInvestigationView() {
  currentInvestigation = null;
  document.getElementById("invStatusLabel").textContent = "PENDIENTE";
  document.getElementById("confidenceLabel").textContent = "-";

  // Toggle empty state / report containers
  const emptyState = document.getElementById("copilotEmptyState");
  const reportContent = document.getElementById("copilotReportContent");
  const actionBar = document.getElementById("decisionActionBar");

  if (emptyState) emptyState.style.display = "flex";
  if (reportContent) reportContent.style.display = "none";
  if (actionBar) actionBar.style.display = "none";

  document.getElementById("btnApproveAction").disabled = true;
  document.getElementById("btnRejectAction").disabled = true;
}


function setInvestigationStep(stepId, state) {
  const step = document.getElementById(stepId);
  if (!step) return;
  const icon = step.querySelector(".step-icon");

  if (state === "active") {
    step.className = "step-item active";
    icon.textContent = "⚙️";
  } else if (state === "completed") {
    step.className = "step-item completed";
    icon.textContent = "✅";
  } else {
    step.className = "step-item";
    icon.textContent = "⏳";
  }
}

async function triggerInvestigation(alertId) {
  const btn = document.getElementById("btnInvestigateAlert");
  btn.disabled = true;
  btn.innerHTML = `<span>⏳ Investigando...</span>`;

  // Show central investigation modal & reset steps
  const modal = document.getElementById("investigationProgressModal");
  const progressBar = document.getElementById("investigationProgressBar");
  const subText = document.getElementById("investigationProgressSub");

  ["stepKyc", "stepTransactions", "stepPolicies", "stepRecommendation"].forEach(s => setInvestigationStep(s, "pending"));
  progressBar.style.width = "10%";
  modal.style.display = "flex";

  // Simulate progress animation steps while fetching
  setInvestigationStep("stepKyc", "active");
  subText.textContent = "Consultando perfil KYC y registros del cliente en SQLite...";

  const stepTimer1 = setTimeout(() => {
    setInvestigationStep("stepKyc", "completed");
    setInvestigationStep("stepTransactions", "active");
    subText.textContent = "Calculando métricas transaccionales y análisis de volumen...";
    progressBar.style.width = "40%";
  }, 400);

  const stepTimer2 = setTimeout(() => {
    setInvestigationStep("stepTransactions", "completed");
    setInvestigationStep("stepPolicies", "active");
    subText.textContent = "Contrastando hallazgos con las Políticas Institucionales AML...";
    progressBar.style.width = "70%";
  }, 800);

  const stepTimer3 = setTimeout(() => {
    setInvestigationStep("stepPolicies", "completed");
    setInvestigationStep("stepRecommendation", "active");
    subText.textContent = "Estructurando reporte explicable y recomendación de cumplimiento...";
    progressBar.style.width = "90%";
  }, 1200);

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

    // Ensure minimum visual feedback time for smooth transition
    await new Promise(r => setTimeout(r, 1400));

    clearTimeout(stepTimer1);
    clearTimeout(stepTimer2);
    clearTimeout(stepTimer3);

    if (res.ok) {
      setInvestigationStep("stepRecommendation", "completed");
      progressBar.style.width = "100%";
      subText.textContent = "¡Investigación completada con éxito!";

      await new Promise(r => setTimeout(r, 400));
      modal.style.display = "none";

      const body = await res.json();
      currentInvestigation = body.data;
      renderInvestigationReport(currentInvestigation);
    } else {
      modal.style.display = "none";
      const errBody = await res.json();
      alert(`Error en investigación: ${errBody.detail || 'Fallo desconocido'}`);
    }
  } catch (err) {
    modal.style.display = "none";
    console.error("Error running investigation:", err);
    alert("Error de conexión al ejecutar la investigación.");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>⚡ Investigar con Copilot</span>`;
  }
}

function renderInvestigationReport(inv) {
  // Toggle empty state / report content
  const emptyState = document.getElementById("copilotEmptyState");
  const reportContent = document.getElementById("copilotReportContent");
  const actionBar = document.getElementById("decisionActionBar");

  if (emptyState) emptyState.style.display = "none";
  if (reportContent) reportContent.style.display = "flex";
  if (actionBar) actionBar.style.display = "flex";

  document.getElementById("invStatusLabel").textContent = inv.status;
  document.getElementById("confidenceLabel").textContent = `${Math.round((inv.confidence_score || 0.85) * 100)}%`;
  document.getElementById("invSummaryText").textContent = inv.summary;

  const rec = inv.recommendation || {};
  const actionBadge = document.getElementById("recActionBadge");
  actionBadge.textContent = rec.action || "REVISIÓN REQUERIDA";

  if (rec.action === "ESCALATE_ALERT") {
    actionBadge.className = "rec-action-badge high";
  } else if (rec.action === "CLOSE_ALERT") {
    actionBadge.className = "rec-action-badge success";
  } else {
    actionBadge.className = "rec-action-badge medium";
  }

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
  } else {
    findingsContainer.innerHTML = `<div style="font-size: 0.8rem; color: var(--text-muted);">Sin hallazgos generados.</div>`;
  }

  // Render Missing Info
  const missingContainer = document.getElementById("missingInfoList");
  if (rec.missing_information && rec.missing_information.length > 0) {
    missingContainer.innerHTML = rec.missing_information.map(m => `<li>${m}</li>`).join("");
  } else {
    missingContainer.innerHTML = `<li>Ninguna información faltante identificada.</li>`;
  }

  // Render Policies
  const policiesContainer = document.getElementById("policyTagsContainer");
  if (rec.applicable_policies && rec.applicable_policies.length > 0) {
    policiesContainer.innerHTML = rec.applicable_policies.map(p => `
      <span class="policy-chip">${p}</span>
    `).join("");
  } else {
    policiesContainer.innerHTML = "";
  }

  // Enable decision buttons if investigation is awaiting approval or already executed
  const isAwaiting = inv.status === "AWAITING_APPROVAL";
  document.getElementById("btnApproveAction").disabled = !isAwaiting;
  document.getElementById("btnRejectAction").disabled = !isAwaiting;
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

