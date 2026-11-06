from datetime import date

from flask import render_template, request, jsonify

from app.blueprints.finance_manager import finance_manager_bp
from app.extensions import db
from app.models.finance import IncomeRecord, ExpenseRecord, MonthlyBudget, ExpenseCategory


DEMO_USER_ID = 1  # placeholder until auth is integrated


@finance_manager_bp.route("/")
def index():
    """Personal finance manager dashboard."""
    return render_template("finance_manager/index.html")


# ---------------------------------------------------------------------------
# Income
# ---------------------------------------------------------------------------

@finance_manager_bp.route("/api/finance/income", methods=["GET", "POST"])
def income():
    if request.method == "GET":
        records = (
            IncomeRecord.query
            .filter_by(user_id=DEMO_USER_ID)
            .order_by(IncomeRecord.date.desc())
            .all()
        )
        return jsonify({"success": True, "data": [r.to_dict() for r in records]})

    # POST — add income record
    data = request.get_json(silent=True) or {}
    try:
        amount = float(data["amount"])
        source = str(data["source"]).strip()
        record_date = date.fromisoformat(data["date"])
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"success": False, "error": f"Invalid input: {exc}"}), 400

    if amount <= 0:
        return jsonify({"success": False, "error": "Amount must be greater than zero."}), 400

    record = IncomeRecord(
        user_id=DEMO_USER_ID,
        amount=amount,
        source=source,
        description=data.get("description", ""),
        date=record_date,
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"success": True, "data": record.to_dict()}), 201


# ---------------------------------------------------------------------------
# Expense
# ---------------------------------------------------------------------------

@finance_manager_bp.route("/api/finance/expense", methods=["GET", "POST"])
def expense():
    if request.method == "GET":
        records = (
            ExpenseRecord.query
            .filter_by(user_id=DEMO_USER_ID)
            .order_by(ExpenseRecord.date.desc())
            .all()
        )
        return jsonify({"success": True, "data": [r.to_dict() for r in records]})

    # POST — add expense record
    data = request.get_json(silent=True) or {}
    try:
        amount = float(data["amount"])
        category_str = str(data["category"]).upper()
        category = ExpenseCategory(category_str)
        record_date = date.fromisoformat(data["date"])
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"success": False, "error": f"Invalid input: {exc}"}), 400

    if amount <= 0:
        return jsonify({"success": False, "error": "Amount must be greater than zero."}), 400

    record = ExpenseRecord(
        user_id=DEMO_USER_ID,
        amount=amount,
        category=category,
        description=data.get("description", ""),
        date=record_date,
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"success": True, "data": record.to_dict()}), 201


# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------

@finance_manager_bp.route("/api/finance/budget", methods=["GET", "POST"])
def budget():
    if request.method == "GET":
        month = request.args.get("month", type=int, default=date.today().month)
        year = request.args.get("year", type=int, default=date.today().year)
        budget_rec = MonthlyBudget.query.filter_by(user_id=DEMO_USER_ID, month=month, year=year).first()
        if not budget_rec:
            return jsonify({"success": True, "data": None})
        return jsonify({"success": True, "data": budget_rec.to_dict()})

    # POST — upsert monthly budget
    data = request.get_json(silent=True) or {}
    try:
        month = int(data["month"])
        year = int(data["year"])
        income_budget = float(data.get("income_budget", 0))
        expense_budget = dict(data.get("expense_budget", {}))
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"success": False, "error": f"Invalid input: {exc}"}), 400

    if not (1 <= month <= 12):
        return jsonify({"success": False, "error": "Month must be between 1 and 12."}), 400

    budget_rec = MonthlyBudget.query.filter_by(user_id=DEMO_USER_ID, month=month, year=year).first()
    if budget_rec:
        budget_rec.income_budget = income_budget
        budget_rec.expense_budget_json = expense_budget
    else:
        budget_rec = MonthlyBudget(
            user_id=DEMO_USER_ID,
            month=month,
            year=year,
            income_budget=income_budget,
            expense_budget_json=expense_budget,
        )
        db.session.add(budget_rec)

    db.session.commit()
    return jsonify({"success": True, "data": budget_rec.to_dict()})


# ---------------------------------------------------------------------------
# Edit and Delete Income
# ---------------------------------------------------------------------------

@finance_manager_bp.route("/api/finance/income/<int:record_id>", methods=["PUT", "DELETE"])
def income_record_detail(record_id: int):
    record = db.session.get(IncomeRecord, record_id)
    if not record or record.user_id != DEMO_USER_ID:
        return jsonify({"success": False, "error": "Income record not found."}), 404

    if request.method == "DELETE":
        db.session.delete(record)
        db.session.commit()
        return jsonify({"success": True, "message": "Income record deleted successfully."})

    # PUT — edit income
    data = request.get_json(silent=True) or {}
    try:
        if "amount" in data:
            amt = float(data["amount"])
            if amt <= 0:
                return jsonify({"success": False, "error": "Amount must be greater than zero."}), 400
            record.amount = amt
        if "source" in data:
            record.source = str(data["source"]).strip()
        if "description" in data:
            record.description = str(data["description"]).strip()
        if "date" in data:
            record.date = date.fromisoformat(data["date"])
    except (TypeError, ValueError) as exc:
        return jsonify({"success": False, "error": f"Invalid update data: {exc}"}), 400

    db.session.commit()
    return jsonify({"success": True, "data": record.to_dict()})


# ---------------------------------------------------------------------------
# Edit and Delete Expense
# ---------------------------------------------------------------------------

@finance_manager_bp.route("/api/finance/expense/<int:record_id>", methods=["PUT", "DELETE"])
def expense_record_detail(record_id: int):
    record = db.session.get(ExpenseRecord, record_id)
    if not record or record.user_id != DEMO_USER_ID:
        return jsonify({"success": False, "error": "Expense record not found."}), 404

    if request.method == "DELETE":
        db.session.delete(record)
        db.session.commit()
        return jsonify({"success": True, "message": "Expense record deleted successfully."})

    # PUT — edit expense
    data = request.get_json(silent=True) or {}
    try:
        if "amount" in data:
            amt = float(data["amount"])
            if amt <= 0:
                return jsonify({"success": False, "error": "Amount must be greater than zero."}), 400
            record.amount = amt
        if "category" in data:
            record.category = ExpenseCategory(str(data["category"]).upper())
        if "description" in data:
            record.description = str(data["description"]).strip()
        if "date" in data:
            record.date = date.fromisoformat(data["date"])
    except (TypeError, ValueError) as exc:
        return jsonify({"success": False, "error": f"Invalid update data: {exc}"}), 400

    db.session.commit()
    return jsonify({"success": True, "data": record.to_dict()})

