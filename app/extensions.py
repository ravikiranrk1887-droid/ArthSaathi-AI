from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Extensions initialized here; bound to the app in create_app()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.landing"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"
