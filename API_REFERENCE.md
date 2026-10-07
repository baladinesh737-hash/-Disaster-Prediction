# 🔌 API REFERENCE - GravityShift AI Backend

Base URL: `http://127.0.0.1:5000`

---

## 🔐 AUTHENTICATION

### POST /admin-login
**Description**: Admin authentication

**Request**:
```json
{
  "password": "admin123"
}
```

**Response** (200):
```json
{
  "status": "success",
  "role": "admin"
}
```

**Response** (401):
```json
{
  "status": "fail",
  "message": "Invalid password"
}
```

---

## 🌦️ WEATHER & PREDICTION

### GET /predict/{city}
**Description**: Get disaster risk prediction for a city

**Example**: `/predict/Chennai`

**Response** (200):
```json
{
  "city": "Chennai",
  "lat": 13.0827,
  "lng": 80.2707,
  "rain": 120.5,
  "humidity": 88,
  "wind": 15.3,
  "temperature": 28.5,
  "description": "Heavy Rain",
  "probability": 0.856,
  "risk": "HIGH",
  "disaster": "FLOOD",
  "gravity": 18.45,
  "buoyancy": 1.55,
  "triage": "RED",
  "timestamp": "2024-01-15 14:30:00"
}
```

**Response** (404):
```json
{
  "error": "City not found or weather API unavailable"
}
```

---

## 🧠 AI ANALYSIS (ADMIN ONLY)

### GET /ai-analysis/{city}
**Description**: AI pre-alert analysis for admin decision-making

**Example**: `/ai-analysis/Chennai`

**Response** (200):
```json
{
  "area": "Chennai",
  "prediction": "High chance of Flood | Strong wind advisory",
  "risk": "HIGH",
  "triage": "RED",
  "disaster": "FLOOD",
  "confidence": 0.856,
  "rain": 120.5,
  "humidity": 88,
  "wind": 15.3,
  "gravity": 18.45,
  "buoyancy": 1.55,
  "admin_only": true,
  "timestamp": "2024-01-15 14:30:00"
}
```

**Prediction Logic**:
- Rain > 100mm → "High chance of Flood"
- Rain > 50mm → "Moderate flood risk"
- Wind > 20 m/s → "Cyclone conditions detected"
- Wind > 12 m/s → "Strong wind advisory"
- Humidity > 85% + Rain > 30mm → "Landslide possibility in hilly areas"

---

## 🤖 AI CHATBOT

### POST /ai-chat
**Description**: Disaster safety chatbot

**Request**:
```json
{
  "query": "flood safety tips"
}
```

**Response** (200):
```json
{
  "response": "🌊 Flood Safety: Move to higher ground immediately. Avoid walking/driving through water. Stay away from electrical lines.",
  "timestamp": "2024-01-15 14:30:00"
}
```

**Supported Queries**:
- Flood safety
- Cyclone alerts
- Evacuation routes
- Disaster tracking
- Impact assessment
- Emergency help/SOS

---

## 🚨 ALERT SYSTEM

### POST /send-alert
**Description**: Admin sends disaster alert to users

**Request**:
```json
{
  "city": "Chennai",
  "risk": "HIGH",
  "rain": 120,
  "start_time": "2024-01-15T18:00",
  "end_time": "2024-01-16T06:00",
  "message": "Heavy rainfall expected. Stay indoors.",
  "lat": 13.0827,
  "lng": 80.2707
}
```

**Response** (200):
```json
{
  "status": "Alert sent",
  "alert_id": 1,
  "city": "Chennai",
  "users_found": 150,
  "sms_sent": 148,
  "sms_failed": 2,
  "numbers_sent": ["+919876543210", "+919876543211"],
  "numbers_failed": ["+919999999999"]
}
```

### GET /alerts
**Description**: Get all sent alerts

**Optional Query**: `?city=Chennai` (filter by city)

**Response** (200):
```json
[
  {
    "id": 1,
    "city": "Chennai",
    "rain": 120,
    "start_time": "2024-01-15T18:00",
    "end_time": "2024-01-16T06:00",
    "message": "Heavy rainfall expected. Stay indoors.",
    "risk": "HIGH",
    "lat": 13.0827,
    "lng": 80.2707,
    "sent_at": "2024-01-15 14:30:00",
    "sms_sent": ["+919876543210"],
    "sms_failed": []
  }
]
```

---

## 🆘 SOS / EMERGENCY HELP

### POST /sos
**Description**: User submits emergency help request

**Request**:
```json
{
  "name": "John Doe",
  "phone": "+919876543210",
  "family_members": 4,
  "address": "123 Main St, T Nagar, Chennai",
  "city": "Chennai",
  "problem": "House flooded, need immediate rescue"
}
```

**Response** (200):
```json
{
  "status": "SOS received",
  "sos_id": 1
}
```

### GET /sos-list
**Description**: Admin fetches all SOS requests

**Response** (200):
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "phone": "+919876543210",
    "family_members": 4,
    "address": "123 Main St, T Nagar, Chennai",
    "city": "Chennai",
    "problem": "House flooded, need immediate rescue",
    "status": "PENDING",
    "submitted_at": "2024-01-15 14:30:00"
  }
]
```

### POST /sos-update/{sos_id}
**Description**: Admin updates SOS status

**Example**: `/sos-update/1`

**Request**:
```json
{
  "status": "IN_PROGRESS"
}
```

**Response** (200):
```json
{
  "status": "updated",
  "sos": {
    "id": 1,
    "status": "IN_PROGRESS",
    ...
  }
}
```

**Status Values**: `PENDING`, `IN_PROGRESS`, `RESOLVED`

---

## 🛡️ RESCUE TEAM

### POST /rescue-update
**Description**: Rescue team submits deployment update

**Request**:
```json
{
  "team_name": "Chennai Rescue Squad Alpha",
  "head_name": "Captain Sharma",
  "phone": "+919876543210",
  "members": 12,
  "location": "Chennai",
  "first_aid": "Yes",
  "food_ready": "Yes"
}
```

**Response** (200):
```json
{
  "status": "Rescue update received",
  "rescue_id": 1,
  "notified": 150
}
```

### GET /rescue-list
**Description**: Get all rescue team deployments

**Response** (200):
```json
[
  {
    "id": 1,
    "team_name": "Chennai Rescue Squad Alpha",
    "head_name": "Captain Sharma",
    "phone": "+919876543210",
    "members": 12,
    "location": "Chennai",
    "first_aid": "Yes",
    "food_ready": "Yes",
    "status": "DEPLOYED",
    "submitted_at": "2024-01-15 14:30:00"
  }
]
```

---

## 🏛️ GOVERNMENT REQUESTS

### POST /government-alert
**Description**: Admin sends HIGH risk request to government

**Request**:
```json
{
  "city": "Chennai",
  "risk": "HIGH",
  "request_type": "accommodation",
  "details": "Need 500 relief camp beds for evacuees"
}
```

**Response** (200):
```json
{
  "status": "Government alert submitted",
  "gov_id": 1,
  "request": "accommodation"
}
```

**Response** (403):
```json
{
  "error": "Government alerts only for HIGH risk situations"
}
```

**Request Types**: `accommodation`, `hospital`, `permission`

### GET /government-list
**Description**: Get all government requests

**Response** (200):
```json
[
  {
    "id": 1,
    "city": "Chennai",
    "risk": "HIGH",
    "request_type": "accommodation",
    "details": "Need 500 relief camp beds for evacuees",
    "status": "SUBMITTED",
    "submitted_at": "2024-01-15 14:30:00"
  }
]
```

---

## 🧭 SAFE ROUTE

### GET /safe-route
**Description**: Find nearest LOW-risk district for evacuation

**Query Parameters**:
- `lat` (required): User's latitude
- `lng` (required): User's longitude

**Example**: `/safe-route?lat=13.0827&lng=80.2707`

**Response** (200):
```json
{
  "status": "ok",
  "from": {
    "lat": 13.0827,
    "lng": 80.2707
  },
  "to": {
    "lat": 11.0168,
    "lng": 76.9558,
    "city": "Coimbatore"
  },
  "distance_km": 425.3,
  "triage": "GREEN",
  "message": "Move to safe zone: Coimbatore (425.3 km away)"
}
```

**Response** (200 - No Safe Zone):
```json
{
  "status": "no_safe_zone",
  "message": "No LOW risk zones found currently"
}
```

---

## 🏥 HEALTH CHECK

### GET /api
**Description**: Backend health check

**Response** (200):
```json
{
  "status": "GravityShift AI Backend Online 🔥",
  "version": "2.0"
}
```

---

## ❌ REMOVED ENDPOINTS

### ~~GET /all~~ (REMOVED)
**Reason**: Automatic data loading removed for admin control

**Replacement**: Admin manually triggers predictions per city using `/predict/{city}`

---

## 🔧 ERROR RESPONSES

### 400 Bad Request
```json
{
  "error": "Missing fields: ['city', 'message']"
}
```

### 401 Unauthorized
```json
{
  "status": "fail",
  "message": "Invalid password"
}
```

### 403 Forbidden
```json
{
  "error": "Government alerts only for HIGH risk situations"
}
```

### 404 Not Found
```json
{
  "error": "City not found or weather API unavailable"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## 📝 NOTES

1. **SMS Functionality**: Requires valid Twilio credentials in `app.py`
2. **Weather Data**: Uses OpenWeatherMap API (key in `app.py`)
3. **CORS**: Enabled for all origins (adjust for production)
4. **Storage**: In-memory (replace with database for production)
5. **Admin Only**: `/ai-analysis` results never sent to users/rescue

---

## 🔐 CONFIGURATION

Edit `backend/app.py`:

```python
WEATHER_API_KEY  = "your_openweather_api_key"
TWILIO_SID       = "your_twilio_sid"
TWILIO_TOKEN     = "your_twilio_token"
TWILIO_FROM      = "+1234567890"
ADMIN_PASSWORD   = "your_secure_password"
```

---

**API Version**: 2.0  
**Last Updated**: 2024  
**Status**: ✅ Production Ready
