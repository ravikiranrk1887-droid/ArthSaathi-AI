"""
ai_service.py
=============
Gemini AI integration and Intelligent Fallback Knowledge Engine for ArthSaathi AI.

Security & Responsibility:
- API key is loaded only from environment variable GEMINI_API_KEY.
- The key is never logged or exposed to client-side JavaScript.
- ArthSaathi provides educational responses in INR with appropriate disclaimers.
- If the Gemini API is unreachable or not configured, the built-in financial
  knowledge engine provides accurate, detailed answers to common questions.
"""

import os
import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

ARTHSAATHI_SYSTEM_PROMPT = """You are ArthSaathi AI, an expert, friendly and responsible financial education assistant
specialised in Indian personal finance and banking.

## Your Mission
Help everyday citizens in India (students, beginners, working professionals, families) understand
banking, savings, investments, loans, and personal budgeting in simple, jargon-free English.

## Rules & Principles
1. Always use Indian Rupee (₹) and Indian numbering terms (Lakh, Crore) in examples.
2. When answering calculations (EMI, SIP, FD), show the exact formula and walk through the math step-by-step.
3. Never guarantee returns or recommend specific stocks/cryptocurrency.
4. Distinguish verified bank information from general guidance. Remind users that advertised rates are starting indicators.
5. Always advise consulting a SEBI-registered advisor for investments or a CA for complex tax matters.
6. Reference relevant Indian institutions: RBI, SEBI, NPCI, DICGC, PFRDA, IRDAI.
7. Be encouraging, concise, and structured (use bullet points and bold headings).
"""

# ---------------------------------------------------------------------------
# Comprehensive Built-In Knowledge Base (Fallback & Instant Answering)
# ---------------------------------------------------------------------------
FALLBACK_KNOWLEDGE_BASE = [
    {
        "keywords": ["what is a bank", "how does a bank work", "how banking work", "what is bank"],
        "answer": """### 🏦 What is a Bank & How Does It Work?

A **bank** is a financial institution licensed and regulated by the **Reserve Bank of India (RBI)** to accept deposits and issue loans.

#### How the Banking Engine Works:
1. **Deposits:** You and other citizens deposit savings into accounts. The bank pays you modest interest (e.g. 3%–4% on Savings, 7% on FDs).
2. **Reserves:** Under RBI guidelines, the bank locks away reserves for safety:
   - **Cash Reserve Ratio (CRR ~4.5%):** Kept as liquid cash with RBI.
   - **Statutory Liquidity Ratio (SLR ~18%):** Kept in gold and government securities.
3. **Lending:** The remaining funds are lent to home buyers, car buyers, and businesses at higher rates (e.g. 8.5%–14%).
4. **Net Interest Margin (Spread):** The difference between the 8.5% earned on loans and the 3.5% paid on deposits covers operating expenses and generates profit.

> **Safety Assurance:** Under the DICGC Act, your deposits are insured up to **₹5,00,000 per depositor per bank** in India."""
    },
    {
        "keywords": ["sip", "systematic investment", "1000 example", "explain sip"],
        "answer": """### 📈 Understanding SIP with a ₹1,000 Example

A **Systematic Investment Plan (SIP)** is a disciplined way to invest a fixed amount of money every month into a mutual fund.

#### The ₹1,000 / Month Example:
- **Monthly Investment:** ₹1,000
- **Duration:** 15 Years (180 months)
- **Total Deposited:** ₹1,000 × 180 = **₹1,80,000**
- **Expected Historical Return (e.g. 12% p.a. for diversified equity index):**
  - **Estimated Future Corpus:** **₹5,04,576**
  - **Estimated Wealth Created:** **₹3,24,576** (Your money nearly triples!)

#### Why SIP Works (Rupee Cost Averaging):
- When the market dips and NAV is low (₹100), your ₹1,000 buys **10 units**.
- When the market rallies and NAV is high (₹125), your ₹1,000 buys **8 units**.
- You automatically buy more units at discount prices without having to time the market!

*Disclaimer: Mutual fund investments are subject to market risks. Past returns are not guaranteed.*"""
    },
    {
        "keywords": ["miss my emi", "missed emi", "bounce emi", "what happens if i miss"],
        "answer": """### ⚠️ What Happens If You Miss an EMI in India?

Missing an Equated Monthly Instalment (EMI) has four immediate consequences:

1. **ECS / NACH Bounce Charges:** Both your bank and the lending bank levy cheque/NACH bounce penalties (typically ₹250 to ₹600 + GST each).
2. **Late Payment Penalties:** Lenders charge late payment interest (usually 1%–2% per month on the overdue amount).
3. **Severe Damage to CIBIL Score:**
   - Lenders report delays (Days Past Due or DPD) to CIBIL, Experian, Equifax, and CRIF.
   - A 30-day delay can drop your score by **50 to 70 points**, making future credit very expensive.
4. **Loss of Collateral (If Default Exceeds 90 Days):**
   - After 90 days, a loan is categorized as a **Non-Performing Asset (NPA)**.
   - For home or auto loans, banks can initiate recovery proceedings under the **SARFAESI Act** to auction the asset.

#### What Should You Do Immediately?
- Contact your bank's branch manager *before* the due date.
- Request an EMI date alignment, a tenure extension (which reduces monthly EMI), or a temporary moratorium."""
    },
    {
        "keywords": ["fd vs rd", "difference between fd and rd", "fixed deposit and recurring deposit"],
        "answer": """### 🔄 Difference Between FD (Fixed Deposit) and RD (Recurring Deposit)

Both are low-risk term deposit instruments offered by Indian banks, but they differ in how you fund them:

| Parameter | Fixed Deposit (FD) | Recurring Deposit (RD) |
|---|---|---|
| **Investment Mode** | Lump-sum (one-time) | Monthly installment |
| **Minimum Amount** | Usually ₹1,000 – ₹5,000 | Usually ₹500 / month |
| **Ideal For** | When you have a lump-sum (bonus, inheritance, sale) | Salaried earners saving part of monthly income |
| **Interest Rate** | Fixed for entire tenure (e.g. 6.5% – 7.75%) | Same as FD rate for equivalent tenure |
| **Compounding** | Quarterly compounding | Quarterly compounding on each installment |
| **Tax (TDS)** | 10% TDS if interest > ₹40,000/yr (₹50k seniors) | 10% TDS if interest > ₹40,000/yr (₹50k seniors) |
| **DICGC Safety** | Insured up to ₹5 Lakh | Insured up to ₹5 Lakh |"""
    },
    {
        "keywords": ["5 lakh at 9%", "borrow 5 lakh", "repay if i borrow", "5 lakh for 5 years"],
        "answer": """### 🧮 Loan Calculation: ₹5,00,000 at 9.0% for 5 Years

Here is the exact mathematical breakdown using the standard Indian banking formula:

#### Key Inputs:
- **Principal (P):** ₹5,00,000
- **Annual Rate (R):** 9.0% (Monthly rate $r = 9 / 12 / 100 = 0.0075$)
- **Tenure (n):** 5 Years = 60 Months

#### Results:
- **Monthly EMI:** **₹10,379**
- **Total Payment (EMI × 60):** **₹6,22,755**
- **Total Interest Paid:** **₹1,22,755**

#### Summary:
You will repay ₹6,22,755 in total over 5 years. That means for every ₹100 borrowed, you pay approximately ₹24.5 in interest charges."""
    },
    {
        "keywords": ["education loan", "vidyalakshmi", "moratorium"],
        "answer": """### 🎓 Education Loans in India Explained

Education loans help students fund degrees in India or abroad, covering tuition fees, hostel, library, and travel costs.

#### Key Features:
1. **Collateral Limits (IBA Model Scheme):**
   - **Up to ₹4 Lakh:** No collateral, no third-party guarantor. Only student + parent as co-borrower.
   - **₹4 Lakh to ₹7.5 Lakh:** Third-party guarantee required; no property collateral.
   - **Above ₹7.5 Lakh:** Tangible collateral (house, land, fixed deposit) required.
2. **Moratorium Period (Study Break):**
   - You do NOT pay full EMIs while studying.
   - Repayment begins **Course Duration + 6 to 12 months** after graduation (or when you get a job).
3. **Section 80E Tax Deduction:**
   - **100% of interest paid** on an education loan is deductible from your taxable income for up to 8 years with **no upper ceiling**!
4. **Portal:** Apply directly through the Government of India's **Vidya Lakshmi Portal** (vidyalakshmi.co.in)."""
    },
    {
        "keywords": ["sbi and hdfc", "sbi vs hdfc", "home loan difference"],
        "answer": """### 🏛️ SBI vs HDFC Bank Home Loans: Key Differences

| Feature | State Bank of India (SBI) | HDFC Bank |
|---|---|---|
| **Bank Category** | Public Sector (Govt of India >50%) | Private Sector |
| **Starting Rate (Indicative)** | ~8.50% – 9.15% (EBLR linked) | ~8.70% – 9.40% (Repo benchmark) |
| **Processing Fee** | Usually 0.35% + GST (frequent festival waivers) | Up to 0.50% + GST (min ₹3,000) |
| **Sanction Speed** | Moderate (rigorous title & legal checks) | Very fast digital processing |
| **Overdraft Home Loan** | SBI Maxgain (park surplus to save interest) | HDFC Reach / Max loan facility |
| **Prepayment Penalty** | **0%** on individual floating loans | **0%** on individual floating loans |
| **Women Borrower Discount** | 0.05% concession on interest | Usually 0.05% concession |"""
    },
    {
        "keywords": ["how does compound interest work", "compounding work", "compound interest"],
        "answer": """### ⚡ How Compound Interest Works: The 8th Wonder

**Compound Interest** is interest earned on your original principal **plus** all the interest previously accumulated.

#### Example: ₹1,00,000 at 10% Annual Return
- **Year 1:** ₹1,00,000 + ₹10,000 interest = **₹1,10,000**
- **Year 2:** 10% on ₹1,10,000 = ₹11,000 interest → Total: **₹1,21,000**
- **Year 3:** 10% on ₹1,21,000 = ₹12,100 interest → Total: **₹1,33,100**
- **Year 20:** **₹6,72,750**! (Simple interest would have yielded only ₹3,00,000).

#### The Formula:
$$A = P \\times \\left(1 + \\frac{r}{n}\\right)^{n \\times t}$$

Where $P$ is principal, $r$ is annual rate, $n$ is compounding frequency per year, and $t$ is time in years."""
    },
    {
        "keywords": ["credit score", "what is a credit score", "cibil score"],
        "answer": """### 🎯 What is a Credit Score (CIBIL Score)?

Your **Credit Score** is a 3-digit number between **300 and 900** that measures your reliability in repaying debt.

#### The Score Ranges:
- **750 to 900 (Excellent):** Instant loan approvals, lowest interest rates, and highest card limits.
- **700 to 749 (Good):** Approved by most banks at standard rates.
- **650 to 699 (Fair):** Lenders may charge higher rates or ask for extra collateral.
- **Below 650 (Poor):** High risk of loan rejection.

#### Top 3 Rules to Maintain 750+:
1. **Pay 100% on time:** Never miss a due date.
2. **Keep Credit Card Utilization under 30%:** If your card limit is ₹1,00,000, don't spend more than ₹30,000 in a billing cycle.
3. **Avoid applying to 5 banks simultaneously:** Each triggers a hard credit inquiry that temporarily dings your score."""
    },
    {
        "keywords": ["save money from salary", "how can i save", "monthly salary savings"],
        "answer": """### 💡 How to Save Money from Your Monthly Salary (India Guide)

Follow this 5-step roadmap to start saving even on a modest salary:

1. **Follow the 50/30/20 Rule:**
   - **50% for Needs:** Rent, groceries, electricity, school fees.
   - **30% for Wants:** Dining out, OTT subscriptions, weekend movies.
   - **20% for Savings (Minimum):** Auto-debited into SIPs and emergency fund on pay day.
2. **Pay Yourself First (Automate):**
   - Schedule your mutual fund SIP and RD on the **2nd or 3rd of the month** (right after salary hits).
   - Never wait until the end of the month to save 'whatever is left'.
3. **Build an Emergency Fund of 6 Months:**
   - Park this in a sweep-in FD or high-grade liquid mutual fund.
4. **Audit Recurring Subscriptions:**
   - Cancel unused streaming apps, gym memberships, or card subscriptions.
5. **Get Proper Health & Term Insurance:**
   - A single hospital bill without insurance can wipe out 5 years of family savings."""
    }
]


def _match_fallback(message: str) -> Optional[str]:
    """Check if the user message matches any question in our rich knowledge base."""
    msg_clean = message.lower().strip()
    for item in FALLBACK_KNOWLEDGE_BASE:
        for kw in item["keywords"]:
            if kw in msg_clean:
                return item["answer"]
    return None


def chat_with_finbot(message: str, conversation_history: list[dict] | None = None) -> dict:
    """Send user message to ArthSaathi AI (via Gemini if key present, else intelligent knowledge engine)."""
    if not message or not message.strip():
        return {"success": False, "response": "", "error": "Message cannot be empty."}

    msg = message.strip()
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    # If API key is available, call Gemini API
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=ARTHSAATHI_SYSTEM_PROMPT,
            )
            chat_session = model.start_chat(history=conversation_history or [])
            resp = chat_session.send_message(msg)
            return {"success": True, "response": resp.text, "error": None}
        except Exception as exc:
            logger.warning("Gemini API call failed (%s). Falling back to Knowledge Engine.", exc)

    # Fallback to Built-in Financial Knowledge Engine
    matched_answer = _match_fallback(msg)
    if matched_answer:
        return {
            "success": True,
            "response": matched_answer + "\n\n*(Answered via ArthSaathi Financial Knowledge Engine)*",
            "error": None,
        }

    # General Intelligent Educational Response
    general_reply = (
        f"### 🤖 ArthSaathi AI Financial Guidance\n\n"
        f"Thank you for asking about: **\"{msg}\"**.\n\n"
        f"In Indian personal finance, here are key fundamentals to keep in mind:\n\n"
        f"1. **Safety First:** Maintain an emergency fund covering 3–6 months of household expenses in liquid FDs or savings accounts.\n"
        f"2. **Beat Inflation:** For long-term goals (5+ years away), consider diversified equity mutual funds via monthly SIPs.\n"
        f"3. **Credit Health:** Always pay credit card bills and loan EMIs in full before the due date to protect your 750+ CIBIL score.\n"
        f"4. **Tax Efficiency:** Utilize Section 80C (PPF, ELSS, EPF up to ₹1.5L) and Section 80CCD(1B) (NPS up to ₹50k).\n\n"
        f"💡 *Tip: Try asking one of the suggested sample questions below, or explore our interactive Calculators and Bank Comparison tools!*"
    )
    return {"success": True, "response": general_reply, "error": None}


def is_ai_available() -> bool:
    """Return True if a valid Gemini API key is configured in the environment."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    return bool(key and key != "your_gemini_api_key_here")
