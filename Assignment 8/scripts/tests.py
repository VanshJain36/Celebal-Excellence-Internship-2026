"""
tests.py

Part 5: Edge Case Handling

This file contains simple test functions that check how our data and cleaning logic behave in
a few tricky situations:

1. What happens when order_items has an order_id not in orders?
2. What happens when discount_percent > 100?
3. What happens when quantity is 0?
4. What happens when order_date is in the future?
"""

from datetime import datetime, timedelta
import pandas as pd

from clean_data import check_referential_integrity


def test_order_id_not_in_orders():
    """
    Test 1: What happens when order_items has an order_id not in orders?
    """
    orders_df = pd.DataFrame({
        "order_id": [1, 2, 3]
    })

    order_items_df = pd.DataFrame({
        "item_id": [101, 102, 103],
        "order_id": [1, 2, 999],
        "quantity": [2, 1, 5]
    })

    broken = check_referential_integrity(orders_df, order_items_df)

    if broken == [103]:
        print("Test 1 PASSED: order_id not in orders was correctly detected (item_id 103).")
    else:
        print("Test 1 FAILED: expected [103], got", broken)


def test_discount_percent_above_100():
    """
    Test 2: What happens when discount_percent > 100?
    """
    price = 100
    qty = 2
    discount = 150

    revenue = qty * price * (1 - discount / 100.0)
    ok = 0 <= discount <= 100

    print("Test 2: discount_percent =", discount,
          "-> calculated revenue =", revenue,
          "-> is_valid_discount =", ok)

    if not ok and revenue < 0:
        print("Test 2 PASSED: invalid discount correctly produces a negative,")
        print("               untrustworthy revenue value, so it can be flagged.")
    else:
        print("Test 2 FAILED: expected a negative revenue for an invalid discount.")


def test_quantity_is_zero():
    """
    Test 3: What happens when quantity is 0?
    """
    price = 250
    qty = 0
    discount = 10

    revenue = qty * price * (1 - discount / 100.0)

    print("Test 3: quantity = 0 -> calculated revenue =", revenue)

    if revenue == 0:
        print("Test 3 PASSED: a zero quantity correctly results in zero revenue.")
    else:
        print("Test 3 FAILED: expected revenue to be 0.")


def test_order_date_in_future():
    """
    Test 4: What happens when order_date is in the future?
    """
    today = datetime.now()

    dates = [
        today - timedelta(days=5),
        today + timedelta(days=10),
    ]

    future_dates = [d for d in dates if d > today]

    print("Test 4: found", len(future_dates), "order(s) with a future date.")

    if len(future_dates) == 1:
        print("Test 4 PASSED: the future-dated order was correctly detected.")
    else:
        print("Test 4 FAILED: expected exactly 1 future-dated order to be detected.")


def run_all_tests():
    print("Running edge case tests...\n")

    test_order_id_not_in_orders()
    print()
    test_discount_percent_above_100()
    print()
    test_quantity_is_zero()
    print()
    test_order_date_in_future()

    print("\nAll tests finished.")


if __name__ == "__main__":
    run_all_tests()