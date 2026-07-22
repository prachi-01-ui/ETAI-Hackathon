const API_BASE_URL = "http://127.0.0.1:8000";

/* ===== DATA ===== */
let NEWS = [
  { id: 1, source: "Reuters", time: "2 min ago", title: "Iran closes Strait of Hormuz to US-flagged vessels amid escalating tensions", summary: "Iranian naval forces announced partial closure measures for vessels flagged under US allies, sending oil futures up 4.2% in early trading.", entities: ["Iran", "USA", "Hormuz", "IRGC"], category: "Maritime Blockade", severity: "critical", countries: ["Iran", "USA", "UAE"], ports: ["Bandar Abbas", "Fujairah"], routes: ["Hormuz Strait"], impact: "Direct disruption to 20% of India's crude imports. Immediate SPR review required.", priority: "Critical" },
  { id: 2, source: "Bloomberg", time: "15 min ago", title: "Houthi forces resume Red Sea attacks; 3 tankers diverted around Cape of Good Hope", summary: "Three VLCC tankers carrying Saudi crude have been rerouted adding 14 days to delivery time and $2.4M in additional freight costs.", entities: ["Houthi", "Saudi Arabia", "Suez Canal", "VLCC"], category: "Maritime Attack", severity: "high", countries: ["Yemen", "Saudi Arabia", "Egypt"], ports: ["Jeddah", "Port Said"], routes: ["Red Sea", "Suez Canal"], impact: "15% of India's imports via this route. Cost increase of ~$180M/month at scale.", priority: "High" },
  { id: 3, source: "Al Jazeera", time: "28 min ago", title: "Russia expands oil export restrictions; ESPO pipeline output cut by 18%", summary: "Moscow announced further curbs on ESPO crude exports as retaliation against new EU sanctions, affecting spot markets.", entities: ["Russia", "EU", "ESPO", "Rosneft"], category: "Sanctions", severity: "high", countries: ["Russia", "EU", "Germany"], ports: ["Kozmino", "Novorossiysk"], routes: ["Arctic Route", "ESPO"], impact: "Moderate. India sources ~5% from Russia via this route. Alternatives available.", priority: "High" },
  { id: 4, source: "S&P Global", time: "42 min ago", title: "Brent crude surges past $98 amid Middle East supply concerns", summary: "Brent crude hit $98.40/bbl on fears of supply disruptions, highest since 2023 energy crisis. WTI at $94.20.", entities: ["Brent", "WTI", "OPEC+", "Middle East"], category: "Price Surge", severity: "medium", countries: ["Saudi Arabia", "Iraq", "UAE"], ports: ["Ras Tanura", "Basra"], routes: ["Persian Gulf", "Strait of Hormuz"], impact: "Cost inflation of ~12% on crude import bill. May trigger SPR drawdown advisory.", priority: "Medium" },
  { id: 5, source: "Lloyd's List", time: "1 hr ago", title: "Port congestion at Fujairah reaches 5-year high; 47 vessels at anchor", summary: "UAE's key bunkering hub sees unprecedented congestion as tankers avoid Hormuz. Wait times exceed 8 days.", entities: ["Fujairah", "UAE", "VLCC", "Bunkering"], category: "Port Congestion", severity: "medium", countries: ["UAE"], ports: ["Fujairah"], routes: ["Persian Gulf"], impact: "Delays for 8 India-bound tankers currently anchored. Estimated delay: 6-10 days.", priority: "Medium" },
  { id: 6, source: "Platts", time: "2 hr ago", title: "Iraq-Turkey pipeline resumes pumping after 3-day technical halt", summary: "The Kirkuk-Ceyhan pipeline resumes operations at 70% capacity following emergency repairs. Full resumption expected in 72 hours.", entities: ["Iraq", "Turkey", "Kirkuk", "Ceyhan"], category: "Infrastructure", severity: "low", countries: ["Iraq", "Turkey"], ports: ["Ceyhan"], routes: ["Mediterranean"], impact: "Minimal direct impact on India. Global supply relief expected in 72 hours.", priority: "Low" },
];

/* ===== LIVE NEWS API ===== */
async function fetchLiveNews() {
  try {
    const response = await fetch(`${API_BASE_URL}/news/energy-risk?limit=6`);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const result = await response.json();

    console.log("Live news loaded:", result);

    if (!result.articles || result.articles.length === 0) {
      console.warn("No live articles returned. Using fallback news.");
      renderNews();
      return;
    }

    NEWS = result.articles.map((article, index) => ({
      id: index + 1,

      source:
        article.source ||
        "Live Intelligence",

      time:
        article.published_at
          ? formatNewsTime(article.published_at)
          : "Live",

      title:
        article.title ||
        "Energy Supply Chain Update",

      summary:
        article.description ||
        "Live energy and supply-chain intelligence update.",

      entities: [],

      category:
        "Live Intelligence",

      severity:
        "medium",

      countries: [],

      ports: [],

      routes: [],

      impact:
        "Live intelligence received. AI impact analysis pending.",

      priority:
        "Medium",

      url:
        article.url || null
    }));

    renderNews();

  } catch (error) {
    console.error("Failed to load live news:", error);

    // Keep existing hardcoded NEWS as fallback
    renderNews();
  }
}


/* ===== FORMAT LIVE NEWS TIME ===== */
function formatNewsTime(publishedAt) {
  const published = new Date(publishedAt);
  const now = new Date();

  const differenceMs = now - published;
  const differenceMinutes = Math.floor(
    differenceMs / (1000 * 60)
  );

  if (differenceMinutes < 1) {
    return "Just now";
  }

  if (differenceMinutes < 60) {
    return `${differenceMinutes} min ago`;
  }

  const differenceHours = Math.floor(
    differenceMinutes / 60
  );

  if (differenceHours < 24) {
    return `${differenceHours} hr ago`;
  }

  const differenceDays = Math.floor(
    differenceHours / 24
  );

  return `${differenceDays} day${differenceDays > 1 ? "s" : ""} ago`;
}

const XAI_FACTORS = [
  { icon: "⚠️", title: "Military Activity Increased", sub: "+34% naval deployments in Hormuz", weight: "+18 pts", pct: 85, color: "#ef4444" },
  { icon: "📈", title: "Brent Crude Rising", sub: "$98.40/bbl — 4-month high", weight: "+12 pts", pct: 70, color: "#f97316" },
  { icon: "🚫", title: "New Sanctions Announced", sub: "EU Round-12 targets Russian oil", weight: "+9 pts", pct: 55, color: "#f97316" },
  { icon: "🛢️", title: "Tanker Delays Detected", sub: "Avg delay 6.2 days — 3σ above norm", weight: "+8 pts", pct: 50, color: "#eab308" },
  { icon: "🚢", title: "Port Congestion Rising", sub: "Fujairah at 5-year high", weight: "+6 pts", pct: 40, color: "#eab308" },
  { icon: "🌐", title: "Geopolitical Clustering", sub: "3 simultaneous hotspots active", weight: "+5 pts", pct: 35, color: "#3b82f6" },
];

const HIST_EVENTS = [
  { name: "Hormuz Crisis 2019", year: "2019", sim: 87, simColor: "#ef4444", desc: "IRGC seized British tanker Stena Impero; oil spiked 4%. US deployed carrier group. India rerouted 22% of imports.", dur: "6 weeks", impact: "$2.1B additional cost" },
  { name: "Red Sea Attacks 2024", year: "2024", sim: 79, simColor: "#f97316", desc: "Houthi attacks forced 90+ vessels to Cape rerouting. Insurance costs tripled on affected routes.", dur: "4+ months", impact: "$4.8B freight overrun" },
  { name: "Russia–Ukraine Supply Shock", year: "2022", sim: 65, simColor: "#eab308", desc: "Western sanctions cut Russian supply; India absorbed discounted Urals crude. ESPO volumes to India up 280%.", dur: "Ongoing", impact: "$8.2B hedging losses globally" },
];

const ALERTS = [
  { sev: "crit", icon: "🔴", title: "Hormuz Closure Alert", desc: "IRGC announced partial closure to US-allied vessels. 3 India-bound VLCCs at risk.", time: "2 min ago", action: "Review SPR" },
  { sev: "crit", icon: "🔴", title: "Oil Price Threshold Breach", desc: "Brent crossed $98/bbl trigger level. Activating procurement hedge protocol.", time: "8 min ago", action: "Activate Hedge" },
  { sev: "high", icon: "🟠", title: "Red Sea Route Disruption", desc: "Recommended rerouting via Cape of Good Hope for 5 vessels scheduled this week.", time: "15 min ago", action: "Reroute" },
  { sev: "high", icon: "🟠", title: "Tanker Insurance Spike", desc: "War-risk premium on Hormuz route up 340bps. Cost impact: $12M/month.", time: "31 min ago", action: "Assess Cost" },
  { sev: "med", icon: "🟡", title: "Fujairah Port Delay", desc: "8 India-bound tankers anchored at Fujairah. ETA delays of 6-10 days forecast.", time: "45 min ago", action: "Monitor" },
  { sev: "low", icon: "🟢", title: "ESPO Alternative Available", desc: "Kozmino port operating normally. 15% additional capacity available for spot booking.", time: "1 hr ago", action: "Procure" },
];

/* ===== CHART INSTANCE ===== */
let trendChart = null;

/* ===== INIT ===== */

window.addEventListener('DOMContentLoaded', async () => {

  updateTimestamp();

  setInterval(updateTimestamp, 30000);


  // -----------------------------------------
  // RISK EVENT MONITORING
  // -----------------------------------------

  if (PLATFORM_SETTINGS.riskEventMonitoring) {

    await fetchLiveNews();

  } else {

    const newsFeed =
      document.getElementById("news-feed");

    if (newsFeed) {

      newsFeed.innerHTML = `
        <div class="empty-state">
          <p>
            Risk event monitoring is currently disabled
            in Platform Settings.
          </p>
        </div>
      `;

    }

  }


  renderXAI();

  renderHistorical();

  renderAlerts();


  // -----------------------------------------
  // INITIALIZE MAP
  // -----------------------------------------

  initMap();


  // Ports are required for map and route matching
  await fetchPorts();


  // -----------------------------------------
  // SHIPPING ROUTE TRACKING
  // -----------------------------------------

  if (PLATFORM_SETTINGS.shippingRouteTracking) {

    await fetchShippingRoutes();

  } else {

    if (
      window.routesLayer &&
      window.map &&
      window.map.hasLayer(window.routesLayer)
    ) {

      window.map.removeLayer(window.routesLayer);

    }

  }


  // -----------------------------------------
  // DASHBOARD COMPONENTS
  // -----------------------------------------

  initGauge();

  initTrendChart('risk');

  initKnowledgeGraph();


  // -----------------------------------------
  // NAVIGATION
  // -----------------------------------------

  setupNav();

});

function updateTimestamp() {
  const now = new Date();
  document.getElementById('last-updated').textContent =
    'Updated: ' + now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  const rm = document.getElementById('rm-calc');
  if (rm) rm.textContent = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
}

/* ===== NEWS ===== */
function renderNews() {
  const feed = document.getElementById('news-feed');
  feed.innerHTML = NEWS.map((n, i) => `
    <div class="news-item" data-id="${n.id}" onclick="selectNews(${n.id})" style="animation-delay:${i * 0.07}s">
      <div class="news-hdr">
        <span class="news-source">${n.source}</span>
        <span class="news-time">${n.time}</span>
      </div>
      <div class="news-title">${n.title}</div>
      <div class="news-summary">${n.summary}</div>
      <div class="news-footer">
        ${n.entities.map(e => `<span class="entity-tag">${e}</span>`).join('')}
        <span class="sev-badge sev-${n.severity}">${n.severity.toUpperCase()}</span>
      </div>
    </div>
  `).join('');
}

async function selectNews(id) {

  // Highlight selected news card
  document
    .querySelectorAll('.news-item')
    .forEach(el => el.classList.remove('selected'));

  document
    .querySelector(
      `.news-item[data-id="${id}"]`
    )
    ?.classList.add('selected');

  // Find selected live article
  const n = NEWS.find(
    article => article.id === id
  );

  if (!n) return;

  const body = document.getElementById(
    'ai-analysis-body'
  );

  if (!body) return;

  // Show loading state while Gemini analyses the article
  body.innerHTML = `
    <div class="ai-field">
      <div class="ai-field-label">
        AI Risk Intelligence
      </div>

      <div class="ai-field-val">
        Gemini is analysing this live intelligence...
      </div>
    </div>
  `;

  try {

    const response = await fetch(
      `${API_BASE_URL}/news/analyze`,
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          title: n.title,
          description: n.summary,
          source: n.source
        })
      }
    );

    if (!response.ok) {
      throw new Error(
        `HTTP error: ${response.status}`
      );
    }

    const result = await response.json();

    console.log(
      "Gemini news analysis:",
      result
    );

    const analysis = result.analysis;

    // Update the live NEWS object so the analysis
    // remains available after Gemini returns
    n.severity =
      analysis.severity || 'medium';

    n.category =
      analysis.category || 'Live Intelligence';

    n.entities =
      analysis.entities || [];

    n.countries =
      analysis.countries || [];

    n.ports =
      analysis.ports || [];

    n.routes =
      analysis.routes || [];

    n.impact =
      analysis.impact ||
      'No significant operational impact identified.';

    n.priority =
      analysis.priority || 'Medium';

    n.risk_score =
      analysis.risk_score ?? 0;

    const impactPct = Math.min(
      100,
      Math.max(
        0,
        Number(n.risk_score) || 0
      )
    );

    // Render Gemini analysis using your existing UI
    body.innerHTML = `

      <div class="ai-field">
        <div class="ai-field-label">
          AI Summary
        </div>

        <div class="ai-field-val">
          ${n.summary}
        </div>
      </div>


      <div class="ai-field">
        <div class="ai-field-label">
          Countries Involved
        </div>

        <div class="ai-tags">
          ${
            n.countries.length
              ? n.countries
                  .map(
                    c =>
                      `<span class="ai-tag">🌍 ${c}</span>`
                  )
                  .join('')
              : '<span class="ai-tag">None identified</span>'
          }
        </div>
      </div>


      <div class="ai-field">
        <div class="ai-field-label">
          Ports Affected
        </div>

        <div class="ai-tags">
          ${
            n.ports.length
              ? n.ports
                  .map(
                    p =>
                      `<span class="ai-tag">⚓ ${p}</span>`
                  )
                  .join('')
              : '<span class="ai-tag">None identified</span>'
          }
        </div>
      </div>


      <div class="ai-field">
        <div class="ai-field-label">
          Shipping Routes
        </div>

        <div class="ai-tags">
          ${
            n.routes.length
              ? n.routes
                  .map(
                    r =>
                      `<span class="ai-tag">🚢 ${r}</span>`
                  )
                  .join('')
              : '<span class="ai-tag">None identified</span>'
          }
        </div>
      </div>


      <div class="ai-field">
        <div class="ai-field-label">
          Event Classification
        </div>

        <div class="ai-tags">
          <span class="ai-tag sev-badge sev-${n.severity}">
            ${n.category}
          </span>
        </div>
      </div>


      <div class="ai-field">
        <div class="ai-field-label">
          Potential Impact on India
        </div>

        <div class="ai-field-val">
          ${n.impact}
        </div>

        <div class="impact-bar">
          <div
            class="impact-fill"
            style="width:${impactPct}%"
          ></div>
        </div>
      </div>


      <div class="ai-field">
        <div class="ai-field-label">
          AI Risk Score
        </div>

        <div class="ai-field-val">
          ${n.risk_score}/100
        </div>
      </div>


      <div class="ai-field">
        <div class="ai-field-label">
          Monitoring Priority
        </div>

        <div class="ai-tags">
          <span class="ai-tag sev-badge sev-${n.severity}">
            ${n.priority}
          </span>
        </div>
      </div>

    `;

    // Refresh news cards so Gemini severity
    // replaces the temporary MEDIUM badge
    renderNews();

    // Re-select the current article visually
    document
      .querySelector(
        `.news-item[data-id="${id}"]`
      )
      ?.classList.add('selected');

  } catch (error) {

    console.error(
      "Gemini news analysis failed:",
      error
    );

    body.innerHTML = `
      <div class="ai-field">

        <div class="ai-field-label">
          AI Analysis
        </div>

        <div class="ai-field-val">
          Unable to analyse this intelligence at the moment.
        </div>

      </div>
    `;
  }
}

/* ===== XAI ===== */
function renderXAI() {
  const el = document.getElementById('xai-factors');
  el.innerHTML = XAI_FACTORS.map(f => `
    <div class="xai-factor">
      <div class="xf-icon" style="background:${f.color}22">${f.icon}</div>
      <div class="xf-body">
        <div class="xf-title">✓ ${f.title}</div>
        <div class="xf-sub">${f.sub}</div>
      </div>
      <div class="xf-bar-wrap"><div class="xf-bar" style="width:${f.pct}%;background:${f.color}"></div></div>
      <div class="xf-weight" style="color:${f.color}">${f.weight}</div>
    </div>
  `).join('');
}

/* ===== HISTORICAL ===== */
function renderHistorical() {
  const el = document.getElementById('hist-events');
  el.innerHTML = HIST_EVENTS.map(h => `
    <div class="hist-item">
      <div class="hist-hdr">
        <span class="hist-name">${h.name}</span>
        <span class="hist-year">${h.year}</span>
        <span class="hist-sim" style="background:${h.simColor}22;color:${h.simColor}">${h.sim}% similar</span>
      </div>
      <div class="hist-desc">${h.desc}</div>
      <div class="hist-meta">
        <span class="hm-item">Duration: <span class="hm-v">${h.dur}</span></span>
        <span class="hm-item">Impact: <span class="hm-v">${h.impact}</span></span>
      </div>
    </div>
  `).join('');
}

/* ===== ALERTS ===== */

function renderAlerts() {

  const el = document.getElementById('alerts-list');

  if (!el) {
    return;
  }

  const classMap = {
    crit: 'alert-crit',
    high: 'alert-high',
    med: 'alert-med',
    low: 'alert-low'
  };


  // Filter alerts according to Platform Settings
  const filteredAlerts = ALERTS.filter(alert => {

    const title = alert.title.toLowerCase();
    const desc = alert.desc.toLowerCase();


    // -----------------------------------------
    // CRITICAL RISK ALERTS
    // -----------------------------------------

    if (
      alert.sev === "crit" &&
      !PLATFORM_SETTINGS.criticalRiskAlerts
    ) {
      return false;
    }


    // -----------------------------------------
    // SUPPLY DISRUPTION ALERTS
    // -----------------------------------------

    const isSupplyDisruption =
      title.includes("disruption") ||
      title.includes("route") ||
      desc.includes("disruption") ||
      desc.includes("rerouting");


    if (
      isSupplyDisruption &&
      !PLATFORM_SETTINGS.supplyDisruptionAlerts
    ) {
      return false;
    }


    // -----------------------------------------
    // RESERVE WARNINGS
    // -----------------------------------------

    const isReserveWarning =
      title.includes("reserve") ||
      title.includes("spr") ||
      desc.includes("reserve") ||
      desc.includes("spr");


    if (
      isReserveWarning &&
      !PLATFORM_SETTINGS.reserveWarnings
    ) {
      return false;
    }


    return true;

  });


  // If every alert has been disabled/filtered
  if (filteredAlerts.length === 0) {

    el.innerHTML = `
      <div class="empty-state">
        <p>
          No active alerts based on your current
          Platform Settings.
        </p>
      </div>
    `;

    return;
  }


  // Render enabled alerts
  el.innerHTML = filteredAlerts.map(a => `

    <div class="alert-item ${classMap[a.sev]}">

      <div class="alert-icon">
        ${a.icon}
      </div>

      <div class="alert-body">

        <div class="alert-title">
          ${a.title}
        </div>

        <div class="alert-desc">
          ${a.desc}
        </div>

        <div class="alert-footer">

          <span class="alert-time">
            ${a.time}
          </span>

          <button class="alert-action">
            ${a.action} →
          </button>

        </div>

      </div>

    </div>

  `).join('');

}

/* ===== MAP ===== */
function initMap() {
  window.map = L.map('world-map', {
    center: [20, 55], zoom: 3,
    zoomControl: false, attributionControl: false,
    scrollWheelZoom: false,
  });
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '', subdomains: 'abcd', maxZoom: 18
  }).addTo(map);

  // Layer groups for backend map data
  window.routesLayer = L.layerGroup().addTo(window.map);
  window.portsLayer = L.layerGroup().addTo(window.map);

  // Shipping routes will be loaded from FastAPI
  

  // Supplier countries (circles)
  const countries = [
    { pos: [25.3, 51.5], name: 'Qatar', risk: 55, color: '#eab308' },
    { pos: [23.9, 45.1], name: 'Saudi Arabia', risk: 70, color: '#f97316' },
    { pos: [33.2, 43.7], name: 'Iraq', risk: 65, color: '#f97316' },
    { pos: [32.4, 53.7], name: 'Iran', risk: 92, color: '#ef4444' },
    { pos: [24.5, 54.4], name: 'UAE', risk: 45, color: '#eab308' },
    { pos: [55, 37], name: 'Russia', risk: 60, color: '#f97316' },
    { pos: [-1.3, 36.8], name: 'East Africa', risk: 30, color: '#22c55e' },
    { pos: [20.6, 72.8], name: 'Mumbai Port', risk: 25, color: '#00D4FF' },
  ];
  countries.forEach(c => {
    L.circleMarker(c.pos, { radius: c.name.includes('Port') ? 10 : 8, fillColor: c.color, color: c.color, weight: 1, fillOpacity: .7 })
      .addTo(map)
      .bindTooltip(`<strong>${c.name}</strong><br/>Risk: ${c.risk}/100`, { permanent: false });
  });

  // Animated tankers
  window.tankersLayer = L.layerGroup().addTo(window.map);

  const tankerIcon = L.divIcon({ html: '🛢️', className: '', iconSize: [18, 18] });
  const tankers = [{ pos: [22, 59] }, { pos: [15, 65] }, { pos: [20, 50] }];
  tankers.forEach(t => {
    L.marker(t.pos, { icon: tankerIcon }).addTo(window.tankersLayer).bindTooltip('VLCC Tanker', { sticky: true });
  });
}

/* ===== GAUGE ===== */
function initGauge(score = 74) {
  const canvas = document.getElementById('risk-gauge');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  const cx = 110, cy = 115, r = 90, sw = 14;
  const startA = Math.PI, endA = 2 * Math.PI;
  const pct = score / 100;
  function draw() {
    ctx.clearRect(0, 0, 220, 130);
    // bg arc
    ctx.beginPath(); ctx.arc(cx, cy, r, startA, endA);
    ctx.strokeStyle = '#1a2d48'; ctx.lineWidth = sw; ctx.stroke();
    // gradient arc
    const grad = ctx.createLinearGradient(20, cy, 200, cy);
    grad.addColorStop(0, '#22c55e'); grad.addColorStop(.5, '#eab308'); grad.addColorStop(1, '#ef4444');
    ctx.beginPath(); ctx.arc(cx, cy, r, startA, startA + (endA - startA) * pct);
    ctx.strokeStyle = grad; ctx.lineWidth = sw; ctx.lineCap = 'round'; ctx.stroke();
    // tick marks
    for (let i = 0; i <= 10; i++) {
      const a = startA + (endA - startA) * (i / 10);
      const x1 = cx + Math.cos(a) * (r - sw / 2 - 2), y1 = cy + Math.sin(a) * (r - sw / 2 - 2);
      const x2 = cx + Math.cos(a) * (r + sw / 2 + 2), y2 = cy + Math.sin(a) * (r + sw / 2 + 2);
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
      ctx.strokeStyle = '#0d1b30'; ctx.lineWidth = 2; ctx.stroke();
    }
    // labels
    ['0', '25', '50', '75', '100'].forEach((lbl, i) => {
      const a = startA + (endA - startA) * (i / 4);
      const x = cx + Math.cos(a) * (r + 25), y = cy + Math.sin(a) * (r + 25);
      ctx.fillStyle = '#4a6a8a'; ctx.font = '10px Inter'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(lbl, x, y);
    });
  }
  draw();
}

/* ===== TREND CHART ===== */
const labels14 = Array.from({ length: 14 }, (_, i) => {
  const d = new Date(); d.setDate(d.getDate() - 13 + i); return d.toLocaleDateString('en', { month: 'short', day: 'numeric' });
});
const CHART_DATA = {
  risk: { label: 'Risk Score', data: [45, 48, 52, 49, 55, 58, 61, 63, 60, 65, 68, 70, 72, 74], color: '#ef4444' },
  oil: { label: 'Brent Crude ($)', data: [72, 74, 73, 75, 78, 80, 82, 85, 83, 88, 91, 94, 96, 98], color: '#f97316' },
  events: { label: 'Active Events', data: [12, 13, 14, 13, 15, 16, 17, 18, 16, 19, 20, 21, 22, 23], color: '#3b82f6' },
};

async function initTrendChart(key) {
  const ctx = document.getElementById('trend-chart');

  if (!ctx) return;

  if (trendChart) {
    trendChart.destroy();
  }

  let chartLabels = labels14;
  let chartData;

  const d = CHART_DATA[key];

  // For Risk Score, load real historical data from FastAPI/PostgreSQL
  if (key === 'risk') {
    try {
      const response = await fetch(
        `${API_BASE_URL}/risk-intelligence/trends/risk-score`
      );

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const history = await response.json();

      console.log("Risk trend history loaded:", history);

      if (history.length > 0) {
        chartLabels = history.map(item => {
          const date = new Date(item.recorded_at);

          return date.toLocaleDateString(
            'en-US',
            {
              month: 'short',
              day: 'numeric'
            }
          );
        });

        chartData = history.map(
          item => item.risk_score
        );
      } else {
        chartData = d.data;
      }

    } catch (error) {
      console.error(
        "Failed to load risk trend history:",
        error
      );

      chartData = d.data;
    }

  } else {
    // Keep existing data for the other chart modes for now
    chartData = d.data;
  }

  trendChart = new Chart(ctx, {
    type: 'line',

    data: {
      labels: chartLabels,

      datasets: [{
        label: d.label,
        data: chartData,

        borderColor: d.color,
        backgroundColor: d.color + '22',

        borderWidth: 2,
        pointRadius: 3,
        pointHoverRadius: 5,

        tension: .4,
        fill: true,
      }]
    },

    options: {
      responsive: true,
      maintainAspectRatio: false,

      plugins: {
        legend: {
          display: false
        },

        tooltip: {
          backgroundColor: '#0d1b30',
          borderColor: '#1a2d48',
          borderWidth: 1,
          titleColor: '#e2eaf5',
          bodyColor: '#8da5bf'
        }
      },

      scales: {
        x: {
          grid: {
            color: '#1a2d4866'
          },

          ticks: {
            color: '#4a6a8a',
            font: {
              size: 10
            }
          }
        },

        y: {
          grid: {
            color: '#1a2d4866'
          },

          ticks: {
            color: '#4a6a8a',
            font: {
              size: 10
            }
          }
        }
      }
    }
  });
}

function switchChart(key, btn) {
  const chartControls = btn.parentElement;

  chartControls
    .querySelectorAll('.ctrl-btn')
    .forEach(b => b.classList.remove('active'));

  btn.classList.add('active');

  initTrendChart(key);
}

/* ===== KNOWLEDGE GRAPH ===== */
async function initKnowledgeGraph() {
  const el = document.getElementById('knowledge-graph');

  if (!el || typeof d3 === 'undefined') return;

  const W = el.clientWidth || 500;
  const H = el.clientHeight || 320;

  d3.select(el).selectAll('*').remove();

  const svg = d3.select(el)
    .append('svg')
    .attr('width', '100%')
    .attr('height', '100%')
    .attr('viewBox', `0 0 ${W} ${H}`);

  try {
    // Load real graph data from Neo4j through FastAPI
    const response = await fetch(
      `${API_BASE_URL}/knowledge-graph/graph`
    );

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const graphData = await response.json();

    console.log(
      "Neo4j knowledge graph loaded:",
      graphData
    );

    if (
      !graphData.nodes ||
      !graphData.links ||
      graphData.nodes.length === 0
    ) {
      throw new Error(
        "Knowledge graph contains no nodes"
      );
    }

    // Convert Neo4j nodes into the format expected by D3
    const nodes = graphData.nodes.map(node => {

      let color = '#00D4FF';
      let size = 9;
      let group = 0;

      switch (node.type) {

        case 'RiskEvent':
          color = '#ef4444';
          size = 12;
          group = 1;
          break;

        case 'ShippingRoute':
          color = '#f97316';
          size = 11;
          group = 2;
          break;

        case 'Port':
          color = '#eab308';
          size = 9;
          group = 3;
          break;

        case 'Refinery':
          color = '#22c55e';
          size = 10;
          group = 4;
          break;

        case 'Supplier':
          color = '#3b82f6';
          size = 10;
          group = 5;
          break;

        default:
          color = '#00D4FF';
          size = 9;
          group = 0;
      }

      return {
        id: node.id,
        label: node.label,
        type: node.type,
        properties: node.properties,
        group: group,
        size: size,
        color: color
      };
    });

    // Neo4j endpoint already returns source and target IDs
    const links = graphData.links.map(link => ({
      source: link.source,
      target: link.target,
      type: link.type
    }));

    // D3 force simulation
    const sim = d3.forceSimulation(nodes)
      .force(
        'link',
        d3.forceLink(links)
          .id(d => d.id)
          .distance(65)
      )
      .force(
        'charge',
        d3.forceManyBody().strength(-180)
      )
      .force(
        'center',
        d3.forceCenter(W / 2, H / 2)
      )
      .force(
        'collision',
        d3.forceCollide(25)
      );

    // Relationship lines
    const link = svg
      .append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', '#1a2d48')
      .attr('stroke-width', 1.2)
      .attr('stroke-opacity', .8);

    // Nodes
    const node = svg
      .append('g')
      .selectAll('g')
      .data(nodes)
      .join('g')
      .attr('class', 'kg-node')
      .call(
        d3.drag()

          .on('start', (e, d) => {
            if (!e.active) {
              sim.alphaTarget(.3).restart();
            }

            d.fx = d.x;
            d.fy = d.y;
          })

          .on('drag', (e, d) => {
            d.fx = e.x;
            d.fy = e.y;
          })

          .on('end', (e, d) => {
            if (!e.active) {
              sim.alphaTarget(0);
            }

            d.fx = null;
            d.fy = null;
          })
      )
      .on(
        'click',
        (e, d) => highlightNode(
          d,
          node,
          link
        )
      );

    // Node circles
    node
      .append('circle')
      .attr('r', d => d.size)
      .attr(
        'fill',
        d => d.color + '33'
      )
      .attr(
        'stroke',
        d => d.color
      )
      .attr(
        'stroke-width',
        1.5
      );

    // Node labels
    node
      .append('text')
      .attr('dy', '3px')
      .attr('text-anchor', 'middle')
      .attr('font-size', '8px')
      .attr('fill', '#8da5bf')
      .attr('font-family', 'Inter')
      .text(d => d.label);

    // Tooltip with Neo4j information
    node
      .append('title')
      .text(d => {
        const riskScore =
          d.properties?.risk_score;

        const riskText =
          riskScore !== undefined
            ? `\nRisk Score: ${riskScore}`
            : '';

        return (
          `${d.label}` +
          `\nType: ${d.type}` +
          riskText
        );
      });

    // Update graph positions
    sim.on('tick', () => {

      link
        .attr(
          'x1',
          d => d.source.x
        )
        .attr(
          'y1',
          d => d.source.y
        )
        .attr(
          'x2',
          d => d.target.x
        )
        .attr(
          'y2',
          d => d.target.y
        );

      node.attr(
        'transform',
        d => `translate(${d.x},${d.y})`
      );
    });

  } catch (error) {

    console.error(
      "Failed to load Neo4j knowledge graph:",
      error
    );

    svg
      .append('text')
      .attr('x', W / 2)
      .attr('y', H / 2)
      .attr('text-anchor', 'middle')
      .attr('fill', '#8da5bf')
      .attr('font-size', '12px')
      .text('Knowledge Graph unavailable');
  }
}

function highlightNode(d, node, link) {
  node.select('circle').attr('stroke-width', n => n.id === d.id ? 3 : 1.5).attr('r', n => n.id === d.id ? n.size * 1.4 : n.size);
  setTimeout(() => node.select('circle').attr('stroke-width', 1.5).attr('r', n => n.size), 1500);
}
/* ===== MAP LAYER TOGGLE ===== */
function toggleMapLayer(btn, layer) {

  if (layer === 'routes' && window.routesLayer) {
    if (window.map.hasLayer(window.routesLayer)) {
      window.map.removeLayer(window.routesLayer);
      btn.classList.remove('active');
    } else {
      window.map.addLayer(window.routesLayer);
      btn.classList.add('active');
    }
  }

  if (layer === 'ports' && window.portsLayer) {
    if (window.map.hasLayer(window.portsLayer)) {
      window.map.removeLayer(window.portsLayer);
      btn.classList.remove('active');
    } else {
      window.map.addLayer(window.portsLayer);
      btn.classList.add('active');
    }
  }

  if (layer === 'tankers' && window.tankersLayer) {
    if (window.map.hasLayer(window.tankersLayer)) {
      window.map.removeLayer(window.tankersLayer);
      btn.classList.remove('active');
    } else {
      window.map.addLayer(window.tankersLayer);
      btn.classList.add('active');
    }
  }
}

/* ===== DIGITAL TWIN ===== */
async function fetchDigitalTwin(runId = 8) {
  const container = document.getElementById('digital-twin-content');

  if (!container) return;

  try {
    const response = await fetch(
      `${API_BASE_URL}/simulations/runs/${runId}/digital-twin`
    );

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const snapshots = await response.json();

    console.log('Digital Twin loaded:', snapshots);

    if (!snapshots.length) {
      container.innerHTML = `
        <div class="empty-state">
          <p>No Digital Twin snapshots available.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = snapshots.map(snapshot => `
  <div class="digital-twin-card">

    <div class="dt-card-header">
      <div>
        <div class="dt-day">SIMULATION DAY ${snapshot.simulation_day}</div>
        <h3>${snapshot.entity_name}</h3>
      </div>

      <span class="dt-status">
        ${snapshot.operational_status}
      </span>
    </div>

    <div class="dt-metrics">
      <div class="dt-metric">
        <span>Risk Score</span>
        <strong>${snapshot.risk_score}/100</strong>
      </div>

      <div class="dt-metric">
        <span>Delay</span>
        <strong>${snapshot.delay_days} days</strong>
      </div>
    </div>

    <div class="dt-progress-section">
      <div class="dt-progress-label">
        <span>Capacity Utilization</span>
        <strong>${snapshot.capacity_utilization}%</strong>
      </div>
      <div class="dt-progress-track">
        <div class="dt-progress-fill"
             style="width: ${snapshot.capacity_utilization}%"></div>
      </div>
    </div>

    <div class="dt-progress-section">
      <div class="dt-progress-label">
        <span>Supply Available</span>
        <strong>${snapshot.supply_available}%</strong>
      </div>
      <div class="dt-progress-track">
        <div class="dt-progress-fill"
             style="width: ${snapshot.supply_available}%"></div>
      </div>
    </div>

    <div class="dt-notes">
      ${snapshot.notes || 'No additional simulation notes.'}
    </div>

  </div>
`).join('');

  } catch (error) {
    console.error('Error loading Digital Twin:', error);

    container.innerHTML = `
      <div class="empty-state">
        <p>Unable to load Digital Twin data.</p>
      </div>
    `;
  }
}

/* ===== SCENARIO SIMULATOR ===== */

let loadedScenarios = [];
async function fetchScenarios() {
  const select = document.getElementById('scenario-select');

  if (!select) return;

  try {
    const response = await fetch(`${API_BASE_URL}/simulations/scenarios`);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const scenarios = await response.json();

    console.log('Scenarios loaded:', scenarios);

    // Remove duplicate scenarios by name
    const uniqueScenarios = scenarios.filter(
      (scenario, index, self) =>
        index === self.findIndex(s => s.name === scenario.name)
    );
    loadedScenarios = uniqueScenarios;

    select.innerHTML = `
      <option value="">Select a scenario</option>
      ${uniqueScenarios.map(scenario => `
        <option value="${scenario.id}">
          ${scenario.name}
        </option>
      `).join('')}
    `;

    select.onchange = function () {
  const scenarioId = Number(this.value);
  const details = document.getElementById('scenario-details');

  if (!scenarioId) {
    details.innerHTML = `
      <p>Select a scenario to view its configuration.</p>
    `;
    return;
  }

  const scenario = loadedScenarios.find(s => s.id === scenarioId);

  if (!scenario) return;

  details.innerHTML = `
<div class="scenario-details">

    <h3>${scenario.name}</h3>

    <p>${scenario.description}</p>

    <div class="scenario-meta">
        <strong>Scenario Type:</strong>
        ${scenario.scenario_type}
    </div>

    <div class="scenario-meta">
        <strong>Severity:</strong>
        ${scenario.severity}
    </div>

    <div class="scenario-meta">
        <strong>Disruption Duration:</strong>
        ${scenario.disruption_duration_days ?? 'Not specified'} days
    </div>

    <div class="scenario-meta">
        <strong>Disruption Level:</strong>
        ${scenario.disruption_percentage}%
    </div>

</div>
`;
};

  } catch (error) {
    console.error('Error loading scenarios:', error);

    select.innerHTML = `
      <option value="">Unable to load scenarios</option>
    `;
  }
}

async function runSelectedSimulation() {
  const select = document.getElementById('scenario-select');
  const results = document.getElementById('simulation-results');
  const button = document.getElementById('run-simulation-btn');

  const scenarioId = Number(select.value);

  if (!scenarioId) {
    results.innerHTML = `
      <div class="empty-state">
        <p>Please select a scenario before running the simulation.</p>
      </div>
    `;
    return;
  }

  try {
    button.disabled = true;
    button.textContent = 'Running Simulation...';

    results.innerHTML = `
      <div class="empty-state">
        <p>AI simulation in progress...</p>
      </div>
    `;

// --------------------------------------------------
// Run real scenario simulation engine
// --------------------------------------------------

const engineResponse = await fetch(
  `${API_BASE_URL}/simulations/engine/run/${scenarioId}`,
  {
    method: 'POST'
  }
);

if (!engineResponse.ok) {
  throw new Error(
    `Simulation engine error: ${engineResponse.status}`
  );
}

const engineResult = await engineResponse.json();

console.log(
  'Simulation engine result:',
  engineResult
);

    const now = new Date().toISOString();

    const response = await fetch(`${API_BASE_URL}/simulations/runs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        scenario_id: scenarioId,
        risk_event_id: 1,
        status: 'Pending',
        confidence_score: 92,
        started_at: now,
        completed_at: now
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const run = await response.json();

    console.log('Simulation created:', run);

  results.innerHTML = `
<div class="glass-card">

    <div class="simulation-header">
        <h2>✅ Simulation Completed</h2>
        <span class="status-badge critical">${run.status}</span>
    </div>

    <div class="metric-grid">

        <div class="metric-card">
            <span>Run ID</span>
            <h2>${run.id}</h2>
        </div>

        <div class="metric-card">
            <span>Confidence</span>
            <h2>${run.confidence_score}%</h2>
        </div>

        <div class="metric-card">
            <span>Scenario</span>
            <h2>${run.scenario_id}</h2>
        </div>

    </div>

</div>
`;

// --------------------------------------------------
// Display AI simulation engine intelligence
// --------------------------------------------------

const scenario = engineResult.scenario;
const alternative = engineResult.recommended_alternative;

results.innerHTML += `
<div class="glass-card">

    <div class="simulation-header">
        <h2>🤖 AI Simulation Intelligence</h2>
        <span class="status-badge">
            ${scenario.severity}
        </span>
    </div>

    <div class="metric-grid">

        <div class="metric-card">
            <span>Scenario</span>
            <h2>${scenario.scenario_name}</h2>
        </div>

        <div class="metric-card">
            <span>Probability</span>
            <h2>${Math.round(scenario.probability * 100)}%</h2>
        </div>

        <div class="metric-card">
            <span>Expected Supply Loss</span>
            <h2>${scenario.expected_supply_loss_percentage}%</h2>
        </div>

        <div class="metric-card">
            <span>Risk Exposure</span>
            <h2>${scenario.risk_exposure}</h2>
        </div>

    </div>

    <div class="scenario-details">

        <h3>AI Recommended Strategy</h3>

        <p>
            ${scenario.recommended_strategy}
        </p>

    </div>

    ${
        alternative
        ? `
        <div class="scenario-details">

            <h3>Recommended Alternative</h3>

            <p>
                <strong>${alternative.route_name}</strong>
            </p>

            <p>
                Risk Level:
                <strong>${alternative.risk_level}</strong>
                &nbsp; | &nbsp;
                Transit:
                <strong>${alternative.transit_days} days</strong>
            </p>

            <p>
                Alternatives evaluated:
                <strong>${engineResult.alternatives_evaluated}</strong>
            </p>

        </div>
        `
        : `
        <div class="scenario-details">
            <h3>Recommended Alternative</h3>
            <p>No viable alternative route currently available.</p>
        </div>
        `
    }

</div>
`;


    // --------------------------------------------------
// Load simulation impact
// --------------------------------------------------

const impactResponse = await fetch(
  `${API_BASE_URL}/simulations/runs/${run.id}/impact`
);

console.log("Impact status:", impactResponse.status);

if (impactResponse.ok) {

  const impact = await impactResponse.json();

  console.log("Impact:", impact);

  results.innerHTML += `

<div class="glass-card">

    <h2>📊 Impact Assessment</h2>

    <div class="metric-grid">

        <div class="metric-card">
            <span>Supply Disruption</span>
            <h2>${impact.supply_disruption_percentage}%</h2>
        </div>

        <div class="metric-card">
            <span>Supply Gap</span>
            <h2>${impact.supply_gap}</h2>
        </div>

        <div class="metric-card">
            <span>Shipment Delay</span>
            <h2>${impact.shipment_delay_days} Days</h2>
        </div>

        <div class="metric-card">
            <span>Economic Loss</span>
            <h2>$${impact.estimated_economic_loss}B</h2>
        </div>

        <div class="metric-card">
            <span>Price Impact</span>
            <h2>${impact.commodity_price_impact_percentage}%</h2>
        </div>

    </div>

    <div class="scenario-details">

        <h3>🤖 AI Insight</h3>

        <p>${impact.summary}</p>

    </div>

</div>
`;

}
else{

  console.error("Impact not found");

}

  } catch (error) {
    console.error('Simulation error:', error);

    results.innerHTML = `
      <div class="empty-state">
        <p>Unable to run simulation. Check the backend connection.</p>
      </div>
    `;

  } finally {
    button.disabled = false;
    button.textContent = 'Run Simulation';
  }
}

document
  .getElementById('run-simulation-btn')
  ?.addEventListener('click', runSelectedSimulation);

/* ===== NAV ===== */
function setupNav() {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', e => {
      e.preventDefault();

      // Update active sidebar item
      document.querySelectorAll('.nav-item').forEach(n => {
        n.classList.remove('active');
      });
      item.classList.add('active');

      // Get selected page
      const section = item.dataset.s;

      // Hide every page before opening the selected page
document.querySelectorAll('.page-section').forEach(page => {
  page.classList.add('hidden-page');
});

      const digitalTwinPage = document.getElementById('digital-twin-page');
      const riskPage = document.getElementById('risk-page');
      const simulatorPage = document.getElementById('scenario-simulator-page');
      const procurementPage = document.getElementById('procurement-page');
      const dashboardPage = document.getElementById('dashboard-page');
      const strategicReservePage = document.getElementById('strategic-reserve-page');
      const reportsPage = document.getElementById('reports-page');
      const settingsPage = document.getElementById('settings-page');

      // Digital Twin
if (section === 'twin') {
 riskPage?.classList.add('hidden-page');
simulatorPage?.classList.add('hidden-page');
procurementPage?.classList.add('hidden-page');
digitalTwinPage?.classList.remove('hidden-page');
strategicReservePage?.classList.add('hidden-page');
settingsPage?.classList.add('hidden-page');

  fetchDigitalTwin(8);

  fetchRefineries().then(refineries => {
  renderRefineries(refineries);
});

  document.querySelector('.main-content')?.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// Scenario Simulator
if (section === 'sim') {
  riskPage?.classList.add('hidden-page');
digitalTwinPage?.classList.add('hidden-page');
procurementPage?.classList.add('hidden-page');
strategicReservePage?.classList.add('hidden-page');
simulatorPage?.classList.remove('hidden-page');
settingsPage?.classList.add('hidden-page');

  fetchScenarios();

  document.querySelector('.main-content')?.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// Dashboard 
if (section === 'dashboard') {

  digitalTwinPage?.classList.add('hidden-page');
  simulatorPage?.classList.add('hidden-page');
  procurementPage?.classList.add('hidden-page');

  dashboardPage?.classList.remove('hidden-page');
  settingsPage?.classList.add('hidden-page');

  document.querySelector('.main-content')?.scrollTo({
    top: 0,
    behavior: 'smooth'
  });

}

      // AI Risk Intelligence
if (section === 'risk') {
digitalTwinPage?.classList.add('hidden-page');
simulatorPage?.classList.add('hidden-page');
procurementPage?.classList.add('hidden-page');
strategicReservePage?.classList.add('hidden-page');
riskPage?.classList.remove('hidden-page');
settingsPage?.classList.add('hidden-page');

  document.querySelector('.main-content')?.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// Procurement
if (section === 'proc') {

  riskPage?.classList.add('hidden-page');
  digitalTwinPage?.classList.add('hidden-page');
  simulatorPage?.classList.add('hidden-page');
strategicReservePage?.classList.add('hidden-page');
dashboardPage?.classList.add('hidden-page');
reportsPage?.classList.add('hidden-page');
  procurementPage?.classList.remove('hidden-page');
  settingsPage?.classList.add('hidden-page');

  fetchSuppliers().then(suppliers => {
    renderSuppliers(suppliers);
  });

  document.querySelector('.main-content')?.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// Strategic Reserve
if (section === 'spr') {
  riskPage?.classList.add('hidden-page');
  digitalTwinPage?.classList.add('hidden-page');
  simulatorPage?.classList.add('hidden-page');
  procurementPage?.classList.add('hidden-page');
  dashboardPage?.classList.add('hidden-page');
reportsPage?.classList.add('hidden-page');
  strategicReservePage?.classList.remove('hidden-page');
settingsPage?.classList.add('hidden-page');

  fetchStrategicReserve();

  document.querySelector('.main-content')?.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// Reports
if (section === 'reports') {
  riskPage?.classList.add('hidden-page');
  digitalTwinPage?.classList.add('hidden-page');
  simulatorPage?.classList.add('hidden-page');
  procurementPage?.classList.add('hidden-page');
  dashboardPage?.classList.add('hidden-page');
  strategicReservePage?.classList.add('hidden-page');

  reportsPage?.classList.remove('hidden-page');
  settingsPage?.classList.add('hidden-page');

  renderExecutiveReport();

  document.querySelector('.main-content')?.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// Settings
if (section === 'settings') {
  riskPage?.classList.add('hidden-page');
  digitalTwinPage?.classList.add('hidden-page');
  simulatorPage?.classList.add('hidden-page');
  procurementPage?.classList.add('hidden-page');
  dashboardPage?.classList.add('hidden-page');
  strategicReservePage?.classList.add('hidden-page');
  reportsPage?.classList.add('hidden-page');

  settingsPage?.classList.remove('hidden-page');

  renderSettings();

  document.querySelector('.main-content')?.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

    });
  });
}

async function fetchSuppliers() {
    try {
        const response = await fetch(`${API_BASE_URL}/suppliers/`);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const suppliers = await response.json();

        console.log(JSON.stringify(suppliers, null, 2));

        return suppliers;
    } catch (error) {
        console.error("Failed to load suppliers:", error);
        return [];
    }
}

async function fetchRefineries() {
  try {
    const response = await fetch(`${API_BASE_URL}/refineries/`);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const refineries = await response.json();

    console.log("Refineries loaded:", refineries);

    return refineries;

  } catch (error) {
    console.error("Failed to load refineries:", error);
    return [];
  }
}

function renderRefineries(refineries) {

  const container = document.getElementById('refineries-list');

  if (!container) {
    return;
  }

  if (!refineries || refineries.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <p>No refinery data available.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = refineries.map(refinery => {

    return `
      <div class="refinery-card">

        <div class="refinery-card-top">
          <div>
            <h3>${refinery.name}</h3>
            <p>${refinery.country}</p>
          </div>

          <span class="refinery-status">
            ${refinery.operational_status}
          </span>
        </div>

        <div class="refinery-metrics">

          <div class="refinery-metric">
            <span>Processing Capacity</span>
            <strong>
              ${Number(refinery.processing_capacity).toLocaleString()}
            </strong>
          </div>

          <div class="refinery-metric">
            <span>Risk Score</span>
            <strong>${refinery.current_risk_score}/100</strong>
          </div>

        </div>

        <div class="refinery-utilization">

          <div class="refinery-utilization-label">
            <span>Current Utilization</span>
            <strong>${refinery.current_utilization}%</strong>
          </div>

          <div class="refinery-progress">
            <div
              class="refinery-progress-fill"
              style="width: ${refinery.current_utilization}%">
            </div>
          </div>

        </div>

      </div>
    `;

  }).join('');
}

function renderSuppliers(suppliers) {

    const container = document.getElementById('procurement-content');

    if (!container) return;

    if (!suppliers || suppliers.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No suppliers found.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = `

        <div class="procurement-summary">

            <div class="metric-card">
                <span>Available Suppliers</span>
                <h2>${suppliers.length}</h2>
            </div>

            <div class="metric-card">
                <span>Lowest Risk Supplier</span>
                <h2>
                    ${
                        [...suppliers].sort(
                            (a, b) =>
                            a.current_risk_score -
                            b.current_risk_score
                        )[0]?.name || 'N/A'
                    }
                </h2>
            </div>

            <div class="metric-card">
                <span>Highest Reliability</span>
                <h2>
                    ${Math.max(
                        ...suppliers.map(
                            s => s.reliability_score || 0
                        )
                    )}%
                </h2>
            </div>

        </div>


        <div class="metric-grid">

            ${suppliers.map(supplier => {

                const risk =
                    supplier.current_risk_score ?? 0;

                const riskLevel =
                    risk >= 70
                        ? 'Critical'
                        : risk >= 40
                        ? 'Medium'
                        : 'Low';

                return `

                    <div class="metric-card">

                        <div class="simulation-header">

                            <h3>${supplier.name}</h3>

                            <span class="status-badge">
                                ${supplier.status}
                            </span>

                        </div>


                        <p>
                            <strong>Country:</strong>
                            ${supplier.country}
                        </p>

                        <p>
                            <strong>Commodity:</strong>
                            ${supplier.commodity_type}
                        </p>

                        <p>
                            <strong>Production Capacity:</strong>
                            ${Number(
                                supplier.production_capacity || 0
                            ).toLocaleString()}
                        </p>

                        <p>
                            <strong>Reliability:</strong>
                            ${supplier.reliability_score ?? 0}%
                        </p>

                        <p>
                            <strong>Current Risk:</strong>
                            ${risk}/100
                        </p>

                        <p>
                            <strong>Risk Level:</strong>
                            ${riskLevel}
                        </p>

                    </div>

                `;

            }).join('')}

        </div>
    `;
}

async function fetchPorts() {
    try {
        const response = await fetch(`${API_BASE_URL}/ports/map-data`);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const ports = await response.json();

        // Store real backend port data for route matching
        window.portsData = ports;

        console.log("Ports loaded:", ports);

        // Create the Ports layer if it does not exist yet
        if (!window.portsLayer) {
            window.portsLayer = L.layerGroup().addTo(window.map);
        } else {
            // Otherwise clear existing markers before refreshing
            window.portsLayer.clearLayers();
        }

        // Add real backend/PostGIS port markers
        ports.forEach(port => {
            L.marker([
                port.latitude,
                port.longitude
            ])
            .addTo(window.portsLayer)
            .bindPopup(`
                <b>${port.name}</b><br>
                Country: ${port.country}<br>
                Risk Score: ${port.current_risk_score ?? port.risk_score ?? 0}<br>
                Congestion: ${port.congestion_level ?? 0}<br>
                Status: ${port.operational_status ?? "Unknown"}
            `);
        });

        return ports;

    } catch (error) {
        console.error("Failed to load ports:", error);
        return [];
    }
}

async function fetchShippingRoutes() {
    try {
        const response = await fetch(`${API_BASE_URL}/shipping-routes/`);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const routes = await response.json();

        // Store real backend shipping-route data
        window.shippingRoutesData = routes;

        console.log("Shipping routes loaded:", routes);

        // Create Routes layer if it does not exist yet
        if (!window.routesLayer) {
            window.routesLayer = L.layerGroup().addTo(window.map);
        } else {
            // Otherwise clear old routes before refreshing
            window.routesLayer.clearLayers();
        }

        routes.forEach(route => {

            // Find corresponding ports from backend port data
            const originPort = window.portsData?.find(
                port => port.id === route.origin_port_id
            );

            const destinationPort = window.portsData?.find(
                port => port.id === route.destination_port_id
            );

            // Determine route colour from risk score
            let routeColor;

            if (route.current_risk_score >= 70) {
                routeColor = "#ef4444";
            } else if (route.current_risk_score >= 40) {
                routeColor = "#f97316";
            } else {
                routeColor = "#22c55e";
            }

            // Draw only when both ports exist
            if (originPort && destinationPort) {

                L.polyline(
                    [
                        [
                            originPort.latitude,
                            originPort.longitude
                        ],
                        [
                            destinationPort.latitude,
                            destinationPort.longitude
                        ]
                    ],
                    {
                        color: routeColor,
                        weight: 4
                    }
                )
                .addTo(window.routesLayer)
                .bindPopup(`
                    <b>${route.name}</b><br>
                    Distance: ${route.distance_km ?? "N/A"} km<br>
                    Travel Time: ${route.estimated_travel_days ?? "N/A"} days<br>
                    Risk Score: ${route.current_risk_score ?? 0}<br>
                    Status: ${route.status ?? "Unknown"}<br>
                    Risk Reason: ${route.risk_reason ?? "None"}
                `);
            }
        });

        return routes;

    } catch (error) {
        console.error(
            "Failed to load shipping routes:",
            error
        );

        return [];
    }
}

async function testBackendConnection() {
  try {
    const response=await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();

    console.log("Backend connection successful:",data);
  } catch(error) {
    console.error("Backend connection failed:",error);
  } 
}

async function fetchRiskEvents() {
  try {
    const response = await fetch(`${API_BASE_URL}/risk-intelligence/events`);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const events = await response.json();

    console.log("Risk events loaded:", events);

    if (events.length > 0) {
  document.getElementById("kv-risk").textContent = events[0].risk_score;

  document.getElementById("gauge-num").textContent = events[0].risk_score;
initGauge(events[0].risk_score);
  document.getElementById("gauge-lbl").textContent = events[0].risk_level.toUpperCase();

document.getElementById("gauge-status").textContent = events[0].status;


  document.getElementById("risk-ring").setAttribute(
  "stroke-dasharray",
  `${events[0].risk_score} 100`
);

document.getElementById("kv-risk-level").textContent = events[0].risk_level + " Risk";

  document.getElementById("kv-conf").textContent = events[0].confidence_score + "%";
document.getElementById("gauge-confidence").textContent =
  events[0].confidence_score + "%";

document.getElementById("kv-verification").textContent =
  events[0].multi_source_verified ? "Multi-source verified" : "Verification pending";
  document.getElementById("kv-corridor").textContent = events[0].region;
document.getElementById("kv-corridor-risk").textContent = events[0].risk_score + "/100";

const activeEvents = events.filter(event => event.status === "Active");

document.getElementById("kv-events").textContent = activeEvents.length;

document.getElementById("kv-events-status").textContent =
  activeEvents.length === 1 ? "1 Active Event" : `${activeEvents.length} Active Events`;
}

    return events;
  } catch (error) {
    console.error("Failed to load risk events:", error);
    return [];
  }
}

async function fetchRecommendations() {
  try {
    const response = await fetch(`${API_BASE_URL}/recommendations/`);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const recommendations = await response.json();



    console.log("Recommendations loaded:", recommendations);

const container = document.getElementById("recommendations-list");
console.log("Recommendations container:", container);
if (container && recommendations.length > 0) {
  container.innerHTML = recommendations.slice(-1).map(rec => `
    <div class="recommendation-item">
      <h3>${rec.title}</h3>
      <p>${rec.description}</p>
      <div>
        <strong>Priority:</strong> ${rec.priority}
        &nbsp; | &nbsp;
        <strong>Confidence:</strong> ${rec.confidence_score}%
        &nbsp; | &nbsp;
        <strong>Risk Reduction:</strong> ${rec.expected_risk_reduction}%
        &nbsp; | &nbsp;
        <strong>Status:</strong> ${rec.status}
      </div>
    </div>
  `).join("");
}

    return recommendations;
  } catch (error) {
    console.error("Failed to load recommendations:", error);
    return [];
  }
}

/* ===== STRATEGIC RESERVE ===== */

async function fetchStrategicReserve() {
  try {

    const response = await fetch(`${API_BASE_URL}/strategic-reserve/`);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();

    console.log("Strategic Reserve loaded:", data);

    renderStrategicReserve(data);

  } catch (error) {

    console.error("Failed to load Strategic Reserve:", error);

    const container = document.getElementById("strategic-reserve-content");

    if (container) {
      container.innerHTML = `
        <div class="empty-state">
          <p>Unable to load strategic reserve data.</p>
        </div>
      `;
    }
  }
}

function renderStrategicReserve(data) {

  const container = document.getElementById("strategic-reserve-content");

  if (!container) {
    return;
  }

  const sitesHTML = data.reserve_sites.map(site => `
    <div class="reserve-site-card">

      <div class="reserve-site-top">
        <div>
          <h3>${site.name}</h3>
          <span>${site.capacity} Million Metric Tonnes</span>
        </div>

        <span class="reserve-status">
          ${site.status}
        </span>
      </div>

      <div class="reserve-fill-label">
        <span>Storage Fill Level</span>
        <strong>${site.fill_percentage}%</strong>
      </div>

      <div class="reserve-progress">
        <div
          class="reserve-progress-fill"
          style="width: ${site.fill_percentage}%">
        </div>
      </div>

    </div>
  `).join("");


 const actionsHTML = data.recommended_actions.map(action => `
    <button
      class="reserve-action-btn"
      onclick="handleReserveAction('${action.replace(/'/g, "\\'")}')"
    >
      ${action}
    </button>
  `).join("");


  container.innerHTML = `

    <div class="reserve-dashboard">

      <!-- KPI CARDS -->
      <div class="reserve-kpi-grid">

        <div class="reserve-kpi-card">
          <span>Total Strategic Reserve</span>
          <strong>${data.total_reserve}</strong>
          <small>Million Metric Tonnes</small>
        </div>

        <div class="reserve-kpi-card">
          <span>Days of Supply</span>
          <strong>${data.days_of_supply}</strong>
          <small>Emergency Coverage</small>
        </div>

        <div class="reserve-kpi-card">
          <span>Overall Fill Level</span>
          <strong>${data.fill_level}%</strong>
          <small>Current Inventory</small>
        </div>

        <div class="reserve-kpi-card">
          <span>Emergency Level</span>
          <strong>${data.emergency_level}</strong>
          <small>Current Assessment</small>
        </div>

      </div>


      <!-- RESERVE LOCATIONS -->
      <div class="reserve-section-title">
        <h3>Reserve Locations</h3>
        <p>Live strategic petroleum reserve availability</p>
      </div>

      <div class="reserve-sites-grid">
        ${sitesHTML}
      </div>


      <!-- AI RECOMMENDATION -->
      <div class="reserve-ai-card">

        <div class="reserve-ai-heading">
          <span class="reserve-ai-icon">✦</span>

          <div>
            <h3>AI Strategic Recommendation</h3>
            <p>Supply resilience assessment</p>
          </div>
        </div>

        <div class="reserve-ai-text">
          ${data.ai_recommendation}
        </div>

        <div class="reserve-actions">
          ${actionsHTML}
        </div>

      </div>

    </div>
  `;
}

async function handleReserveAction(action) {

  console.log("Strategic Reserve action selected:", action);

  try {

    if (action.toLowerCase().includes("increase")) {

      alert(
        "Reserve Expansion Activated\n\n" +
        "Strategic petroleum reserve replenishment has been prioritized."
      );

    } else if (
      action.toLowerCase().includes("diversify")
    ) {

      alert(
        "Import Diversification Activated\n\n" +
        "Procurement strategy will prioritize alternative suppliers and shipping routes."
      );

    } else {

      alert(
        "Strategic action activated:\n\n" + action
      );

    }

  } catch (error) {

    console.error(
      "Failed to execute strategic reserve action:",
      error
    );

    alert("Unable to execute strategic reserve action.");

  }
}

/* ===== EXECUTIVE REPORT ===== */

async function renderExecutiveReport() {

  const container = document.getElementById("reports-content");

  if (!container) return;

  container.innerHTML = `
    <div class="empty-state">
      <p>Generating live executive intelligence...</p>
    </div>
  `;

  try {

    // --------------------------------------------------
    // Find latest simulation run
    // --------------------------------------------------

    const runsResponse = await fetch(
      `${API_BASE_URL}/simulations/runs`
    );

    if (!runsResponse.ok) {
      throw new Error(`Runs HTTP error: ${runsResponse.status}`);
    }

    const runs = await runsResponse.json();

    if (!runs.length) {
      throw new Error("No simulation runs available");
    }

    const latestRun = runs.reduce((latest, run) =>
      run.id > latest.id ? run : latest
    );


    // --------------------------------------------------
    // Load live system intelligence
    // --------------------------------------------------

    const [
      impactResponse,
      reserveResponse,
      refineriesResponse
    ] = await Promise.all([

      fetch(
        `${API_BASE_URL}/simulations/runs/${latestRun.id}/impact`
      ),

      fetch(
        `${API_BASE_URL}/strategic-reserve/`
      ),

      fetch(
        `${API_BASE_URL}/refineries/`
      )

    ]);


    if (
      !impactResponse.ok ||
      !reserveResponse.ok ||
      !refineriesResponse.ok
    ) {
      throw new Error("Failed to load report intelligence");
    }


    const impact = await impactResponse.json();
    const reserve = await reserveResponse.json();
    const refineries = await refineriesResponse.json();


    console.log("Report latest run:", latestRun);
    console.log("Report impact:", impact);
    console.log("Report reserve:", reserve);
    console.log("Report refineries:", refineries);


    // --------------------------------------------------
    // Determine overall risk
    // --------------------------------------------------

    const disruption =
      Number(impact.supply_disruption_percentage || 0);

    let overallRiskScore = disruption;

    if (disruption >= 60) {
      overallRiskScore = 92;
    }
    else if (disruption >= 40) {
      overallRiskScore = 70;
    }
    else if (disruption >= 20) {
      overallRiskScore = 50;
    }
    else {
      overallRiskScore = 30;
    }


    let riskLevel = "LOW RISK";

    if (overallRiskScore >= 80) {
      riskLevel = "CRITICAL RISK";
    }
    else if (overallRiskScore >= 60) {
      riskLevel = "HIGH RISK";
    }
    else if (overallRiskScore >= 40) {
      riskLevel = "MODERATE RISK";
    }


    // --------------------------------------------------
    // Generate refinery finding dynamically
    // --------------------------------------------------

    const refinerySummary = refineries
      .map(refinery =>
        `${refinery.name} is ${refinery.operational_status} at ` +
        `${refinery.current_utilization}% utilization`
      )
      .join(", ");


    // --------------------------------------------------
    // Save report data for printable report
    // --------------------------------------------------

    window.executiveReportData = {

      latestRun,
      impact,
      reserve,
      refineries,

      overallRiskScore,
      riskLevel,

      refinerySummary

    };

    


    // --------------------------------------------------
    // Render report
    // --------------------------------------------------

    container.innerHTML = `

      <div class="executive-report">

        <div class="report-summary-header">

          <div>

            <span class="report-label">
              EXECUTIVE RISK BRIEF
            </span>

            <h2>
              Energy Supply Chain Resilience Assessment
            </h2>

            <p>
              Live operational intelligence generated from the
              latest supply-chain simulation, refinery network
              and strategic reserve status.
            </p>

          </div>

          <div class="report-risk-badge">
            ${riskLevel}
          </div>

        </div>


        <!-- KPI SUMMARY -->

        <div class="report-kpi-grid">

          <div class="report-kpi-card">

            <span>Overall Risk Score</span>

            <strong>
              ${overallRiskScore}/100
            </strong>

            <small>
              Current Exposure
            </small>

          </div>


          <div class="report-kpi-card">

            <span>Supply Disruption</span>

            <strong>
              ${impact.supply_disruption_percentage}%
            </strong>

            <small>
              Simulation Run #${latestRun.id}
            </small>

          </div>


          <div class="report-kpi-card">

            <span>Economic Exposure</span>

            <strong>
              $${impact.estimated_economic_loss}B
            </strong>

            <small>
              Estimated Loss
            </small>

          </div>


          <div class="report-kpi-card">

            <span>Reserve Readiness</span>

            <strong>
              ${reserve.fill_level}%
            </strong>

            <small>
              Strategic Inventory
            </small>

          </div>

        </div>


        <!-- EXECUTIVE FINDINGS -->

        <div class="report-section">

          <div class="report-section-heading">

            <h3>Executive Findings</h3>

            <span>LIVE ASSESSMENT</span>

          </div>


          <div class="report-findings-grid">


            <div class="report-finding">

              <span class="report-finding-number">
                01
              </span>

              <div>

                <h4>Supply Chain Disruption</h4>

                <p>
                  The latest simulation indicates
                  ${impact.supply_disruption_percentage}%
                  supply disruption with an estimated
                  shipment delay of
                  ${impact.shipment_delay_days} days.
                </p>

              </div>

            </div>


            <div class="report-finding">

              <span class="report-finding-number">
                02
              </span>

              <div>

                <h4>Economic & Commodity Impact</h4>

                <p>
                  Estimated economic exposure is
                  $${impact.estimated_economic_loss}B
                  with a projected commodity price impact of
                  ${impact.commodity_price_impact_percentage}%.
                </p>

              </div>

            </div>


            <div class="report-finding">

              <span class="report-finding-number">
                03
              </span>

              <div>

                <h4>Refinery Resilience</h4>

                <p>
                  ${refinerySummary}.
                </p>

              </div>

            </div>


            <div class="report-finding">

              <span class="report-finding-number">
                04
              </span>

              <div>

                <h4>Strategic Reserve Position</h4>

                <p>
                  Strategic reserves currently maintain an
                  overall fill level of ${reserve.fill_level}%,
                  providing approximately
                  ${reserve.days_of_supply} days of emergency
                  supply coverage.
                </p>

              </div>

            </div>

          </div>

        </div>


        <!-- AI RECOMMENDATION -->

        <div class="report-ai-recommendation">

          <div>

            <span class="report-label">
              AI RECOMMENDATION
            </span>

            <h3>
              Recommended Response Strategy
            </h3>

            <p id="gemini-recommendation-text">
  Loading AI recommendation...
</p>

          </div>


          <button
            id="generate-report-btn"
            class="report-download-btn"
            onclick="generateExecutiveReport()"
          >
            Generate Executive Report
          </button>

        </div>

      </div>
    `;

   const recommendation = await fetchGeminiRecommendation(
    latestRun,
    impact,
    reserve,
    refineries
);

const recommendationElement = document.getElementById(
  "gemini-recommendation-text"
);

if (recommendationElement) {
  recommendationElement.textContent = recommendation;
}


  } catch (error) {

    console.error(
      "Failed to generate Executive Report:",
      error
    );

    container.innerHTML = `
      <div class="empty-state">
        <p>
          Unable to generate executive report from
          current intelligence.
        </p>
      </div>
    `;

  }

}

/* ===== GENERATE EXECUTIVE REPORT ===== */

function generateExecutiveReport() {

  const data = window.executiveReportData;

  if (!data) {
    alert(
      "Executive report data is not available yet. Please reopen the Reports page."
    );
    return;
  }


  const {
    latestRun,
    impact,
    reserve,
    refineries,
    overallRiskScore,
    riskLevel,
    refinerySummary
  } = data;


  const reportWindow = window.open('', '_blank');

  if (!reportWindow) {
    alert('Please allow pop-ups to generate the report.');
    return;
  }


  const generatedAt = new Date().toLocaleString();


  /* ---------------------------------------------
     Generate refinery section dynamically
  --------------------------------------------- */

  const refineryHTML = refineries.map(refinery => `

    <div class="refinery-row">

      <div>
        <strong>${refinery.name}</strong>
        <span>${refinery.country}</span>
      </div>

      <div>
        <span>Utilization</span>
        <strong>${refinery.current_utilization}%</strong>
      </div>

      <div>
        <span>Risk Score</span>
        <strong>${refinery.current_risk_score}/100</strong>
      </div>

      <div>
        <span>Status</span>
        <strong>${refinery.operational_status}</strong>
      </div>

    </div>

  `).join('');


  reportWindow.document.write(`

    <!DOCTYPE html>

    <html>

    <head>

      <title>
        Energy Supply Chain Executive Report
      </title>


      <style>

        * {
          box-sizing: border-box;
        }


        body {

          font-family:
            Arial,
            Helvetica,
            sans-serif;

          margin: 0;

          padding: 40px;

          color: #172033;

          background: white;

        }


        /* --------------------------------
           REPORT HEADER
        -------------------------------- */

        .report-header {

          border-bottom:
            3px solid #0b6b8a;

          padding-bottom: 20px;

          margin-bottom: 30px;

        }


        .report-label {

          color: #0b8db5;

          font-size: 12px;

          font-weight: bold;

          letter-spacing: 1.5px;

          margin-bottom: 10px;

        }


        .report-header h1 {

          margin:
            8px 0 8px;

          font-size: 28px;

          color: #10213a;

        }


        .subtitle {

          color: #5d6b7e;

          font-size: 14px;

          line-height: 1.6;

        }


        .generated {

          margin-top: 10px;

          font-size: 12px;

          color: #778397;

        }


        /* --------------------------------
           RISK BANNER
        -------------------------------- */

        .risk-banner {

          margin:
            25px 0;

          padding:
            16px 20px;

          border-left:
            5px solid #dc3545;

          background:
            #fff2f3;

          color:
            #b42332;

          font-weight:
            bold;

        }


        /* --------------------------------
           KPI GRID
        -------------------------------- */

        .kpi-grid {

          display: grid;

          grid-template-columns:
            repeat(4, 1fr);

          gap: 12px;

          margin-bottom: 30px;

        }


        .kpi {

          border:
            1px solid #d9e0e8;

          border-radius:
            8px;

          padding:
            16px;

        }


        .kpi span {

          display: block;

          color: #687588;

          font-size: 12px;

          margin-bottom: 8px;

        }


        .kpi strong {

          display: block;

          font-size: 23px;

          color: #10213a;

        }


        .kpi small {

          display: block;

          margin-top: 6px;

          color: #7b8797;

          font-size: 10px;

        }


        /* --------------------------------
           HEADINGS
        -------------------------------- */

        h2 {

          margin-top: 30px;

          color: #10213a;

          font-size: 20px;

          border-bottom:
            1px solid #d9e0e8;

          padding-bottom: 8px;

        }


        /* --------------------------------
           FINDINGS
        -------------------------------- */

        .finding {

          margin:
            18px 0;

          padding:
            16px;

          border:
            1px solid #d9e0e8;

          border-radius:
            8px;

        }


        .finding h3 {

          margin:
            0 0 8px;

          color:
            #10213a;

          font-size:
            16px;

        }


        .finding p {

          margin: 0;

          color:
            #4f5e72;

          line-height:
            1.6;

          font-size:
            13px;

        }


        /* --------------------------------
           REFINERY NETWORK
        -------------------------------- */

        .refinery-row {

          display:
            grid;

          grid-template-columns:
            2fr 1fr 1fr 1fr;

          gap:
            15px;

          padding:
            14px;

          margin:
            10px 0;

          border:
            1px solid #d9e0e8;

          border-radius:
            8px;

        }


        .refinery-row span {

          display:
            block;

          color:
            #687588;

          font-size:
            11px;

          margin-bottom:
            4px;

        }


        .refinery-row strong {

          color:
            #10213a;

          font-size:
            13px;

        }


        /* --------------------------------
           AI RECOMMENDATION
        -------------------------------- */

        .recommendation {

          margin-top:
            25px;

          padding:
            20px;

          background:
            #eef8fb;

          border-left:
            5px solid #0b8db5;

        }


        .recommendation h3 {

          margin-top:
            0;

          color:
            #10213a;

        }


        .recommendation p {

          line-height:
            1.7;

          color:
            #43536a;

        }


        /* --------------------------------
           FOOTER
        -------------------------------- */

        .footer {

          margin-top:
            40px;

          padding-top:
            15px;

          border-top:
            1px solid #d9e0e8;

          font-size:
            11px;

          color:
            #7b8797;

          text-align:
            center;

        }


        /* --------------------------------
           PRINT SETTINGS
        -------------------------------- */

        @media print {

          body {
            padding: 20px;
          }


          .kpi-grid {

            grid-template-columns:
              repeat(4, 1fr);

          }


          .finding {

            break-inside:
              avoid;

          }


          .refinery-row {

            break-inside:
              avoid;

          }


          .recommendation {

            break-inside:
              avoid;

          }

        }

      </style>

    </head>


    <body>


      <!-- =====================================
           HEADER
      ====================================== -->

      <div class="report-header">


        <div class="report-label">
          EXECUTIVE RISK INTELLIGENCE
        </div>


        <h1>
          Energy Supply Chain Resilience Assessment
        </h1>


        <div class="subtitle">

          AI Risk Intelligence Agent —
          Executive Intelligence Report

        </div>


        <div class="generated">

          Generated:
          ${generatedAt}

          <br>

          Simulation Run:
          #${latestRun.id}

        </div>


      </div>



      <!-- =====================================
           RISK STATUS
      ====================================== -->

      <div class="risk-banner">

        ${riskLevel}

        —

        Current supply-chain risk assessment
        based on latest simulation intelligence.

      </div>



      <!-- =====================================
           KPI SUMMARY
      ====================================== -->

      <div class="kpi-grid">


        <div class="kpi">

          <span>
            Overall Risk Score
          </span>

          <strong>
            ${overallRiskScore}/100
          </strong>

          <small>
            Current Exposure
          </small>

        </div>


        <div class="kpi">

          <span>
            Supply Disruption
          </span>

          <strong>
            ${impact.supply_disruption_percentage}%
          </strong>

          <small>
            Simulated Impact
          </small>

        </div>


        <div class="kpi">

          <span>
            Economic Exposure
          </span>

          <strong>
            $${impact.estimated_economic_loss}B
          </strong>

          <small>
            Estimated Loss
          </small>

        </div>


        <div class="kpi">

          <span>
            Reserve Readiness
          </span>

          <strong>
            ${reserve.fill_level}%
          </strong>

          <small>
            Strategic Inventory
          </small>

        </div>


      </div>



      <!-- =====================================
           EXECUTIVE FINDINGS
      ====================================== -->

      <h2>
        Executive Findings
      </h2>


      <div class="finding">

        <h3>
          1. Supply Chain Disruption
        </h3>

        <p>

          The latest simulation indicates
          ${impact.supply_disruption_percentage}%
          supply disruption with an estimated
          shipment delay of
          ${impact.shipment_delay_days} days.

        </p>

      </div>



      <div class="finding">

        <h3>
          2. Economic & Commodity Impact
        </h3>

        <p>

          Estimated economic exposure is
          $${impact.estimated_economic_loss}B
          with a projected commodity price
          impact of
          ${impact.commodity_price_impact_percentage}%.

          The simulation identifies a supply
          gap of ${impact.supply_gap}.

        </p>

      </div>



      <div class="finding">

        <h3>
          3. Refinery Resilience
        </h3>

        <p>

          ${refinerySummary}.

        </p>

      </div>



      <div class="finding">

        <h3>
          4. Strategic Reserve Position
        </h3>

        <p>

          Strategic reserves currently maintain
          an overall fill level of
          ${reserve.fill_level}%,
          providing approximately
          ${reserve.days_of_supply}
          days of emergency supply coverage.

          Current emergency assessment:
          ${reserve.emergency_level}.

        </p>

      </div>



      <!-- =====================================
           REFINERY NETWORK
      ====================================== -->

      <h2>
        Refinery Network Status
      </h2>


      ${refineryHTML}



      <!-- =====================================
           AI RESPONSE STRATEGY
      ====================================== -->

      <h2>
        AI Recommended Response Strategy
      </h2>


      <div class="recommendation">

        <h3>
          Recommended Actions
        </h3>

        <p>

          ${reserve.ai_recommendation}

        </p>

      </div>



      <!-- =====================================
           SIMULATION INTELLIGENCE
      ====================================== -->

      <h2>
        Simulation Intelligence Summary
      </h2>


      <div class="finding">

        <p>

          ${impact.summary}

        </p>

      </div>



      <!-- =====================================
           FOOTER
      ====================================== -->

      <div class="footer">

        Generated by AI Risk Intelligence Agent

        <br>

        Energy Supply Chain Resilience Platform

        <br>

        Simulation Run #${latestRun.id}

      </div>


    </body>

    </html>

  `);


  reportWindow.document.close();

  reportWindow.focus();


  setTimeout(() => {

    reportWindow.print();

  }, 500);

}

/* ===== PLATFORM SETTINGS STATE ===== */

const PLATFORM_SETTINGS = {
  riskEventMonitoring:
    localStorage.getItem("riskEventMonitoring") !== "false",

  shippingRouteTracking:
    localStorage.getItem("shippingRouteTracking") !== "false",

  refineryMonitoring:
    localStorage.getItem("refineryMonitoring") !== "false",

  criticalRiskAlerts:
    localStorage.getItem("criticalRiskAlerts") !== "false",

  supplyDisruptionAlerts:
    localStorage.getItem("supplyDisruptionAlerts") !== "false",

  reserveWarnings:
    localStorage.getItem("reserveWarnings") !== "false"
};

/* ===== PLATFORM SETTINGS ===== */

function renderSettings() {

  const container = document.getElementById("settings-content");

  if (!container) {
    return;
  }

  container.innerHTML = `

    <div class="settings-wrapper">

      <!-- SYSTEM STATUS -->
      <div class="settings-status-card">

        <div>
          <span class="settings-label">SYSTEM STATUS</span>
          <h2>AI Risk Intelligence Engine</h2>
          <p>
            Real-time geopolitical risk monitoring and
            energy supply-chain resilience configuration.
          </p>
        </div>

        <div class="settings-online">
          <span class="settings-online-dot"></span>
          Operational
        </div>

      </div>


      <!-- SETTINGS GRID -->
      <div class="settings-grid">


        <!-- AI ENGINE -->
        <div class="settings-card">

          <div class="settings-card-header">
            <div>
              <h3>AI Engine</h3>
              <p>Risk intelligence model configuration</p>
            </div>

            <span class="settings-version">v3.2</span>
          </div>

          <div class="settings-row">
            <div>
              <strong>Geopolitical Risk Model</strong>
              <span>Primary intelligence engine</span>
            </div>

            <span class="settings-value">Active</span>
          </div>

          <div class="settings-row">
            <div>
              <strong>Risk Sensitivity</strong>
              <span>Event detection threshold</span>
            </div>

            <span class="settings-value">High</span>
          </div>

          <div class="settings-row">
            <div>
              <strong>Simulation Engine</strong>
              <span>Supply-chain digital twin</span>
            </div>

            <span class="settings-value">Enabled</span>
          </div>

        </div>


        <!-- MONITORING -->
        <div class="settings-card">

          <div class="settings-card-header">
            <div>
              <h3>Monitoring</h3>
              <p>Live infrastructure intelligence</p>
            </div>
          </div>

          <div class="settings-row">
            <div>
              <strong>Risk Event Monitoring</strong>
              <span>Continuous geopolitical surveillance</span>
            </div>

            <span
  class="settings-toggle ${PLATFORM_SETTINGS.riskEventMonitoring ? "active" : ""}"
  data-setting="riskEventMonitoring">
</span>
          </div>

          <div class="settings-row">
            <div>
              <strong>Shipping Route Tracking</strong>
              <span>Monitor critical energy corridors</span>
            </div>

            <span
  class="settings-toggle ${PLATFORM_SETTINGS.shippingRouteTracking ? "active" : ""}"
  data-setting="shippingRouteTracking">
</span>
          </div>

          <div class="settings-row">
            <div>
              <strong>Refinery Monitoring</strong>
              <span>Operational capacity intelligence</span>
            </div>

            <span
  class="settings-toggle ${PLATFORM_SETTINGS.refineryMonitoring ? "active" : ""}"
  data-setting="refineryMonitoring">
</span>
          </div>

        </div>


        <!-- ALERTS -->
        <div class="settings-card">

          <div class="settings-card-header">
            <div>
              <h3>Alert Configuration</h3>
              <p>Risk notification preferences</p>
            </div>
          </div>

          <div class="settings-row">
            <div>
              <strong>Critical Risk Alerts</strong>
              <span>Immediate high-severity notifications</span>
            </div>

            <span
  class="settings-toggle ${PLATFORM_SETTINGS.criticalRiskAlerts ? "active" : ""}"
  data-setting="criticalRiskAlerts">
</span>
          </div>

          <div class="settings-row">
            <div>
              <strong>Supply Disruption Alerts</strong>
              <span>Notify when supply availability changes</span>
            </div>

            <span
  class="settings-toggle ${PLATFORM_SETTINGS.supplyDisruptionAlerts ? "active" : ""}"
  data-setting="supplyDisruptionAlerts">
</span>
          </div>

          <div class="settings-row">
            <div>
              <strong>Reserve Warnings</strong>
              <span>Strategic inventory threshold alerts</span>
            </div>

            <span
  class="settings-toggle ${PLATFORM_SETTINGS.reserveWarnings ? "active" : ""}"
  data-setting="reserveWarnings">
</span>
          </div>

        </div>


        <!-- SYSTEM INFORMATION -->
        <div class="settings-card">

          <div class="settings-card-header">
            <div>
              <h3>System Information</h3>
              <p>Platform runtime configuration</p>
            </div>
          </div>

          <div class="settings-row">
            <div>
              <strong>Platform</strong>
              <span>Energy Supply Chain Resilience</span>
            </div>

            <span class="settings-value">Online</span>
          </div>

          <div class="settings-row">
            <div>
              <strong>API Status</strong>
              <span>FastAPI backend services</span>
            </div>

            <span class="settings-value">Connected</span>
          </div>

          <div class="settings-row">
            <div>
              <strong>Data Mode</strong>
              <span>Operational intelligence feed</span>
            </div>

            <span class="settings-value">Live</span>
          </div>

        </div>


      </div>

    </div>
  `;

  // Make settings toggles functional
const toggles = container.querySelectorAll(".settings-toggle");

toggles.forEach(toggle => {

  toggle.addEventListener("click", async () => {

    const settingName = toggle.dataset.setting;

    if (!settingName) {
      return;
    }

    // Reverse current setting
    PLATFORM_SETTINGS[settingName] =
      !PLATFORM_SETTINGS[settingName];

    // Save setting so it remains after refresh
    localStorage.setItem(
      settingName,
      PLATFORM_SETTINGS[settingName]
    );

    // Update visual toggle state
    toggle.classList.toggle(
      "active",
      PLATFORM_SETTINGS[settingName]
    );

    // Apply the setting immediately
    await applyPlatformSetting(settingName);

    console.log(
      `Setting updated: ${settingName} =`,
      PLATFORM_SETTINGS[settingName]
    );

  });

});

}

/* ===== APPLY PLATFORM SETTINGS ===== */

async function applyPlatformSetting(settingName) {

  // -----------------------------------------
  // RISK EVENT MONITORING
  // -----------------------------------------

  if (settingName === "riskEventMonitoring") {

    if (PLATFORM_SETTINGS.riskEventMonitoring) {

      await fetchLiveNews();

    } else {

      const newsFeed =
        document.getElementById("news-feed");

      if (newsFeed) {

        newsFeed.innerHTML = `
          <div class="empty-state">
            <p>
              Risk event monitoring is currently disabled
              in Platform Settings.
            </p>
          </div>
        `;

      }

    }

  }


  // -----------------------------------------
  // SHIPPING ROUTE TRACKING
  // -----------------------------------------

  if (settingName === "shippingRouteTracking") {

    if (PLATFORM_SETTINGS.shippingRouteTracking) {

      await fetchShippingRoutes();

      if (
        window.routesLayer &&
        window.map &&
        !window.map.hasLayer(window.routesLayer)
      ) {

        window.map.addLayer(window.routesLayer);

      }

    } else {

      if (
        window.routesLayer &&
        window.map &&
        window.map.hasLayer(window.routesLayer)
      ) {

        window.map.removeLayer(window.routesLayer);

      }

    }

  }


  // -----------------------------------------
  // REFINERY MONITORING
  // -----------------------------------------

  if (settingName === "refineryMonitoring") {

    const refineryContainer =
      document.getElementById("refineries-list");

    if (PLATFORM_SETTINGS.refineryMonitoring) {

      const refineries =
        await fetchRefineries();

      renderRefineries(refineries);

    } else {

      if (refineryContainer) {

        refineryContainer.innerHTML = `
          <div class="empty-state">
            <p>
              Refinery monitoring is currently disabled
              in Platform Settings.
            </p>
          </div>
        `;

      }

    }

  }


  // -----------------------------------------
  // ALERT SETTINGS
  // -----------------------------------------

  if (
    settingName === "criticalRiskAlerts" ||
    settingName === "supplyDisruptionAlerts" ||
    settingName === "reserveWarnings"
  ) {

    renderAlerts();

  }

}

async function fetchAgentActionCenter() {
  try {

   const [decisionsResponse, outcomesResponse] = await Promise.all([
  fetch("http://127.0.0.1:8000/decisions/"),
  fetch("http://127.0.0.1:8000/outcomes/")
]);

    if (!decisionsResponse.ok || !outcomesResponse.ok) {
      throw new Error("Failed to load agent action data");
    }

    const decisions = await decisionsResponse.json();
    const outcomes = await outcomesResponse.json();

    console.log("Agent decisions loaded:", decisions);
    console.log("Agent outcomes loaded:", outcomes);

    // ---------- METRICS ----------

    const totalDecisions = decisions.length;

    const executedDecisions = decisions.filter(
      decision => decision.action_type?.toLowerCase() === "executed"
    ).length;

    const pendingDecisions = decisions.filter(
      decision => decision.action_type?.toLowerCase() === "pending"
    ).length;

    const successfulOutcomes = outcomes.filter(
      outcome => outcome.outcome_status?.toLowerCase() === "successful"
    ).length;

    const successRate = outcomes.length
      ? Math.round((successfulOutcomes / outcomes.length) * 100)
      : 0;


    document.getElementById("agent-total-decisions").textContent =
      totalDecisions;

    document.getElementById("agent-executed-decisions").textContent =
      executedDecisions;

    document.getElementById("agent-pending-decisions").textContent =
      pendingDecisions;

    document.getElementById("agent-success-rate").textContent =
      `${successRate}%`;


    // ---------- LATEST DECISION ----------

    if (!decisions.length) {
      document.getElementById("latest-action-content").innerHTML = `
        <div class="empty-state">
          <p>No agent decisions available.</p>
        </div>
      `;
      return;
    }

    // Highest ID = newest decision
    const latestDecision = [...decisions].sort(
      (a, b) => b.id - a.id
    )[0];

    // Fetch the recommendation linked to the latest decision
let linkedRecommendation = null;

if (latestDecision && latestDecision.recommendation_id) {
  try {
    const recommendationResponse = await fetch(
      `http://127.0.0.1:8000/recommendations/${latestDecision.recommendation_id}`
    );

    if (recommendationResponse.ok) {
      linkedRecommendation = await recommendationResponse.json();
    }
  } catch (error) {
    console.error("Failed to load linked recommendation:", error);
  }
}

// ------------------------------------------------------------
// RECENT AGENT DECISIONS
// ------------------------------------------------------------

const recentDecisionsContainer =
    document.getElementById("recent-decisions-list");

if (recentDecisionsContainer) {

    const recentDecisions = [...decisions]
        .sort((a, b) => b.id - a.id)
        .slice(0, 3);

    const recommendationResults = await Promise.all(
        recentDecisions.map(async (decision) => {

            let recommendation = null;

            if (decision.recommendation_id) {
                try {
                    const response = await fetch(
                        `http://127.0.0.1:8000/recommendations/${decision.recommendation_id}`
                    );

                    if (response.ok) {
                        recommendation = await response.json();
                    }

                } catch (error) {
                    console.error(
                        `Failed to load recommendation ${decision.recommendation_id}:`,
                        error
                    );
                }
            }

            return {
                decision,
                recommendation
            };
        })
    );

    recentDecisionsContainer.innerHTML =
       recommendationResults.map(({ decision, recommendation }) => {

    const decisionTitle =
        recommendation?.title ||
        "Autonomous Operational Decision";

    const decisionType =
        recommendation?.recommendation_type ||
        "Operational Action";

    const priority =
        recommendation?.priority ||
        "Medium";

    const decisionStatus =
        decision.action_type || "Pending";

    return `
        <div class="decision-history-card">

            <div class="decision-history-card-top">
                <span class="decision-history-id">
                    Decision #${decision.id}
                </span>

                <span class="decision-history-status">
                    ${decisionStatus}
                </span>
            </div>

            <h4 class="decision-history-title">
                ${decisionTitle}
            </h4>

                        <div class="decision-history-meta">
                <span>${decisionType}</span>
                <span>${priority} Priority</span>
            </div>

            ${
                decisionStatus.toLowerCase() === "pending"
                    ? `
                        <button
                            class="execute-decision-btn"
                            onclick="executeDecision(${decision.id})"
                        >
                            Execute Action
                        </button>
                    `
                    : ""
            }
 </div>
    `;
}).join("");
}
console.log("Latest Decision:", latestDecision);
console.log("Linked Recommendation:", linkedRecommendation);


    // Find outcome belonging to this decision
    const matchingOutcome = outcomes.find(
      outcome =>
        outcome.decision_action_id === latestDecision.id
    );


    // ---------- STATUS ----------

    const statusElement =
      document.getElementById("latest-action-status");

    statusElement.textContent =
      latestDecision.action_type || "UNKNOWN";


    // ---------- LATEST ACTION CONTENT ----------

    const outcomeHTML = matchingOutcome
      ? `
        <div class="agent-outcome-grid">

          <div>
            <span>Risk Reduction</span>
            <strong>
              ${matchingOutcome.actual_risk_reduction ?? "--"}%
            </strong>
          </div>

          <div>
            <span>Supply Restored</span>
            <strong>
              ${matchingOutcome.supply_restored_percentage ?? "--"}%
            </strong>
          </div>

          <div>
            <span>Actual Cost</span>
            <strong>
              ${matchingOutcome.actual_cost != null
                ? "$" + matchingOutcome.actual_cost.toLocaleString()
                : "--"}
            </strong>
          </div>

          <div>
            <span>Actual Benefit</span>
            <strong>
              ${matchingOutcome.actual_benefit != null
                ? "$" + matchingOutcome.actual_benefit.toLocaleString()
                : "--"}
            </strong>
          </div>

        </div>
      `
      : `
        <div class="agent-pending-message">
          Outcome pending execution.
        </div>
      `;

document.getElementById("latest-action-content").innerHTML = `

  <!-- DECISION TAKEN -->
  <div class="agent-decision-reason">

    <span class="agent-info-label">Decision Taken</span>

    <h3>
      ${linkedRecommendation?.title || "Operational Action"}
    </h3>

    <p>
      ${linkedRecommendation?.description || ""}
    </p>

  </div>


  <!-- DECISION DETAILS -->
  <div class="agent-decision-info">

    <div>
      <span class="agent-info-label">Decision ID</span>
      <strong>#${latestDecision.id}</strong>
    </div>

    <div>
      <span class="agent-info-label">Decision Agent</span>
      <strong>
        ${latestDecision.decided_by || "AI Risk Intelligence Agent"}
      </strong>
    </div>

  </div>


  <!-- RECOMMENDATION DETAILS -->
  <div class="agent-decision-info">

    <div>
      <span class="agent-info-label">Action Type</span>
      <strong>
        ${linkedRecommendation?.recommendation_type || "--"}
      </strong>
    </div>

    <div>
      <span class="agent-info-label">Priority</span>
      <strong>
        ${linkedRecommendation?.priority || "--"}
      </strong>
    </div>

    <div>
      <span class="agent-info-label">AI Confidence</span>
      <strong>
        ${linkedRecommendation?.confidence_score ?? "--"}%
      </strong>
    </div>

  </div>


  <!-- DECISION REASON -->
  <div class="agent-decision-reason">

    <span class="agent-info-label">Decision Reason</span>

    <p>
      ${
        linkedRecommendation?.reasoning ||
        latestDecision.decision_reason ||
        "Autonomous operational decision generated by the risk intelligence workflow."
      }
    </p>

  </div>


  <!-- MEASURED OUTCOME -->
  ${outcomeHTML}

`;

  } catch (error) {

    console.error("Agent Action Center error:", error);

    const container =
      document.getElementById("latest-action-content");

    if (container) {
      container.innerHTML = `
        <div class="empty-state">
          <p>Unable to load agent action intelligence.</p>
        </div>
      `;
    }
  }
}

// ------------------------------------------------------------
// EXECUTE PENDING AGENT DECISION
// ------------------------------------------------------------

async function executeDecision(decisionId) {
    try {
        const response = await fetch(
            `http://127.0.0.1:8000/decisions/${decisionId}/execute`,
            {
                method: "PUT"
            }
        );

        if (!response.ok) {
            throw new Error("Failed to execute decision");
        }

        const result = await response.json();

        console.log("Decision executed:", result);

        // Reload dashboard data so decision + outcome update immediately
        await fetchAgentActionCenter();

    } catch (error) {
        console.error("Execute decision error:", error);
        alert("Unable to execute decision.");
    }
}



testBackendConnection();
fetchSuppliers();
fetchRiskEvents();
fetchRecommendations();
fetchAgentActionCenter();


async function fetchGeminiRecommendation(
  simulation,
  impact,
  reserve,
  refineries
) {

  try {

    const response = await fetch("http://127.0.0.1:8000/gemini/recommendation", {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({

       simulation: simulation,

impact: impact,

reserve: reserve,

refineries: refineries

      })

    });

    const data = await response.json();

    console.log("Gemini Recommendation:", data);

    return data.recommendation;

  } catch (error) {

    console.error(error);

    return "Unable to generate AI recommendation.";

  }

}