# 🚀 STARTUP INSTRUCTIONS

## ✅ Your System Status:

Based on your test results:
- ✅ Ollama is running (version 0.20.5)
- ✅ Models installed: `mistral:latest` and `llama3:latest`
- ✅ AI generation working
- ⚠️ Backend needs to be started

---

## 🎯 START YOUR SYSTEM (3 Steps)

### Step 1: Ollama is Already Running ✅

You're good! Ollama is running on port 11434.

**If you need to restart it later:**
```bash
ollama serve
```

---

### Step 2: Start Backend

**Option A - Using Batch File (Easiest)**:
```bash
# Double-click this file:
START_BACKEND.bat
```

**Option B - Manual**:
```bash
cd "d:\freshthon project\backend"
python app.py
```

**Expected Output**:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

**Keep this terminal open!** Backend must stay running.

---

### Step 3: Open Admin Panel

1. Open your browser
2. Navigate to: `d:\freshthon project\frontend\admin.html`
3. Login with password: `admin123`
4. Click 🤖 icon (bottom-right)
5. Test chatbot!

---

## 🧪 TEST YOUR SETUP

### Quick Test:
```bash
# Double-click this file:
RUN_TESTS.bat
```

### Manual Test:

**Terminal 1** (Ollama - already running ✅):
```bash
ollama serve
```

**Terminal 2** (Backend):
```bash
cd "d:\freshthon project\backend"
python app.py
```

**Terminal 3** (Test):
```bash
cd "d:\freshthon project\backend"
python test_ollama.py
```

**Expected**: ✅ ALL TESTS PASSED

---

## 💬 TEST CHATBOT

### In Admin Dashboard:

1. Click robot icon 🤖 (bottom-right)
2. Type: **"What should people do during a cyclone?"**
3. Press Enter

**Expected Response** (from Mistral AI):
```
During a cyclone, people should:
1. Stay indoors away from windows
2. Secure loose objects outside
3. Keep emergency supplies ready
4. Follow official evacuation orders
5. Monitor weather updates
```

### More Test Queries:

- "flood safety tips"
- "evacuation procedures"
- "emergency contacts in India"
- "how to prepare for disasters"

---

## 🔧 YOUR CONFIGURATION

### Current Setup:
- **Model**: `mistral:latest` (4.07 GB)
- **Alternative**: `llama3:latest` (4.34 GB)
- **Response Length**: 150 tokens
- **Temperature**: 0.7 (balanced)

### To Switch Models:

Edit `backend/app.py` (line ~320):

```python
# Change from mistral to llama3
"model": "mistral:latest"  # Current
# to
"model": "llama3:latest"   # Alternative
```

Then restart backend.

---

## 📊 EXPECTED BEHAVIOR

### When Chatbot Works (Ollama Connected):
- ✅ Response time: 2-5 seconds
- ✅ Natural language responses
- ✅ Contextual understanding
- ✅ Backend logs show: `"source": "ollama"`

### When Fallback Active (Ollama Down):
- ⚠️ Response time: <1 second
- ⚠️ Emoji-prefixed responses
- ⚠️ Rule-based answers
- ⚠️ Backend logs show: `"source": "fallback"`

---

## 🐛 TROUBLESHOOTING

### Backend Won't Start?

**Check Python version**:
```bash
python --version
```
Should be Python 3.8+

**Install dependencies**:
```bash
cd "d:\freshthon project\backend"
pip install -r requirements.txt
```

### Chatbot Not Responding?

**Check backend logs** (in terminal running app.py):
```
[OLLAMA ERROR] Connection refused  → Ollama not running
[OLLAMA ERROR] Model not found     → Wrong model name
```

**Fix**:
1. Verify Ollama running: `curl http://localhost:11434/api/version`
2. Check model name in `app.py` matches installed model
3. Restart backend

### Slow Responses?

**Switch to faster model**:
```python
# In app.py, change to:
"model": "mistral:latest"  # Faster than llama3
```

Or reduce response length:
```python
"max_tokens": 100  # Shorter responses
```

---

## 🎯 COMPLETE WORKFLOW

### Daily Startup:

1. **Ollama** (if not running):
   ```bash
   ollama serve
   ```

2. **Backend**:
   ```bash
   # Double-click:
   START_BACKEND.bat
   ```

3. **Open Browser**:
   - Navigate to `frontend/admin.html`
   - Login: `admin123`

4. **Use System**:
   - Place markers
   - Run AI analysis
   - Send alerts
   - Chat with AI

### Shutdown:

1. Close browser
2. Press `Ctrl+C` in backend terminal
3. Press `Ctrl+C` in Ollama terminal (optional - can keep running)

---

## ✅ SUCCESS CHECKLIST

After starting, verify:

- [ ] Ollama running (check with `curl http://localhost:11434/api/version`)
- [ ] Backend running (check with `curl http://127.0.0.1:5000/api`)
- [ ] Admin panel opens in browser
- [ ] Login works with `admin123`
- [ ] Map loads empty
- [ ] Chatbot icon visible (🤖)
- [ ] Chatbot responds to queries
- [ ] Responses are intelligent (not emoji-prefixed)

---

## 🎉 YOU'RE READY!

Your system is configured and ready to use!

**Next Steps**:
1. Start backend: `START_BACKEND.bat`
2. Open admin panel: `frontend/admin.html`
3. Test chatbot with disaster queries
4. Explore all features!

---

## 📞 QUICK COMMANDS

```bash
# Check Ollama
curl http://localhost:11434/api/version

# Check Backend
curl http://127.0.0.1:5000/api

# List Models
ollama list

# Test Everything
RUN_TESTS.bat

# Start Backend
START_BACKEND.bat
```

---

**Your disaster management system with AI is ready to go! 🚀🤖**
