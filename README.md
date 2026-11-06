# ArthSaathi AI — Learn Finance. Compare Banks. Make Smarter Decisions.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://arth-saathi-ai.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)

> 🌐 **Live Production Website:** **[https://arth-saathi-ai.vercel.app/](https://arth-saathi-ai.vercel.app/)**

ArthSaathi AI is an AI-powered financial literacy, banking comparison, and personal finance decision-support platform built specifically for Indian citizens — including students, working professionals, and families.

---

## 🌟 Key Highlights & Modules

### 1. Home Dashboard (Module 1)
- Overview command centre with personalized learning progress, quick metric cards, daily rotating financial tips, recently recommended lessons, available calculators, and latest bank rate verification status.

### 2. Financial Education Centre (Module 2)
- 15+ comprehensive structured lessons across 5 core categories:
  - **A. Banking Fundamentals:** Savings, Current, and Salary accounts, UPI, NEFT, RTGS, IMPS, simple vs compound interest, and inflation.
  - **B. Investment Education:** Savings vs investing, mutual funds, SIP compounding, equity vs debt vs index funds, PPF, and NPS.
  - **C. Loan Education:** Home loans (fixed vs floating), education loans with moratorium rules, CIBIL scores (300-900), and prepayment mathematics.
  - **D. Personal Financial Planning:** 50/30/20 monthly budgeting, emergency funds, and debt management.
  - **E. Indian Banking System:** RBI monetary policy (repo rates), public vs private banks, small finance banks, payment banks, and DICGC deposit insurance.
- **Strict 10-Part Lesson Architecture:** Definition, Plain English explanation, Real-world Indian example in ₹, Step-by-step mechanism, Advantages, Risks, Common mistakes, FAQs, Knowledge Quiz, and Related Calculator.

### 3. Financial Calculators (Module 3)
- 7 interactive mathematical calculators powered by pure Python/JS math (zero AI hallucinations):
  1. **Loan EMI Calculator:** Monthly EMI, total interest, total repayment, principal vs interest Chart.js doughnut, and year-by-year amortization table. Handles zero-interest loans.
  2. **Fixed Deposit (FD) Calculator:** Principal, interest, maturity with quarterly/monthly compounding.
  3. **SIP Mutual Fund Calculator:** Total invested, estimated gains, final corpus, and power of compounding breakdown.
  4. **Recurring Deposit (RD) Calculator:** Cumulative quarterly compounding formula standard in Indian banks.
  5. **Compound Interest Calculator:** Frequency selector (monthly, quarterly, semi-annual, annual).
  6. **Inflation Calculator:** Purchasing power erosion over time.
  7. **Loan Prepayment Calculator:** Months saved, interest saved, and before vs after comparison table.

### 4. Indian Bank Comparison Engine (Module 4)
- 10 Major Indian Banks: **State Bank of India (SBI), HDFC Bank, ICICI Bank, Axis Bank, Kotak Mahindra Bank, Bank of Baroda (BOB), Canara Bank, Punjab National Bank (PNB), Union Bank of India, and Indian Bank**.
- 7 Products: Home Loans, Education Loans, Personal Loans, Vehicle Loans, Business Loans (MSME), Fixed Deposits, and Savings Accounts.
- Interactive filtering by bank, product category, loan/deposit amount, tenure, and customer eligibility (Salaried, Self-employed, Women borrower discount, Senior citizen bonus).
- Complete side-by-side comparison cards and downloadable CSV comparison matrix with official bank website links.
- Clearly marked **DEMO DATA** badges and verification metadata.

### 5. Investment Centre (Module 5)
- Comprehensive guide to 14 Indian asset classes: Direct Stocks, Mutual Funds, SIP, Equity Funds, Debt Funds, Index Funds, ETFs, Corporate Bonds, Government Securities (G-Secs via RBI Retail Direct), Treasury Bills (T-Bills), PPF, NPS, Fixed Deposits, and Sovereign Gold Bonds (SGB).
- Each asset covers: definition, how it works, minimum investment, risk category, liquidity, tax considerations (80C, LTCG, STCG, slab rates), advantages, disadvantages, and important risks.
- Searchable and filterable comparison matrix.

### 6. AI Financial Assistant (ArthSaathi Assistant — Module 6)
- Powered by **Google Gemini API** with an intelligent system prompt for Indian banking and personal finance.
- **Intelligent Offline Knowledge Engine:** If no API key is provided, or if the API is unreachable, ArthSaathi automatically responds with rich, accurate, structured answers to common Indian finance questions.
- Pre-populated quick question pills, conversation history persistence in SQLite, markdown formatting, and copy message actions.

### 7. Personal Finance Manager (Module 7)
- Add, Edit, and Delete Income records.
- Add, Edit, and Delete Expense records across 9 Indian categories (Food, Rent, Bills, Transport, Education, Shopping, Healthcare, Entertainment, Other).
- Set Monthly Budget with live progress utilization bar (green < 70%, yellow 70-90%, red > 90%).
- Interactive Chart.js category-wise expense doughnut chart.
- Dynamic automated savings suggestions (50/30/20 check, emergency fund recommendation, food spend alerts).

### 8. Learning Progress & Quizzes (Module 8)
- Lesson completion tracking with restart capability.
- Instant quiz grading with correct/incorrect feedback and detailed explanations.
- Overall progress gauge and Dynamic Level Badges (**Beginner Level**, **Intermediate Investor**, **Advanced Financial Master**).
- Quiz history table with past attempts, scores, and retake buttons.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.12, Flask 3.1, Flask Blueprints, Jinja2 |
| **Database** | SQLite, SQLAlchemy 2.0 (14 tables with enums and foreign keys) |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5.3, Chart.js 4.4, Lucide Icons |
| **AI Integration** | Google Gemini API (gemini-1.5-flash) with fallback knowledge engine |
| **Mathematics** | Python `math`, `numpy`, `pandas` |

---

## 🚀 Quick Start Guide

### ⚡ Live Production URL
Access the deployed application instantly with zero setup:
👉 **[https://arth-saathi-ai.vercel.app/](https://arth-saathi-ai.vercel.app/)**

---

### Local Setup & Development

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Installation
```bash
# Clone or navigate to the directory
cd D:\Backend\finbot-ai

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory (or copy from `.env.example`):
```bash
copy .env.example .env
```
Edit `.env` (optional for AI features):
```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=finbot_secret_key_prod_2024
DATABASE_URL=sqlite:///finbot.db
DEBUG=True
```
*(Note: If you do not have a Gemini API key, ArthSaathi AI continues to run seamlessly using its built-in Intelligent Financial Knowledge Engine!)*

### 4. Initialize Database & Seed Data
```bash
python scripts/init_db.py
python scripts/seed_all_lessons.py
```

### 5. Run the Application
```bash
python run.py
```
Open your browser at: **`http://localhost:5000`**

---

## 🧪 Automated Testing

Run the automated test suite covering all calculators, edge cases, APIs, bank filters, finance manager CRUD, and quiz grading:

```bash
python -m unittest tests/test_finbot.py
```
All 17 tests will execute and verify the application logic.

---

## 📡 REST API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/calculators/api/calculate/emi` | POST | Calculate loan EMI and full amortization schedule |
| `/calculators/api/calculate/fd` | POST | Calculate Fixed Deposit maturity and interest |
| `/calculators/api/calculate/sip` | POST | Calculate Mutual Fund SIP future value and corpus |
| `/calculators/api/calculate/rd` | POST | Calculate Recurring Deposit maturity |
| `/calculators/api/calculate/compound` | POST | Generic compound interest calculation |
| `/calculators/api/calculate/inflation` | POST | Purchasing power erosion analysis |
| `/calculators/api/calculate/prepayment` | POST | Prepayment interest and tenure savings |
| `/banks/api/banks/list` | GET | List all 10 banks |
| `/banks/api/banks/compare` | GET | Compare interest rates and product features |
| `/investments/api/instruments` | GET | Filterable list of 14 investment asset classes |
| `/chatbot/api/chat` | POST | Send message to ArthSaathi AI assistant |
| `/chatbot/api/chat/history` | GET | Retrieve conversation history |
| `/finance/api/finance/income` | GET, POST | Fetch or add income records |
| `/finance/api/finance/income/<id>` | PUT, DELETE | Edit or delete income record |
| `/finance/api/finance/expense` | GET, POST | Fetch or add expense records |
| `/finance/api/finance/expense/<id>` | PUT, DELETE | Edit or delete expense record |
| `/finance/api/finance/budget` | GET, POST | Get or upsert monthly budget |
| `/learning/api/learning/progress` | GET, POST | Get or update lesson completion status |
| `/learning/api/learning/quiz` | POST | Submit quiz answers for grading |
| `/learning/api/learning/quiz-history` | GET | Retrieve past quiz scores |
| `/learning/api/learning/restart` | POST | Reset completion for a lesson |

---

## 🛡️ Responsible Finance & Accuracy Disclaimer

1. **Educational Purpose:** ArthSaathi AI is designed purely for financial literacy and decision support. It does not provide SEBI-registered portfolio advice, tax advice, or loan approval guarantees.
2. **Bank Rates Data:** All bank interest rate figures stored in the database are indicative demo records with source URLs and verification dates. Contractual rates are subject to individual creditworthiness (CIBIL score, income, employment).
3. **No Financial Credentials:** ArthSaathi AI never connects to live bank accounts, nor asks for passwords, PINs, OTPs, or CVVs.

---

Built with ❤️ for Financial Empowerment in India 🇮🇳
