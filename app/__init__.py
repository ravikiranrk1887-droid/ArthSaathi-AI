from flask import Flask
from dotenv import load_dotenv

from app.config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    """Application factory — creates and configures the Flask app."""
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class)

    # ------------------------------------------------------------------
    # Initialise extensions
    # ------------------------------------------------------------------
    db.init_app(app)
    login_manager.init_app(app)

    # ------------------------------------------------------------------
    # Register blueprints
    # ------------------------------------------------------------------
    from app.blueprints.main import main_bp
    from app.blueprints.education import education_bp
    from app.blueprints.calculators import calculators_bp
    from app.blueprints.banks import banks_bp
    from app.blueprints.chatbot import chatbot_bp
    from app.blueprints.finance_manager import finance_manager_bp
    from app.blueprints.learning import learning_bp
    from app.blueprints.investments import investments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(education_bp)
    app.register_blueprint(calculators_bp)
    app.register_blueprint(banks_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(finance_manager_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(investments_bp)

    # ------------------------------------------------------------------
    # Create database tables on first run
    # ------------------------------------------------------------------
    with app.app_context():
        # Import all models so SQLAlchemy is aware of them before create_all()
        from app.models import user, lesson, quiz, bank, finance, chat  # noqa: F401
        db.create_all()

    return app
