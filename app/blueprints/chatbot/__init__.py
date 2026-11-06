from flask import Blueprint

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

from app.blueprints.chatbot import routes  # noqa: F401, E402
