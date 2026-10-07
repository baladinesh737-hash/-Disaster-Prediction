"""
GravityShift AI – Disaster Risk Prediction & Emergency Response System
Backend: Flask | ML: Logistic Regression | SMS: Twilio | Data: Pandas/Excel
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd
from datetime import datetime
import hashlib
import os
import math

try:
    from role_login import generate_login_token, register_role_login
except ModuleNotFoundError:
    from backend.role_login import generate_login_token, register_role_login

# Serve static files from frontend folder (parent directory)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app = Flask(__name__, static_folder=frontend_path, static_url_path="")
CORS(app)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
WEATHER_API_KEY  = "9b024b490ebf051691f8ab7d6da8b193"
TWILIO_SID       = "YOUR_TWILIO_SID"
TWILIO_TOKEN     = "YOUR_TWILIO_TOKEN"
TWILIO_FROM      = "+1XXXXXXXXXX"
ADMIN_PASSWORD   = "admin123"
SECRET_KEY       = os.getenv("SECRET_KEY", "gravityshift-secret")
USERS_FILE       = "users.xlsx"

# ══════════════════════════════════════════════════════════════════════════════
# IN-MEMORY STORES  (replace with SQLite for production)
# ══════════════════════════════════════════════════════════════════════════════
alerts_store    = []   # alerts sent by admin → shown on user + rescue dashboards
sos_store       = []   # emergency help requests from users → shown on admin
rescue_store    = []   # rescue team readiness updates → shown on admin + users
gov_store       = []   # government requests from admin

# ══════════════════════════════════════════════════════════════════════════════
# ML MODEL
# ══════════════════════════════════════════════════════════════════════════════
_X = [
    [0,45,3],[5,55,5],[10,60,8],[20,65,10],
    [30,70,12],[50,75,18],[70,80,25],[90,85,35],
    [110,88,42],[140,92,55],[160,95,65],[200,98,80],
    [2,40,2],[8,50,6],[15,58,9],[25,62,11],
]
_y = [0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0]

scaler = StandardScaler()
_Xs    = scaler.fit_transform(_X)
model  = LogisticRegression(max_iter=1000)
model.fit(_Xs, _y)

# ══════════════════════════════════════════════════════════════════════════════
# DISTRICTS
# ══════════════════════════════════════════════════════════════════════════════
DISTRICTS = [
    {"name": "Chennai",     "lat": 13.0827, "lng": 80.2707},
    {"name": "Coimbatore",  "lat": 11.0168, "lng": 76.9558},
    {"name": "Madurai",     "lat":  9.9252, "lng": 78.1198},
    {"name": "Salem",       "lat": 11.6643, "lng": 78.1460},
    {"name": "Trichy",      "lat": 10.7905, "lng": 78.7047},
    {"name": "Tirunelveli", "lat":  8.7139, "lng": 77.7567},
    {"name": "Dharmapuri",  "lat": 12.1211, "lng": 78.1582},
    {"name": "Erode",       "lat": 11.3410, "lng": 77.7172},
    {"name": "Vellore",     "lat": 12.9165, "lng": 79.1325},
    {"name": "Thoothukudi", "lat":  8.7642, "lng": 78.1348},
    {"name": "Kanchipuram", "lat": 12.8185, "lng": 79.6947},
    {"name": "Thanjavur",   "lat": 10.7870, "lng": 79.1378},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fetch_weather(city: str) -> dict | None:
    try:
        url = (f"http://api.openweathermap.org/data/2.5/weather"
               f"?q={city}&appid={WEATHER_API_KEY}&units=metric")
        r = requests.get(url, timeout=6).json()
        return r if r.get("cod") == 200 else None
    except Exception:
        return None


def compute_risk(rain: float, humidity: float, wind: float) -> dict:
    feat     = scaler.transform([[rain, humidity, wind]])
    prob     = float(model.predict_proba(feat)[0][1])
    gravity  = round(min((rain * 0.045) + (humidity * 0.08) + (wind * 0.12), 20.0), 2)
    buoyancy = round(max(0.0, 20.0 - gravity), 2)

    if prob >= 0.65:
        risk, disaster = "HIGH",   "FLOOD"
    elif prob >= 0.45:
        risk, disaster = "HIGH",   "CYCLONE" if wind > 20 else "FLOOD"
    elif prob >= 0.30:
        risk, disaster = "MEDIUM", "FLOOD"
    else:
        risk, disaster = "LOW",    "NORMAL"

    # Triage classification
    if risk == "HIGH" and rain > 100:
        triage = "RED"
    elif risk == "MEDIUM":
        triage = "ORANGE"
    else:
        triage = "GREEN"

    return {
        "probability": round(prob, 3),
        "risk":        risk,
        "disaster":    disaster,
        "gravity":     gravity,
        "buoyancy":    buoyancy,
        "triage":      triage,
    }


def build_payload(city: str, w: dict) -> dict:
    rain     = w.get("rain", {}).get("1h", 0)
    humidity = w["main"]["humidity"]
    wind     = w["wind"]["speed"]
    scores   = compute_risk(rain, humidity, wind)
    return {
        "city":        city.title(),
        "lat":         w["coord"]["lat"],
        "lng":         w["coord"]["lon"],
        "rain":        rain,
        "humidity":    humidity,
        "wind":        wind,
        "temperature": w["main"]["temp"],
        "description": w["weather"][0]["description"].title(),
        **scores,
        "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def send_sms(to: str, body: str) -> bool:
    """Send SMS via Twilio. Returns True on success."""
    try:
        from twilio.rest import Client
        Client(TWILIO_SID, TWILIO_TOKEN).messages.create(
            body=body, from_=TWILIO_FROM, to=to
        )
        return True
    except Exception as e:
        print(f"[SMS ERROR] {e}")
        return False


def load_users_by_city(city: str) -> list[dict]:
    """Load users from Excel filtered by city."""
    if not os.path.exists(USERS_FILE):
        return []
    try:
        df = pd.read_excel(USERS_FILE)
        df.columns = [c.strip().lower() for c in df.columns]
        filtered = df[df["city"].str.strip().str.lower() == city.strip().lower()]
        return filtered.to_dict(orient="records")
    except Exception as e:
        print(f"[EXCEL ERROR] {e}")
        return []


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Return distance in km between two coordinates."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES – SAFE ROUTE
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/safe-route")
def safe_route():
    """
    GET /safe-route?lat=<lat>&lng=<lng>
    Finds the nearest LOW-risk district from the caller's coordinates.
    """
    try:
        user_lat = float(request.args.get("lat"))
        user_lng = float(request.args.get("lng"))
    except (TypeError, ValueError):
        return jsonify({"error": "Provide valid lat and lng query parameters"}), 400

    safe_zones = []
    for d in DISTRICTS:
        w = fetch_weather(d["name"])
        if w:
            rain     = w.get("rain", {}).get("1h", 0)
            humidity = w["main"]["humidity"]
            wind     = w["wind"]["speed"]
            scores   = compute_risk(rain, humidity, wind)
        else:
            scores = compute_risk(0, 55, 5)

        if scores["risk"] == "LOW":
            dist = haversine(user_lat, user_lng, d["lat"], d["lng"])
            safe_zones.append({"district": d, "scores": scores, "distance_km": dist})

    if not safe_zones:
        return jsonify({"status": "no_safe_zone", "message": "No LOW risk zones found currently"}), 200

    nearest = min(safe_zones, key=lambda x: x["distance_km"])
    d       = nearest["district"]

    return jsonify({
        "status":  "ok",
        "from":    {"lat": user_lat, "lng": user_lng},
        "to":      {"lat": d["lat"], "lng": d["lng"], "city": d["name"]},
        "distance_km": round(nearest["distance_km"], 1),
        "triage":  nearest["scores"]["triage"],
        "message": f"Move to safe zone: {d['name']} ({round(nearest['distance_km'], 1)} km away)",
    })


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES – AI PRE-ALERT  (Admin only — never forwarded to users/rescue)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/ai-analysis/<city>")
def ai_analysis(city):
    """
    GET /ai-analysis/<city>
    Admin-only pre-alert: predicts disaster type BEFORE sending an alert.
    Response is NEVER stored in alerts_store — purely advisory for admin.
    """
    w = fetch_weather(city)
    if not w:
        return jsonify({"error": "City not found or weather API unavailable"}), 404

    rain     = w.get("rain", {}).get("1h", 0)
    humidity = w["main"]["humidity"]
    wind     = w["wind"]["speed"]
    scores   = compute_risk(rain, humidity, wind)

    # Multi-disaster prediction logic
    predictions = []
    confidence  = round(scores["probability"], 3)

    if rain > 100:
        predictions.append("High chance of Flood")
    elif rain > 50:
        predictions.append("Moderate flood risk")

    if wind > 20:
        predictions.append("Cyclone conditions detected")
    elif wind > 12:
        predictions.append("Strong wind advisory")

    if humidity > 85 and rain > 30:
        predictions.append("Landslide possibility in hilly areas")

    if not predictions:
        predictions.append("No immediate disaster threat")

    return jsonify({
        "area":        city.title(),
        "prediction":  " | ".join(predictions),
        "risk":        scores["risk"],
        "triage":      scores["triage"],
        "disaster":    scores["disaster"],
        "confidence":  confidence,
        "rain":        rain,
        "humidity":    humidity,
        "wind":        wind,
        "gravity":     scores["gravity"],
        "buoyancy":    scores["buoyancy"],
        "admin_only":  True,
        "timestamp":   now(),
    })


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES – CORE
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api")
def api_status():
    """API health check endpoint."""
    return jsonify({"status": "GravityShift AI Backend Online 🔥", "version": "2.0"})


@app.route("/predict/<city>")
def predict(city):
    """Predict flood risk for a single city."""
    w = fetch_weather(city)
    if not w:
        return jsonify({"error": "City not found or weather API unavailable"}), 404
    return jsonify(build_payload(city, w))





# ══════════════════════════════════════════════════════════════════════════════
# ROUTES – AUTH
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if password == ADMIN_PASSWORD:
        return jsonify({
            "status": "success",
            "role": "admin",
            "token": generate_login_token("admin", password, SECRET_KEY),
        })
    return jsonify({"status": "fail", "message": "Invalid password"}), 401


register_role_login(app, ADMIN_PASSWORD, SECRET_KEY)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES – ALERT SYSTEM  (Admin → Users + Rescue)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/send-alert", methods=["POST"])
def send_alert():
    """
    Admin sends an alert for a location.
    Reads users from Excel, sends SMS via Twilio,
    stores alert for User + Rescue dashboards.
    """
    data = request.get_json(silent=True) or {}

    required = ["city", "rain", "start_time", "end_time", "message"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    city    = data["city"].strip()
    rain    = data["rain"]
    start   = data["start_time"]
    end     = data["end_time"]
    message = data["message"]
    risk    = data.get("risk", "HIGH")
    lat     = data.get("lat")
    lng     = data.get("lng")

    alert_obj = {
        "id":         len(alerts_store) + 1,
        "city":       city,
        "rain":       rain,
        "start_time": start,
        "end_time":   end,
        "message":    message,
        "risk":       risk,
        "lat":        lat,
        "lng":        lng,
        "sent_at":    now(),
        "sms_sent":   [],
        "sms_failed": [],
    }

    # Load users from Excel and send SMS
    users = load_users_by_city(city)
    for user in users:
        phone = str(user.get("phone", "")).strip()
        if not phone.startswith("+"):
            phone = f"+91{phone}"
        sms_body = (
            f"🚨 DISASTER ALERT – {city}\n"
            f"Risk: {risk} | Rain: {rain}mm\n"
            f"Period: {start} to {end}\n"
            f"{message}\n"
            f"– GravityShift AI Emergency System"
        )
        ok = send_sms(phone, sms_body)
        if ok:
            alert_obj["sms_sent"].append(phone)
        else:
            alert_obj["sms_failed"].append(phone)

    alerts_store.append(alert_obj)

    return jsonify({
        "status":        "Alert sent",
        "alert_id":      alert_obj["id"],
        "city":          city,
        "users_found":   len(users),
        "sms_sent":      len(alert_obj["sms_sent"]),
        "sms_failed":    len(alert_obj["sms_failed"]),
        "numbers_sent":  alert_obj["sms_sent"],
        "numbers_failed": alert_obj["sms_failed"],
    })


@app.route("/alerts", methods=["GET"])
def get_alerts():
    """Return all alerts (for User + Rescue dashboards)."""
    city = request.args.get("city", "").strip().lower()
    if city:
        filtered = [a for a in alerts_store if a["city"].lower() == city]
        return jsonify(filtered)
    return jsonify(alerts_store)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES – SOS / USER HELP  (User → Admin)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/sos", methods=["POST"])
def sos():
    """
    User submits emergency help request.
    Stored for Admin dashboard. SMS sent to admin if configured.
    """
    data = request.get_json(silent=True) or {}

    required = ["name", "phone", "address", "problem"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    sos_obj = {
        "id":             len(sos_store) + 1,
        "name":           data["name"],
        "phone":          data["phone"],
        "family_members": data.get("family_members", 1),
        "address":        data["address"],
        "problem":        data["problem"],
        "city":           data.get("city", "Unknown"),
        "status":         "PENDING",
        "submitted_at":   now(),
    }
    sos_store.append(sos_obj)

    # Notify admin via SMS (optional)
    send_sms(
        TWILIO_FROM,
        f"🆘 SOS #{sos_obj['id']} from {sos_obj['name']} "
        f"({sos_obj['city']}): {sos_obj['problem'][:80]}"
    )

    return jsonify({"status": "SOS received", "sos_id": sos_obj["id"]})


@app.route("/sos-list", methods=["GET"])
def sos_list():
    """Admin fetches all SOS requests."""
    return jsonify(sos_store)


@app.route("/sos-update/<int:sos_id>", methods=["POST"])
def sos_update(sos_id):
    """Admin updates SOS status (PENDING → IN_PROGRESS → RESOLVED)."""
    data   = request.get_json(silent=True) or {}
    status = data.get("status", "IN_PROGRESS")
    for s in sos_store:
        if s["id"] == sos_id:
            s["status"] = status
            return jsonify({"status": "updated", "sos": s})
    return jsonify({"error": "SOS not found"}), 404


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES – RESCUE TEAM  (Rescue → Admin + Users)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/rescue-update", methods=["POST"])
def rescue_update():
    """
    Rescue team submits readiness form.
    Stored for Admin. Users can see rescue is deployed.
    """
    data = request.get_json(silent=True) or {}

    required = ["team_name", "head_name", "phone", "members", "location"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    rescue_obj = {
        "id":          len(rescue_store) + 1,
        "team_name":   data["team_name"],
        "head_name":   data["head_name"],
        "phone":       data["phone"],
        "members":     data["members"],
        "location":    data["location"],
        "first_aid":   data.get("first_aid", "No"),
        "food_ready":  data.get("food_ready", "No"),
        "status":      "DEPLOYED",
        "submitted_at": now(),
    }
    rescue_store.append(rescue_obj)

    # Notify users in that location via SMS
    users = load_users_by_city(rescue_obj["location"])
    for user in users:
        phone = str(user.get("phone", "")).strip()
        if not phone.startswith("+"):
            phone = f"+91{phone}"
        send_sms(
            phone,
            f"✅ Rescue Team '{rescue_obj['team_name']}' is deployed to "
            f"{rescue_obj['location']}. Help is on the way. "
            f"Contact: {rescue_obj['phone']}"
        )

    return jsonify({
        "status":     "Rescue update received",
        "rescue_id":  rescue_obj["id"],
        "notified":   len(users),
    })


@app.route("/rescue-list", methods=["GET"])
def rescue_list():
    """Return all rescue deployments (for Admin + User dashboards)."""
    return jsonify(rescue_store)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES – GOVERNMENT  (Admin → Government, only HIGH risk)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/government-alert", methods=["POST"])
def government_alert():
    """
    Admin sends government-level request when risk is VERY HIGH.
    Requires risk=HIGH in payload.
    """
    data = request.get_json(silent=True) or {}

    if data.get("risk", "").upper() != "HIGH":
        return jsonify({"error": "Government alerts only for HIGH risk situations"}), 403

    required = ["city", "request_type", "details"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    gov_obj = {
        "id":           len(gov_store) + 1,
        "city":         data["city"],
        "risk":         "HIGH",
        "request_type": data["request_type"],  # accommodation / hospital / permission
        "details":      data["details"],
        "status":       "SUBMITTED",
        "submitted_at": now(),
    }
    gov_store.append(gov_obj)

    return jsonify({
        "status":     "Government alert submitted",
        "gov_id":     gov_obj["id"],
        "request":    gov_obj["request_type"],
    })


@app.route("/government-list", methods=["GET"])
def government_list():
    """Return all government requests."""
    return jsonify(gov_store)


# ══════════════════════════════════════════════════════════════════════════════
# STATIC FILES & DEFAULT ROUTING
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/<path:filename>")
def serve_static(filename):
    """Serve static files (CSS, JS, images)."""
    return send_from_directory(app.static_folder, filename)


@app.route("/")
def serve_index():
    """Serve index.html for root path."""
    return send_from_directory(app.static_folder, "index.html")


@app.errorhandler(404)
def page_not_found(error):
    """Serve index.html for all non-API routes (SPA support)."""
    if request.path.startswith("/"):
        # Try to serve the requested file
        requested = request.path.lstrip("/")
        if requested and os.path.exists(os.path.join(app.static_folder, requested)):
            return send_from_directory(app.static_folder, requested)
        # Default to index.html for SPA routing
        return send_from_directory(app.static_folder, "index.html")
    return jsonify({"error": "Not found"}), 404


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES – AI CHATBOT
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/ai-chat", methods=["POST"])
def ai_chat():
    """
    AI chatbot endpoint for disaster queries.
    Connected to local Ollama AI.
    """
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        # Connect to local Ollama API
        ollama_url = "http://localhost:11434/api/generate"
        
        # System prompt for disaster management context
        system_prompt = """You are a disaster management AI assistant. Provide VERY SHORT responses (1-2 sentences, max 30 words) about:
- Flood safety and evacuation
- Cyclone/storm preparedness
- Emergency contacts and procedures
- Disaster impact assessment
- Safety instructions

Be extremely concise and actionable."""
        
        # Combine system prompt with user query
        full_prompt = f"{system_prompt}\n\nUser: {query}\n\nAssistant:"
        
        # Call Ollama API
        ollama_response = requests.post(
            ollama_url,
            json={
                "model": "mistral:latest",  # Using your installed model
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 50  # Very short responses
                }
            },
            timeout=30
        )
        
        if ollama_response.status_code == 200:
            ollama_data = ollama_response.json()
            ai_response = ollama_data.get("response", "").strip()
            
            # Fallback if response is empty
            if not ai_response:
                ai_response = "I'm having trouble processing that. Could you rephrase your question?"
            
            return jsonify({
                "response": ai_response,
                "timestamp": now(),
                "source": "ollama"
            })
        else:
            # Fallback to rule-based if Ollama fails
            return fallback_ai_response(query)
            
    except requests.exceptions.ConnectionError:
        # Ollama not running - use fallback
        return fallback_ai_response(query)
    except Exception as e:
        print(f"[OLLAMA ERROR] {e}")
        return fallback_ai_response(query)


def fallback_ai_response(query):
    """
    Fallback rule-based responses if Ollama is unavailable.
    """
    query = query.lower()
    response = ""
    
    if "flood" in query or "water" in query:
        response = "🌊 Move to higher ground. Avoid water. Stay away from power lines."
    elif "cyclone" in query or "wind" in query or "storm" in query:
        response = "🌪 Stay indoors away from windows. Secure loose objects. Follow evacuation orders."
    elif "safe" in query or "evacuation" in query:
        response = "🏃 Head to relief camp. Carry ID, medicines, water. Call 108 for help."
    elif "movement" in query or "track" in query:
        response = "📍 Check live map. RED = danger. Move to GREEN zones."
    elif "impact" in query or "damage" in query:
        response = "⚠ HIGH risk = severe damage. MEDIUM = moderate. Stay updated."
    elif "help" in query or "sos" in query:
        response = "🆘 Call 108 (ambulance), 100 (police), 1078 (disaster helpline)."
    else:
        response = "🤖 Ask about: flood safety, cyclone alerts, evacuation, emergency contacts."
    
    return jsonify({
        "response": response,
        "timestamp": now(),
        "source": "fallback"
    })


# ══════════════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app.run(debug=True, port=5000)
