import enum
from datetime import datetime, timezone

from app.extensions import db


class ExpenseCategory(str, enum.Enum):
    FOOD = "FOOD"
    EDUCATION = "EDUCATION"
    TRANSPORT = "TRANSPORT"
    SHOPPING = "SHOPPING"
    RENT = "RENT"
    BILLS = "BILLS"
    HEALTHCARE = "HEALTHCARE"
    ENTERTAINMENT = "ENTERTAINMENT"
    OTHER = "OTHER"


class IncomeRecord(db.Model):
    """A single income entry for a user."""

    __tablename__ = "income_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)        # INR
    source = db.Column(db.String(100), nullable=False)  # e.g. "Salary", "Freelance"
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "source": self.source,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
        }

    def __repr__(self) -> str:
        return f"<IncomeRecord user={self.user_id} ₹{self.amount} on {self.date}>"


class ExpenseRecord(db.Model):
    """A single expense entry for a user."""

    __tablename__ = "expense_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)        # INR
    category = db.Column(db.Enum(ExpenseCategory), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category.value if self.category else None,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
        }

    def __repr__(self) -> str:
        return f"<ExpenseRecord user={self.user_id} cat={self.category} ₹{self.amount}>"


class MonthlyBudget(db.Model):
    """Monthly budget plan for a user.

    expense_budget_json structure:
    {
        "FOOD": 5000,
        "EDUCATION": 3000,
        "TRANSPORT": 2000,
        ...
    }
    """

    __tablename__ = "monthly_budgets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    month = db.Column(db.Integer, nullable=False)   # 1-12
    year = db.Column(db.Integer, nullable=False)
    income_budget = db.Column(db.Float, nullable=False, default=0.0)   # expected monthly income (INR)
    expense_budget_json = db.Column(db.JSON, nullable=False, default=dict)  # per-category limits
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint("user_id", "month", "year", name="uq_user_month_year"),)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "month": self.month,
            "year": self.year,
            "income_budget": self.income_budget,
            "expense_budget": self.expense_budget_json,
        }

    def __repr__(self) -> str:
        return f"<MonthlyBudget user={self.user_id} {self.month}/{self.year}>"
