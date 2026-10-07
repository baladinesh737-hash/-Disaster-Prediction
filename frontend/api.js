/**
 * GravityShift AI – Shared API & Utility Layer
 * Used by all dashboards: user, admin, rescue, government
 */
const API_BASE = "http://127.0.0.1:5000";

// ── HTTP HELPERS ──────────────────────────────────────────────────────────────
function getAuthHeaders() {
  const token = localStorage.getItem("admin_token");
  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

async function apiGet(path, requireAuth = false) {
  if (requireAuth) {
    const token = localStorage.getItem("admin_token");
    if (!token) {
      alert("⚠ Please login first");
      window.location.href = "index.html";
      return;
    }
  }

  const url = path.startsWith("http") ? path : API_BASE + path;
  const headers = getAuthHeaders();
  
  const res = await fetch(url, {
    method: "GET",
    headers: headers
  });
  
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || `GET ${path} failed`);
  }
  return data;
}

async function apiPost(path, body, requireAuth = false) {
  if (requireAuth) {
    const token = localStorage.getItem("admin_token");
    if (!token) {
      alert("⚠ Please login first");
      window.location.href = "index.html";
      return;
    }
  }
  
  // Using the API_BASE defined at the top of the file
  const url = path.startsWith("http") ? path : API_BASE + path;
  
  const res = await fetch(url, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body),
  });
  
  if (res.status === 401) {
    alert("⚠ Session expired. Please login again.");
    localStorage.removeItem("admin_token");
    window.location.href = "index.html";
    return;
  }
  
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `POST ${path} failed`);
  return data;
}

// ── RISK COLORS ───────────────────────────────────────────────────────────────
function riskColor(risk) {
  return risk === "HIGH" ? "#ff3b3b" : risk === "MEDIUM" ? "#ff9500" : "#00cc66";
}

function riskBg(risk) {
  return risk === "HIGH"
    ? "rgba(255,59,59,0.15)"
    : risk === "MEDIUM"
    ? "rgba(255,149,0,0.15)"
    : "rgba(0,204,102,0.15)";
}

// ── CLOCK ─────────────────────────────────────────────────────────────────────
function startClock(elId) {
  const el = document.getElementById(elId);
  if (!el) return;
  const tick = () => (el.textContent = new Date().toLocaleTimeString());
  tick();
  setInterval(tick, 1000);
}

// ── TOAST ─────────────────────────────────────────────────────────────────────
function showToast(msg, type = "info") {
  let t = document.getElementById("toast");
  if (!t) {
    t = document.createElement("div");
    t.id = "toast";
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.className = `toast toast-${type} show`;
  setTimeout(() => t.classList.remove("show"), 3500);
}

// ── LEAFLET MAP INIT ──────────────────────────────────────────────────────────
function initLeafletMap(containerId, center = [10.8, 78.7], zoom = 7) {
  const map = L.map(containerId).setView(center, zoom);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap",
  }).addTo(map);
  return map;
}

function plotDistricts(map, districts) {
  // Remove old circles
  map.eachLayer((l) => {
    if (l instanceof L.Circle) map.removeLayer(l);
  });
  districts.forEach((d) => {
    const color  = riskColor(d.risk);
    const radius = d.risk === "HIGH" ? 28000 : d.risk === "MEDIUM" ? 18000 : 10000;
    L.circle([d.lat, d.lng], {
      color, fillColor: color, fillOpacity: 0.35, radius, weight: 2,
    })
      .addTo(map)
      .bindPopup(
        `<b>${d.city}</b><br>
         Risk: <b style="color:${color}">${d.risk}</b><br>
         Rain: ${d.rain} mm | Humidity: ${d.humidity}%<br>
         Wind: ${d.wind} m/s | Temp: ${d.temperature}°C<br>
         Disaster: ${d.disaster}`
      );
  });
}

// Manual district loading (admin controlled)
async function loadDistrictsManual(map) {
  try {
    const data = await apiGet("/predict/Chennai"); // Example: load single city
    // Admin can extend this to load multiple cities on demand
    return data;
  } catch (e) {
    console.error("Failed to load district data", e);
    return null;
  }
}

// ── FORMAT DATE ───────────────────────────────────────────────────────────────
function fmtTime(ts) {
  if (!ts) return "--";
  return new Date(ts).toLocaleString();
}

// ── SHARED STYLES (injected into every page) ──────────────────────────────────
const SHARED_CSS = `
  :root {
    --bg: #050a14;
    --glass: rgba(255,255,255,0.05);
    --border: rgba(255,255,255,0.1);
    --accent: #00d4ff;
    --accent2: #7c3aed;
    --red: #ff3b3b;
    --orange: #ff9500;
    --green: #00cc66;
    --text: #e2e8f0;
    --dim: #94a3b8;
    --font: 'Inter', sans-serif;
    --title: 'Orbitron', monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: var(--font); min-height: 100vh; }
  .glass {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    backdrop-filter: blur(16px);
    padding: 1.2rem;
  }
  .btn {
    padding: 0.7rem 1.4rem; border: none; border-radius: 10px;
    cursor: pointer; font-weight: 600; font-size: 0.9rem; transition: opacity .2s;
  }
  .btn:hover { opacity: 0.85; }
  .btn-primary { background: linear-gradient(135deg, var(--accent), var(--accent2)); color: #fff; }
  .btn-danger  { background: var(--red); color: #fff; }
  .btn-success { background: var(--green); color: #fff; }
  .btn-warn    { background: var(--orange); color: #fff; }
  input, select, textarea {
    background: rgba(255,255,255,0.07); border: 1px solid var(--border);
    border-radius: 10px; padding: 0.7rem 1rem; color: var(--text);
    font-family: var(--font); font-size: 0.9rem; width: 100%; outline: none;
  }
  input:focus, select:focus, textarea:focus { border-color: var(--accent); }
  label { font-size: 0.8rem; color: var(--dim); display: block; margin-bottom: 0.3rem; }
  .form-group { margin-bottom: 0.9rem; }
  .risk-badge {
    display: inline-block; padding: 0.25rem 0.8rem; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
  }
  .risk-HIGH   { background: rgba(255,59,59,0.2);  color: var(--red);    border: 1px solid var(--red); }
  .risk-MEDIUM { background: rgba(255,149,0,0.2);  color: var(--orange); border: 1px solid var(--orange); }
  .risk-LOW    { background: rgba(0,204,102,0.2);  color: var(--green);  border: 1px solid var(--green); }
  .toast {
    position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 9999;
    padding: 0.8rem 1.4rem; border-radius: 12px; font-size: 0.9rem;
    opacity: 0; transition: opacity .3s; pointer-events: none;
  }
  .toast.show { opacity: 1; }
  .toast-info    { background: #1e3a5f; border: 1px solid var(--accent); color: var(--text); }
  .toast-success { background: #0d3320; border: 1px solid var(--green);  color: var(--green); }
  .toast-error   { background: #3a0d0d; border: 1px solid var(--red);    color: var(--red); }
  .section-title { font-family: var(--title); font-size: 0.9rem; color: var(--accent); margin-bottom: 1rem; letter-spacing: .05em; }
  .overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.75);
    display: flex; align-items: center; justify-content: center;
    z-index: 9000; backdrop-filter: blur(6px);
  }
  .modal {
    background: #0d1b2e; border: 1px solid var(--border); border-radius: 20px;
    padding: 2rem; width: 90%; max-width: 480px; max-height: 90vh; overflow-y: auto;
  }
  .modal h3 { font-family: var(--title); color: var(--accent); margin-bottom: 1.2rem; font-size: 1rem; }
  .hidden { display: none !important; }
  .pulse { animation: pulse 1.5s infinite; }
  @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(1.3)} }
  .spinner {
    width: 36px; height: 36px; border: 3px solid rgba(0,212,255,.2);
    border-top-color: var(--accent); border-radius: 50%;
    animation: spin .8s linear infinite; margin: 1rem auto;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-thumb { background: var(--accent2); border-radius: 3px; }
`;

// Inject shared CSS into current page
(function injectCSS() {
  const style = document.createElement("style");
  style.textContent = SHARED_CSS;
  document.head.insertBefore(style, document.head.firstChild);
})();
