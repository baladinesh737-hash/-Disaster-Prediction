"""
Run this once to create a sample users.xlsx for testing.
Usage: python create_sample_users.py
"""
import pandas as pd

users = [
    {"name": "Ravi Kumar",    "phone": "919876543210", "city": "Chennai"},
    {"name": "Priya Devi",    "phone": "919876543211", "city": "Chennai"},
    {"name": "Arjun Raj",     "phone": "919629129027", "city": "Coimbatore"},
    {"name": "Meena Selvi",   "phone": "919876543213", "city": "Coimbatore"},
    {"name": "Karthik S",     "phone": "919876543214", "city": "Madurai"},
    {"name": "Lakshmi V",     "phone": "919876543215", "city": "Madurai"},
    {"name": "Suresh P",      "phone": "919876543216", "city": "Salem"},
    {"name": "Divya N",       "phone": "919876543217", "city": "Trichy"},
]

df = pd.DataFrame(users)
df.to_excel("users.xlsx", index=False)
print("✅ users.xlsx created with", len(users), "users")
print(df.to_string())
