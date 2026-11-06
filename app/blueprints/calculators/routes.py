from flask import render_template, request, jsonify

from app.blueprints.calculators import calculators_bp
from app.services import calculator_service


@calculators_bp.route("/")
def index():
    """Calculator hub page."""
    return render_template("calculators/index.html")


def _json_error(message: str, status: int = 400):
    return jsonify({"success": False, "error": message}), status


# ---------------------------------------------------------------------------
# EMI Calculator
# ---------------------------------------------------------------------------

@calculators_bp.route("/api/calculate/emi", methods=["POST"])
def calculate_emi():
    data = request.get_json(silent=True) or {}
    try:
        principal = float(data["principal"])
        annual_rate = float(data["annual_rate"])
        tenure_months = int(data["tenure_months"])
    except (KeyError, TypeError, ValueError) as exc:
        return _json_error(f"Invalid input: {exc}")

    try:
        result = calculator_service.calculate_emi(principal, annual_rate, tenure_months)
        return jsonify({"success": True, "data": result})
    except ValueError as exc:
        return _json_error(str(exc))


# ---------------------------------------------------------------------------
# Fixed Deposit Calculator
# ---------------------------------------------------------------------------

@calculators_bp.route("/api/calculate/fd", methods=["POST"])
def calculate_fd():
    data = request.get_json(silent=True) or {}
    try:
        principal = float(data["principal"])
        annual_rate = float(data["annual_rate"])
        years = float(data["years"])
        compounding_freq = int(data.get("compounding_freq", 4))  # default quarterly
    except (KeyError, TypeError, ValueError) as exc:
        return _json_error(f"Invalid input: {exc}")

    try:
        result = calculator_service.calculate_fd(principal, annual_rate, years, compounding_freq)
        return jsonify({"success": True, "data": result})
    except ValueError as exc:
        return _json_error(str(exc))


# ---------------------------------------------------------------------------
# SIP Calculator
# ---------------------------------------------------------------------------

@calculators_bp.route("/api/calculate/sip", methods=["POST"])
def calculate_sip():
    data = request.get_json(silent=True) or {}
    try:
        monthly_amount = float(data["monthly_amount"])
        annual_rate = float(data["annual_rate"])
        years = int(data["years"])
    except (KeyError, TypeError, ValueError) as exc:
        return _json_error(f"Invalid input: {exc}")

    try:
        result = calculator_service.calculate_sip(monthly_amount, annual_rate, years)
        return jsonify({"success": True, "data": result})
    except ValueError as exc:
        return _json_error(str(exc))


# ---------------------------------------------------------------------------
# Recurring Deposit Calculator
# ---------------------------------------------------------------------------

@calculators_bp.route("/api/calculate/rd", methods=["POST"])
def calculate_rd():
    data = request.get_json(silent=True) or {}
    try:
        monthly_deposit = float(data["monthly_deposit"])
        annual_rate = float(data["annual_rate"])
        months = int(data["months"])
    except (KeyError, TypeError, ValueError) as exc:
        return _json_error(f"Invalid input: {exc}")

    try:
        result = calculator_service.calculate_rd(monthly_deposit, annual_rate, months)
        return jsonify({"success": True, "data": result})
    except ValueError as exc:
        return _json_error(str(exc))


# ---------------------------------------------------------------------------
# Compound Interest Calculator
# ---------------------------------------------------------------------------

@calculators_bp.route("/api/calculate/compound", methods=["POST"])
def calculate_compound():
    data = request.get_json(silent=True) or {}
    try:
        principal = float(data["principal"])
        annual_rate = float(data["annual_rate"])
        years = float(data["years"])
        compounding_freq = int(data.get("compounding_freq", 12))
    except (KeyError, TypeError, ValueError) as exc:
        return _json_error(f"Invalid input: {exc}")

    try:
        result = calculator_service.calculate_compound_interest(principal, annual_rate, years, compounding_freq)
        return jsonify({"success": True, "data": result})
    except ValueError as exc:
        return _json_error(str(exc))


# ---------------------------------------------------------------------------
# Inflation Calculator
# ---------------------------------------------------------------------------

@calculators_bp.route("/api/calculate/inflation", methods=["POST"])
def calculate_inflation():
    data = request.get_json(silent=True) or {}
    try:
        amount = float(data["amount"])
        inflation_rate = float(data["inflation_rate"])
        years = int(data["years"])
    except (KeyError, TypeError, ValueError) as exc:
        return _json_error(f"Invalid input: {exc}")

    try:
        result = calculator_service.calculate_inflation(amount, inflation_rate, years)
        return jsonify({"success": True, "data": result})
    except ValueError as exc:
        return _json_error(str(exc))


# ---------------------------------------------------------------------------
# Loan Prepayment Calculator
# ---------------------------------------------------------------------------

@calculators_bp.route("/api/calculate/prepayment", methods=["POST"])
def calculate_prepayment():
    data = request.get_json(silent=True) or {}
    try:
        principal = float(data["principal"])
        annual_rate = float(data["annual_rate"])
        remaining_months = int(data["remaining_months"])
        extra_monthly = float(data.get("extra_monthly", 0))
        lump_sum = float(data.get("lump_sum", 0))
    except (KeyError, TypeError, ValueError) as exc:
        return _json_error(f"Invalid input: {exc}")

    try:
        result = calculator_service.calculate_loan_prepayment(
            principal, annual_rate, remaining_months, extra_monthly, lump_sum
        )
        return jsonify({"success": True, "data": result})
    except ValueError as exc:
        return _json_error(str(exc))
