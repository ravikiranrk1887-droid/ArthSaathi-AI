"""
scripts/seed_data.py
====================
Seeds the database with:
- 10 Indian banks
- Bank products (home loan, education loan, personal loan, FD, savings account)
- Interest rates — ALL MARKED is_demo_data=True
- 5 sample lessons with quiz questions

⚠️  ALL interest rate data is DEMO DATA for educational purposes only.
    Rates are approximate and may not reflect current offerings.
    Always verify at the official bank website before making any financial decision.
"""

import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.extensions import db
from app.models.bank import Bank, BankProduct, InterestRate, BankType, ProductType, RateType
from app.models.lesson import Lesson, LessonCategory
from app.models.quiz import QuizQuestion

SEED_DATE = date(2024, 11, 3)  # last_verified demo date

# ---------------------------------------------------------------------------
# Bank master data
# ---------------------------------------------------------------------------

BANKS = [
    {
        "name": "State Bank of India",
        "short_name": "SBI",
        "bank_type": BankType.PUBLIC,
        "established_year": 1955,
        "headquarters": "Mumbai, Maharashtra",
        "website_url": "https://www.sbi.co.in",
    },
    {
        "name": "HDFC Bank",
        "short_name": "HDFC",
        "bank_type": BankType.PRIVATE,
        "established_year": 1994,
        "headquarters": "Mumbai, Maharashtra",
        "website_url": "https://www.hdfcbank.com",
    },
    {
        "name": "ICICI Bank",
        "short_name": "ICICI",
        "bank_type": BankType.PRIVATE,
        "established_year": 1994,
        "headquarters": "Mumbai, Maharashtra",
        "website_url": "https://www.icicibank.com",
    },
    {
        "name": "Axis Bank",
        "short_name": "AXIS",
        "bank_type": BankType.PRIVATE,
        "established_year": 1993,
        "headquarters": "Mumbai, Maharashtra",
        "website_url": "https://www.axisbank.com",
    },
    {
        "name": "Kotak Mahindra Bank",
        "short_name": "KOTAK",
        "bank_type": BankType.PRIVATE,
        "established_year": 2003,
        "headquarters": "Mumbai, Maharashtra",
        "website_url": "https://www.kotak.com",
    },
    {
        "name": "Bank of Baroda",
        "short_name": "BOB",
        "bank_type": BankType.PUBLIC,
        "established_year": 1908,
        "headquarters": "Vadodara, Gujarat",
        "website_url": "https://www.bankofbaroda.in",
    },
    {
        "name": "Canara Bank",
        "short_name": "CANARA",
        "bank_type": BankType.PUBLIC,
        "established_year": 1906,
        "headquarters": "Bengaluru, Karnataka",
        "website_url": "https://canarabank.com",
    },
    {
        "name": "Punjab National Bank",
        "short_name": "PNB",
        "bank_type": BankType.PUBLIC,
        "established_year": 1894,
        "headquarters": "New Delhi",
        "website_url": "https://www.pnbindia.in",
    },
    {
        "name": "Union Bank of India",
        "short_name": "UNION",
        "bank_type": BankType.PUBLIC,
        "established_year": 1919,
        "headquarters": "Mumbai, Maharashtra",
        "website_url": "https://www.unionbankofindia.co.in",
    },
    {
        "name": "Indian Bank",
        "short_name": "INDIAN",
        "bank_type": BankType.PUBLIC,
        "established_year": 1907,
        "headquarters": "Chennai, Tamil Nadu",
        "website_url": "https://www.indianbank.in",
    },
]

# ---------------------------------------------------------------------------
# Product and rate definitions
# Rates are DEMO approximations; is_demo_data=True on every record
# ---------------------------------------------------------------------------

DEMO_NOTE = (
    "⚠️ DEMO DATA — for educational purposes only. "
    "Actual rates may differ. Please verify on the bank's official website."
)

PRODUCTS_TEMPLATE = [
    # (product_type, product_name, description, features, eligibility, rate_min, rate_max, rate_type)
    (
        ProductType.HOME_LOAN,
        "Home Loan",
        "Floating rate home loan for purchase/construction of residential property.",
        {"max_amount": 75_000_000, "min_amount": 500_000, "max_tenure_months": 360, "min_tenure_months": 12,
         "processing_fee": "0.35% + GST"},
        {"min_age": 21, "max_age": 70, "min_salary": 25000, "cibil_score": 700},
        8.50, 9.50, RateType.FLOATING,
    ),
    (
        ProductType.EDUCATION_LOAN,
        "Education Loan",
        "Loan for higher education in India and abroad.",
        {"max_amount": 1_500_000, "min_amount": 50_000, "max_tenure_months": 180, "min_tenure_months": 12,
         "moratorium": "Course duration + 1 year"},
        {"min_age": 16, "max_age": 35, "guarantor": "Parent/Guardian required for amounts over ₹7.5 lakh"},
        9.00, 11.50, RateType.FLOATING,
    ),
    (
        ProductType.PERSONAL_LOAN,
        "Personal Loan",
        "Unsecured personal loan for any legitimate financial need.",
        {"max_amount": 4_000_000, "min_amount": 50_000, "max_tenure_months": 60, "min_tenure_months": 12,
         "processing_fee": "1-2% + GST"},
        {"min_age": 21, "max_age": 60, "min_salary": 20000, "cibil_score": 720},
        10.50, 16.00, RateType.FIXED,
    ),
    (
        ProductType.VEHICLE_LOAN,
        "Vehicle Loan",
        "Loan for purchase of new or used two-wheelers and four-wheelers.",
        {"max_amount": 2_000_000, "min_amount": 100_000, "max_tenure_months": 84, "min_tenure_months": 12,
         "ltv": "Up to 90% of vehicle value"},
        {"min_age": 21, "max_age": 65, "min_salary": 15000},
        8.75, 12.00, RateType.FIXED,
    ),
    (
        ProductType.BUSINESS_LOAN,
        "Business Loan (MSME)",
        "Collateral-free and secured business loans for MSMEs and enterprises under CGTMSE scheme.",
        {"max_amount": 20_000_000, "min_amount": 100_000, "max_tenure_months": 84, "min_tenure_months": 12,
         "processing_fee": "1-2% + GST", "scheme": "CGTMSE / MUDRA"},
        {"min_vintage_years": 2, "min_annual_turnover": 500_000, "cibil_score": 700},
        9.75, 14.50, RateType.FLOATING,
    ),
    (
        ProductType.FIXED_DEPOSIT,
        "Fixed Deposit",
        "Term deposit with guaranteed returns. Compounded quarterly.",
        {"min_amount": 5000, "max_tenure_months": 120, "min_tenure_months": 7,
         "compounding": "Quarterly", "premature_withdrawal": "Penalty 0.5-1% below contracted rate"},
        {"min_age": 18},
        6.50, 7.75, RateType.FIXED,
    ),
    (
        ProductType.SAVINGS_ACCOUNT,
        "Savings Account",
        "Regular savings account with interest on daily balance.",
        {"min_balance": 1000, "atm_withdrawals": "5 free/month", "internet_banking": True},
        {"min_age": 10},  # minors allowed with guardian
        2.70, 4.00, RateType.FIXED,
    ),
]

# Per-bank rate adjustments (offset applied to base rates above)
BANK_RATE_OFFSETS = {
    "SBI":    0.00,
    "HDFC":   0.15,
    "ICICI":  0.20,
    "AXIS":   0.25,
    "KOTAK":  0.30,
    "BOB":    -0.10,
    "CANARA": -0.05,
    "PNB":    0.00,
    "UNION":  -0.10,
    "INDIAN": -0.15,
}


def seed_banks():
    """Insert banks and their products/rates if not already seeded."""
    for bank_data in BANKS:
        bank = Bank.query.filter_by(short_name=bank_data["short_name"]).first()
        if not bank:
            bank = Bank(**bank_data)
            db.session.add(bank)
            db.session.flush()

        offset = BANK_RATE_OFFSETS.get(bank.short_name, 0.0)

        for (
            ptype, pname, desc, features, eligibility,
            base_min, base_max, rate_type
        ) in PRODUCTS_TEMPLATE:
            existing_prod = BankProduct.query.filter_by(bank_id=bank.id, product_type=ptype).first()
            if not existing_prod:
                product = BankProduct(
                    bank_id=bank.id,
                    product_type=ptype,
                    product_name=f"{bank.short_name} {pname}",
                    description=desc,
                    features_json=features,
                    eligibility_json=eligibility,
                )
                db.session.add(product)
                db.session.flush()

                rate = InterestRate(
                    bank_product_id=product.id,
                    rate_min=round(base_min + offset, 2),
                    rate_max=round(base_max + offset, 2),
                    rate_type=rate_type,
                    effective_date=SEED_DATE,
                    last_verified=SEED_DATE,
                    source_url=bank_data["website_url"],
                    notes=DEMO_NOTE,
                    is_demo_data=True,
                )
                db.session.add(rate)

    db.session.commit()
    print(f"  Seeded {len(BANKS)} banks with {len(PRODUCTS_TEMPLATE)} products each.")


# ---------------------------------------------------------------------------
# Lesson seed data
# ---------------------------------------------------------------------------

LESSONS = [
    {
        "title": "What is a Savings Account?",
        "slug": "what-is-a-savings-account",
        "category": LessonCategory.BANKING,
        "subcategory": "Accounts",
        "difficulty": "BEGINNER",
        "order_index": 1,
        "content_json": {
            "summary": "A savings account is the most basic bank account that lets you deposit money safely and earn interest on it.",
            "sections": [
                {
                    "heading": "Definition",
                    "body": (
                        "A savings account is a deposit account held at a bank that provides principal security "
                        "and a modest interest rate. In India, savings account interest rates typically range "
                        "from 2.7% to 7% per annum, depending on the bank and balance."
                    ),
                },
                {
                    "heading": "How Interest Works",
                    "body": (
                        "As per RBI guidelines, interest is calculated on the daily closing balance and credited "
                        "to the account quarterly. For example, if you maintain ₹1,00,000 in your SBI savings "
                        "account at 2.7% p.a., you will earn approximately ₹2,700 annually."
                    ),
                },
                {
                    "heading": "Types of Savings Accounts in India",
                    "body": (
                        "1. Regular Savings Account — Standard account with minimum balance requirement.\n"
                        "2. Zero Balance Account (BSBD) — Jan Dhan accounts require no minimum balance.\n"
                        "3. Salary Account — Opened by employer; usually zero balance.\n"
                        "4. Senior Citizen Account — Higher interest rates for citizens above 60 years."
                    ),
                },
            ],
            "key_points": [
                "Interest is calculated on daily balance, paid quarterly.",
                "Most banks require a minimum average monthly balance (e.g., ₹1,000–₹10,000).",
                "Deposits are insured up to ₹5 lakh under DICGC.",
                "Jan Dhan accounts offer zero minimum balance for financial inclusion.",
                "Interest earned is taxable under 'Income from Other Sources'; TDS if > ₹40,000/year.",
            ],
        },
    },
    {
        "title": "Understanding EMI: How Loan Repayments Work",
        "slug": "understanding-emi-loan-repayments",
        "category": LessonCategory.LOANS,
        "subcategory": "EMI",
        "difficulty": "BEGINNER",
        "order_index": 1,
        "content_json": {
            "summary": "EMI (Equated Monthly Instalment) is the fixed monthly payment you make to repay a loan. Learn how it is calculated.",
            "sections": [
                {
                    "heading": "What is EMI?",
                    "body": (
                        "EMI stands for Equated Monthly Instalment. It is the fixed amount you pay each month "
                        "to repay a loan. Each EMI has two components: the principal repayment and the interest "
                        "charged on the outstanding balance. In the early months, a larger portion goes toward "
                        "interest; over time, more goes toward principal — this is called loan amortization."
                    ),
                },
                {
                    "heading": "The EMI Formula",
                    "body": (
                        "EMI = P × r × (1+r)^n / ((1+r)^n - 1)\n\n"
                        "Where:\n"
                        "  P = Principal loan amount (₹)\n"
                        "  r = Monthly interest rate = Annual Rate / 12 / 100\n"
                        "  n = Total number of monthly instalments\n\n"
                        "Example: Home loan of ₹30,00,000 at 8.5% for 20 years (240 months):\n"
                        "  r = 8.5 / 12 / 100 = 0.007083\n"
                        "  EMI = 30,00,000 × 0.007083 × (1.007083)^240 / ((1.007083)^240 - 1)\n"
                        "  EMI ≈ ₹26,035 per month"
                    ),
                },
                {
                    "heading": "Total Interest Paid",
                    "body": (
                        "Total Payment = EMI × n\n"
                        "Total Interest = Total Payment - Principal\n\n"
                        "In the above example:\n"
                        "  Total Payment = ₹26,035 × 240 = ₹62,48,400\n"
                        "  Total Interest = ₹62,48,400 - ₹30,00,000 = ₹32,48,400\n\n"
                        "This shows you pay more than double the loan amount in interest over 20 years!"
                    ),
                },
            ],
            "key_points": [
                "EMI = Principal + Interest component, calculated using compound interest formula.",
                "Early EMIs are mostly interest; later EMIs are mostly principal repayment.",
                "Longer tenure = lower EMI but higher total interest paid.",
                "Pre-paying a loan reduces both EMI tenure and total interest significantly.",
                "Use ArthSaathi's EMI Calculator to model your loan before applying.",
            ],
        },
    },
    {
        "title": "Fixed Deposits (FD): Safe Returns Explained",
        "slug": "fixed-deposits-fd-safe-returns",
        "category": LessonCategory.INVESTMENT,
        "subcategory": "Fixed Income",
        "difficulty": "BEGINNER",
        "order_index": 1,
        "content_json": {
            "summary": "Fixed Deposits are one of India's most popular investment instruments offering guaranteed returns. Learn how they work.",
            "sections": [
                {
                    "heading": "What is a Fixed Deposit?",
                    "body": (
                        "A Fixed Deposit (FD) is a financial instrument where you deposit a lump sum with a "
                        "bank for a fixed tenure (7 days to 10 years) at a predetermined interest rate. "
                        "Unlike savings accounts, the rate is locked in for the entire tenure, making FDs "
                        "a low-risk, predictable investment."
                    ),
                },
                {
                    "heading": "How FD Interest is Calculated",
                    "body": (
                        "FDs in India compound interest quarterly (most common):\n\n"
                        "A = P × (1 + r/n)^(n×t)\n\n"
                        "Where:\n"
                        "  P = Principal (₹)\n"
                        "  r = Annual interest rate (decimal)\n"
                        "  n = Compounding frequency (4 for quarterly)\n"
                        "  t = Time in years\n\n"
                        "Example: ₹1,00,000 FD at 7% for 2 years (quarterly compounding):\n"
                        "  A = 1,00,000 × (1 + 0.07/4)^(4×2)\n"
                        "  A = 1,00,000 × (1.0175)^8\n"
                        "  A ≈ ₹1,14,888\n"
                        "  Interest Earned ≈ ₹14,888"
                    ),
                },
                {
                    "heading": "Tax on FD Interest",
                    "body": (
                        "FD interest is fully taxable as 'Income from Other Sources'. Banks deduct TDS at 10% "
                        "if interest exceeds ₹40,000 per year (₹50,000 for senior citizens). "
                        "Submit Form 15G (or 15H for seniors) to avoid TDS if your total income is below "
                        "the taxable limit."
                    ),
                },
            ],
            "key_points": [
                "FD rates are fixed — you know exactly what you'll earn at maturity.",
                "DICGC insures FDs up to ₹5 lakh per depositor per bank.",
                "Senior citizens typically get 0.25–0.50% higher rates.",
                "Premature withdrawal incurs a penalty (usually 0.5–1% rate reduction).",
                "Tax Saver FDs have a 5-year lock-in and qualify for Section 80C deduction (up to ₹1.5 lakh).",
            ],
        },
    },
    {
        "title": "SIP Investing: Growing Wealth Through Mutual Funds",
        "slug": "sip-investing-mutual-funds",
        "category": LessonCategory.INVESTMENT,
        "subcategory": "Mutual Funds",
        "difficulty": "INTERMEDIATE",
        "order_index": 2,
        "content_json": {
            "summary": "SIP (Systematic Investment Plan) lets you invest small amounts regularly in mutual funds to build long-term wealth through rupee cost averaging.",
            "sections": [
                {
                    "heading": "What is a SIP?",
                    "body": (
                        "A Systematic Investment Plan (SIP) allows you to invest a fixed amount (e.g., ₹5,000/month) "
                        "in a mutual fund at regular intervals (weekly, monthly, quarterly). "
                        "Over time, SIP leverages rupee cost averaging — you buy more units when prices are low "
                        "and fewer when prices are high."
                    ),
                },
                {
                    "heading": "The Power of Compounding in SIPs",
                    "body": (
                        "SIP Future Value = P × ((1+r)^n - 1) / r × (1+r)\n\n"
                        "Where:\n"
                        "  P = Monthly SIP amount (₹)\n"
                        "  r = Monthly return rate = Annual Rate / 12 / 100\n"
                        "  n = Total months\n\n"
                        "Example: ₹5,000/month SIP for 15 years at 12% p.a.:\n"
                        "  Total invested = ₹9,00,000\n"
                        "  Estimated corpus ≈ ₹25,22,880\n"
                        "  Estimated gains ≈ ₹16,22,880\n\n"
                        "Your money nearly triples! This is the power of compounding + regular investing."
                    ),
                },
                {
                    "heading": "Important Disclaimer",
                    "body": (
                        "Mutual fund investments are subject to market risks. Past performance does not "
                        "guarantee future returns. The 12% return used above is a historical average for "
                        "large-cap equity mutual funds — actual returns will vary. Always consult a "
                        "SEBI-registered investment advisor before investing."
                    ),
                },
            ],
            "key_points": [
                "SIP automates investing — great for building discipline.",
                "Rupee cost averaging reduces the risk of market timing.",
                "Even ₹500/month can build significant wealth over 20+ years.",
                "Equity SIPs held > 1 year attract Long-Term Capital Gains Tax at 10% (above ₹1 lakh gains).",
                "You can pause, increase, or stop a SIP anytime (unlike FD).",
            ],
        },
    },
    {
        "title": "UPI and Digital Payments in India",
        "slug": "upi-digital-payments-india",
        "category": LessonCategory.INDIAN_BANKING,
        "subcategory": "Digital Banking",
        "difficulty": "BEGINNER",
        "order_index": 1,
        "content_json": {
            "summary": "UPI (Unified Payments Interface) has revolutionised money transfers in India. Learn how it works and how to use it safely.",
            "sections": [
                {
                    "heading": "What is UPI?",
                    "body": (
                        "UPI (Unified Payments Interface) is a real-time payment system developed by NPCI "
                        "(National Payments Corporation of India) that enables instant bank-to-bank transfers "
                        "using a mobile phone. Launched in 2016, UPI processes over 10 billion transactions "
                        "monthly as of 2024, making India the world leader in real-time payments."
                    ),
                },
                {
                    "heading": "How UPI Works",
                    "body": (
                        "1. Link your bank account to a UPI-enabled app (BHIM, PhonePe, Google Pay, Paytm, etc.)\n"
                        "2. Create a VPA (Virtual Payment Address) — e.g., yourname@okaxis\n"
                        "3. To send money: enter recipient's VPA or scan QR code → enter amount → authenticate with UPI PIN\n"
                        "4. Transfer happens instantly 24×7, including holidays.\n\n"
                        "Daily limit: ₹1 lakh per transaction (₹2 lakh for verified merchants)."
                    ),
                },
                {
                    "heading": "UPI Safety Tips",
                    "body": (
                        "✅ Never share your UPI PIN with anyone — not even bank employees.\n"
                        "✅ Verify the payee name before confirming any payment.\n"
                        "✅ 'Request Money' doesn't require your PIN — fraudsters ask you to enter it.\n"
                        "✅ If you receive an unknown collect request, decline it immediately.\n"
                        "✅ Report fraud to your bank and cybercrime.gov.in immediately."
                    ),
                },
            ],
            "key_points": [
                "UPI is free for individuals — no transaction charges.",
                "Transfers are instant and irreversible — always verify recipient details.",
                "BHIM is the government's official UPI app, built by NPCI.",
                "UPI Lite allows offline transactions up to ₹500 without internet.",
                "India's UPI is being adopted by countries like Singapore, France, and UAE.",
            ],
        },
    },
]


def seed_lessons():
    """Insert lessons and their quiz questions if not already seeded."""
    if Lesson.query.count() > 0:
        print("  Lessons already seeded — skipping.")
        return

    quiz_data = {
        "what-is-a-savings-account": [
            {
                "question": "Up to what amount are bank deposits insured by DICGC in India?",
                "options": ["₹1 lakh", "₹2 lakh", "₹5 lakh", "₹10 lakh"],
                "correct_index": 2,
                "explanation": "DICGC (Deposit Insurance and Credit Guarantee Corporation) insures deposits up to ₹5 lakh per depositor per bank.",
            },
            {
                "question": "How is savings account interest calculated in India as per RBI guidelines?",
                "options": [
                    "On the minimum monthly balance",
                    "On the daily closing balance",
                    "On the average weekly balance",
                    "On the opening balance",
                ],
                "correct_index": 1,
                "explanation": "RBI mandates that savings account interest be calculated on the daily closing balance and credited quarterly.",
            },
            {
                "question": "Which type of account requires NO minimum balance?",
                "options": ["Regular Savings Account", "Salary Account", "BSBD (Jan Dhan) Account", "Premium Savings Account"],
                "correct_index": 2,
                "explanation": "Basic Savings Bank Deposit (BSBD) accounts under the Jan Dhan scheme require zero minimum balance.",
            },
        ],
        "understanding-emi-loan-repayments": [
            {
                "question": "In the EMI formula, what does 'r' represent?",
                "options": [
                    "Annual interest rate",
                    "Monthly interest rate (Annual Rate / 12 / 100)",
                    "Daily interest rate",
                    "Quarterly interest rate",
                ],
                "correct_index": 1,
                "explanation": "'r' in the EMI formula is the monthly interest rate = Annual Rate ÷ 12 ÷ 100. For 8.4% annual rate, r = 0.007.",
            },
            {
                "question": "In loan amortization, what happens to the interest component of EMI over time?",
                "options": [
                    "It stays the same throughout",
                    "It increases over time",
                    "It decreases over time as outstanding balance reduces",
                    "It doubles every year",
                ],
                "correct_index": 2,
                "explanation": "As you repay the principal, the outstanding balance reduces, so the interest charged each month decreases while the principal component increases.",
            },
            {
                "question": "For a ₹30 lakh home loan at 8.5% for 20 years, what approximately is the total interest paid?",
                "options": ["₹10 lakh", "₹32 lakh", "₹50 lakh", "₹5 lakh"],
                "correct_index": 1,
                "explanation": "Total payment ≈ ₹62.5 lakh for ₹30 lakh principal, meaning total interest ≈ ₹32.5 lakh — more than the loan itself!",
            },
        ],
        "fixed-deposits-fd-safe-returns": [
            {
                "question": "What form should you submit to avoid TDS on FD interest if your income is below the taxable limit?",
                "options": ["Form 16", "Form 26AS", "Form 15G (or 15H for seniors)", "Form 10E"],
                "correct_index": 2,
                "explanation": "Form 15G (for individuals below 60) and Form 15H (for senior citizens) are submitted to banks to avoid TDS deduction when income is below the taxable limit.",
            },
            {
                "question": "At what compounding frequency do most Indian banks calculate FD interest?",
                "options": ["Annually", "Monthly", "Quarterly", "Daily"],
                "correct_index": 2,
                "explanation": "Most Indian banks compound FD interest quarterly, which gives slightly better returns than annual compounding.",
            },
            {
                "question": "What is the lock-in period for a Tax Saver FD that qualifies under Section 80C?",
                "options": ["1 year", "3 years", "5 years", "7 years"],
                "correct_index": 2,
                "explanation": "Tax Saver FDs have a mandatory 5-year lock-in period. Premature withdrawal is not allowed.",
            },
        ],
        "sip-investing-mutual-funds": [
            {
                "question": "What is 'Rupee Cost Averaging' in SIP investing?",
                "options": [
                    "You always buy at the same price",
                    "You buy more units when price is high, fewer when low",
                    "You buy more units when price is low, fewer when high — averaging purchase cost",
                    "You fix the number of units purchased every month",
                ],
                "correct_index": 2,
                "explanation": "Rupee Cost Averaging means your fixed SIP amount buys more mutual fund units when NAV is low and fewer when high, averaging out your purchase cost over time.",
            },
            {
                "question": "What is the Long-Term Capital Gains Tax rate on equity mutual funds held over 1 year in India?",
                "options": ["0%", "10% on gains above ₹1 lakh", "15%", "30%"],
                "correct_index": 1,
                "explanation": "LTCG on equity funds is 10% on gains exceeding ₹1 lakh in a financial year (as per budget 2024-25). Gains up to ₹1 lakh are exempt.",
            },
            {
                "question": "Which body regulates mutual funds in India?",
                "options": ["RBI", "IRDAI", "SEBI", "PFRDA"],
                "correct_index": 2,
                "explanation": "SEBI (Securities and Exchange Board of India) regulates mutual funds. All AMCs (Asset Management Companies) must be SEBI-registered.",
            },
        ],
        "upi-digital-payments-india": [
            {
                "question": "Which organisation developed UPI in India?",
                "options": ["RBI", "NPCI", "SBI", "Ministry of Finance"],
                "correct_index": 1,
                "explanation": "UPI was developed by NPCI (National Payments Corporation of India), which is owned by a consortium of banks and operates under RBI guidelines.",
            },
            {
                "question": "A fraudster calls and asks you to enter your UPI PIN to 'receive' ₹5,000. What should you do?",
                "options": [
                    "Enter the PIN quickly to receive the money",
                    "Decline — entering your UPI PIN is only required to SEND money, never to receive",
                    "Share your PIN only if the caller knows your account number",
                    "Enter PIN if the caller says they are from your bank",
                ],
                "correct_index": 1,
                "explanation": "UPI PIN is only required to AUTHORISE payments you MAKE. You never need to enter your PIN to receive money. This is a classic fraud technique.",
            },
            {
                "question": "What is the standard per-transaction UPI limit for individual users?",
                "options": ["₹10,000", "₹50,000", "₹1,00,000", "₹5,00,000"],
                "correct_index": 2,
                "explanation": "The standard UPI transaction limit is ₹1 lakh per transaction for most use cases. Some banks allow up to ₹2 lakh for verified merchants.",
            },
        ],
    }

    for lesson_data in LESSONS:
        slug = lesson_data["slug"]
        lesson = Lesson(**lesson_data)
        db.session.add(lesson)
        db.session.flush()

        for q_data in quiz_data.get(slug, []):
            question = QuizQuestion(
                lesson_id=lesson.id,
                question=q_data["question"],
                options_json=q_data["options"],
                correct_index=q_data["correct_index"],
                explanation=q_data["explanation"],
            )
            db.session.add(question)

    db.session.commit()
    print(f"  Seeded {len(LESSONS)} lessons with quiz questions.")


# ---------------------------------------------------------------------------
# Master seed function
# ---------------------------------------------------------------------------

def seed_all():
    print("Seeding banks...")
    seed_banks()
    print("Seeding lessons...")
    seed_lessons()
    print("All seed data inserted successfully.")


if __name__ == "__main__":
    # Allow running standalone: python scripts/seed_data.py
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_all()
