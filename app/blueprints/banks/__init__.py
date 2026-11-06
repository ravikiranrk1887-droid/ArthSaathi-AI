from flask import Blueprint

banks_bp = Blueprint("banks", __name__, url_prefix="/banks")

from app.blueprints.banks import routes  # noqa: F401, E402
