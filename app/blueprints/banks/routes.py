from flask import render_template, request, jsonify

from app.blueprints.banks import banks_bp
from app.services import bank_service


@banks_bp.route("/")
def index():
    """Bank comparison hub page."""
    banks = bank_service.get_all_banks()
    return render_template("banks/index.html", banks=banks)


@banks_bp.route("/compare")
def compare():
    """Interactive bank product comparison page."""
    return render_template("banks/compare.html")


@banks_bp.route("/api/banks/list", methods=["GET"])
def api_banks_list():
    """Return JSON list of all banks."""
    banks = bank_service.get_all_banks()
    return jsonify({"success": True, "data": banks})


@banks_bp.route("/api/banks/compare", methods=["GET"])
def api_compare():
    """Compare banks for a given product type.

    Query params:
        product_type : e.g. HOME_LOAN, FIXED_DEPOSIT
        bank_ids     : comma-separated list of bank IDs (optional)
        amount       : loan/deposit amount in ₹ (optional, for filtering)
        duration     : tenure in months (optional, for filtering)
    """
    product_type = request.args.get("product_type", "").strip()
    if not product_type:
        return jsonify({"success": False, "error": "product_type is required."}), 400

    # Optional bank filter
    bank_ids_param = request.args.get("bank_ids", "")
    bank_ids = None
    if bank_ids_param:
        try:
            bank_ids = [int(x) for x in bank_ids_param.split(",") if x.strip()]
        except ValueError:
            return jsonify({"success": False, "error": "bank_ids must be comma-separated integers."}), 400

    # Optional amount / duration filters
    amount = None
    duration = None
    try:
        if request.args.get("amount"):
            amount = float(request.args["amount"])
        if request.args.get("duration"):
            duration = int(request.args["duration"])
    except ValueError:
        return jsonify({"success": False, "error": "amount and duration must be numeric."}), 400

    if amount or duration:
        data = bank_service.filter_rates(product_type, amount=amount, duration=duration)
    else:
        data = bank_service.get_comparison_data(product_type, bank_ids=bank_ids)

    return jsonify({"success": True, "data": data, "count": len(data)})
