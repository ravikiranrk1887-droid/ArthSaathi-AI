import enum
from datetime import datetime, timezone

from app.extensions import db


class LessonCategory(str, enum.Enum):
    BANKING = "BANKING"
    INVESTMENT = "INVESTMENT"
    LOANS = "LOANS"
    PLANNING = "PLANNING"
    INDIAN_BANKING = "INDIAN_BANKING"


class Lesson(db.Model):
    """A financial literacy lesson unit."""

    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    category = db.Column(db.Enum(LessonCategory), nullable=False, index=True)
    subcategory = db.Column(db.String(100), nullable=True)
    # JSON blob: {"sections": [...], "key_points": [...], "summary": "..."}
    content_json = db.Column(db.JSON, nullable=False, default=dict)
    difficulty = db.Column(db.String(20), nullable=False, default="BEGINNER")  # BEGINNER / INTERMEDIATE / ADVANCED
    order_index = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    progress_records = db.relationship("LessonProgress", backref="lesson", lazy="dynamic", cascade="all, delete-orphan")
    saved_by = db.relationship("SavedLesson", backref="lesson", lazy="dynamic", cascade="all, delete-orphan")
    quiz_questions = db.relationship("QuizQuestion", backref="lesson", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "category": self.category.value if self.category else None,
            "subcategory": self.subcategory,
            "difficulty": self.difficulty,
            "order_index": self.order_index,
        }

    def __repr__(self) -> str:
        return f"<Lesson {self.slug!r}>"


class LessonProgress(db.Model):
    """Tracks a user's progress through a lesson."""

    __tablename__ = "lesson_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False, index=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    time_spent = db.Column(db.Integer, default=0)  # seconds

    __table_args__ = (db.UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson"),)

    def __repr__(self) -> str:
        return f"<LessonProgress user={self.user_id} lesson={self.lesson_id} completed={self.completed}>"


class SavedLesson(db.Model):
    """Lessons bookmarked by a user."""

    __tablename__ = "saved_lessons"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False, index=True)
    saved_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint("user_id", "lesson_id", name="uq_user_saved_lesson"),)

    def __repr__(self) -> str:
        return f"<SavedLesson user={self.user_id} lesson={self.lesson_id}>"
