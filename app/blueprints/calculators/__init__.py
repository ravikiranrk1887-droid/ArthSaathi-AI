from flask import Blueprint

calculators_bp = Blueprint("calculators", __name__, url_prefix="/calculators")

from app.blueprints.calculators import routes  # noqa: F401, E402
