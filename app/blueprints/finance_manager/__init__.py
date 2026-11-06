from flask import Blueprint

finance_manager_bp = Blueprint("finance_manager", __name__, url_prefix="/finance")

from app.blueprints.finance_manager import routes  # noqa: F401, E402
