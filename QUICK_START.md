# ⚡ QUICK START GUIDE

## 🚀 Get Running in 2 Minutes

### Step 1: Start Backend (30 seconds)
```bash
cd "d:\freshthon project\backend"
python app.py
```

**Expected Output**:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### Step 2: Open Admin Panel (10 seconds)
1. Open browser
2. Navigate to: `d:\freshthon project\frontend\admin.html`
3. Login with password: `admin123`

### Step 3: Test Core Features (1 minute)

#### ✅ Empty Map
- Map should load with NO circles or markers
- Only base map tiles visible

#### ✅ Place Marker
1. Click "📍 Place Disaster Zone" (button turns red)
2. Click anywhere on map
3. Red marker appears
4. Sidebar shows coordinates

#### ✅ Map Toggle
1. Click "🛰 Satellite"
2. Ventusky weather radar loads
3. Click "🗺 Live Map"
4. Returns to Leaflet map

#### ✅ AI Analysis
1. Enter "Chennai" in AI panel
2. Click "Analyze"
3. Purple panel shows prediction
4. Click "📋 Use in Alert Form"
5. Alert modal opens with pre-filled data

#### ✅ Send Alert
1. Click "🚨 Send Disaster Alert"
2. Fill form (or use AI data)
3. Click "📡 SEND ALERT"
4. Success toast appears
5. Check "📋 Sent Alerts" tab

#### ✅ AI Chatbot
1. Click robot icon (🤖) bottom-right
2. Type: "flood safety"
3. Press Enter
4. Response appears instantly

---

## 🎯 5-Minute Full Demo

### Scenario: Chennai Flood Alert

**1. AI Analysis** (1 min)
```
→ Enter "Chennai" in AI panel
→ Click "Analyze"
→ Review: HIGH risk, Flood prediction, 85% confidence
```

**2. Mark Location** (30 sec)
```
→ Click "Place Disaster Zone"
→ Click on Chennai area on map
→ Marker placed at 13.0827, 80.2707
```

**3. Send Alert** (1 min)
```
→ Click "Send Disaster Alert"
→ Click "Use in Alert Form" (auto-fills from AI)
→ Add custom message: "Evacuate low-lying areas immediately"
→ Set start time: Today 6 PM
→ Set end time: Tomorrow 6 AM
→ Click "SEND ALERT"
```

**4. Monitor** (30 sec)
```
→ Check "📋 Sent Alerts" tab
→ Verify alert appears with coordinates
→ Check stats bar: Alerts: 1
```

**5. Chat Test** (1 min)
```
→ Click robot icon
→ Ask: "What should people do during flood?"
→ Get response: "Move to higher ground..."
→ Ask: "evacuation route"
→ Get response: "Head to nearest relief camp..."
```

**6. Government Request** (1 min)
```
→ Scroll to Government Request panel
→ Enter city: Chennai
→ Click "🏠 Accommodation"
→ Details: "Need 500 relief camp beds"
→ Click "Send to Government"
→ Check "🏛 Government" tab
```

---

## 🔥 Power User Tips

### Keyboard Shortcuts
- `Enter` in city input → Triggers analysis
- `Enter` in chat → Sends message
- `Esc` → Close modals (if implemented)

### Workflow Optimization
1. **Pre-analyze cities** before disasters hit
2. **Place markers** during planning phase
3. **Use AI data** to auto-fill alerts
4. **Monitor SOS** inbox every 5 minutes
5. **Update rescue** status regularly

### Best Practices
- ✅ Always run AI analysis before sending alerts
- ✅ Place markers for precise location tracking
- ✅ Use satellite view for weather verification
- ✅ Update SOS status promptly (PENDING → IN_PROGRESS → RESOLVED)
- ✅ Send government requests for HIGH risk only

---

## 🐛 Troubleshooting

### Backend Not Starting?
```bash
# Install dependencies
pip install flask flask-cors requests numpy scikit-learn pandas openpyxl

# Run again
python app.py
```

### Map Not Loading?
- Check browser console (F12)
- Verify Leaflet CDN loaded
- Clear browser cache

### AI Analysis Fails?
- Verify backend running on port 5000
- Check city name spelling
- Try different city (e.g., "Chennai", "Mumbai")

### Chatbot Not Responding?
- Check Network tab for `/ai-chat` POST request
- Verify backend logs for errors
- Refresh page and try again

### Marker Not Placing?
- Ensure "Place Disaster Zone" button is RED (active)
- Click directly on map (not on controls)
- Try clearing markers and placing again

---

## 📱 Mobile Testing

### Responsive Design
- Admin panel works on tablets (iPad)
- User dashboard mobile-friendly
- Chatbot adapts to screen size

### Touch Controls
- Tap to place markers
- Swipe to pan map
- Pinch to zoom

---

## 🎓 Learning Path

### Beginner (5 minutes)
1. Login
2. Place marker
3. Toggle map
4. Send alert

### Intermediate (15 minutes)
1. AI analysis
2. Alert with coordinates
3. SOS management
4. Rescue monitoring

### Advanced (30 minutes)
1. Government requests
2. Multi-city analysis
3. Evacuation routes
4. Full disaster response workflow

---

## 🔗 Quick Links

- **Backend**: http://127.0.0.1:5000
- **Admin**: `frontend/admin.html`
- **User**: `frontend/user.html`
- **API Docs**: `API_REFERENCE.md`
- **Testing**: `TESTING_GUIDE.md`
- **Full Docs**: `IMPLEMENTATION_SUMMARY.md`

---

## 📞 Emergency Contacts (India)

- **Ambulance**: 108
- **Police**: 100
- **Disaster Helpline**: 1078
- **Fire**: 101
- **Women Helpline**: 1091

---

## ✅ Success Checklist

After 2 minutes, you should have:
- [x] Backend running
- [x] Admin panel open
- [x] Logged in successfully
- [x] Map loaded (empty)
- [x] Marker placed
- [x] Satellite view tested
- [x] AI analysis working
- [x] Alert sent
- [x] Chatbot responding

**Status**: ✅ System Operational

---

## 🎉 You're Ready!

You now have a fully functional disaster management control room.

**Next Steps**:
1. Explore all tabs (SOS, Rescue, Alerts, Government)
2. Test user dashboard (`user.html`)
3. Read full documentation
4. Customize for your needs

---

**Time to Production**: 2 minutes ⚡  
**Difficulty**: Easy 🟢  
**Status**: Ready to Deploy 🚀
