from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    """Registered user of FinBot AI."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    lesson_progresses = db.relationship("LessonProgress", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    saved_lessons = db.relationship("SavedLesson", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    quiz_results = db.relationship("QuizResult", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    income_records = db.relationship("IncomeRecord", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    expense_records = db.relationship("ExpenseRecord", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    monthly_budgets = db.relationship("MonthlyBudget", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    chat_conversations = db.relationship("ChatConversation", backref="user", lazy="dynamic", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active,
        }

    def __repr__(self) -> str:
        return f"<User {self.username!r}>"


@login_manager.user_loader
def load_user(user_id: str) -> "User | None":
    """Flask-Login callback to reload user from session."""
    return db.session.get(User, int(user_id))
