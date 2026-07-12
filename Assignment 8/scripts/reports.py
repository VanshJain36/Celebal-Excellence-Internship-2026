"""
reports.py

This is a simple command-line tool that:
1. Asks the user for a report type (daily / weekly / monthly)
2. Asks the user for a date range
3. Connects to the SQLite database
4. Prints a summary report:
   - total orders, revenue, unique customers
   - top 3 products
   - comparison with the previous period (% change)
"""

import os
import sqlite3
from datetime import datetime, timedelta

script_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(script_dir, ".."))
database_path = os.path.join(project_dir, "database", "ecommerce.db")


def ask_type():
    """Ask the user to choose daily, weekly, or monthly report."""
    print("What type of report do you want?")
    print("1. daily")
    print("2. weekly")
    print("3. monthly")
    choice = input("Enter a number (1/2/3): ").strip()

    if choice == "1":
        return "daily"
    elif choice == "2":
        return "weekly"
    elif choice == "3":
        return "monthly"
    else:
        print("Invalid choice, defaulting to 'monthly'.")
        return "monthly"


def ask_dates():
    """Ask the user for a start date and end date (YYYY-MM-DD)."""
    print("\nEnter the date range for the report.")
    start = input("Start date (YYYY-MM-DD): ").strip()
    end = input("End date (YYYY-MM-DD): ").strip()
    return start, end


def get_summary(connection, start_text, end_text):
    cur = connection.cursor()

    cur.execute("""
        SELECT
            COUNT(DISTINCT order_id) AS total_orders,
            COUNT(DISTINCT customer_id) AS unique_customers
        FROM orders
        WHERE DATE(order_date) BETWEEN DATE(?) AND DATE(?)
    """, (start_text, end_text))
    row = cur.fetchone()
    total_orders = row[0] if row[0] is not None else 0
    unique_customers = row[1] if row[1] is not None else 0

    cur.execute("""
        SELECT
            SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS total_revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE DATE(o.order_date) BETWEEN DATE(?) AND DATE(?)
    """, (start_text, end_text))
    row = cur.fetchone()
    total_revenue = row[0] if row[0] is not None else 0.0

    cur.execute("""
        SELECT
            p.product_name,
            SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS product_revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE DATE(o.order_date) BETWEEN DATE(?) AND DATE(?)
        GROUP BY p.product_name
        ORDER BY product_revenue DESC
        LIMIT 3
    """, (start_text, end_text))
    top3 = cur.fetchall()

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "unique_customers": unique_customers,
        "top_3_products": top3
    }


def get_prev_period(start_text, end_text):

    start_date = datetime.strptime(start_text, "%Y-%m-%d")
    end_date = datetime.strptime(end_text, "%Y-%m-%d")

    period_length = (end_date - start_date).days + 1

    previous_end = start_date - timedelta(days=1)
    previous_start = previous_end - timedelta(days=period_length - 1)

    return previous_start.strftime("%Y-%m-%d"), previous_end.strftime("%Y-%m-%d")


def percent_change(old_value, new_value):
    """Return the percent change from old_value to new_value."""
    if old_value == 0 or old_value is None:
        return None
    return round((new_value - old_value) * 100.0 / old_value, 2)


def print_report(report_type, start_text, end_text, current_summary, previous_summary):
    """Print the final summary report in a readable format."""
    print("\n" + "=" * 50)
    print(report_type.upper(), "REPORT")
    print("Period:", start_text, "to", end_text)
    print("=" * 50)

    print("Total Orders     :", current_summary["total_orders"])
    print("Total Revenue    :", round(current_summary["total_revenue"], 2))
    print("Unique Customers :", current_summary["unique_customers"])

    print("\nTop 3 Products:")
    if len(current_summary["top_3_products"]) == 0:
        print("  No product sales found in this period.")
    else:
        rank = 1
        for product_name, product_revenue in current_summary["top_3_products"]:
            print("  ", rank, "-", product_name, ":", round(product_revenue, 2))
            rank += 1

    print("\nComparison with previous period:")
    orders_change = percent_change(previous_summary["total_orders"], current_summary["total_orders"])
    revenue_change = percent_change(previous_summary["total_revenue"], current_summary["total_revenue"])
    customers_change = percent_change(previous_summary["unique_customers"], current_summary["unique_customers"])

    print("  Orders change     :", orders_change, "%" if orders_change is not None else "(no previous data)")
    print("  Revenue change    :", revenue_change, "%" if revenue_change is not None else "(no previous data)")
    print("  Customers change  :", customers_change, "%" if customers_change is not None else "(no previous data)")
    print("=" * 50)


def main():
    connection = sqlite3.connect(database_path)

    report_type = ask_type()
    start_text, end_text = ask_dates()

    current_summary = get_summary(connection, start_text, end_text)
    previous_start, previous_end = get_prev_period(start_text, end_text)
    previous_summary = get_summary(connection, previous_start, previous_end)

    print_report(report_type, start_text, end_text, current_summary, previous_summary)
    connection.close()


if __name__ == "__main__":
    main()
