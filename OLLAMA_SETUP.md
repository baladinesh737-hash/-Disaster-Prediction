# 🤖 OLLAMA AI INTEGRATION GUIDE

## ✅ What Was Changed

The chatbot now connects to your **local Ollama AI** instead of using rule-based responses.

### Backend Changes:
- **File**: `backend/app.py`
- **Endpoint**: `/ai-chat`
- **Connection**: `http://localhost:11434/api/generate`
- **Fallback**: Rule-based responses if Ollama is unavailable

---

## 🚀 SETUP INSTRUCTIONS

### Step 1: Verify Ollama is Running

Check if Ollama is already running on your laptop:

```bash
# Test Ollama connection
curl http://localhost:11434/api/version
```

**Expected Response**:
```json
{"version":"0.1.x"}
```

If you get a response, Ollama is running! ✅

---

### Step 2: Check Available Models

```bash
# List installed models
ollama list
```

**Common Models**:
- `llama3.2` (recommended - fast & accurate)
- `llama3.1`
- `llama2`
- `mistral`
- `phi3`

---

### Step 3: Configure Model in Backend

Edit `backend/app.py` line ~320:

```python
# Change this to your installed model
"model": "llama3.2",  # ← Change to your model name
```

**Available Options**:
```python
"model": "llama3.2"     # Fast, accurate (recommended)
"model": "llama3.1"     # Larger, more capable
"model": "mistral"      # Alternative option
"model": "phi3"         # Lightweight
```

---

### Step 4: Test Connection

1. **Start Backend**:
```bash
cd "d:\freshthon project\backend"
python app.py
```

2. **Test API Directly**:
```bash
curl -X POST http://127.0.0.1:5000/ai-chat \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"flood safety tips\"}"
```

**Expected Response**:
```json
{
  "response": "During floods, move to higher ground immediately...",
  "timestamp": "2024-01-15 14:30:00",
  "source": "ollama"
}
```

If `"source": "ollama"` appears, connection successful! ✅

---

## 🎯 USAGE

### In Admin Dashboard:

1. Click robot icon (🤖) at bottom-right
2. Type your question:
   - "What should people do during a cyclone?"
   - "How to prepare for floods?"
   - "Evacuation procedures for coastal areas"
3. Press Enter
4. Get AI-powered response from Ollama

### Example Queries:

**Disaster Safety**:
```
"flood safety tips"
"cyclone preparedness checklist"
"earthquake emergency procedures"
```

**Impact Assessment**:
```
"what is the impact of heavy rainfall?"
"how does wind speed affect buildings?"
"landslide risk factors"
```

**Evacuation**:
```
"evacuation route planning"
"what to carry during evacuation?"
"safe zones during disasters"
```

---

## ⚙️ CONFIGURATION OPTIONS

### Adjust Response Length

Edit `backend/app.py`:

```python
"options": {
    "temperature": 0.7,      # Creativity (0.0-1.0)
    "max_tokens": 150        # Response length
}
```

**Recommendations**:
- **Short responses**: `max_tokens: 100`
- **Medium responses**: `max_tokens: 150` (default)
- **Detailed responses**: `max_tokens: 300`

### Adjust Temperature

```python
"temperature": 0.3   # More focused, factual
"temperature": 0.7   # Balanced (default)
"temperature": 0.9   # More creative
```

---

## 🔧 TROUBLESHOOTING

### Issue 1: "Connection Error"

**Symptom**: Chatbot shows fallback responses

**Solution**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If not running, start Ollama
ollama serve
```

### Issue 2: "Model Not Found"

**Symptom**: Error in backend logs

**Solution**:
```bash
# Pull the model
ollama pull llama3.2

# Verify installation
ollama list
```

### Issue 3: Slow Responses

**Symptom**: Chatbot takes >10 seconds

**Solutions**:
1. Use smaller model: `phi3` or `mistral`
2. Reduce max_tokens: `100` instead of `150`
3. Check system resources (RAM/CPU)

### Issue 4: Ollama Port Conflict

**Symptom**: Ollama not on port 11434

**Solution**:
```python
# Change port in app.py
ollama_url = "http://localhost:YOUR_PORT/api/generate"
```

---

## 🎨 CUSTOMIZATION

### Custom System Prompt

Edit the system prompt in `app.py` to change AI behavior:

```python
system_prompt = """You are a disaster management AI assistant for NDMA India.

Provide SHORT, ACTIONABLE responses (2-3 sentences) about:
- Flood, cyclone, earthquake safety
- Emergency evacuation procedures
- Indian disaster helpline numbers (108, 1078)
- Relief camp locations
- Government disaster protocols

Use simple language. Focus on immediate actions.
Include relevant Indian emergency contacts."""
```

### Add Context Awareness

Make AI aware of current alerts:

```python
# Get recent alerts
recent_alerts = alerts_store[-3:] if alerts_store else []
alert_context = f"Recent alerts: {[a['city'] for a in recent_alerts]}"

full_prompt = f"{system_prompt}\n\n{alert_context}\n\nUser: {query}\n\nAssistant:"
```

---

## 📊 PERFORMANCE METRICS

### Response Times (Typical):

| Model | Response Time | Quality |
|-------|--------------|---------|
| phi3 | 1-2 seconds | Good |
| llama3.2 | 2-4 seconds | Excellent |
| llama3.1 | 4-8 seconds | Best |
| mistral | 2-5 seconds | Very Good |

### System Requirements:

- **RAM**: 8GB minimum (16GB recommended)
- **CPU**: 4 cores minimum
- **Disk**: 5GB for model storage

---

## 🔄 FALLBACK SYSTEM

If Ollama is unavailable, the system automatically uses **rule-based responses**:

```python
def fallback_ai_response(query):
    # Predefined responses for common queries
    if "flood" in query:
        return "Flood Safety: Move to higher ground..."
```

**Fallback Triggers**:
- Ollama not running
- Connection timeout (>30 seconds)
- Model not found
- API error

**User Experience**:
- Seamless fallback (no error shown)
- Response marked with `"source": "fallback"`
- Still provides helpful information

---

## 🚀 ADVANCED FEATURES

### 1. Streaming Responses (Future)

```python
"stream": True  # Enable real-time streaming
```

### 2. Multi-Model Support

```python
# Try multiple models in order
models = ["llama3.2", "mistral", "phi3"]
for model in models:
    try:
        response = call_ollama(model, query)
        break
    except:
        continue
```

### 3. Context Memory

```python
# Store conversation history
conversation_history = []
conversation_history.append({"role": "user", "content": query})
conversation_history.append({"role": "assistant", "content": response})
```

---

## 📝 TESTING CHECKLIST

### Basic Tests:
- [ ] Ollama running on port 11434
- [ ] Model installed and listed
- [ ] Backend connects successfully
- [ ] Chatbot responds in <5 seconds
- [ ] Responses are relevant and helpful

### Advanced Tests:
- [ ] Fallback works when Ollama stopped
- [ ] Multiple rapid queries handled
- [ ] Long queries processed correctly
- [ ] Special characters handled
- [ ] Empty queries rejected

---

## 🎯 QUICK REFERENCE

### Start Ollama:
```bash
ollama serve
```

### Test Model:
```bash
ollama run llama3.2 "What is flood safety?"
```

### Check Logs:
```bash
# Backend logs show:
[OLLAMA ERROR] Connection refused  # Ollama not running
[OLLAMA ERROR] Model not found     # Wrong model name
```

### API Endpoint:
```
POST http://127.0.0.1:5000/ai-chat
Body: {"query": "your question"}
```

---

## 🔐 SECURITY NOTES

- Ollama runs **locally** - no data sent to cloud
- All queries processed on your laptop
- No API keys required
- Complete privacy

---

## 📞 SUPPORT

### If Ollama Not Installed:

1. **Download**: https://ollama.ai/download
2. **Install**: Run installer for Windows
3. **Pull Model**: `ollama pull llama3.2`
4. **Start**: `ollama serve`

### If Issues Persist:

1. Check `backend/app.py` logs
2. Verify Ollama version: `ollama --version`
3. Test Ollama directly: `ollama run llama3.2`
4. Check firewall settings (port 11434)

---

## ✅ SUCCESS INDICATORS

You'll know it's working when:
- ✅ Chatbot responds in 2-5 seconds
- ✅ Responses are contextual and intelligent
- ✅ Backend logs show `"source": "ollama"`
- ✅ No "Connection Error" messages
- ✅ Responses vary (not rule-based)

---

**Status**: ✅ Ollama Integration Complete  
**Fallback**: ✅ Rule-based backup active  
**Privacy**: ✅ 100% local processing
