"""
Quick test script to verify login endpoint
"""
import requests
import json

API = "http://127.0.0.1:5000"

def test_login(role, password):
    print(f"\n[TEST] Testing {role} login with password: {password}")
    
    response = requests.post(
        f"{API}/role-login",
        json={"role": role, "password": password},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"[TEST] Status Code: {response.status_code}")
    print(f"[TEST] Response: {response.json()}")
    return response.json()

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING LOGIN SYSTEM")
    print("=" * 60)
    
    # Test admin login
    test_login("admin", "admin123")
    
    # Test rescue login
    test_login("rescue", "rescue123")
    
    # Test government login
    test_login("government", "gov123")
    
    # Test wrong password
    test_login("admin", "wrongpass")
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60)
