"""
Ollama Connection Test Script
Tests if Ollama is running and configured correctly
"""

import requests
import json

def test_ollama_connection():
    """Test if Ollama is running on localhost:11434"""
    print("=" * 60)
    print(" OLLAMA CONNECTION TEST")
    print("=" * 60)
    
    # Test 1: Check Ollama version
    print("\n[TEST 1] Checking Ollama service...")
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        if response.status_code == 200:
            version = response.json().get("version", "unknown")
            print(f" Ollama is running (version: {version})")
        else:
            print(f" Ollama responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Ollama is NOT running on port 11434")
        print("   → Start Ollama: ollama serve")
        return False
    except Exception as e:
        print(f" Error: {e}")
        return False
    
    # Test 2: List available models
    print("\n[TEST 2] Checking available models...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print(f" Found {len(models)} model(s):")
                for model in models:
                    name = model.get("name", "unknown")
                    size = model.get("size", 0) / (1024**3)  # Convert to GB
                    print(f"   - {name} ({size:.2f} GB)")
            else:
                print("  No models installed")
                print("   → Install model: ollama pull llama3.2")
                return False
        else:
            print(f" Failed to list models: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 3: Test generation with first available model
    print("\n[TEST 3] Testing AI generation...")
    try:
        test_model = models[0].get("name") if models else "llama3.2"
        print(f"   Using model: {test_model}")
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": test_model,
                "prompt": "What is flood safety? Answer in one sentence.",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 50
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get("response", "").strip()
            if ai_response:
                print(f"✅ AI Response: {ai_response[:100]}...")
            else:
                print("⚠️  Empty response from AI")
                return False
        else:
            print(f"❌ Generation failed: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out (>30 seconds)")
        print("   → Try a smaller model or increase timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 4: Test backend integration
    print("\n[TEST 4] Testing backend /ai-chat endpoint...")
    try:
        response = requests.post(
            "http://127.0.0.1:5000/ai-chat",
            json={"query": "flood safety tips"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            chat_response = result.get("response", "")
            source = result.get("source", "unknown")
            
            if source == "ollama":
                print(f"✅ Backend connected to Ollama")
                print(f"   Response: {chat_response[:100]}...")
            elif source == "fallback":
                print("⚠️  Backend using fallback (rule-based)")
                print("   → Check backend logs for errors")
            else:
                print(f"⚠️  Unknown source: {source}")
        else:
            print(f"❌ Backend error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is NOT running on port 5000")
        print("   → Start backend: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - Ollama is ready!")
    print("=" * 60)
    return True


def print_recommendations():
    """Print configuration recommendations"""
    print("\n📋 CONFIGURATION RECOMMENDATIONS:")
    print("-" * 60)
    print("1. Model Selection:")
    print("   - Fast: phi3 (1-2 sec)")
    print("   - Balanced: llama3.2 (2-4 sec) ← RECOMMENDED")
    print("   - Best: llama3.1 (4-8 sec)")
    print()
    print("2. Response Settings (in app.py):")
    print("   - Short: max_tokens=100")
    print("   - Medium: max_tokens=150 ← CURRENT")
    print("   - Long: max_tokens=300")
    print()
    print("3. Temperature:")
    print("   - Factual: 0.3")
    print("   - Balanced: 0.7 ← CURRENT")
    print("   - Creative: 0.9")
    print("-" * 60)


def print_troubleshooting():
    """Print troubleshooting guide"""
    print("\n🔧 TROUBLESHOOTING:")
    print("-" * 60)
    print("If Ollama not running:")
    print("  → ollama serve")
    print()
    print("If model not found:")
    print("  → ollama pull llama3.2")
    print()
    print("If backend not running:")
    print("  → cd backend")
    print("  → python app.py")
    print()
    print("Check Ollama logs:")
    print("  → Check terminal where 'ollama serve' is running")
    print()
    print("Test Ollama directly:")
    print("  → ollama run llama3.2 'What is flood safety?'")
    print("-" * 60)


if __name__ == "__main__":
    success = test_ollama_connection()
    
    if success:
        print_recommendations()
    else:
        print_troubleshooting()
    
    print("\n💡 TIP: Run this script anytime to verify Ollama setup")
    print("   → python test_ollama.py\n")
