"""Additional offline checks for Homework 1 tool boundaries."""

from types import SimpleNamespace

import pytest

from agent import db, tools
from agent.auth import AuthContext

SHOPPER = AuthContext(user_id=1, role="shopper")


def test_policy_ids_are_case_sensitive(world):
    result = tools.get_policy(SHOPPER, "CW-RETURNS")
    assert result["error"] == "not_found"
    assert "CW-RETURNS" in result["reason"]


def test_product_filters_sort_and_limits(world_copy):
    with db.connection() as conn:
        products = db.list_products(conn, store_id=1)[:3]
        for product, price in zip(products, [1200, 1000, 1000]):
            conn.execute(
                "UPDATE products SET title = ?, description = ?, price_cents = ? WHERE id = ?",
                ("BoundaryFixture", "DescriptionToken", price, product.id),
            )
        conn.commit()
    result = tools.search_products(
        SHOPPER, " BOUNDARYfixture descriptionTOKEN ",
        store="BLUE-HERON-CERAMICS", max_price_usd=10, limit=100,
    )
    assert [p["product_id"] for p in result["products"]] == [p.id for p in products[1:]]
    assert result["count"] == 2
    assert tools.search_products(SHOPPER, "BoundaryFixture", limit=0)["count"] == 1
    assert tools.search_products(SHOPPER, "BoundaryFixture absenttoken")["count"] == 0
    assert tools.search_products(SHOPPER, "BoundaryFixture", max_price_usd=9)["count"] == 0


@pytest.mark.parametrize("price", [0, -1, float("nan")])
def test_invalid_product_price(price):
    assert tools.search_products(SHOPPER, "mug", max_price_usd=price)["error"] == "invalid_argument"


def test_cancellation_denies_before_disclosing_status(world_copy):
    result = tools.cancel_order(AuthContext(user_id=2, role="shopper"), 4127, "cancel")
    assert result["error"] == "permission_denied"
    assert "delivered" not in result["reason"]
    with db.connection() as conn:
        assert db.get_order(conn, 4127).status == "delivered"


def test_cancel_kill_switch_precedes_database_access(monkeypatch):
    monkeypatch.setenv("CARTWHEEL_KILL_SWITCH", "readonly")
    monkeypatch.setenv("CARTWHEEL_DB", "/nonexistent/cartwheel.db")
    assert tools.cancel_order(SHOPPER, 4127, "cancel")["error"] == "paused"


@pytest.mark.parametrize("role", ["merchant", "support"])
def test_cancellation_status_rule_applies_to_every_role(world_copy, role):
    ctx = AuthContext(user_id=9001, role=role, store_id=1 if role == "merchant" else None)
    result = tools.cancel_order(ctx, 4127, "cancel")
    assert result["error"] == "not_eligible"
    assert "delivered" in result["reason"]
    assert "before shipment" in result["reason"]


def test_order_search_substrings_and_surrounding_text(order_search_cases):
    title, expected = order_search_cases
    result = tools.find_order(SHOPPER, f"{title.lower()} I bought last week")
    assert [o["order_id"] for o in result["orders"]] == expected["shopper"][:5]
    assert tools.find_order(SHOPPER, "   ") == {"ok": True, "orders": []}


@pytest.mark.parametrize("ctx", [
    SimpleNamespace(role="unknown", user_id=1, store_id=None),
    SimpleNamespace(role="shopper", user_id=None, store_id=None),
    SimpleNamespace(role="merchant", user_id=9001, store_id=None),
    SimpleNamespace(role="support", user_id=None, store_id=None),
])
def test_order_search_rejects_invalid_context(ctx, monkeypatch):
    monkeypatch.setenv("CARTWHEEL_DB", "/nonexistent/cartwheel.db")
    assert tools.find_order(ctx, "mug")["error"] == "permission_denied"
