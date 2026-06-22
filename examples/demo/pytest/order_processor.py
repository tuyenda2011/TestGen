from dataclasses import dataclass
from typing import List, Dict, Optional

class OutOfStockError(Exception):
    """Raised when an item is out of stock."""
    pass

class InvalidPromoCodeError(Exception):
    """Raised when a promo code is invalid or expired."""
    pass

class PaymentError(Exception):
    """Raised when payment fails or is invalid."""
    pass

@dataclass
class OrderItem:
    product_id: str
    name: str
    price: float
    quantity: int
    stock_available: int

class OrderProcessor:
    TAX_RATES = {
        "VN": 0.10,
        "US": 0.08,
        "SG": 0.07,
    }
    
    VALID_PROMO_CODES = {
        "SAVE10": 0.10,  # 10% off
        "SAVE20": 0.20,  # 20% off
        "FREE5": 5.0,    # Flat 5.0 discount
    }

    def __init__(self, country_code: str = "VN", customer_tier: str = "Standard"):
        if country_code not in self.TAX_RATES:
            raise ValueError(f"Unsupported country code: {country_code}")
        if customer_tier not in ["Standard", "Silver", "Gold", "VIP"]:
            raise ValueError(f"Invalid customer tier: {customer_tier}")
        self.country_code = country_code
        self.customer_tier = customer_tier

    def calculate_item_subtotal(self, item: OrderItem) -> float:
        if item.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if item.price < 0:
            raise ValueError("Price cannot be negative")
        if item.quantity > item.stock_available:
            raise OutOfStockError(f"Insufficient stock for {item.name}. Available: {item.stock_available}")
        
        subtotal = item.price * item.quantity
        # Silver gets 2% off items, Gold gets 5%, VIP gets 10%
        tier_discounts = {"Standard": 0.0, "Silver": 0.02, "Gold": 0.05, "VIP": 0.10}
        discount = tier_discounts.get(self.customer_tier, 0.0)
        
        # Additional bulk discount: buy more than 5 of the same item gets an extra 5% off subtotal
        if item.quantity >= 5:
            discount += 0.05
            
        return round(subtotal * (1 - discount), 2)

    def process_order(self, items: List[OrderItem], promo_code: Optional[str] = None) -> Dict[str, float]:
        if not items:
            raise ValueError("Order must contain at least one item")
            
        subtotal = 0.0
        for item in items:
            subtotal += self.calculate_item_subtotal(item)
            
        promo_discount = 0.0
        if promo_code:
            if promo_code not in self.VALID_PROMO_CODES:
                raise InvalidPromoCodeError(f"Promo code {promo_code} is not valid")
            discount_val = self.VALID_PROMO_CODES[promo_code]
            if discount_val < 1.0:
                # Percentage promo code
                promo_discount = subtotal * discount_val
            else:
                # Flat promo code
                promo_discount = min(discount_val, subtotal)
                
        taxable_amount = max(0.0, subtotal - promo_discount)
        tax_rate = self.TAX_RATES[self.country_code]
        tax = taxable_amount * tax_rate
        total = taxable_amount + tax
        
        # High value checkout restriction for standard tier
        if total > 10000.0 and self.customer_tier == "Standard":
            raise PaymentError("High-value transaction requires VIP/Gold tier or manual verification")

        return {
            "subtotal": round(subtotal, 2),
            "promo_discount": round(promo_discount, 2),
            "tax": round(tax, 2),
            "total": round(total, 2)
        }
