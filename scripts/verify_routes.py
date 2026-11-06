"""
scripts/verify_routes.py
========================
Verifies that all 12 major pages and endpoints in ArthSaathi AI return HTTP 200 OK.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()
client = app.test_client()

ROUTES_TO_TEST = [
    ("/", "Landing Page"),
    ("/dashboard", "Dashboard"),
    ("/education/", "Education Hub"),
    ("/education/BANKING", "Category: Banking"),
    ("/education/lesson/what-is-a-bank-how-it-works", "Lesson Detail"),
    ("/investments/", "Investment Centre"),
    ("/calculators/", "Calculators Suite"),
    ("/banks/", "Banks Directory"),
    ("/banks/compare", "Bank Comparison Engine"),
    ("/chatbot/", "AI Chatbot Assistant"),
    ("/finance/", "Personal Finance Manager"),
    ("/learning/", "Learning Progress"),
]

print("=== VERIFYING ALL MAJOR ROUTES ===")
all_pass = True
for url, name in ROUTES_TO_TEST:
    res = client.get(url)
    status = res.status_code
    if status == 200:
        print(f" [PASS] {status} - {name} ({url})")
    else:
        print(f" [FAIL] {status} - {name} ({url})")
        all_pass = False

if all_pass:
    print("\n All 12 routes verified successfully with HTTP 200 OK!")
else:
    print("\n Some routes encountered errors.")
    sys.exit(1)
