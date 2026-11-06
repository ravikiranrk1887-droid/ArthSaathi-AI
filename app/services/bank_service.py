"""
bank_service.py
===============
Service layer for bank and product data operations.
Reads from the database; never makes external API calls.
"""

from typing import Optional

from app.extensions import db
from app.models.bank import Bank, BankProduct, InterestRate, ProductType


def get_all_banks() -> list[dict]:
    """Return a list of all banks ordered by name."""
    banks = Bank.query.order_by(Bank.name).all()
    return [b.to_dict() for b in banks]


def get_bank_details(bank_id: int) -> Optional[dict]:
    """Return full details for a single bank including all products and rates.

    Returns None if the bank is not found.
    """
    bank = db.session.get(Bank, bank_id)
    if not bank:
        return None

    result = bank.to_dict()
    products = []
    for product in bank.products.all():
        p_dict = product.to_dict()
        p_dict["rates"] = [r.to_dict() for r in product.interest_rates.all()]
        products.append(p_dict)

    result["products"] = products
    return result


def get_products_by_type(product_type: str) -> list[dict]:
    """Return all bank products of a given type.

    Args:
        product_type: One of the ProductType enum values as a string
                      e.g. 'HOME_LOAN', 'FIXED_DEPOSIT'
    """
    try:
        ptype = ProductType(product_type.upper())
    except ValueError:
        return []

    products = (
        BankProduct.query
        .filter_by(product_type=ptype)
        .join(Bank)
        .order_by(Bank.name)
        .all()
    )

    result = []
    for product in products:
        p_dict = product.to_dict()
        p_dict["bank"] = product.bank.to_dict()
        p_dict["rates"] = [r.to_dict() for r in product.interest_rates.all()]
        result.append(p_dict)

    return result


def get_comparison_data(product_type: str, bank_ids: Optional[list[int]] = None) -> list[dict]:
    """Build comparison data for a product type across multiple banks.

    Args:
        product_type : Product category to compare (e.g. 'HOME_LOAN')
        bank_ids     : Optional filter to specific bank IDs. If None, all banks are included.

    Returns:
        List of comparison rows sorted by minimum interest rate (ascending).
    """
    try:
        ptype = ProductType(product_type.upper())
    except ValueError:
        return []

    query = (
        BankProduct.query
        .filter_by(product_type=ptype)
        .join(Bank)
    )

    if bank_ids:
        query = query.filter(Bank.id.in_(bank_ids))

    products = query.order_by(Bank.name).all()

    comparison = []
    for product in products:
        rates = product.interest_rates.order_by(InterestRate.rate_min).all()
        if not rates:
            continue
        best_rate = rates[0]
        comparison.append(
            {
                "bank_id": product.bank.id,
                "bank_name": product.bank.name,
                "bank_short": product.bank.short_name,
                "bank_type": product.bank.bank_type.value if product.bank.bank_type else None,
                "product_id": product.id,
                "product_name": product.product_name,
                "features": product.features_json,
                "eligibility": product.eligibility_json,
                "rate_min": best_rate.rate_min,
                "rate_max": best_rate.rate_max,
                "rate_type": best_rate.rate_type.value if best_rate.rate_type else None,
                "last_verified": best_rate.last_verified.isoformat() if best_rate.last_verified else None,
                "source_url": best_rate.source_url,
                "is_demo_data": best_rate.is_demo_data,
                "notes": best_rate.notes,
            }
        )

    # Sort by lowest starting rate
    comparison.sort(key=lambda x: x["rate_min"])
    return comparison


def filter_rates(
    product_type: str,
    amount: Optional[float] = None,
    duration: Optional[int] = None,
) -> list[dict]:
    """Filter comparison data by loan amount eligibility and duration.

    This is a best-effort filter using the features_json metadata.
    Banks without metadata for the given filters are included by default.
    """
    data = get_comparison_data(product_type)

    if amount is not None:
        filtered = []
        for row in data:
            features = row.get("features") or {}
            max_amount = features.get("max_amount")
            min_amount = features.get("min_amount", 0)
            if max_amount is None or (min_amount <= amount <= max_amount):
                filtered.append(row)
        data = filtered

    if duration is not None:
        filtered = []
        for row in data:
            features = row.get("features") or {}
            max_tenure = features.get("max_tenure_months")
            min_tenure = features.get("min_tenure_months", 1)
            if max_tenure is None or (min_tenure <= duration <= max_tenure):
                filtered.append(row)
        data = filtered

    return data
