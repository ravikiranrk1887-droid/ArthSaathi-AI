from datetime import datetime, timezone

from app.extensions import db


class QuizQuestion(db.Model):
    """A multiple-choice question associated with a lesson."""

    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False, index=True)
    question = db.Column(db.Text, nullable=False)
    # JSON list of exactly 4 option strings, e.g. ["Option A", "Option B", "Option C", "Option D"]
    options_json = db.Column(db.JSON, nullable=False)
    correct_index = db.Column(db.Integer, nullable=False)  # 0-based index into options_json
    explanation = db.Column(db.Text, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "lesson_id": self.lesson_id,
            "question": self.question,
            "options": self.options_json,
            "explanation": self.explanation,
        }

    def __repr__(self) -> str:
        return f"<QuizQuestion id={self.id} lesson={self.lesson_id}>"


class QuizResult(db.Model):
    """Stores the outcome of a user's quiz attempt."""

    __tablename__ = "quiz_results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)   # number of correct answers
    total = db.Column(db.Integer, nullable=False)   # total questions attempted
    # JSON list of selected indices, e.g. [0, 2, 1, 3]
    answers_json = db.Column(db.JSON, nullable=False, default=list)
    taken_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def percentage(self) -> float:
        if self.total == 0:
            return 0.0
        return round(self.score / self.total * 100, 1)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "lesson_id": self.lesson_id,
            "score": self.score,
            "total": self.total,
            "percentage": self.percentage(),
            "answers": self.answers_json,
            "taken_at": self.taken_at.isoformat() if self.taken_at else None,
        }

    def __repr__(self) -> str:
        return f"<QuizResult user={self.user_id} lesson={self.lesson_id} score={self.score}/{self.total}>"
