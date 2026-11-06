from flask import render_template

from app.blueprints.main import main_bp


@main_bp.route("/")
def landing():
    """Public landing page."""
    return render_template("landing.html")


@main_bp.route("/dashboard")
def dashboard():
    """User dashboard — overview of all features."""
    return render_template("dashboard.html")
