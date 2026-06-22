import pytest

from source_under_test import apply_store_credit, calculate_discount, final_total, shipping_fee


def test_calculate_discount_caps_vip_discount():
    assert calculate_discount(1000, "VIP") == 50.0


def test_shipping_fee_domestic_fragile_heavy_order():
    assert shipping_fee(6, "domestic", fragile=True) == 22.5


def test_apply_store_credit_never_returns_negative_total():
    assert apply_store_credit(25.0, 30.0) == 0.0


def test_final_total_rejects_negative_subtotal():
    order = {
        "subtotal": -1,
        "weight_kg": 1,
        "destination": "domestic",
        "customer_tier": "standard",
        "fragile": False,
        "store_credit": 0,
    }
    with pytest.raises(ValueError, match="subtotal"):
        final_total(order)
