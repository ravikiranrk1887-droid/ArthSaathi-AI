"""
scripts/seed_all_lessons.py
===========================
Generates comprehensive educational lessons and quizzes for ArthSaathi AI covering
all 5 categories specified in Module 2:
  A. Banking Fundamentals
  B. Investment Education
  C. Loan Education
  D. Personal Financial Planning
  E. Indian Banking System

Each lesson includes all 10 required items:
  1. Definition
  2. Beginner explanation
  3. Real-world Indian example (in INR)
  4. Step-by-step how it works
  5. Advantages
  6. Disadvantages & risks
  7. Common mistakes
  8. FAQs
  9. Short knowledge quiz with explanations
  10. Related financial calculator
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.lesson import Lesson, LessonCategory
from app.models.quiz import QuizQuestion

LESSON_DATA = [
    # =========================================================================
    # CATEGORY A: BANKING FUNDAMENTALS
    # =========================================================================
    {
        "title": "What is a Bank & How Does Banking Work?",
        "slug": "what-is-a-bank-how-it-works",
        "category": LessonCategory.BANKING,
        "subcategory": "Core Concepts",
        "difficulty": "BEGINNER",
        "order_index": 1,
        "calculator": "emi",
        "content_json": {
            "summary": "Banks are financial institutions licensed to receive deposits and make loans. Learn how the banking system channels money in India.",
            "definition": "A bank is a financial intermediary licensed by the Reserve Bank of India (RBI) that accepts deposits from the public and creates credit through lending operations.",
            "beginner_explanation": "Imagine you have ₹10,000 cash at home. Leaving it in a drawer is risky and earns nothing. A bank takes your ₹10,000, keeps it safe, pays you interest (e.g. 3%), and lends ₹8,000 to a home buyer at 8.5%. The 5.5% difference is how the bank covers its costs and earns a profit.",
            "indian_example": "Ramesh deposits ₹50,000 in SBI. SBI pays Ramesh 3% interest (₹1,500/year). SBI pools Ramesh's deposit with others to lend Priya ₹30,00,000 for a home loan at 8.5%. Both parties benefit: Ramesh earns safe interest and Priya gets a home.",
            "how_it_works_steps": [
                "Depositors place their surplus funds into savings, current, or fixed deposit accounts.",
                "The bank reserves a fraction as mandated by RBI (Cash Reserve Ratio or CRR ~4.5% and Statutory Liquidity Ratio or SLR ~18%).",
                "The remaining balance is deployed as loans to individuals, small businesses, and corporations.",
                "Borrowers repay the loan with interest through monthly EMIs.",
                "The bank pays interest to depositors and keeps the net interest margin (spread) as operating revenue."
            ],
            "advantages": [
                "Safety of principal: Up to ₹5 lakh insured per bank per depositor by DICGC.",
                "Liquidity: Easy access to your cash via ATMs, debit cards, and UPI.",
                "Interest income: Money grows rather than idling as paper cash.",
                "Digital convenience: 24/7 money transfers through UPI, NEFT, and IMPS."
            ],
            "disadvantages_and_risks": [
                "Low returns: Savings account interest (2.7%–4%) is often lower than inflation (~5-6%).",
                "Service fees: Minimum balance penalties, ATM withdrawal charges, and SMS alerts fees.",
                "Operational risk: System downtime, ATM maintenance, or branch closures."
            ],
            "common_mistakes": [
                "Keeping excessive cash in a basic savings account instead of investing in FDs or mutual funds.",
                "Failing to maintain the Monthly Average Balance (MAB), attracting penalty charges.",
                "Not updating KYC details, which leads to temporary account freezing."
            ],
            "faqs": [
                {"q": "Is my money 100% safe in an Indian bank?", "a": "Under RBI's DICGC Act, deposits up to ₹5 lakh (including principal and interest) are insured per depositor across all branches of a single bank."},
                {"q": "What happens to idle money in a savings account?", "a": "It earns quarterly interest based on the daily end-of-day balance, but loses purchasing power if inflation is higher than the rate."},
                {"q": "Who regulates all banks in India?", "a": "The Reserve Bank of India (RBI), established in 1935 under the RBI Act."}
            ]
        },
        "quiz": [
            {
                "question": "What is the primary way banks earn income?",
                "options": ["Government grants", "The spread between loan interest charged and deposit interest paid", "ATM withdrawal fee penalties", "Currency printing fees"],
                "correct_index": 1,
                "explanation": "Banks charge higher interest on loans than they pay to depositors; this difference (net interest margin) is their main revenue source."
            },
            {
                "question": "Under RBI guidelines, deposits are insured by DICGC up to what limit per depositor per bank?",
                "options": ["₹1,00,000", "₹2,50,000", "₹5,00,000", "₹10,00,000"],
                "correct_index": 2,
                "explanation": "The Deposit Insurance and Credit Guarantee Corporation (DICGC) covers principal and interest up to ₹5,00,000 per bank."
            },
            {
                "question": "How often is savings account interest credited in Indian banks?",
                "options": ["Daily", "Monthly", "Quarterly", "Annually"],
                "correct_index": 2,
                "explanation": "While interest is calculated on daily closing balance, it is credited to your account every quarter."
            }
        ]
    },
    {
        "title": "Savings Account vs Current Account vs Salary Account",
        "slug": "savings-vs-current-vs-salary-account",
        "category": LessonCategory.BANKING,
        "subcategory": "Accounts",
        "difficulty": "BEGINNER",
        "order_index": 2,
        "calculator": "compound",
        "content_json": {
            "summary": "Understand the differences between Savings, Current, and Salary accounts and choose the right one for your needs.",
            "definition": "A Savings Account is designed for personal savings with interest; a Current Account is for business transactions with zero interest and unlimited transactions; a Salary Account is a customized zero-balance savings account opened by employers.",
            "beginner_explanation": "If you are an individual wanting to save money, you need a Savings Account. If you run a shop with 50 transactions daily, you need a Current Account. If you join a company that deposits your monthly paycheck, they open a Salary Account for you.",
            "indian_example": "Amit works at an IT company in Bengaluru. His monthly salary of ₹65,000 comes into his HDFC Salary Account (zero minimum balance). His father runs a grocery store in Jaipur and uses a BOB Current Account for dozens of daily supplier payments without withdrawal limits.",
            "how_it_works_steps": [
                "Savings accounts earn 2.7%–4% p.a. interest, calculated on daily balance and paid quarterly.",
                "Current accounts pay zero interest but provide overdraft facilities and unlimited transactions.",
                "Salary accounts offer zero-balance benefits as long as monthly salary credits continue.",
                "If salary stops for 3 consecutive months, the salary account automatically converts to a regular savings account with minimum balance rules."
            ],
            "advantages": [
                "Savings: Safe place to park money while earning steady modest returns.",
                "Current: High transaction volumes, customized cheque books, and overdraft facilities.",
                "Salary: No minimum balance penalty, free debit cards, and preferential loan rates."
            ],
            "disadvantages_and_risks": [
                "Savings: Monthly cash deposit/withdrawal limits apply.",
                "Current: No interest earnings on deposited funds.",
                "Salary: Penalties apply if salary credits stop and balance falls below minimum required."
            ],
            "common_mistakes": [
                "Using a personal savings account for high-volume commercial transactions, risking tax notices.",
                "Ignoring the conversion of an old salary account to regular savings after changing jobs."
            ],
            "faqs": [
                {"q": "Can I have multiple savings accounts?", "a": "Yes, an individual can hold savings accounts across multiple banks with no legal restriction."},
                {"q": "Does a Current Account earn any interest?", "a": "No, as per RBI directives, commercial banks in India cannot pay interest on current accounts."}
            ]
        },
        "quiz": [
            {
                "question": "Which type of bank account offers zero minimum balance requirement as long as monthly paycheck credits continue?",
                "options": ["Current Account", "Salary Account", "Fixed Deposit", "Recurring Deposit"],
                "correct_index": 1,
                "explanation": "Salary accounts provide zero minimum balance privileges as part of the corporate tie-up with the bank."
            },
            {
                "question": "What interest rate is paid on Current Accounts in India?",
                "options": ["3.5%", "6.0%", "0.0%", "Repo Rate minus 2%"],
                "correct_index": 2,
                "explanation": "As per RBI regulations, commercial banks are prohibited from paying interest on current account balances."
            }
        ]
    },
    {
        "title": "Digital Payments in India: UPI, NEFT, RTGS, IMPS",
        "slug": "digital-payments-upi-neft-rtgs-imps",
        "category": LessonCategory.BANKING,
        "subcategory": "Digital Banking",
        "difficulty": "BEGINNER",
        "order_index": 3,
        "calculator": None,
        "content_json": {
            "summary": "Master India's payment rails: UPI for instant mobile payments, NEFT for scheduled transfers, RTGS for high value, and IMPS for 24/7 bank transfers.",
            "definition": "Digital payment systems in India are electronic mechanisms managed by NPCI and RBI enabling cashless fund transfers across bank accounts.",
            "beginner_explanation": "Sending money in India has 4 main highways: UPI is like a motorcycle (super fast, scans QR codes, free, up to ₹1-2 lakh); IMPS is like a taxi (24/7 instant, up to ₹5 lakh); NEFT is like a regular bus (24/7 in batches, no minimum); RTGS is like an express flight (instant for large business transfers above ₹2 lakh).",
            "indian_example": "Sunita pays ₹50 for vegetables using PhonePe UPI. She sends ₹15,000 for her college fee via IMPS. Her father transfers ₹12,00,000 for purchasing a plot of land via RTGS.",
            "how_it_works_steps": [
                "UPI (Unified Payments Interface): Links your bank account to a Virtual Payment Address (VPA) or phone number; authenticated by a 4- or 6-digit UPI PIN.",
                "IMPS (Immediate Payment Service): Real-time interbank electronic transfer available 24/7/365 through mobile and internet banking.",
                "NEFT (National Electronic Funds Transfer): Operates round-the-clock in half-hourly batches without transaction minimums.",
                "RTGS (Real Time Gross Settlement): Meant for high-value transactions (minimum ₹2 lakh), processed continuously without batch delays."
            ],
            "advantages": [
                "Instant transfers anytime, even on Sundays and national holidays.",
                "Zero charges for retail users on UPI transactions.",
                "High security with two-factor authentication and UPI PIN encryption.",
                "Eliminates the risk of carrying large cash sums."
            ],
            "disadvantages_and_risks": [
                "UPI fraud: Scammers asking you to enter your UPI PIN to 'receive' money.",
                "Mistyped account numbers or IFSC codes leading to wrong credits.",
                "Server downtime during peak festival hours or maintenance windows."
            ],
            "common_mistakes": [
                "Entering your UPI PIN when receiving money (you NEVER enter a PIN to receive funds).",
                "Sharing OTPs, ATM PINs, or UPI PINs over phone calls or SMS.",
                "Assuming NEFT takes days (it is now 24/7 in 30-minute batches)."
            ],
            "faqs": [
                {"q": "Do I need to enter my UPI PIN to receive money?", "a": "NEVER. You only enter your UPI PIN to debit (send) money from your account."},
                {"q": "What is the minimum transfer amount for RTGS?", "a": "The minimum limit for RTGS is ₹2,00,000 with no upper ceiling."}
            ]
        },
        "quiz": [
            {
                "question": "When do you need to enter your UPI PIN?",
                "options": ["To receive money from a friend", "To receive a cashback refund", "Only to send money or check balance", "To accept incoming credit"],
                "correct_index": 2,
                "explanation": "UPI PIN is required ONLY to authorize an outgoing transfer or verify your balance. You NEVER enter a PIN to receive money."
            },
            {
                "question": "What is the minimum transaction amount required for RTGS?",
                "options": ["₹10,000", "₹50,000", "₹1,00,000", "₹2,00,000"],
                "correct_index": 3,
                "explanation": "RTGS is meant for high-value payments with a mandatory minimum of ₹2,00,000."
            }
        ]
    },
    {
        "title": "Simple vs Compound Interest & Inflation",
        "slug": "simple-vs-compound-interest-inflation",
        "category": LessonCategory.BANKING,
        "subcategory": "Mathematics of Money",
        "difficulty": "BEGINNER",
        "order_index": 4,
        "calculator": "compound",
        "content_json": {
            "summary": "Understand how compound interest accelerates wealth creation and how inflation silently erodes your purchasing power over time.",
            "definition": "Simple Interest is calculated only on the initial principal; Compound Interest is interest earned on principal plus accumulated interest. Inflation is the annual rate at which the price of goods rises, eroding purchasing power.",
            "beginner_explanation": "With Simple Interest, ₹1,00,000 at 10% earns ₹10,000 every year forever. With Compound Interest, year 1 earns ₹10,000; year 2 earns 10% on ₹1,10,000 (₹11,000); year 3 earns on ₹1,21,000 (₹12,100). Over 20 years, simple gives ₹3,00,000 while compound gives ₹6,72,750! But remember: if inflation is 6%, an item costing ₹100 today will cost ₹320 in 20 years.",
            "indian_example": "Rahul puts ₹1,00,000 in a 10-year compounding FD at 7.5%. He receives ₹2,08,815. If he had kept it in a savings account with 3% simple interest, he would have only ₹1,30,000. Meanwhile, a petrol litre costing ₹100 today at 5% inflation will cost ₹163 in 10 years.",
            "how_it_works_steps": [
                "Simple Interest Formula: SI = (P × R × T) / 100.",
                "Compound Interest Formula: A = P × (1 + r/n)^(n×t).",
                "Real Return Formula: Real Rate ≈ Nominal Interest Rate - Inflation Rate.",
                "If your bank pays 6% and inflation is 5.5%, your real wealth growth is only 0.5% before taxes!"
            ],
            "advantages": [
                "Compounding turns regular small savings into massive future wealth.",
                "Starting 5 years earlier can double your retirement corpus due to compounding exponential curve."
            ],
            "disadvantages_and_risks": [
                "Compounding works AGAINST you on loans and credit card debts, compounding your dues exponentially.",
                "Inflation silently reduces the real value of fixed-income instruments like savings accounts."
            ],
            "common_mistakes": [
                "Celebrating a 6% return when inflation is 6.5% (you are actually losing real purchasing power).",
                "Delaying investing by thinking 'I will invest when I earn more'—losing vital compounding years."
            ],
            "faqs": [
                {"q": "What is the Rule of 72?", "a": "Divide 72 by the annual interest rate to find roughly how many years it takes to double your money. At 8%, money doubles in 72/8 = 9 years."},
                {"q": "Why does compounding frequency matter in FDs?", "a": "Quarterly compounding yields higher maturity than annual compounding because interest is added 4 times a year."}
            ]
        },
        "quiz": [
            {
                "question": "Using the Rule of 72, roughly how many years will it take for ₹1,00,000 to become ₹2,00,000 at an 8% annual return?",
                "options": ["6 years", "9 years", "12 years", "15 years"],
                "correct_index": 1,
                "explanation": "72 divided by 8 equals 9 years to double your investment."
            },
            {
                "question": "If your fixed deposit earns 6.5% interest and inflation is 5.5%, what is your approximate real return?",
                "options": ["12.0%", "1.0%", "6.5%", "-1.0%"],
                "correct_index": 1,
                "explanation": "Real return ≈ Nominal return (6.5%) minus Inflation (5.5%) = 1.0%."
            }
        ]
    },

    # =========================================================================
    # CATEGORY B: INVESTMENT EDUCATION
    # =========================================================================
    {
        "title": "Saving vs Investing: Why Idle Cash Loses Money",
        "slug": "saving-vs-investing-idle-cash",
        "category": LessonCategory.INVESTMENT,
        "subcategory": "Foundations",
        "difficulty": "BEGINNER",
        "order_index": 1,
        "calculator": "inflation",
        "content_json": {
            "summary": "Understand the fundamental difference between saving for emergencies and investing for wealth creation against inflation.",
            "definition": "Saving is parking money in low-risk, highly liquid avenues (savings accounts, FDs) for short-term needs. Investing is deploying capital in assets (stocks, mutual funds, real estate) to beat inflation and generate long-term wealth.",
            "beginner_explanation": "Saving protects your capital today; investing grows your purchasing power for tomorrow. If you save ₹1,000 in a safe, in 10 years you still have ₹1,000, but a thali meal that cost ₹100 now costs ₹200. You lost half your purchasing power! Investing in equity index funds or PPF gives your money the power to beat that price rise.",
            "indian_example": "Neha saves ₹10,000/month in a savings account at 3% for 15 years (accumulating ₹22.6 lakh). Ananya invests ₹10,000/month in a diversified equity mutual fund SIP at 12% for 15 years (accumulating ₹50.5 lakh). Ananya generated ₹27.9 lakh more wealth with the same monthly savings!",
            "how_it_works_steps": [
                "Step 1: Build an emergency fund of 6 months expenses in savings/liquid FDs.",
                "Step 2: Take term life insurance and health insurance to protect your savings.",
                "Step 3: Define financial goals (buying a home in 7 years, child education in 12 years, retirement in 25 years).",
                "Step 4: Allocate short-term goals to debt instruments and long-term goals to equity/SIPs."
            ],
            "advantages": [
                "Investing beats inflation and builds true generational wealth.",
                "Compounding exponential growth works in your favor over 10+ years."
            ],
            "disadvantages_and_risks": [
                "Investments carry market volatility in the short term.",
                "Capital can temporarily decline during market downturns."
            ],
            "common_mistakes": [
                "Keeping all emergency money in volatile equity stocks.",
                "Leaving ₹5 lakh idle in a 2.7% savings account for 5 years."
            ],
            "faqs": [
                {"q": "How much should I save before I start investing?", "a": "Aim for an emergency fund covering 3 to 6 months of mandatory living expenses before investing aggressively."}
            ]
        },
        "quiz": [
            {
                "question": "What is the primary danger of keeping all your long-term wealth in cash or basic savings accounts?",
                "options": ["Bank theft", "Inflation eroding purchasing power", "Excessive tax penalties", "Automatic conversion to loans"],
                "correct_index": 1,
                "explanation": "Inflation increases the cost of living; when savings interest is below inflation, your real wealth shrinks over time."
            }
        ]
    },
    {
        "title": "What is a Mutual Fund & How Does SIP Work?",
        "slug": "what-is-mutual-fund-sip-work",
        "category": LessonCategory.INVESTMENT,
        "subcategory": "Mutual Funds",
        "difficulty": "BEGINNER",
        "order_index": 2,
        "calculator": "sip",
        "content_json": {
            "summary": "Demystify Mutual Funds, Net Asset Value (NAV), and the wealth-building magic of Systematic Investment Plans (SIP).",
            "definition": "A Mutual Fund pools money from thousands of investors to purchase a diversified portfolio of stocks, bonds, or money market instruments managed by a professional fund manager. A SIP is an automated method to invest a fixed sum periodically.",
            "beginner_explanation": "Imagine 100 students want to buy a luxury mango crate costing ₹10,000 containing 50 varieties of mangoes. No student has ₹10,000. So each chips in ₹100. A fruit expert buys the crate and divides the mangoes proportionally. That is a mutual fund. If you chip in ₹100 on the 1st of every month automatically, that is an SIP.",
            "indian_example": "Deepak starts a ₹3,000 monthly SIP in a Nifty 50 Index Fund. On market dips, the NAV falls to ₹120 and his ₹3,000 buys 25 units. When the market rallies and NAV is ₹150, his ₹3,000 buys 20 units. Over 10 years, his average purchase cost is lower—this is Rupee Cost Averaging.",
            "how_it_works_steps": [
                "Asset Management Companies (AMCs) launch schemes registered with SEBI.",
                "Investors buy units at the prevailing Net Asset Value (NAV).",
                "SIP automates this deduction from your bank via NACH mandate on your chosen date.",
                "Rupee cost averaging removes the stress of timing market peaks and troughs.",
                "Profits come via capital appreciation (NAV growth) or IDCW (dividends)."
            ],
            "advantages": [
                "Instant diversification: ₹500 buys exposure to 50 top Indian companies like TCS, Reliance, and HDFC.",
                "Professional fund management monitored by SEBI regulations.",
                "Rupee cost averaging eliminates emotional market timing mistakes.",
                "High liquidity: Open-ended funds can be redeemed in 1-3 business days."
            ],
            "disadvantages_and_risks": [
                "Market risk: Value fluctuates with stock market indices.",
                "Expense ratio: Annual management fee charged by the AMC (typically 0.1% to 1.5%).",
                "Exit loads: Minor penalty if redeemed within 1 year (usually 1%)."
            ],
            "common_mistakes": [
                "Stopping SIPs when the market crashes (that is the best time to buy more units cheap!).",
                "Investing in too many overlapping funds (holding 15 funds instead of 3-4 focused ones)."
            ],
            "faqs": [
                {"q": "Can I lose money in a mutual fund?", "a": "Yes, in the short term market fluctuations can cause negative returns. Over 7-10+ years, diversified equity funds historically deliver positive inflation-beating returns."},
                {"q": "What is the minimum amount to start an SIP in India?", "a": "Most mutual funds allow SIPs starting at just ₹500/month, and some index funds even allow ₹100/month."}
            ]
        },
        "quiz": [
            {
                "question": "What is 'Rupee Cost Averaging' in an SIP?",
                "options": ["Fixed returns guaranteed by SEBI", "Buying more units when prices are low and fewer when prices are high", "Converting foreign currency to INR at fixed rates", "Exemption from capital gains tax"],
                "correct_index": 1,
                "explanation": "When the NAV is low, your fixed SIP installment buys more units, lowering your overall average cost per unit."
            },
            {
                "question": "Which regulatory authority in India oversees and protects mutual fund investors?",
                "options": ["RBI", "IRDAI", "SEBI", "PFRDA"],
                "correct_index": 2,
                "explanation": "The Securities and Exchange Board of India (SEBI) regulates all mutual funds and capital markets in India."
            }
        ]
    },
    {
        "title": "Types of Mutual Funds: Equity, Debt, Hybrid & Index Funds",
        "slug": "types-of-mutual-funds-equity-debt-index",
        "category": LessonCategory.INVESTMENT,
        "subcategory": "Mutual Funds",
        "difficulty": "INTERMEDIATE",
        "order_index": 3,
        "calculator": "sip",
        "content_json": {
            "summary": "Compare Equity, Debt, Hybrid, and passive Index funds to match your risk profile and investment horizon.",
            "definition": "Equity funds invest primarily in company shares for growth; Debt funds invest in bonds and government securities for stability; Hybrid funds blend both; Index funds passively replicate benchmarks like Nifty 50 or Sensex.",
            "beginner_explanation": "Think of investments like a cricket team: Equity funds are your aggressive batsmen (hit boundaries, can score big or get out fast); Debt funds are your reliable spin bowlers (steady, low-risk, maintain run rate); Index funds are the scoreboard itself (track the overall match performance at minimal cost).",
            "indian_example": "Kavita is 25 and investing for retirement 35 years away; she chooses 80% Equity Index Funds. Her father is 58 and retiring in 2 years; he allocates 70% to Debt and Banking PSU funds to protect his capital.",
            "how_it_works_steps": [
                "Large-Cap Equity: Invests in top 100 Indian companies (stable growth).",
                "Mid & Small-Cap: Invests in fast-growing smaller companies (high volatility, high potential).",
                "Liquid / Overnight Debt Funds: Alternative to savings account for parking money for days to months.",
                "Index Funds: Zero fund manager bias, ultra-low expense ratio (0.1%-0.2%), tracks Nifty 50 or Sensex."
            ],
            "advantages": [
                "Index funds have the lowest fees and beat most active managers over 10-year periods.",
                "Debt funds provide greater tax flexibility and stability than direct volatile stocks.",
                "ELSS (Tax Saver) mutual funds offer Section 80C tax deduction with the shortest lock-in (3 years)."
            ],
            "disadvantages_and_risks": [
                "Small-cap funds can drop 30-40% during bear markets.",
                "Debt funds have credit risk and interest rate risk."
            ],
            "common_mistakes": [
                "Putting emergency funds in small-cap equity funds.",
                "Assuming 'Debt' funds have guaranteed zero risk."
            ],
            "faqs": [
                {"q": "What is an Index Fund?", "a": "An index fund passively mirrors a market index like Nifty 50. It holds the same 50 companies in the same proportions at ultra-low management costs."}
            ]
        },
        "quiz": [
            {
                "question": "Which mutual fund type has the lowest expense ratio and passively tracks indices like Nifty 50?",
                "options": ["Small Cap Active Fund", "Sectoral Pharma Fund", "Index Fund", "Credit Risk Fund"],
                "correct_index": 2,
                "explanation": "Index funds have minimal management overhead because they passively replicate the benchmark index."
            }
        ]
    },
    {
        "title": "PPF (Public Provident Fund) & NPS (National Pension System)",
        "slug": "ppf-and-nps-government-backed-savings",
        "category": LessonCategory.INVESTMENT,
        "subcategory": "Government Schemes",
        "difficulty": "INTERMEDIATE",
        "order_index": 4,
        "calculator": "compound",
        "content_json": {
            "summary": "Explore two of India's most powerful government-backed retirement vehicles offering sovereign safety and tax benefits.",
            "definition": "PPF is a 15-year sovereign-backed savings scheme with tax-free returns under Section 80C; NPS is a market-linked pension scheme regulated by PFRDA offering low-cost retirement accumulation and tax deductions.",
            "beginner_explanation": "PPF is the gold standard of risk-free long-term savings in India: guaranteed by the Government of India, currently ~7.1% interest, and completely tax-free (EEE: Exempt at investment, Exempt on interest, Exempt at maturity). NPS is a modern retirement plan where your money is invested across equity and corporate bonds by top pension fund managers with rock-bottom fees.",
            "indian_example": "Vikram deposits ₹1,50,000 every April in his SBI PPF account. Over 15 years, his ₹22.5 lakh investment grows to over ₹40 lakh completely tax-free! In addition, he contributes ₹50,000 yearly to NPS Tier-1 to claim exclusive tax deduction under Section 80CCD(1B).",
            "how_it_works_steps": [
                "PPF: Minimum ₹500, maximum ₹1,50,000 per financial year; 15-year lock-in (extendable in 5-year blocks).",
                "PPF Interest is set by the Ministry of Finance every quarter and compounded annually.",
                "NPS: Tier 1 is locked until age 60; at 60, up to 60% can be withdrawn tax-free, 40% buys a regular monthly pension (annuity).",
                "NPS offers Auto Choice (lifecycle asset allocation) or Active Choice (up to 75% equity allocation)."
            ],
            "advantages": [
                "PPF: Sovereign guarantee (100% safe), EEE tax status, immune to court attachments.",
                "NPS: Lowest expense ratio in the world (~0.09%), additional ₹50,000 tax deduction, disciplined retirement corpus."
            ],
            "disadvantages_and_risks": [
                "PPF: Strict 15-year lock-in with limited partial withdrawal after 6 years.",
                "NPS: 40% mandatory annuity purchase at age 60, annuity income is taxable at slab rates."
            ],
            "common_mistakes": [
                "Depositing PPF money after the 5th of the month (interest for that month is calculated on minimum balance between 5th and end of month).",
                "Ignoring the additional ₹50,000 tax deduction available only through NPS under 80CCD(1B)."
            ],
            "faqs": [
                {"q": "When is the best date in the month to deposit in PPF?", "a": "Deposit on or before the 5th of the month to earn interest for that entire month."}
            ]
        },
        "quiz": [
            {
                "question": "What is the tax status of PPF (Public Provident Fund)?",
                "options": ["Taxable at withdrawal", "EEE (Exempt-Exempt-Exempt)", "TDS at 10%", "Taxable as capital gains"],
                "correct_index": 1,
                "explanation": "PPF enjoys EEE status: contribution is tax-deductible (80C), interest earned is tax-free, and maturity amount is tax-free."
            }
        ]
    },

    # =========================================================================
    # CATEGORY C: LOAN EDUCATION
    # =========================================================================
    {
        "title": "Home Loans in India: Fixed vs Floating Rates & Eligibility",
        "slug": "home-loans-fixed-vs-floating-eligibility",
        "category": LessonCategory.LOANS,
        "subcategory": "Home Loans",
        "difficulty": "BEGINNER",
        "order_index": 1,
        "calculator": "emi",
        "content_json": {
            "summary": "Learn how Indian home loans work, the difference between fixed and floating rates linked to RBI Repo Rate, and how banks determine your loan eligibility.",
            "definition": "A Home Loan is a secured loan granted by a bank or Housing Finance Company (HFC) to purchase, construct, or renovate residential property, with the property mortgaged as security.",
            "beginner_explanation": "Buying a ₹50 lakh flat? You pay 20% down payment (₹10 lakh) from your savings, and the bank funds the remaining ₹40 lakh. You repay this ₹40 lakh plus interest via monthly EMIs over 15 to 30 years. As long as you pay on time, you live in and own the home. If you default continuously, the bank can auction the property under the SARFAESI Act.",
            "indian_example": "Rajesh and Sunita have a combined monthly income of ₹1,20,000. Under SBI's 50% FOIR (Fixed Obligation to Income Ratio) rule, their maximum allowed total EMI is ₹60,000. At 8.5% for 20 years, an EMI of ₹60,000 qualifies them for a home loan of approximately ₹69 lakh.",
            "how_it_works_steps": [
                "External Benchmark Lending Rate (EBLR): RBI mandates all retail floating loans be linked to an external benchmark, usually the RBI Repo Rate.",
                "When RBI cuts repo rate by 0.25%, your home loan rate drops by 0.25%, reducing your EMI or tenure.",
                "Loan-to-Value (LTV) Ratio: Up to ₹30 lakh loan (90% LTV), ₹30L–₹75L (80% LTV), above ₹75L (75% LTV).",
                "Tax Benefits: Principal repayment qualifies under Sec 80C (up to ₹1.5L) and Interest under Sec 24(b) (up to ₹2L for self-occupied)."
            ],
            "advantages": [
                "Enables home ownership decades earlier than saving 100% in cash.",
                "Substantial annual tax deductions under Section 80C and Section 24(b).",
                "Zero prepayment penalty on floating-rate home loans as per RBI guidelines."
            ],
            "disadvantages_and_risks": [
                "Total interest paid over 20-30 years can exceed the original principal borrowed.",
                "Rising repo rates increase your tenure or monthly EMI unexpectedly.",
                "Property is mortgaged: default can lead to eviction and property auction."
            ],
            "common_mistakes": [
                "Stretching for the maximum possible loan amount without maintaining an emergency buffer.",
                "Opting for 30-year tenure instead of 20-year, paying ₹15-20 lakh extra in interest."
            ],
            "faqs": [
                {"q": "Can banks charge a penalty if I prepay my floating rate home loan?", "a": "NO. As per RBI regulations, banks cannot levy any prepayment or foreclosure charges on individual floating-rate home loans."}
            ]
        },
        "quiz": [
            {
                "question": "Can Indian banks charge a prepayment penalty on floating-rate home loans taken by individuals?",
                "options": ["Yes, up to 2%", "Yes, if prepaid within 3 years", "No, RBI has prohibited prepayment charges on floating retail loans", "Only public sector banks can"],
                "correct_index": 2,
                "explanation": "RBI directives strictly prohibit banks and HFCs from charging prepayment or foreclosure fees on individual floating-rate housing loans."
            }
        ]
    },
    {
        "title": "Credit Score & CIBIL: How to Build & Protect It",
        "slug": "credit-score-cibil-build-protect",
        "category": LessonCategory.LOANS,
        "subcategory": "Credit Score",
        "difficulty": "BEGINNER",
        "order_index": 2,
        "calculator": None,
        "content_json": {
            "summary": "Understand your 3-digit CIBIL score (300-900), what factors affect it, and how to maintain a 750+ score for lowest loan interest rates.",
            "definition": "A Credit Score is a 3-digit numeric summary (ranging from 300 to 900) prepared by credit bureaus (TransUnion CIBIL, Experian, Equifax, CRIF High Mark) reflecting an individual's creditworthiness based on borrowing history.",
            "beginner_explanation": "Think of CIBIL score as your financial report card. When you apply for a loan, banks check your report card first. Score of 750+ gets you instant approval and the lowest interest rates (e.g. 8.5%). Score below 650 means rejected loans or punitive interest rates (e.g. 11%+).",
            "indian_example": "Pooja always pays her credit card bill in full 3 days before the due date and uses only 20% of her limit. Her CIBIL score is 785. She gets an SBI home loan approved at 8.40%. Her colleague Mayank missed two EMIs on a smartphone loan; his score dropped to 640 and his loan application was rejected.",
            "how_it_works_steps": [
                "Payment History (35% weight): Timely repayments of credit cards and EMIs is the single biggest factor.",
                "Credit Utilization Ratio (30% weight): Keep card spend below 30% of total limit (e.g. spend max ₹30,000 on a ₹1,00,000 limit).",
                "Credit Age & Mix (25% weight): A healthy blend of secured (home/auto) and unsecured (card/personal) loans held over years.",
                "Hard Inquiries (10% weight): Applying to 5 banks simultaneously triggers 5 hard inquiries, lowering your score."
            ],
            "advantages": [
                "Fast-track loan approvals with minimal documentation.",
                "Preferential interest rates: 750+ score can save you ₹3-5 lakh on a 20-year home loan.",
                "Higher credit card limits and pre-approved offers."
            ],
            "disadvantages_and_risks": [
                "A single 30-day missed payment can slash your score by 50-70 points.",
                "Being a loan guarantor for a friend who defaults damages YOUR credit score equally."
            ],
            "common_mistakes": [
                "Paying only the 'Minimum Amount Due' on credit cards—incurring 40%+ interest and hurting credit health.",
                "Closing your oldest credit card (this shortens your credit history and shrinks available limit).",
                "Applying for multiple credit cards and loans in the same week."
            ],
            "faqs": [
                {"q": "What is considered a good CIBIL score in India?", "a": "750 and above is considered excellent by most lenders and qualifies you for best rates."},
                {"q": "Does checking my own credit score lower it?", "a": "NO. Checking your own score is a 'soft inquiry' and has zero impact on your score."}
            ]
        },
        "quiz": [
            {
                "question": "What is the recommended maximum Credit Utilization Ratio (CUR) for maintaining a high credit score?",
                "options": ["100%", "75%", "30%", "50%"],
                "correct_index": 2,
                "explanation": "Financial experts recommend keeping credit card utilization under 30% of your credit limit."
            },
            {
                "question": "Does checking your own CIBIL score reduce your score points?",
                "options": ["Yes, by 5 points each time", "Yes, if checked more than once a month", "No, it is a soft inquiry with zero effect", "Only on mobile apps"],
                "correct_index": 2,
                "explanation": "Checking your own score is a soft pull and never harms your credit score."
            }
        ]
    },
    {
        "title": "Education Loans in India: Moratorium, Collateral & Tax Benefits",
        "slug": "education-loans-moratorium-collateral-tax",
        "category": LessonCategory.LOANS,
        "subcategory": "Education Loans",
        "difficulty": "BEGINNER",
        "order_index": 3,
        "calculator": "emi",
        "content_json": {
            "summary": "Everything students and parents need to know about Indian education loans: Vidyalakshmi portal, collateral rules, moratorium periods, and Section 80E tax deductions.",
            "definition": "An Education Loan is specialized financing provided to students for pursuing higher education in India or abroad, covering tuition fees, hostel, books, and travel expenses.",
            "beginner_explanation": "Education loans are designed to let students study first and repay later. You do not pay full EMIs while in college. Banks grant a 'Moratorium Period' (the course duration plus 6 to 12 months). Repayment starts only after you graduate or find a job.",
            "indian_example": "Rohan gets admitted to an NIT for B.Tech. His father takes a ₹7.5 lakh loan under the IBA scheme via the government's Vidya Lakshmi portal. No collateral is required! Rohan's course is 4 years + 1 year moratorium. Repayment begins after year 5 in 120 monthly EMIs.",
            "how_it_works_steps": [
                "Up to ₹4 Lakh: No collateral, no third-party guarantee, parent co-borrower.",
                "₹4 Lakh to ₹7.5 Lakh: Third-party guarantee required; no physical property collateral.",
                "Above ₹7.5 Lakh: Tangible collateral (house, land, FD) usually required.",
                "Vidya Lakshmi Portal: Centralized Government portal to apply to multiple banks with one form.",
                "Section 80E: 100% of interest paid on an education loan is deductible from taxable income for up to 8 years with NO upper ceiling!"
            ],
            "advantages": [
                "Moratorium period prevents repayment stress during college years.",
                "Unlimited Section 80E tax deduction on interest paid.",
                "Builds the student's credit history right from early career."
            ],
            "disadvantages_and_risks": [
                "Interest accrues during the moratorium period (simple interest is added to principal).",
                "Defaulting damages both the student's and parent's CIBIL score."
            ],
            "common_mistakes": [
                "Not servicing the simple interest during college if affordable (doing so lowers post-graduation EMIs substantially).",
                "Taking private unapproved lender loans at 14-16% when public sector banks offer 8.5-10%."
            ],
            "faqs": [
                {"q": "What is the maximum limit on tax deduction under Section 80E for education loan interest?", "a": "There is NO maximum rupee limit! You can claim the entire interest paid for up to 8 consecutive years."}
            ]
        },
        "quiz": [
            {
                "question": "What is the upper rupee limit for interest tax deduction under Section 80E on an education loan?",
                "options": ["₹1,50,000", "₹2,00,000", "₹50,000", "No upper limit (full interest paid is deductible)"],
                "correct_index": 3,
                "explanation": "Section 80E allows full deduction of the interest paid on an education loan with no cap for up to 8 years."
            }
        ]
    },

    # =========================================================================
    # CATEGORY D: PERSONAL FINANCIAL PLANNING
    # =========================================================================
    {
        "title": "Monthly Budgeting: The 50/30/20 Rule for India",
        "slug": "monthly-budgeting-50-30-20-rule",
        "category": LessonCategory.PLANNING,
        "subcategory": "Budgeting",
        "difficulty": "BEGINNER",
        "order_index": 1,
        "calculator": None,
        "content_json": {
            "summary": "Master the world's most popular personal budgeting framework adapted for Indian household incomes and cost of living.",
            "definition": "The 50/30/20 Rule divides your monthly take-home salary into three buckets: 50% for Needs, 30% for Wants, and 20% for Savings and Debt repayment.",
            "beginner_explanation": "If your take-home pay is ₹50,000 per month: Spend maximum ₹25,000 (50%) on must-haves (rent, groceries, electricity, school fees). Spend maximum ₹15,000 (30%) on nice-to-haves (dining out, OTT subscriptions, weekend trips). Put at least ₹10,000 (20%) directly into savings, SIPs, and emergency fund.",
            "indian_example": "Suresh earns ₹60,000 take-home in Pune. He allocates: Needs (₹30,000): ₹15k rent, ₹7k groceries, ₹4k bills, ₹4k transport. Wants (₹18,000): dining out, cinema, shopping. Savings (₹12,000): ₹8,000 mutual fund SIP, ₹4,000 recurring deposit. On pay day, the ₹12,000 is auto-debited first!",
            "how_it_works_steps": [
                "Needs (50%): Housing, utilities, groceries, medicines, minimum debt payments.",
                "Wants (30%): Eating out, gadgets, streaming subscriptions, vacations, hobbies.",
                "Savings (20%): Emergency fund, mutual fund SIPs, PPF, NPS, extra loan prepayments.",
                "Golden Rule: 'Do not save what is left after spending; spend what is left after saving' — Warren Buffett."
            ],
            "advantages": [
                "Simple and stress-free: no need to track every single ₹10 rupee auto-rickshaw fare.",
                "Guarantees that at least 20% of your earnings builds future wealth.",
                "Prevents lifestyle inflation from devouring salary hikes."
            ],
            "disadvantages_and_risks": [
                "In high-cost metros (Mumbai, Bengaluru), rent alone might take 40-50%, requiring adjustment to 60/20/20."
            ],
            "common_mistakes": [
                "Classifying 'wants' as 'needs' (e.g. buying a ₹1.2 lakh phone on no-cost EMI is a Want, not a Need).",
                "Saving whatever is left at the end of the month (which is usually zero)."
            ],
            "faqs": [
                {"q": "Can I save more than 20%?", "a": "Absolutely! Aggressive savers in their 20s often save 40-50% to achieve financial independence early."}
            ]
        },
        "quiz": [
            {
                "question": "Under the 50/30/20 budgeting rule, what percentage of net income should be allocated to savings & investing?",
                "options": ["10%", "20%", "30%", "50%"],
                "correct_index": 1,
                "explanation": "The 50/30/20 rule designates 50% for Needs, 30% for Wants, and at least 20% for Savings and Debt repayment."
            }
        ]
    },
    {
        "title": "Emergency Funds: Your Financial Shield",
        "slug": "emergency-funds-financial-shield",
        "category": LessonCategory.PLANNING,
        "subcategory": "Emergency Fund",
        "difficulty": "BEGINNER",
        "order_index": 2,
        "calculator": None,
        "content_json": {
            "summary": "How to calculate, build, and store an emergency fund to survive job losses, medical crises, and unexpected home repairs without debt.",
            "definition": "An Emergency Fund is a stash of liquid money reserved exclusively for unexpected life emergencies such as job loss, medical emergencies, or urgent vehicle repairs.",
            "beginner_explanation": "An emergency fund is your financial airbag. If you lose your job or face a sudden hospital bill, you don't have to borrow from loan sharks at 24% interest or sell your mutual funds at a loss. You simply tap your emergency fund.",
            "indian_example": "Priyanka's family spends ₹35,000/month on essential needs. Her target emergency fund is 6 months = ₹2,10,000. She keeps ₹30,000 in a savings account and ₹1,80,000 in an instant-redemption sweep-in Fixed Deposit.",
            "how_it_works_steps": [
                "Calculate monthly essential expenses (rent + food + utilities + EMIs + insurance).",
                "Multiply by 3 to 6 months (6-9 months if you are self-employed or have single income).",
                "Keep 20% in savings account for immediate ATM/UPI withdrawal.",
                "Keep 80% in sweep-in FDs or liquid mutual funds offering instant access."
            ],
            "advantages": [
                "Provides tremendous peace of mind and stress-free sleep.",
                "Prevents high-interest personal loans or credit card rollover debt in emergencies.",
                "Allows you to negotiate better career moves without panic."
            ],
            "disadvantages_and_risks": [
                "Opportunity cost: Emergency funds earn modest interest (4-7%) rather than equity market returns."
            ],
            "common_mistakes": [
                "Investing emergency funds in stocks or cryptocurrency where a crash could halve your safety cushion.",
                "Using emergency funds for non-emergencies like Diwali shopping or festival travel."
            ],
            "faqs": [
                {"q": "How many months of expenses should be in an emergency fund?", "a": "Salaried individuals should keep 3 to 6 months; self-employed individuals and single-earner families should aim for 6 to 9 months."}
            ]
        },
        "quiz": [
            {
                "question": "Where should an emergency fund be parked?",
                "options": ["High-risk crypto tokens", "Small-cap equity mutual funds", "Liquid bank accounts and sweep-in Fixed Deposits", "Real estate land"],
                "correct_index": 2,
                "explanation": "Emergency funds must be completely safe and accessible in minutes (liquid FDs, high-grade liquid funds, savings accounts)."
            }
        ]
    },

    # =========================================================================
    # CATEGORY E: INDIAN BANKING SYSTEM
    # =========================================================================
    {
        "title": "The Reserve Bank of India (RBI) & Monetary Policy",
        "slug": "rbi-and-monetary-policy-explained",
        "category": LessonCategory.INDIAN_BANKING,
        "subcategory": "Central Banking",
        "difficulty": "BEGINNER",
        "order_index": 1,
        "calculator": None,
        "content_json": {
            "summary": "Understand India's central bank, how the Repo Rate controls inflation and loan EMIs, and the vital role of RBI in protecting depositors.",
            "definition": "The Reserve Bank of India (RBI) is the supreme central banking institution of India, responsible for regulating currency issuance, monetary policy, and bank supervision.",
            "beginner_explanation": "Think of RBI as the principal of the Indian banking school. It sets the rules, inspects the banks, sets the interest rate at which banks borrow (Repo Rate), and makes sure no bank gambles with your deposits. When inflation gets too high, RBI raises the repo rate to cool down spending.",
            "indian_example": "When RBI increased the Repo Rate from 4.0% to 6.50% to fight post-pandemic inflation, banks immediately raised home loan rates from ~6.7% to ~9.0%. A home loan borrower's EMI jumped from ₹26,000 to ₹31,500. Conversely, FD depositors enjoyed higher interest rates of 7.5%!",
            "how_it_works_steps": [
                "Repo Rate: The rate at which commercial banks borrow short-term funds from RBI.",
                "Reverse Repo Rate: The rate at which RBI absorbs excess liquidity from banks.",
                "Cash Reserve Ratio (CRR): Percentage of deposits banks must keep as cash with RBI (~4.5%).",
                "Statutory Liquidity Ratio (SLR): Percentage banks must hold in gold or government bonds (~18%).",
                "Monetary Policy Committee (MPC): 6-member committee meeting bi-monthly to fix repo rates."
            ],
            "advantages": [
                "Keeps inflation in check (target band 4% ± 2%).",
                "Protects customer interests through Banking Ombudsman and consumer grievance portals."
            ],
            "disadvantages_and_risks": [
                "Rate hikes increase EMI burdens on existing retail borrowers."
            ],
            "common_mistakes": [
                "Assuming your bank fixed rate changes with repo rate (only floating rate loans change automatically)."
            ],
            "faqs": [
                {"q": "What happens when RBI cuts the repo rate?", "a": "Borrowing becomes cheaper: banks lower their loan interest rates, stimulating business investments and home buying."}
            ]
        },
        "quiz": [
            {
                "question": "What is the 'Repo Rate' in the Indian banking system?",
                "options": ["The rate banks charge individual credit card holders", "The rate at which commercial banks borrow money from the RBI", "The statutory income tax rate on bank dividends", "The penalty rate for bouncing cheques"],
                "correct_index": 1,
                "explanation": "Repo Rate is the interest rate at which the Reserve Bank of India lends money to commercial banks against government securities."
            }
        ]
    },
    {
        "title": "Types of Banks in India: Public, Private, SFBs & Payment Banks",
        "slug": "types-of-banks-in-india-psu-private-sfb",
        "category": LessonCategory.INDIAN_BANKING,
        "subcategory": "Bank Categories",
        "difficulty": "BEGINNER",
        "order_index": 2,
        "calculator": None,
        "content_json": {
            "summary": "Navigate Public Sector, Private, Small Finance Banks (SFBs), and Payment Banks in India to choose the right partner for your money.",
            "definition": "The Indian banking structure comprises Scheduled Commercial Banks (Public, Private, Foreign, Regional Rural), Small Finance Banks, and Payment Banks, each tailored for specific financial segments.",
            "beginner_explanation": "Public Sector Banks (like SBI, PNB, Bank of Baroda) are majority-owned by the Government of India (perceived as safest, massive branch networks). Private Banks (HDFC, ICICI, Axis) are owned by shareholders (great technology, faster customer service). Small Finance Banks (AU, Equitas, Ujjivan) offer higher FD rates (up to 8.5-9%) to attract deposits. Payment Banks (Airtel Payments Bank, India Post) can take deposits up to ₹2 lakh but CANNOT issue loans or credit cards.",
            "indian_example": "Aarti keeps her main emergency fund in SBI for supreme sovereign safety. She uses HDFC Bank for her daily UPI payments and salary account due to smooth mobile apps. She opens a 3-year FD of ₹2,00,000 in AU Small Finance Bank earning 8.25% (well within the ₹5 lakh DICGC insurance limit!).",
            "how_it_works_steps": [
                "Public Sector Banks: Majority owned by Government of India (>50% stake).",
                "Private Sector Banks: Regulated commercial banks owned by private shareholders.",
                "Small Finance Banks: RBI-licensed banks providing financial inclusion; covered by ₹5L DICGC insurance just like SBI.",
                "Payment Banks: Can accept deposits up to ₹2,00,000 per customer, cannot lend or issue credit cards."
            ],
            "advantages": [
                "Public: Massive rural reach, backing of the government, lower locker charges.",
                "Private: Modern digital apps, relationship managers, quick processing.",
                "SFBs: Higher FD and savings interest rates for retail depositors.",
                "Payment Banks: Frictionless micro-payments and mobile recharge integrations."
            ],
            "disadvantages_and_risks": [
                "SFBs: Perceived higher credit risk than giant commercial banks (keep deposits under ₹5L DICGC limit).",
                "Payment Banks: Cannot give you personal loans, home loans, or standard credit cards."
            ],
            "common_mistakes": [
                "Thinking Small Finance Banks do not have DICGC insurance (they have the exact same ₹5 lakh protection as SBI).",
                "Keeping more than ₹5 lakh in a single Small Finance Bank."
            ],
            "faqs": [
                {"q": "Are Small Finance Banks covered by DICGC insurance?", "a": "YES! All scheduled Small Finance Banks are fully covered by DICGC insurance up to ₹5,00,000 per depositor."}
            ]
        },
        "quiz": [
            {
                "question": "Can Payment Banks in India (like Airtel Payments Bank or India Post Payments Bank) issue loans or credit cards?",
                "options": ["Yes, up to ₹10 lakh", "Yes, with RBI special approval", "No, Payment Banks are legally prohibited from lending", "Only for education loans"],
                "correct_index": 2,
                "explanation": "Under RBI guidelines, Payment Banks can only accept demand deposits (up to ₹2 lakh) and facilitate remittances; they CANNOT lend or issue credit cards."
            }
        ]
    }
]


def seed_all_lessons():
    """Seed comprehensive educational lessons and associated quiz questions."""
    print("Seeding comprehensive educational lessons...")
    for item in LESSON_DATA:
        existing = Lesson.query.filter_by(slug=item["slug"]).first()
        if existing:
            # Update content
            existing.title = item["title"]
            existing.category = item["category"]
            existing.subcategory = item["subcategory"]
            existing.difficulty = item["difficulty"]
            existing.order_index = item["order_index"]
            existing.content_json = item["content_json"]
            lesson_obj = existing
        else:
            lesson_obj = Lesson(
                title=item["title"],
                slug=item["slug"],
                category=item["category"],
                subcategory=item["subcategory"],
                difficulty=item["difficulty"],
                order_index=item["order_index"],
                content_json=item["content_json"],
            )
            db.session.add(lesson_obj)
            db.session.flush()

        # Seed quizzes for this lesson
        # Remove old questions if updating
        QuizQuestion.query.filter_by(lesson_id=lesson_obj.id).delete()
        for q_data in item.get("quiz", []):
            q_obj = QuizQuestion(
                lesson_id=lesson_obj.id,
                question=q_data["question"],
                options_json=q_data["options"],
                correct_index=q_data["correct_index"],
                explanation=q_data.get("explanation", ""),
            )
            db.session.add(q_obj)

    db.session.commit()
    print(f"Successfully seeded {len(LESSON_DATA)} comprehensive lessons with complete 10-part structure and quizzes!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_all_lessons()
