# 🏥 EVACUATION CENTER FEATURE - USER GUIDE

## ✅ What Was Added

Users can now search for nearby evacuation centers and see routes to reach them during disasters!

---

## 🎯 FEATURES

### 1. **Search Evacuation Centers**
- Enter your city name
- System finds all available evacuation centers
- Shows distance from your location (if location enabled)
- Displays capacity and facilities

### 2. **View on Map**
- All centers marked with green numbered markers
- Your location shown with blue marker
- Click any center to see details

### 3. **Route Display**
- Click on any evacuation center card
- System draws route from your location to center
- Shows distance in kilometers
- Green dashed line indicates path

### 4. **Facility Information**
- Medical facilities
- Food availability
- Water supply
- Shelter capacity

---

## 🚀 HOW TO USE

### Step 1: Open User Dashboard
```
Open: frontend/user.html in browser
```

### Step 2: Find Evacuation Centers

1. **Scroll to "🏥 Evacuation Centers" section** (in sidebar)
2. **Enter your city** (e.g., "Chennai", "Coimbatore")
3. **Click "Find" button**
4. **Allow location access** (optional but recommended)

### Step 3: View Results

You'll see:
- Number of centers found
- List of evacuation centers with:
  - Name
  - Capacity (number of people)
  - Distance from you (if location enabled)
  - Available facilities (Medical, Food, Water, Shelter)

### Step 4: See Route

1. **Click on any evacuation center card**
2. **Map automatically shows**:
   - Your location (blue marker)
   - Selected center (green marker)
   - Route between them (green dashed line)
3. **Distance displayed** in toast notification

---

## 📊 EXAMPLE USAGE

### Scenario: Flood in Chennai

**User Action**:
1. Opens user dashboard
2. Enters "Chennai" in evacuation center search
3. Clicks "Find"
4. Allows location access

**System Response**:
```
🏥 Found 2 evacuation center(s) in Chennai

1. Chennai Central Relief Camp
   Capacity: 500 people
   📍 2.3 km away
   [Medical] [Food] [Water]

2. Anna Nagar Community Center
   Capacity: 300 people
   📍 4.1 km away
   [Food] [Water] [Shelter]
```

**User clicks on "Chennai Central Relief Camp"**:
- Map zooms to show route
- Green dashed line from user to center
- Toast: "📍 Route to Chennai Central Relief Camp (2.3 km)"

---

## 🗺️ MAP FEATURES

### Markers:
- **Blue Dot** = Your current location
- **Green Numbered Circles** = Evacuation centers (1, 2, 3...)
- **Green Dashed Line** = Route to selected center

### Interactions:
- **Click marker** = See center details in popup
- **Click center card** = Draw route on map
- **Map auto-zooms** = Shows all centers or selected route

---

## 📍 AVAILABLE EVACUATION CENTERS

### Chennai (2 centers):
1. **Chennai Central Relief Camp**
   - Capacity: 500
   - Facilities: Medical, Food, Water

2. **Anna Nagar Community Center**
   - Capacity: 300
   - Facilities: Food, Water, Shelter

### Coimbatore (1 center):
1. **Coimbatore District Stadium**
   - Capacity: 800
   - Facilities: Medical, Food, Water, Shelter

### Madurai (1 center):
1. **Madurai Corporation Hall**
   - Capacity: 400
   - Facilities: Food, Water

### Salem (1 center):
1. **Salem Relief Center**
   - Capacity: 350
   - Facilities: Medical, Food, Water

### Trichy (1 center):
1. **Trichy Emergency Shelter**
   - Capacity: 450
   - Facilities: Medical, Food, Water, Shelter

### Tirunelveli (1 center):
1. **Tirunelveli District Center**
   - Capacity: 300
   - Facilities: Food, Water

### Vellore (1 center):
1. **Vellore Relief Camp**
   - Capacity: 250
   - Facilities: Medical, Food

---

## 🔧 TECHNICAL DETAILS

### Backend Endpoint:
```
GET /evacuation-centers?city=<city>&lat=<lat>&lng=<lng>
```

**Parameters**:
- `city` (required): City name
- `lat` (optional): User latitude
- `lng` (optional): User longitude

**Response**:
```json
{
  "city": "Chennai",
  "total_centers": 2,
  "centers": [
    {
      "name": "Chennai Central Relief Camp",
      "city": "Chennai",
      "lat": 13.0878,
      "lng": 80.2785,
      "capacity": 500,
      "facilities": ["Medical", "Food", "Water"],
      "distance_km": 2.3
    }
  ],
  "timestamp": "2024-01-15 14:30:00"
}
```

### Frontend Functions:
- `findEvacuationCenters()` - Search centers
- `loadEvacuationCenters()` - Fetch from API
- `displayEvacuationCentersOnMap()` - Show markers
- `showEvacuationRoute()` - Draw route line

---

## 🎨 UI ELEMENTS

### Evacuation Center Card:
```
┌─────────────────────────────────┐
│ 🏥 Chennai Central Relief Camp  │
│ Capacity: 500 people            │
│ 📍 2.3 km away                  │
│ [Medical] [Food] [Water]        │
└─────────────────────────────────┘
```

### Map Display:
```
     🗺️ Map
┌─────────────────────┐
│   ●1 (Center 1)     │
│    \                │
│     \               │
│      ● (You)        │
│                     │
│   ●2 (Center 2)     │
└─────────────────────┘
```

---

## 🔐 PRIVACY & PERMISSIONS

### Location Access:
- **Optional** - System works without location
- **Used for**: Distance calculation and route display
- **Not stored**: Location data not saved on server
- **Browser-based**: Uses HTML5 Geolocation API

### Without Location:
- Centers still displayed
- No distance shown
- No route drawing
- Can still view center details

---

## 🐛 TROUBLESHOOTING

### Issue 1: "No evacuation centers found"

**Cause**: City not in database or wrong spelling

**Solution**:
- Check city spelling (e.g., "Chennai" not "Chenai")
- Try nearby cities
- Available cities: Chennai, Coimbatore, Madurai, Salem, Trichy, Tirunelveli, Vellore

### Issue 2: Location not working

**Cause**: Browser blocked location access

**Solution**:
1. Click lock icon in address bar
2. Allow location access
3. Refresh page
4. Try search again

### Issue 3: Route not showing

**Cause**: Location access denied

**Solution**:
- Enable location in browser settings
- Or view center on map without route
- Distance still shown if location was enabled once

### Issue 4: Map not loading

**Cause**: Leaflet library not loaded

**Solution**:
- Check internet connection
- Refresh page
- Check browser console for errors

---

## 💡 PRO TIPS

1. **Enable location** for best experience
2. **Search before disaster** to know nearest centers
3. **Save center addresses** offline
4. **Check facilities** before heading out
5. **Choose nearest center** with required facilities

---

## 🚀 FUTURE ENHANCEMENTS

Planned features:
- [ ] Real-time center availability status
- [ ] Turn-by-turn navigation
- [ ] Traffic-aware routing
- [ ] Center contact numbers
- [ ] Booking/reservation system
- [ ] Real-time occupancy updates
- [ ] Multiple route options
- [ ] Offline map support

---

## 📞 EMERGENCY CONTACTS

If evacuation centers are full:
- **Disaster Helpline**: 1078
- **Ambulance**: 108
- **Police**: 100
- **Fire**: 101

---

## ✅ TESTING CHECKLIST

- [ ] Search for "Chennai" - Shows 2 centers
- [ ] Allow location - Shows distances
- [ ] Click center card - Route appears on map
- [ ] Deny location - Still shows centers (no distance)
- [ ] Click map marker - Popup shows details
- [ ] Search invalid city - Shows error
- [ ] Multiple searches - Previous results cleared

---

## 📊 SUCCESS METRICS

Feature is working when:
- ✅ Search returns evacuation centers
- ✅ Centers displayed on map with markers
- ✅ Distance calculated (if location enabled)
- ✅ Route drawn on map when center clicked
- ✅ Facilities shown for each center
- ✅ Map auto-zooms to show route

---

**Your users can now find safe evacuation centers during disasters! 🏥🗺️**
