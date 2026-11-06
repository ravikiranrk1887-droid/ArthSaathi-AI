"""
tests/test_finbot.py
====================
Comprehensive automated test suite for ArthSaathi AI:
  1. Financial Calculators (EMI, FD, SIP, RD, Compound Interest, Inflation, Prepayment)
  2. Edge Cases (Zero-interest, invalid/negative values)
  3. Bank Comparison API & Filters
  4. Personal Finance Manager CRUD (Income, Expense, Budget)
  5. Learning Progress & Quiz Grading
  6. AI Service (Intelligent Fallback Engine & Context)
"""

import unittest
import json
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.services import calculator_service, ai_service, bank_service


class TestArthSaathi(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    # -------------------------------------------------------------------------
    # 1. CALCULATOR TESTS
    # -------------------------------------------------------------------------
    def test_emi_calculation(self):
        """Test standard EMI calculation: ₹10,00,000 at 8.5% for 10 years (120 months)"""
        res = calculator_service.calculate_emi(1_000_000, 8.5, 120)
        self.assertIn("emi", res)
        self.assertIn("total_interest", res)
        self.assertIn("total_payment", res)
        # Expected EMI is approx ₹12,398.57
        self.assertAlmostEqual(res["emi"], 12398.57, delta=1.0)
        self.assertTrue(len(res["amortization"]) == 120)

    def test_emi_zero_interest(self):
        """Test zero-interest loan edge case"""
        res = calculator_service.calculate_emi(120_000, 0.0, 12)
        self.assertEqual(res["emi"], 10_000.0)
        self.assertEqual(res["total_interest"], 0.0)
        self.assertEqual(res["total_payment"], 120_000.0)

    def test_emi_invalid_inputs(self):
        """Test negative or zero principal error handling"""
        with self.assertRaises(ValueError):
            calculator_service.calculate_emi(-50000, 8.5, 120)
        with self.assertRaises(ValueError):
            calculator_service.calculate_emi(50000, -8.5, 120)
        with self.assertRaises(ValueError):
            calculator_service.calculate_emi(50000, 8.5, 0)

    def test_fd_calculation(self):
        """Test FD calculation: ₹1,00,000 at 7% for 2 years compounded quarterly"""
        res = calculator_service.calculate_fd(100_000, 7.0, 2.0, 4)
        self.assertAlmostEqual(res["maturity"], 114888.18, delta=1.0)
        self.assertAlmostEqual(res["interest"], 14888.18, delta=1.0)

    def test_sip_calculation(self):
        """Test SIP calculation: ₹5,000/month at 12% for 15 years"""
        res = calculator_service.calculate_sip(5_000, 12.0, 15)
        self.assertEqual(res["invested"], 900_000.0)
        self.assertGreater(res["final_value"], 2_500_000.0)
        self.assertAlmostEqual(res["gains"], res["final_value"] - res["invested"], delta=0.1)

    def test_rd_calculation(self):
        """Test RD calculation: ₹5,000/month at 7% for 24 months"""
        res = calculator_service.calculate_rd(5_000, 7.0, 24)
        self.assertEqual(res["total_deposited"], 120_000.0)
        self.assertGreater(res["interest"], 8_000.0)
        self.assertEqual(res["maturity"], res["total_deposited"] + res["interest"])

    def test_compound_interest(self):
        """Test Compound interest: ₹1,00,000 at 8% for 5 years compounded annually"""
        res = calculator_service.calculate_compound_interest(100_000, 8.0, 5, 1)
        self.assertAlmostEqual(res["amount"], 146932.81, delta=1.0)

    def test_inflation_calculator(self):
        """Test Inflation: ₹1,00,000 at 6% for 10 years"""
        res = calculator_service.calculate_inflation(100_000, 6.0, 10)
        self.assertAlmostEqual(res["future_cost"], 179084.77, delta=1.0)
        self.assertAlmostEqual(res["purchasing_power"], 55839.48, delta=1.0)

    def test_loan_prepayment(self):
        """Test Prepayment savings"""
        res = calculator_service.calculate_loan_prepayment(
            principal=3_000_000,
            annual_rate=8.5,
            remaining_months=240,
            extra_monthly=3000,
            lump_sum=100000
        )
        self.assertGreater(res["interest_saved"], 500_000.0)
        self.assertGreater(res["months_saved"], 40)

    # -------------------------------------------------------------------------
    # 2. BANK COMPARISON API TESTS
    # -------------------------------------------------------------------------
    def test_api_banks_list(self):
        """Test fetching list of banks"""
        resp = self.client.get("/banks/api/banks/list")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data["success"])
        self.assertGreaterEqual(len(data["data"]), 10)

    def test_api_bank_compare_home_loan(self):
        """Test comparing banks for HOME_LOAN"""
        resp = self.client.get("/banks/api/banks/compare?product_type=HOME_LOAN")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data["success"])
        self.assertGreaterEqual(len(data["data"]), 10)
        first_row = data["data"][0]
        self.assertIn("bank_name", first_row)
        self.assertIn("rate_min", first_row)
        self.assertTrue(first_row["is_demo_data"])

    def test_api_bank_compare_invalid_type(self):
        """Test bank comparison with invalid product type"""
        resp = self.client.get("/banks/api/banks/compare?product_type=INVALID_PRODUCT")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(len(data["data"]), 0)

    # -------------------------------------------------------------------------
    # 3. PERSONAL FINANCE MANAGER CRUD TESTS
    # -------------------------------------------------------------------------
    def test_income_crud(self):
        """Test adding, fetching, and deleting income records"""
        # Add income
        resp = self.client.post("/finance/api/finance/income", json={
            "amount": 75000,
            "source": "Salary",
            "date": "2024-11-01",
            "description": "Monthly Paycheck"
        })
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertTrue(data["success"])
        rec_id = data["data"]["id"]

        # Fetch incomes
        get_resp = self.client.get("/finance/api/finance/income")
        self.assertEqual(get_resp.status_code, 200)
        incomes = json.loads(get_resp.data)["data"]
        self.assertTrue(any(i["id"] == rec_id for i in incomes))

        # Delete income
        del_resp = self.client.delete(f"/finance/api/finance/income/{rec_id}")
        self.assertEqual(del_resp.status_code, 200)

    def test_expense_crud(self):
        """Test adding, fetching, and deleting expense records"""
        # Add expense
        resp = self.client.post("/finance/api/finance/expense", json={
            "amount": 2500,
            "category": "FOOD",
            "date": "2024-11-01",
            "description": "Grocery shopping"
        })
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertTrue(data["success"])
        rec_id = data["data"]["id"]

        # Fetch expenses
        get_resp = self.client.get("/finance/api/finance/expense")
        self.assertEqual(get_resp.status_code, 200)

        # Delete expense
        del_resp = self.client.delete(f"/finance/api/finance/expense/{rec_id}")
        self.assertEqual(del_resp.status_code, 200)

    # -------------------------------------------------------------------------
    # 4. LEARNING PROGRESS & QUIZ GRADING TESTS
    # -------------------------------------------------------------------------
    def test_quiz_grading(self):
        """Test submitting quiz answers and receiving feedback"""
        from app.models.lesson import Lesson
        lesson = Lesson.query.first()
        self.assertIsNotNone(lesson)

        questions = lesson.quiz_questions.all()
        if questions:
            answers = [q.correct_index for q in questions]
            resp = self.client.post("/learning/api/learning/quiz", json={
                "lesson_id": lesson.id,
                "answers": answers
            })
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.data)
            self.assertTrue(data["success"])
            self.assertEqual(data["data"]["score"], len(questions))
            self.assertEqual(data["data"]["percentage"], 100.0)

    # -------------------------------------------------------------------------
    # 5. AI CHATBOT INTEGRATION & FALLBACK TESTS
    # -------------------------------------------------------------------------
    def test_ai_chatbot_fallback_sip(self):
        """Test AI chatbot fallback answering for SIP question"""
        resp = self.client.post("/chatbot/api/chat", json={
            "message": "Explain SIP with a ₹1,000 example"
        })
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data["success"])
        self.assertIn("SIP", data["response"])
        self.assertIn("1,000", data["response"])

    def test_ai_chatbot_fallback_emi(self):
        """Test AI chatbot answering missed EMI question"""
        resp = self.client.post("/chatbot/api/chat", json={
            "message": "What happens if I miss my EMI?"
        })
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data["success"])
        self.assertIn("CIBIL", data["response"])


if __name__ == "__main__":
    unittest.main()
