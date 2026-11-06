import enum
from datetime import datetime, timezone

from app.extensions import db


class BankType(str, enum.Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    COOPERATIVE = "COOPERATIVE"
    FOREIGN = "FOREIGN"
    SMALL_FINANCE = "SMALL_FINANCE"


class ProductType(str, enum.Enum):
    EDUCATION_LOAN = "EDUCATION_LOAN"
    HOME_LOAN = "HOME_LOAN"
    PERSONAL_LOAN = "PERSONAL_LOAN"
    VEHICLE_LOAN = "VEHICLE_LOAN"
    BUSINESS_LOAN = "BUSINESS_LOAN"
    FIXED_DEPOSIT = "FIXED_DEPOSIT"
    SAVINGS_ACCOUNT = "SAVINGS_ACCOUNT"


class RateType(str, enum.Enum):
    FIXED = "FIXED"
    FLOATING = "FLOATING"


class Bank(db.Model):
    """An Indian bank entity."""

    __tablename__ = "banks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    short_name = db.Column(db.String(20), nullable=False, unique=True, index=True)
    bank_type = db.Column(db.Enum(BankType), nullable=False, index=True)
    established_year = db.Column(db.Integer, nullable=True)
    headquarters = db.Column(db.String(100), nullable=True)
    logo_placeholder = db.Column(db.String(200), nullable=True)  # path or initials
    website_url = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    products = db.relationship("BankProduct", backref="bank", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "short_name": self.short_name,
            "bank_type": self.bank_type.value if self.bank_type else None,
            "established_year": self.established_year,
            "headquarters": self.headquarters,
            "website_url": self.website_url,
        }

    def __repr__(self) -> str:
        return f"<Bank {self.short_name!r}>"


class BankProduct(db.Model):
    """A financial product offered by a bank (loan, FD, savings account, etc.)."""

    __tablename__ = "bank_products"

    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.Integer, db.ForeignKey("banks.id"), nullable=False, index=True)
    product_type = db.Column(db.Enum(ProductType), nullable=False, index=True)
    product_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # JSON: {"max_amount": 5000000, "tenure_years": "1-30", "processing_fee": "0.5%", ...}
    features_json = db.Column(db.JSON, nullable=True, default=dict)
    # JSON: {"min_age": 21, "min_salary": 25000, "cibil_score": 700, ...}
    eligibility_json = db.Column(db.JSON, nullable=True, default=dict)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    interest_rates = db.relationship("InterestRate", backref="product", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "bank_id": self.bank_id,
            "product_type": self.product_type.value if self.product_type else None,
            "product_name": self.product_name,
            "description": self.description,
            "features": self.features_json,
            "eligibility": self.eligibility_json,
        }

    def __repr__(self) -> str:
        return f"<BankProduct {self.product_name!r} bank={self.bank_id}>"


class InterestRate(db.Model):
    """Interest-rate record for a BankProduct.

    ⚠️  All rows with is_demo_data=True are for educational demonstration only.
    Always verify current rates on the official bank website before making
    any financial decision.
    """

    __tablename__ = "interest_rates"

    id = db.Column(db.Integer, primary_key=True)
    bank_product_id = db.Column(db.Integer, db.ForeignKey("bank_products.id"), nullable=False, index=True)
    rate_min = db.Column(db.Float, nullable=False)   # percent, e.g. 8.50
    rate_max = db.Column(db.Float, nullable=False)   # percent, e.g. 9.50
    rate_type = db.Column(db.Enum(RateType), nullable=False, default=RateType.FLOATING)
    effective_date = db.Column(db.Date, nullable=True)
    last_verified = db.Column(db.Date, nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    is_demo_data = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "bank_product_id": self.bank_product_id,
            "rate_min": self.rate_min,
            "rate_max": self.rate_max,
            "rate_type": self.rate_type.value if self.rate_type else None,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "last_verified": self.last_verified.isoformat() if self.last_verified else None,
            "source_url": self.source_url,
            "notes": self.notes,
            "is_demo_data": self.is_demo_data,
        }

    def __repr__(self) -> str:
        return f"<InterestRate product={self.bank_product_id} {self.rate_min}-{self.rate_max}%>"
