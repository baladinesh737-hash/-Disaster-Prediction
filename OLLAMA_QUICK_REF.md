# 🚀 OLLAMA QUICK REFERENCE CARD

## ⚡ ESSENTIAL COMMANDS

### Check if Ollama is Running
```bash
curl http://localhost:11434/api/version
```

### Start Ollama
```bash
ollama serve
```

### List Installed Models
```bash
ollama list
```

### Install Model
```bash
ollama pull llama3.2
```

### Test Model Directly
```bash
ollama run llama3.2 "What is flood safety?"
```

---

## 🧪 TEST YOUR SETUP

### Quick Test (30 seconds)
```bash
cd "d:\freshthon project\backend"
python test_ollama.py
```

**Expected**: ✅ ALL TESTS PASSED

---

## 🎯 CONFIGURATION

### File: `backend/app.py` (line ~320)

```python
# Change model
"model": "llama3.2"

# Adjust response length
"max_tokens": 150

# Adjust creativity
"temperature": 0.7
```

---

## 🔧 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Connection refused | `ollama serve` |
| Model not found | `ollama pull llama3.2` |
| Slow responses | Use `phi3` model |
| Backend error | Check `python app.py` logs |

---

## 📊 MODEL COMPARISON

| Model | Speed | Quality | Size |
|-------|-------|---------|------|
| phi3 | ⚡⚡⚡ | ⭐⭐⭐ | 2GB |
| llama3.2 | ⚡⚡ | ⭐⭐⭐⭐ | 4GB |
| llama3.1 | ⚡ | ⭐⭐⭐⭐⭐ | 8GB |

**Recommended**: llama3.2 (best balance)

---

## 🎮 USAGE

### In Admin Dashboard:
1. Click 🤖 (bottom-right)
2. Type your question
3. Press Enter
4. Get AI response!

### Example Queries:
- "flood safety tips"
- "cyclone preparedness"
- "evacuation procedures"
- "emergency contacts"

---

## ✅ SUCCESS CHECK

**Ollama Working** if:
- ✅ Response in 2-5 seconds
- ✅ Natural language (not emoji-prefixed)
- ✅ Backend logs: `"source": "ollama"`

**Fallback Active** if:
- ⚠️ Instant response (<1 sec)
- ⚠️ Emoji-prefixed responses
- ⚠️ Backend logs: `"source": "fallback"`

---

## 🔗 QUICK LINKS

- **Ollama Docs**: https://ollama.ai/docs
- **Model Library**: https://ollama.ai/library
- **Setup Guide**: `OLLAMA_SETUP.md`
- **Integration Guide**: `OLLAMA_INTEGRATION.md`

---

## 📞 EMERGENCY COMMANDS

### Restart Everything:
```bash
# Stop Ollama (Ctrl+C in terminal)
# Restart
ollama serve

# Restart backend
cd backend
python app.py
```

### Reset Model:
```bash
ollama rm llama3.2
ollama pull llama3.2
```

### Check Logs:
```bash
# Backend logs (in terminal running app.py)
# Look for: [OLLAMA ERROR] or [OLLAMA SUCCESS]
```

---

## 💡 PRO TIPS

1. Keep Ollama running in background
2. Use llama3.2 for best results
3. Test with `test_ollama.py` first
4. Check backend logs if issues
5. Fallback always works as backup

---

**Print this card and keep it handy! 📋**
