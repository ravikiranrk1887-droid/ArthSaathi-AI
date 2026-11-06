"""
calculator_service.py
=====================
Pure-Python financial calculators for ArthSaathi AI.

All calculations use standard financial mathematics — no AI involvement.
Results are in INR (₹) unless otherwise noted.
"""

import math


# ---------------------------------------------------------------------------
# EMI Calculator
# ---------------------------------------------------------------------------

def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> dict:
    """Calculate EMI using the standard formula:

    EMI = P × r × (1+r)^n / ((1+r)^n - 1)

    Args:
        principal      : Loan amount in ₹
        annual_rate    : Annual interest rate in % (e.g. 8.5 for 8.5%)
        tenure_months  : Loan tenure in months

    Returns:
        dict with emi, total_interest, total_payment, and full amortization schedule.
    """
    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")
    if tenure_months <= 0:
        raise ValueError("Tenure must be at least 1 month.")
    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    n = tenure_months

    if annual_rate == 0:
        emi = principal / n
        schedule = [
            {
                "month": m,
                "emi": round(emi, 2),
                "principal": round(emi, 2),
                "interest": 0.0,
                "balance": round(max(principal - emi * m, 0), 2),
            }
            for m in range(1, n + 1)
        ]
        return {
            "emi": round(emi, 2),
            "total_interest": 0.0,
            "total_payment": round(principal, 2),
            "amortization": schedule,
        }

    r = annual_rate / 12 / 100
    emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    total_payment = emi * n
    total_interest = total_payment - principal

    schedule = []
    balance = principal
    for month in range(1, n + 1):
        interest_component = balance * r
        principal_component = emi - interest_component
        balance -= principal_component
        schedule.append(
            {
                "month": month,
                "emi": round(emi, 2),
                "principal": round(principal_component, 2),
                "interest": round(interest_component, 2),
                "balance": round(max(balance, 0), 2),
            }
        )

    return {
        "emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment, 2),
        "amortization": schedule,
    }


# ---------------------------------------------------------------------------
# Fixed Deposit Calculator
# ---------------------------------------------------------------------------

def calculate_fd(principal: float, annual_rate: float, years: float, compounding_freq: int) -> dict:
    """Fixed Deposit maturity using compound interest:

    A = P × (1 + r/n)^(n×t)

    Args:
        principal        : Deposit amount in ₹
        annual_rate      : Annual rate in %
        years            : Investment duration in years
        compounding_freq : 1=Annually, 2=Semi-annually, 4=Quarterly, 12=Monthly

    Returns:
        dict with principal, interest earned, and maturity amount.
    """
    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")
    if annual_rate <= 0:
        raise ValueError("Annual rate must be greater than zero.")
    if years <= 0:
        raise ValueError("Duration must be greater than zero.")
    if compounding_freq not in (1, 2, 4, 12):
        raise ValueError("Compounding frequency must be 1, 2, 4, or 12.")

    r = annual_rate / 100
    n = compounding_freq
    t = years
    maturity = principal * (1 + r / n) ** (n * t)
    interest = maturity - principal

    return {
        "principal": round(principal, 2),
        "interest": round(interest, 2),
        "maturity": round(maturity, 2),
        "annual_rate": annual_rate,
        "years": years,
        "compounding_freq": compounding_freq,
    }


# ---------------------------------------------------------------------------
# SIP (Systematic Investment Plan) Calculator
# ---------------------------------------------------------------------------

def calculate_sip(monthly_amount: float, annual_rate: float, years: int) -> dict:
    """Future Value of a SIP:

    FV = P × ((1+r)^n - 1) / r × (1+r)

    Args:
        monthly_amount : Monthly SIP investment in ₹
        annual_rate    : Expected annual return in %
        years          : Investment horizon in years

    Returns:
        dict with total invested, estimated gains, and final corpus.
    """
    if monthly_amount <= 0:
        raise ValueError("Monthly amount must be greater than zero.")
    if annual_rate < 0:
        raise ValueError("Annual rate cannot be negative.")
    if years <= 0:
        raise ValueError("Investment years must be at least 1.")

    r = annual_rate / 12 / 100
    n = years * 12
    invested = monthly_amount * n

    if r == 0:
        fv = invested
    else:
        fv = monthly_amount * ((1 + r) ** n - 1) / r * (1 + r)

    gains = fv - invested

    return {
        "monthly_amount": monthly_amount,
        "invested": round(invested, 2),
        "gains": round(gains, 2),
        "final_value": round(fv, 2),
        "annual_rate": annual_rate,
        "years": years,
    }


# ---------------------------------------------------------------------------
# Recurring Deposit Calculator
# ---------------------------------------------------------------------------

def calculate_rd(monthly_deposit: float, annual_rate: float, months: int) -> dict:
    """RD maturity calculation using quarterly compounding (standard Indian practice):

    Each installment: A_i = P × (1 + r/4)^(quarters_remaining)

    Args:
        monthly_deposit : Monthly deposit amount in ₹
        annual_rate     : Annual interest rate in %
        months          : Total tenure in months

    Returns:
        dict with total deposited, interest earned, and maturity amount.
    """
    if monthly_deposit <= 0:
        raise ValueError("Monthly deposit must be greater than zero.")
    if annual_rate <= 0:
        raise ValueError("Annual rate must be greater than zero.")
    if months <= 0:
        raise ValueError("Tenure must be at least 1 month.")

    r = annual_rate / 4 / 100  # quarterly rate
    maturity = 0.0
    for i in range(months):
        quarters_remaining = (months - i) / 3
        maturity += monthly_deposit * (1 + r) ** quarters_remaining

    total_deposited = monthly_deposit * months
    interest = maturity - total_deposited

    return {
        "monthly_deposit": monthly_deposit,
        "total_deposited": round(total_deposited, 2),
        "interest": round(interest, 2),
        "maturity": round(maturity, 2),
        "annual_rate": annual_rate,
        "months": months,
    }


# ---------------------------------------------------------------------------
# Compound Interest Calculator
# ---------------------------------------------------------------------------

def calculate_compound_interest(
    principal: float, annual_rate: float, years: float, compounding_freq: int
) -> dict:
    """Generic compound interest calculator.

    A = P × (1 + r/n)^(n×t)

    Returns:
        dict with principal, interest earned, and final amount.
    """
    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")
    if annual_rate < 0:
        raise ValueError("Annual rate cannot be negative.")
    if years <= 0:
        raise ValueError("Years must be greater than zero.")

    r = annual_rate / 100
    n = compounding_freq if compounding_freq > 0 else 1
    t = years
    amount = principal * (1 + r / n) ** (n * t)
    interest = amount - principal

    return {
        "principal": round(principal, 2),
        "interest": round(interest, 2),
        "amount": round(amount, 2),
        "annual_rate": annual_rate,
        "years": years,
        "compounding_freq": n,
    }


# ---------------------------------------------------------------------------
# Inflation Calculator
# ---------------------------------------------------------------------------

def calculate_inflation(amount: float, inflation_rate: float, years: int) -> dict:
    """Calculate the impact of inflation on purchasing power.

    Future cost    : amount × (1 + i)^t
    Purchasing power of today's money after t years : amount / (1 + i)^t

    Args:
        amount         : Current amount / cost in ₹
        inflation_rate : Annual inflation rate in %
        years          : Number of years

    Returns:
        dict with future cost and real purchasing power loss.
    """
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if inflation_rate < 0:
        raise ValueError("Inflation rate cannot be negative.")
    if years <= 0:
        raise ValueError("Years must be at least 1.")

    future_cost = amount * (1 + inflation_rate / 100) ** years
    purchasing_power = amount / (1 + inflation_rate / 100) ** years
    value_lost = amount - purchasing_power

    return {
        "original_amount": round(amount, 2),
        "future_cost": round(future_cost, 2),
        "purchasing_power": round(purchasing_power, 2),
        "value_lost": round(value_lost, 2),
        "inflation_rate": inflation_rate,
        "years": years,
    }


# ---------------------------------------------------------------------------
# Loan Prepayment Calculator
# ---------------------------------------------------------------------------

def calculate_loan_prepayment(
    principal: float,
    annual_rate: float,
    remaining_months: int,
    extra_monthly: float = 0.0,
    lump_sum: float = 0.0,
) -> dict:
    """Calculate interest and time savings from loan prepayment.

    Supports:
    - Lump-sum prepayment (reduces outstanding principal immediately)
    - Extra monthly EMI (shortens tenure, keeping EMI higher than standard)
    - Combination of both

    Args:
        principal        : Current outstanding principal in ₹
        annual_rate      : Annual interest rate in %
        remaining_months : Months left on the original loan
        extra_monthly    : Additional amount paid per month over standard EMI (₹)
        lump_sum         : One-time prepayment amount (₹)

    Returns:
        dict with original vs new totals, interest saved, and months saved.
    """
    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")
    if remaining_months <= 0:
        raise ValueError("Remaining months must be at least 1.")
    if annual_rate < 0:
        raise ValueError("Annual rate cannot be negative.")
    if lump_sum < 0:
        raise ValueError("Lump sum cannot be negative.")
    if extra_monthly < 0:
        raise ValueError("Extra monthly payment cannot be negative.")

    lump_sum = min(lump_sum, principal)  # can't overpay

    orig = calculate_emi(principal, annual_rate, remaining_months)
    orig_emi = orig["emi"]
    orig_total = orig["total_payment"]

    new_principal = principal - lump_sum

    if new_principal <= 0:
        # Fully paid off by lump sum
        return {
            "original_emi": orig_emi,
            "original_total": round(orig_total, 2),
            "original_interest": round(orig["total_interest"], 2),
            "new_total": round(lump_sum, 2),
            "interest_saved": round(orig["total_interest"], 2),
            "months_saved": remaining_months,
            "new_tenure_months": 0,
        }

    if extra_monthly > 0:
        new_emi = orig_emi + extra_monthly
        r = annual_rate / 12 / 100
        if r > 0:
            try:
                new_months = math.ceil(
                    math.log(new_emi / (new_emi - new_principal * r)) / math.log(1 + r)
                )
            except (ValueError, ZeroDivisionError):
                new_months = remaining_months
        else:
            new_months = math.ceil(new_principal / new_emi)

        new_total = new_emi * new_months + lump_sum
    else:
        if new_principal > 0:
            new_calc = calculate_emi(new_principal, annual_rate, remaining_months)
            new_total = new_calc["total_payment"] + lump_sum
            new_months = remaining_months
        else:
            new_total = lump_sum
            new_months = 0

    interest_paid = new_total - principal
    interest_saved = orig["total_interest"] - interest_paid
    months_saved = remaining_months - new_months

    return {
        "original_emi": round(orig_emi, 2),
        "original_total": round(orig_total, 2),
        "original_interest": round(orig["total_interest"], 2),
        "new_total": round(new_total, 2),
        "interest_saved": round(max(interest_saved, 0), 2),
        "months_saved": max(months_saved, 0),
        "new_tenure_months": max(new_months, 0),
    }
