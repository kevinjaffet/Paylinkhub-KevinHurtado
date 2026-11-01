const REFRESH_INTERVAL_MS = 30000;
const PROVIDERS = [
  ["core", "CORE"],
  ["pagos", "PAGOS"],
  ["fx", "FX"],
];
const STATUS_LABELS = {
  ok: "Operativo",
  degraded: "Degradado",
  unavailable: "No disponible",
};

const form = document.querySelector("#customer-form");
const customerInput = document.querySelector("#customer-id");
const loadButton = document.querySelector("#load-button");
const autoRefreshInput = document.querySelector("#auto-refresh");
const statusNode = document.querySelector("#status");
const partialAlert = document.querySelector("#partial-alert");
const dashboardNode = document.querySelector("#dashboard");
const providersNode = document.querySelector("#providers");
const ratesNode = document.querySelector("#rates");
const customerNode = document.querySelector("#customer");
const transactionRows = document.querySelector("#transaction-rows");
const noTransactions = document.querySelector("#no-transactions");

let selectedCustomerId = "";
let requestInFlight = false;
let refreshTimer = null;
let transactions = [];

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const customerId = customerInput.value.trim();
  if (!customerId) {
    showStatus("Ingresa el ID del cliente.", true);
    return;
  }
  loadDashboard(customerId, { refresh: false });
});

autoRefreshInput.addEventListener("change", () => {
  if (autoRefreshInput.checked) {
    startAutoRefresh();
  } else {
    stopAutoRefresh();
  }
});

function startAutoRefresh() {
  stopAutoRefresh();
  refreshTimer = window.setInterval(() => {
    if (!selectedCustomerId || requestInFlight) {
      return;
    }
    loadDashboard(selectedCustomerId, { refresh: true });
  }, REFRESH_INTERVAL_MS);
}

function stopAutoRefresh() {
  if (refreshTimer !== null) {
    window.clearInterval(refreshTimer);
    refreshTimer = null;
  }
}

async function loadDashboard(customerId, { refresh }) {
  if (requestInFlight) {
    return;
  }

  requestInFlight = true;
  loadButton.disabled = true;
  showStatus(refresh ? "Actualizando dashboard..." : "Consultando dashboard...", false);

  try {
    const response = await fetch(`/api/v1/dashboard/${encodeURIComponent(customerId)}`);
    if (!response.ok) {
      throw new Error(`El servicio respondió HTTP ${response.status}.`);
    }

    const body = await response.text();
    if (!body.trim()) {
      throw new Error("El servicio devolvió una respuesta vacía.");
    }

    let payload;
    try {
      payload = JSON.parse(body);
    } catch {
      throw new Error("El servicio devolvió una respuesta no válida.");
    }

    selectedCustomerId = customerId;
    renderDashboard(payload);
    showStatus("Dashboard actualizado.", false);
  } catch (error) {
    const message = error instanceof TypeError
      ? "No se pudo conectar con el servicio."
      : error.message;
    showStatus(message, true);
    if (!refresh) {
      clearDashboard();
    }
  } finally {
    requestInFlight = false;
    loadButton.disabled = false;
  }
}

function renderDashboard(payload) {
  dashboardNode.hidden = false;
  renderProviders(payload.providers || {});
  renderRates(payload.exchange_rates);
  renderCustomer(payload.customer);
  renderPartial(payload.partial, payload.warnings);
  transactions = Array.isArray(payload.transactions) ? payload.transactions : [];
  renderTransactions(transactions);
}

function renderProviders(providers) {
  providersNode.innerHTML = `<div class="provider-list">${PROVIDERS.map(([key, label]) => {
    const state = providers[key] || "unavailable";
    const safeState = STATUS_LABELS[state] ? state : "unavailable";
    return `<article class="provider">
      <div><span>${label}</span><b>${STATUS_LABELS[safeState]}</b></div>
      <span class="dot ${safeState}" aria-hidden="true"></span>
    </article>`;
  }).join("")}</div>`;
}

function renderRates(rates) {
  if (!rates) {
    ratesNode.hidden = true;
    ratesNode.innerHTML = "";
    return;
  }

  ratesNode.hidden = false;
  ratesNode.innerHTML = `<div class="rate-list">
    <article class="rate"><div><span>Base</span><b>${escapeHtml(rates.base)}</b></div></article>
    <article class="rate"><div><span>EUR</span><b>${escapeHtml(rates.EUR)}</b></div></article>
    <article class="rate"><div><span>GBP</span><b>${escapeHtml(rates.GBP)}</b></div></article>
  </div>`;
}

function renderCustomer(customer) {
  if (!customer) {
    customerNode.innerHTML = "<h2>Cliente</h2><p class=\"empty\">No hay información del cliente.</p>";
    return;
  }

  customerNode.innerHTML = `<h2>Cliente</h2><div class="customer-grid">
    <div><span>Nombre</span><b>${escapeHtml(customer.full_name)}</b></div>
    <div><span>Email</span><b>${escapeHtml(customer.email)}</b></div>
    <div><span>Teléfono</span><b>${escapeHtml(customer.phone)}</b></div>
  </div>`;
}

function renderPartial(partial, warnings) {
  const messages = Array.isArray(warnings) ? warnings.filter(Boolean) : [];
  if (!partial && messages.length === 0) {
    partialAlert.hidden = true;
    partialAlert.innerHTML = "";
    return;
  }

  partialAlert.hidden = false;
  const items = messages.map((warning) => `<li>${escapeHtml(warning)}</li>`).join("");
  partialAlert.innerHTML = `<h2>Respuesta parcial</h2>${items ? `<ul>${items}</ul>` : ""}`;
}

function renderTransactions(items) {
  noTransactions.hidden = items.length > 0;
  transactionRows.innerHTML = items.map((transaction) => {
    const products = Array.isArray(transaction.products) ? transaction.products : [];
    const productCount = products.length;
    const productLabel = productCount === 1 ? "1 producto" : `${productCount} productos`;
    const productList = products.map((product) => `<li>${escapeHtml(product)}</li>`).join("");
    return `<article class="transaction">
      <p class="transaction-id"><span>ID</span> <b>${escapeHtml(transaction.id)}</b></p>
      <ul class="product-list">${productList}</ul>
      <p class="transaction-summary">
        <span>${productLabel}</span>
        <span>Cantidad ${escapeHtml(transaction.quantity)}</span>
        <b>Total USD ${escapeHtml(transaction.total_usd)}</b>
      </p>
    </article>`;
  }).join("");
}

function clearDashboard() {
  dashboardNode.hidden = true;
  partialAlert.hidden = true;
  partialAlert.innerHTML = "";
  transactions = [];
  transactionRows.innerHTML = "";
}

function showStatus(message, isError) {
  statusNode.textContent = message;
  statusNode.classList.toggle("error", isError);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
