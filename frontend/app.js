const configForm = document.getElementById("config-form");
const statusEl = document.getElementById("status");
const validationEl = document.getElementById("validation-message");
const resultOutput = document.getElementById("result-output");
const logsOutput = document.getElementById("logs-output");

const fields = {
    api_key: document.getElementById("api_key"),
    api_secret: document.getElementById("api_secret"),
    binance_api_base: document.getElementById("binance_api_base"),
    symbol: document.getElementById("symbol"),
    interval: document.getElementById("interval"),
    use_binance: document.getElementById("use_binance"),
    live_trading_enabled: document.getElementById("live_trading_enabled"),
    include_super_agent: document.getElementById("include_super_agent"),
    num_agents: document.getElementById("num_agents"),
    num_trades: document.getElementById("num_trades"),
};

function buildConfigPayload() {
    return {
        api_key: fields.api_key.value,
        api_secret: fields.api_secret.value,
        binance_api_base: fields.binance_api_base.value.trim() || null,
        symbol: fields.symbol.value,
        interval: fields.interval.value,
        use_binance: fields.use_binance.checked,
        live_trading_enabled: fields.live_trading_enabled.checked,
        include_super_agent: fields.include_super_agent.checked,
        num_agents: Number(fields.num_agents.value),
        num_trades: Number(fields.num_trades.value),
    };
}

function validateBinanceConfig(payload) {
    if (!payload.use_binance) {
        return null;
    }
    if (!payload.api_key?.trim() || !payload.api_secret?.trim()) {
        return "Digite a chave Binance API e o Secret antes de testar ou usar o modo Binance.";
    }
    return null;
}

function setValidationMessage(message) {
    validationEl.textContent = message || "";
    validationEl.style.display = message ? "block" : "none";
}

async function fetchConfig() {
    const response = await fetch("/api/config");
    const config = await response.json();
    fields.api_key.value = config.api_key || "";
    fields.api_secret.value = config.api_secret || "";
    fields.binance_api_base.value = config.binance_api_base || "";
    fields.symbol.value = config.symbol || "EURUSDT";
    fields.interval.value = config.interval || "1d";
    fields.use_binance.checked = config.use_binance || false;
    fields.live_trading_enabled.checked = config.live_trading_enabled || false;
    fields.include_super_agent.checked = config.include_super_agent || false;
    fields.num_agents.value = config.num_agents || 5;
    fields.num_trades.value = config.num_trades || 100;
}

async function saveConfig() {
    const payload = buildConfigPayload();
    const validation = validateBinanceConfig(payload);

    if (validation) {
        statusEl.textContent = validation;
        setValidationMessage(validation);
        return { success: false, detail: validation };
    }
    setValidationMessage("");

    const response = await fetch("/api/config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    const data = await response.json();
    statusEl.textContent = data.success ? "Configuração salva com sucesso." : "Falha ao salvar configuração.";
    return data;
}

async function runSimulation() {
    statusEl.textContent = "Executando simulação...";
    await saveConfig();
    const response = await fetch("/api/simulate", { method: "POST" });
    const data = await response.json();

    if (!data.success) {
        statusEl.textContent = `Erro: ${data.detail || "checagem falhou"}`;
        return;
    }

    statusEl.textContent = `Simulação concluída com ${data.agents.length} agentes.`;
    resultOutput.textContent = JSON.stringify(data, null, 2);
    await loadLogs();
    await loadSuccessTrades();
}

async function testBinanceConnection() {
    statusEl.textContent = "Carregando conta Binance...";
    const payload = buildConfigPayload();
    const validation = validateBinanceConfig(payload);

    if (validation) {
        statusEl.textContent = validation;
        setValidationMessage(validation);
        document.getElementById("binance-account-section").style.display = "none";
        return;
    }
    setValidationMessage("");

    await saveConfig();
    const response = await fetch("/api/binance/test");
    const data = await response.json();

    if (!data.success) {
        statusEl.textContent = `Erro: ${data.detail || "falha na conexão"}`;
        document.getElementById("binance-account-section").style.display = "none";
        return;
    }

    statusEl.textContent = "Conta Binance carregada com sucesso.";
    renderBinanceAccount(data.data);
}

function renderBinanceAccount(account) {
    const section = document.getElementById("binance-account-section");
    const container = document.getElementById("binance-account-info");
    
    if (!account || !account.balances) {
        container.innerHTML = "<p>Não foi possível obter informações da conta.</p>";
        section.style.display = "block";
        return;
    }

    // Filtra apenas ativos com saldo > 0
    const balances = account.balances.filter(b => b.amount > 0);
    
    // Separa USDT e outros ativos
    const usdtBalance = balances.find(b => b.asset === "USDT");
    const otherBalances = balances.filter(b => b.asset !== "USDT").slice(0, 20);

    let html = `
        <div class="binance-summary">
            <div class="binance-total">
                <span class="label">Total em USDT:</span>
                <span class="value">$${account.total_usdt?.toFixed(2) || "0.00"}</span>
            </div>
            ${usdtBalance ? `
            <div class="binance-row">
                <span class="asset">${usdtBalance.asset}</span>
                <span class="amount">${usdtBalance.amount.toFixed(8)}</span>
                <span class="value">$${usdtBalance.value_usdt?.toFixed(2) || "0.00"}</span>
            </div>
            ` : ""}
        </div>
        <details class="binance-balances">
            <summary>Outros ativos (${otherBalances.length})</summary>
            <table class="balances-table">
                <thead>
                    <tr>
                        <th>Ativo</th>
                        <th>Disponível</th>
                        <th>Bloqueado</th>
                        <th>Total</th>
                        <th>Valor (USDT)</th>
                    </tr>
                </thead>
                <tbody>
                    ${otherBalances.map(b => `
                    <tr>
                        <td><strong>${b.asset}</strong></td>
                        <td>${b.free.toFixed(8)}</td>
                        <td>${b.locked.toFixed(8)}</td>
                        <td>${b.amount.toFixed(8)}</td>
                        <td>${b.value_usdt ? '$' + b.value_usdt.toFixed(2) : '-'}</td>
                    </tr>
                    `).join("")}
                </tbody>
            </table>
        </details>
    `;

    container.innerHTML = html;
    section.style.display = "block";
}

async function loadLogs() {
    const response = await fetch("/api/logs");
    const data = await response.json();
    logsOutput.textContent = data.lines ? data.lines.join("\n") : "Nenhum log encontrado.";
}

async function loadSuccessTrades() {
    const response = await fetch("/api/success-trades?limit=50");
    const data = await response.json();
    const output = document.getElementById("success-output");
    if (!data.success) {
        output.textContent = "Não foi possível carregar os trades de sucesso.";
        return;
    }
    output.textContent = JSON.stringify(data.trades, null, 2);
}

async function loadStrategies() {
    const response = await fetch("/api/strategies");
    const data = await response.json();
    const output = document.getElementById("strategies-output");
    if (!data || data.length === 0) {
        output.textContent = "Nenhuma estratégia disponível.";
        return;
    }
    output.textContent = JSON.stringify(data, null, 2);
}

async function loadCoins() {
    const response = await fetch("/api/coins");
    const data = await response.json();
    const output = document.getElementById("coins-output");
    if (!data || data.length === 0) {
        output.textContent = "Nenhuma moeda disponível.";
        return;
    }
    output.textContent = JSON.stringify(data, null, 2);
    
    // Atualiza o select de símbolos com as moedas do backend
    const symbolSelect = document.getElementById("symbol");
    symbolSelect.innerHTML = "";
    data.forEach(coin => {
        const option = document.createElement("option");
        option.value = coin.replace("/", "");
        option.textContent = coin;
        symbolSelect.appendChild(option);
    });
}

window.addEventListener("DOMContentLoaded", async () => {
    await fetchConfig();
    document.getElementById("save-config").addEventListener("click", saveConfig);
    document.getElementById("binance-test").addEventListener("click", testBinanceConnection);
    document.getElementById("run-sim").addEventListener("click", runSimulation);
    document.getElementById("refresh-logs").addEventListener("click", loadLogs);
    document.getElementById("refresh-success").addEventListener("click", loadSuccessTrades);
    document.getElementById("load-strategies").addEventListener("click", loadStrategies);
    document.getElementById("load-coins").addEventListener("click", loadCoins);
    await loadLogs();
    await loadSuccessTrades();
    await loadCoins();
});
