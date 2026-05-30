// Global state variables
let activeTab = "overview";
let activeGraph = "workforce";
let previewGraphType = "workforce";
let latencyChartInstance = null;
let xaiChartInstance = null;
let mainGraphNodes = [];
let mainGraphLinks = [];
let mainGraphAnimationId = null;

let previewGraphNodes = [];
let previewGraphLinks = [];
let previewGraphAnimationId = null;

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
    initClock();
    initTabRouting();
    initChatSystem();
    initSimulationSystem();
    initGraphTabs();
    initTelemetrySystem();
    
    // Initial loads
    loadOverviewData();
    loadMainGraph(activeGraph);
    loadPreviewGraph(previewGraphType);
});

// 1. Live Time clock
function initClock() {
    const timeEl = document.getElementById("live-time");
    setInterval(() => {
        const now = new Date();
        timeEl.textContent = now.toLocaleTimeString();
    }, 1000);
}

// 2. Sidebar Tab Navigation Routing
function initTabRouting() {
    const navItems = document.querySelectorAll(".nav-item");
    const tabContents = document.querySelectorAll(".tab-content");
    const pageTitle = document.getElementById("page-title");
    const pageSubtitle = document.getElementById("page-subtitle");
    
    const titles = {
        "overview": { title: "Enterprise Overview", subtitle: "Real-time collaborative agent operations" },
        "copilot": { title: "AI Copilot Workspace", subtitle: "Discuss metrics and query multi-agent orchestrations" },
        "simulation": { title: "What-If Simulator", subtitle: "Predict financial opex health from strategic parameters" },
        "graph": { title: "Enterprise Graph Topology", subtitle: "Visualizing Workforce, Supply Chain, and OPEX connections" },
        "telemetry": { title: "System Telemetry & Monitoring", subtitle: "Active performance metrics, drift alerts, and server logs" }
    };
    
    navItems.forEach(item => {
        item.addEventListener("click", (e) => {
            e.preventDefault();
            const tabName = item.getAttribute("data-tab");
            
            navItems.forEach(nav => nav.classList.remove("active"));
            item.classList.add("active");
            
            tabContents.forEach(tab => {
                tab.classList.remove("active");
                if (tab.id === `${tabName}-tab`) {
                    tab.classList.add("active");
                }
            });
            
            activeTab = tabName;
            pageTitle.textContent = titles[tabName].title;
            pageSubtitle.textContent = titles[tabName].subtitle;
            
            // Resize or trigger specific layouts if needed
            if (tabName === "graph") {
                loadMainGraph(activeGraph);
            } else if (tabName === "overview") {
                loadPreviewGraph(previewGraphType);
            }
        });
    });
}

// 3. Load Overview Page data
async function loadOverviewData() {
    try {
        const res = await fetch("/api/monitoring/metrics");
        const data = await res.json();
        
        // Load agent roster status list
        const listEl = document.getElementById("agent-status-list");
        listEl.innerHTML = "";
        
        data.agents.forEach(agent => {
            const card = document.createElement("div");
            card.className = "agent-status-card";
            
            const badgeClass = agent.status === "Active" ? "badge-active" : "badge-idle";
            const pulseMarkup = agent.status === "Active" ? '<span class="pulse-dot green" style="margin-right:8px; width:6px; height:6px;"></span>' : '';
            
            card.innerHTML = `
                <div class="agent-info">
                    <span class="agent-name">${agent.name}</span>
                    <span class="agent-runs">Calls: ${agent.total_runs} | Err: ${Math.round(agent.err_rate * 100)}%</span>
                </div>
                <span class="agent-badge ${badgeClass}">${pulseMarkup}${agent.status}</span>
            `;
            listEl.appendChild(card);
        });
        
    } catch (e) {
        console.error("Failed to load overview data:", e);
    }
}

// 4. Copilot Chat Workspace and XAI Graphs
function initChatSystem() {
    const form = document.getElementById("chat-input-form");
    const input = document.getElementById("chat-input-field");
    const box = document.getElementById("chat-messages-box");
    const flowStepsBox = document.getElementById("agent-flow-steps");
    const suggestions = document.querySelectorAll(".suggestion-chip");
    
    // Suggestions click handler
    suggestions.forEach(chip => {
        chip.addEventListener("click", () => {
            input.value = chip.textContent;
            input.focus();
        });
    });
    
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        
        input.value = "";
        
        // Append user message
        appendChatMessage("user", text);
        
        // Show loading in flow steps
        flowStepsBox.innerHTML = '<div class="loading-spinner"></div>';
        
        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            
            // Append assistant response
            appendChatMessage("assistant", data.answer, data.retrieved_context);
            
            // Render Agent execution steps logs
            renderFlowSteps(data.flow_steps);
            
            // Render XAI SHAP features chart
            renderXAIChart(data.xai);
            
            // Reload overview agent counts
            loadOverviewData();
            
        } catch (e) {
            console.error("Chat error:", e);
            appendChatMessage("assistant", "Sorry, an error occurred while coordinating agents. Please try again.");
            flowStepsBox.innerHTML = '<div class="empty-state"><i class="fa-solid fa-triangle-exclamation font-red"></i><p>Execution failed</p></div>';
        }
    });
}

function appendChatMessage(sender, text, retrievedContext = null) {
    const box = document.getElementById("chat-messages-box");
    const msg = document.createElement("div");
    msg.className = `message ${sender}-msg`;
    
    const avatar = sender === "user" ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
    
    // Parse markdown list structure manually for clean render
    let parsedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    parsedText = parsedText.replace(/### (.*?)\n/g, '<h4>$1</h4>');
    parsedText = parsedText.replace(/\n- (.*?)/g, '<br>• $1');
    
    let contextMarkup = '';
    if (retrievedContext && retrievedContext.length > 0) {
        contextMarkup = `
            <div class="rag-sources">
                <span class="rag-source-title">Retrieved Local Context (RAG):</span>
                <div>
                    ${retrievedContext.map(doc => `<span class="rag-source-chip" title="${doc.snippet}"><i class="fa-solid fa-file-invoice"></i> ${doc.source} (score: ${doc.score})</span>`).join(' ')}
                </div>
            </div>
        `;
    }
    
    msg.innerHTML = `
        <div class="msg-avatar">${avatar}</div>
        <div class="msg-content">
            <p>${parsedText}</p>
            ${contextMarkup}
        </div>
    `;
    
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

function renderFlowSteps(steps) {
    const container = document.getElementById("agent-flow-steps");
    container.innerHTML = "";
    
    steps.forEach((step, idx) => {
        setTimeout(() => {
            const stepEl = document.createElement("div");
            stepEl.className = "trace-step";
            stepEl.innerHTML = `
                <div class="trace-icon"><i class="fa-solid fa-angle-right"></i></div>
                <div class="trace-content">
                    <span class="trace-name">${step.agent}</span>
                    <span class="trace-desc">${step.message}</span>
                </div>
            `;
            container.appendChild(stepEl);
            container.scrollTop = container.scrollHeight;
        }, idx * 300);
    });
}

function renderXAIChart(xai) {
    const ctx = document.getElementById("xai-features-chart").getContext("2d");
    
    // Destroy previous instance
    if (xaiChartInstance) {
        xaiChartInstance.destroy();
    }
    
    document.getElementById("xai-empty-state").style.display = "none";
    document.getElementById("xai-features-chart").style.display = "block";
    
    // Feature weight colors (green positive, red negative impact)
    const colors = xai.weights.map(w => w >= 0 ? "rgba(0, 242, 254, 0.6)" : "rgba(255, 51, 102, 0.6)");
    const borderColors = xai.weights.map(w => w >= 0 ? "rgba(0, 242, 254, 1)" : "rgba(255, 51, 102, 1)");
    
    xaiChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: xai.features,
            datasets: [{
                label: 'SHAP / LIME Weight',
                data: xai.weights,
                backgroundColor: colors,
                borderColor: borderColors,
                borderWidth: 1.5
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.06)' },
                    ticks: { color: '#8b92b6', font: { family: 'Inter', size: 10 } }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#f1f3fa', font: { family: 'Inter', size: 10 } }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// 5. Simulation Workspace System
function initSimulationSystem() {
    const slideHeadcount = document.getElementById("slide-headcount");
    const slideMarketing = document.getElementById("slide-marketing");
    const slideMarkup = document.getElementById("slide-markup");
    const slideSLA = document.getElementById("slide-sla");
    const selectRisk = document.getElementById("select-risk");
    
    const valHeadcount = document.getElementById("val-headcount");
    const valMarketing = document.getElementById("val-marketing");
    const valMarkup = document.getElementById("val-markup");
    const valSLA = document.getElementById("val-sla");
    
    const btnRunSim = document.getElementById("btn-run-simulation");
    
    // Sliders change event listeners
    slideHeadcount.addEventListener("input", () => {
        const val = slideHeadcount.value;
        valHeadcount.textContent = val >= 0 ? `+${val}%` : `${val}%`;
    });
    
    slideMarketing.addEventListener("input", () => {
        const val = slideMarketing.value;
        valMarketing.textContent = val >= 0 ? `+${val}%` : `${val}%`;
    });
    
    slideMarkup.addEventListener("input", () => {
        const val = slideMarkup.value;
        valMarkup.textContent = val >= 0 ? `+${val}%` : `${val}%`;
    });
    
    slideSLA.addEventListener("input", () => {
        valSLA.textContent = `${slideSLA.value} hour${slideSLA.value > 1 ? 's' : ''}`;
    });
    
    btnRunSim.addEventListener("click", async () => {
        const headcount = parseFloat(slideHeadcount.value) / 100;
        const marketing = parseFloat(slideMarketing.value) / 100;
        const markup = parseFloat(slideMarkup.value) / 100;
        const sla = parseFloat(slideSLA.value);
        const risk = selectRisk.value;
        
        btnRunSim.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Running...';
        
        try {
            const res = await fetch("/api/simulate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    headcount_change: headcount,
                    marketing_change: marketing,
                    markup_change: markup,
                    sla_target: sla,
                    risk_tolerance: risk
                })
            });
            const data = await res.json();
            
            // Update UI health score metrics
            document.getElementById("sim-health-val").textContent = data.health_score.after;
            document.getElementById("global-health-val").textContent = data.health_score.after;
            
            // Update outcome rows bars
            updateSimBars(data.metrics);
            
        } catch (e) {
            console.error("Simulation run failed:", e);
        } finally {
            btnRunSim.innerHTML = '<i class="fa-solid fa-play"></i> Run Simulation';
        }
    });
}

function updateSimBars(metrics) {
    // 1. Sales
    const salesAfter = metrics.weekly_sales.after;
    const salesPercent = Math.min(100, Math.max(20, (salesAfter / 1046964.0) * 60));
    const salesBar = document.getElementById("sim-bar-sales");
    salesBar.style.width = `${salesPercent}%`;
    salesBar.textContent = `$${(salesAfter / 1e6).toFixed(2)}M (${metrics.weekly_sales.percent_change >= 0 ? '+' : ''}${metrics.weekly_sales.percent_change}%)`;
    
    // 2. CSAT
    const csatAfter = metrics.csat.after;
    const csatPercent = (csatAfter / 5.0) * 100;
    const csatBar = document.getElementById("sim-bar-csat");
    csatBar.style.width = `${csatPercent}%`;
    csatBar.textContent = `${csatAfter.toFixed(2)} / 5 (${metrics.csat.percent_change >= 0 ? '+' : ''}${metrics.csat.percent_change}%)`;
    
    // 3. Attrition
    const attritionAfter = metrics.attrition_rate.after;
    const attritionPercent = Math.min(100, (attritionAfter / 40.0) * 100); // 40% max range
    const attritionBar = document.getElementById("sim-bar-attrition");
    attritionBar.style.width = `${attritionPercent}%`;
    attritionBar.textContent = `${attritionAfter.toFixed(1)}%`;
    
    // 4. Net Margin
    const marginAfter = metrics.net_profit_margin.after;
    const marginPercent = Math.min(100, Math.max(10, ((marginAfter + 15) / 75) * 100)); // Normal range [-15, 60]
    const marginBar = document.getElementById("sim-bar-margin");
    marginBar.style.width = `${marginPercent}%`;
    marginBar.textContent = `${marginAfter.toFixed(1)}%`;
}

// 6. Network Physics Graph Visualization (HTML5 Canvas physics implementation)
function initGraphTabs() {
    const buttons = document.querySelectorAll(".graph-selection-buttons button");
    const previewBtn = document.getElementById("btn-preview-toggle");
    
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            buttons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            activeGraph = btn.getAttribute("data-graph");
            loadMainGraph(activeGraph);
        });
    });
    
    document.getElementById("btn-graph-reset").addEventListener("click", () => {
        loadMainGraph(activeGraph);
    });
    
    if (previewBtn) {
        previewBtn.addEventListener("click", () => {
            const types = ["workforce", "supply_chain", "financial"];
            const currentIdx = types.indexOf(previewGraphType);
            previewGraphType = types[(currentIdx + 1) % types.length];
            previewBtn.textContent = `Graph: ${previewGraphType.replace('_', ' ').toUpperCase()}`;
            loadPreviewGraph(previewGraphType);
        });
    }
}

async function loadMainGraph(type) {
    if (mainGraphAnimationId) {
        cancelAnimationFrame(mainGraphAnimationId);
    }
    
    try {
        const res = await fetch(`/api/graphs/${type}`);
        const data = await res.json();
        
        mainGraphNodes = data.nodes;
        mainGraphLinks = data.links;
        
        initPhysicsLayout(mainGraphNodes, mainGraphLinks);
        
        const canvas = document.getElementById("main-graph-canvas");
        animateGraph(canvas, mainGraphNodes, mainGraphLinks, true);
        
    } catch (e) {
        console.error("Failed to load graph data:", e);
    }
}

async function loadPreviewGraph(type) {
    if (previewGraphAnimationId) {
        cancelAnimationFrame(previewGraphAnimationId);
    }
    
    try {
        const res = await fetch(`/api/graphs/${type}`);
        const data = await res.json();
        
        previewGraphNodes = data.nodes;
        previewGraphLinks = data.links;
        
        initPhysicsLayout(previewGraphNodes, previewGraphLinks);
        
        const canvas = document.getElementById("preview-graph-canvas");
        animateGraph(canvas, previewGraphNodes, previewGraphLinks, false);
        
    } catch (e) {
        console.error("Failed to load preview graph data:", e);
    }
}

// Simple force-directed graph physics initializer
function initPhysicsLayout(nodes, links) {
    // Arrange nodes in circle
    const center = { x: 300, y: 200 };
    const radius = 120;
    
    nodes.forEach((node, idx) => {
        const angle = (idx / nodes.length) * Math.PI * 2;
        node.x = center.x + Math.cos(angle) * radius + (Math.random() - 0.5) * 10;
        node.y = center.y + Math.sin(angle) * radius + (Math.random() - 0.5) * 10;
        node.vx = 0;
        node.vy = 0;
    });
}

function animateGraph(canvas, nodes, links, isMainGraph) {
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    
    // Fit canvas resolution to element dimensions
    const resizeCanvas = () => {
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
    };
    resizeCanvas();
    
    // Physics constants
    const centerAttraction = 0.015;
    const nodeRepulsion = 1200;
    const linkTension = 0.04;
    const linkLength = 80;
    const damping = 0.85;
    
    // Mouse hover trackers
    let hoveredNode = null;
    let mouse = { x: -100, y: -100 };
    
    if (isMainGraph) {
        canvas.addEventListener("mousemove", (e) => {
            const rect = canvas.getBoundingClientRect();
            mouse.x = e.clientX - rect.left;
            mouse.y = e.clientY - rect.top;
        });
        canvas.addEventListener("mouseleave", () => {
            mouse.x = -100;
            mouse.y = -100;
            const tooltip = document.getElementById("graph-tooltip");
            if (tooltip) tooltip.textContent = "Hover nodes for metadata info";
        });
    }
    
    const colors = {
        "Leadership": "#9a4dff", "Finance": "#00c6ff", "HR": "#00f2fe",
        "Support": "#ff3366", "Retail": "#ffc837", "Risk": "#ff758c",
        "DC": "#9a4dff", "Hub": "#00c6ff", "Store": "#00f2fe",
        "Inflow": "#00f2fe", "Reserve": "#9a4dff", "Outflow": "#ff3366"
    };

    const tick = () => {
        const w = canvas.width;
        const h = canvas.height;
        const cx = w / 2;
        const cy = h / 2;
        
        // 1. Node Repulsion (push away from each other)
        for (let i = 0; i < nodes.length; i++) {
            const n1 = nodes[i];
            for (let j = i + 1; j < nodes.length; j++) {
                const n2 = nodes[j];
                const dx = n2.x - n1.x;
                const dy = n2.y - n1.y;
                let dist = Math.sqrt(dx * dx + dy * dy);
                if (dist === 0) dist = 0.1;
                
                const force = nodeRepulsion / (dist * dist);
                const fx = (dx / dist) * force;
                const fy = (dy / dist) * force;
                
                n1.vx -= fx;
                n1.vy -= fy;
                n2.vx += fx;
                n2.vy += fy;
            }
        }
        
        // 2. Link Spring Tension (pull together connected nodes)
        links.forEach(link => {
            const n1 = nodes.find(n => n.id === link.source);
            const n2 = nodes.find(n => n.id === link.target);
            if (!n1 || !n2) return;
            
            const dx = n2.x - n1.x;
            const dy = n2.y - n1.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist === 0) return;
            
            const displacement = dist - linkLength;
            const force = displacement * linkTension;
            const fx = (dx / dist) * force;
            const fy = (dy / dist) * force;
            
            n1.vx += fx;
            n1.vy += fy;
            n2.vx -= fx;
            n2.vy -= fy;
        });
        
        // 3. Center Attraction & Bounds
        hoveredNode = null;
        nodes.forEach(node => {
            node.vx += (cx - node.x) * centerAttraction;
            node.vy += (cy - node.y) * centerAttraction;
            
            // Apply velocity damping
            node.x += node.vx;
            node.y += node.vy;
            node.vx *= damping;
            node.vy *= damping;
            
            // Check hover
            const nodeSize = node.size || 12;
            const dx = mouse.x - node.x;
            const dy = mouse.y - node.y;
            if (Math.sqrt(dx * dx + dy * dy) < nodeSize + 4) {
                hoveredNode = node;
            }
        });
        
        // Draw scene
        ctx.clearRect(0, 0, w, h);
        
        // Draw Links
        links.forEach(link => {
            const n1 = nodes.find(n => n.id === link.source);
            const n2 = nodes.find(n => n.id === link.target);
            if (!n1 || !n2) return;
            
            ctx.beginPath();
            ctx.moveTo(n1.x, n1.y);
            ctx.lineTo(n2.x, n2.y);
            ctx.strokeStyle = "rgba(255,255,255,0.06)";
            ctx.lineWidth = link.value || 2;
            ctx.stroke();
        });
        
        // Draw Nodes
        nodes.forEach(node => {
            const size = node.size || 12;
            const color = colors[node.group] || "#00c6ff";
            
            ctx.beginPath();
            ctx.arc(node.x, node.y, size, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.shadowBlur = 10;
            ctx.shadowColor = color;
            ctx.fill();
            ctx.shadowBlur = 0; // reset
            
            // Outer glow if hovered
            if (node === hoveredNode) {
                ctx.beginPath();
                ctx.arc(node.x, node.y, size + 5, 0, Math.PI * 2);
                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // Show tooltip metadata
                if (isMainGraph) {
                    const tooltip = document.getElementById("graph-tooltip");
                    tooltip.innerHTML = `<strong>${node.label}</strong><br>Category: ${node.group}`;
                }
            }
            
            // Text labels
            if (isMainGraph || size > 15) {
                ctx.fillStyle = "#f1f3fa";
                ctx.font = `600 ${size > 15 ? 12 : 10}px Inter`;
                ctx.textAlign = "center";
                ctx.fillText(node.id, node.x, node.y + size + 14);
            }
        });
        
        // Loop frame
        if (isMainGraph) {
            mainGraphAnimationId = requestAnimationFrame(tick);
        } else {
            previewGraphAnimationId = requestAnimationFrame(tick);
        }
    };
    
    tick();
}

// 7. Telemetry & Metrics Update system
function initTelemetrySystem() {
    const ctx = document.getElementById("latency-line-chart").getContext("2d");
    const pointsLimit = 20;
    
    const labels = Array.from({ length: pointsLimit }, (_, i) => `${i}s`);
    const defaultData = Array.from({ length: pointsLimit }, () => 15.0 + Math.random() * 5);
    
    latencyChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'API Request Latency (ms)',
                data: defaultData,
                borderColor: '#00f2fe',
                backgroundColor: 'rgba(0, 242, 254, 0.08)',
                fill: true,
                tension: 0.4,
                borderWidth: 2,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { display: false },
                y: {
                    grid: { color: 'rgba(255,255,255,0.06)' },
                    ticks: { color: '#8b92b6', font: { family: 'Inter', size: 10 } }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
    
    // Poll telemetry data periodically (3s)
    setInterval(updateTelemetryStats, 3000);
    updateTelemetryStats(); // first run
}

async function updateTelemetryStats() {
    try {
        const res = await fetch("/api/monitoring/metrics");
        const data = await res.json();
        
        // Update stats row
        document.getElementById("stat-cpu").textContent = `${data.system.cpu_utilization_pct}%`;
        document.getElementById("stat-mem").textContent = `${data.system.memory_usage_gb} GB / 16.0 GB`;
        document.getElementById("stat-latency").textContent = `${data.system.api_latency_ms} ms`;
        
        // Format uptime
        const s = data.system.uptime_seconds;
        const uptimeStr = new Date(s * 1000).toISOString().substr(11, 8);
        document.getElementById("stat-uptime").textContent = uptimeStr;
        
        // Add point to chart
        if (latencyChartInstance) {
            const chartData = latencyChartInstance.data.datasets[0].data;
            chartData.shift();
            chartData.push(data.system.api_latency_ms);
            latencyChartInstance.update('none'); // silent update
        }
        
        // Update model drift stability list
        const driftList = document.getElementById("drift-status-rows");
        driftList.innerHTML = "";
        data.model_drift.forEach(model => {
            const row = document.createElement("div");
            const isWarning = model.status.includes("Warning");
            row.className = `drift-row ${isWarning ? 'warning' : 'healthy'}`;
            
            const icon = isWarning ? '<i class="fa-solid fa-triangle-exclamation"></i>' : '<i class="fa-solid fa-shield-halved"></i>';
            
            row.innerHTML = `
                <div class="drift-info">
                    <span class="drift-name">${icon} ${model.model_name}</span>
                    <span class="drift-psi">Stability Index (PSI): ${model.population_stability_index} / Thresh: ${model.threshold}</span>
                </div>
                <span>${model.status}</span>
            `;
            driftList.appendChild(row);
        });
        
        // Update system terminal logs
        const logsBox = document.getElementById("terminal-logs-box");
        logsBox.innerHTML = "";
        data.alerts.forEach(alert => {
            const logLine = document.createElement("div");
            const isWarning = alert.severity === "Warning";
            logLine.className = `log-entry ${isWarning ? 'log-warning' : 'log-info'}`;
            logLine.innerHTML = `
                <span class="log-time">[${alert.timestamp}]</span>
                <span>[${alert.source}] [${alert.severity.toUpperCase()}] ${alert.message}</span>
            `;
            logsBox.appendChild(logLine);
        });
        
    } catch (e) {
        console.error("Failed to fetch telemetry metrics update:", e);
    }
}
