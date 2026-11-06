from flask import Blueprint

education_bp = Blueprint("education", __name__, url_prefix="/education")

from app.blueprints.education import routes  # noqa: F401, E402
