"""
generate_orders.py
"""

import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)

number_of_orders = 500

status_list = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
status_weights = [0.15, 0.20, 0.45, 0.10, 0.10]
region_codes = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]


def read_customer_ids(file_path):
    ids = []
    with open(file_path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            ids.append(row["customer_id"])
    return ids


def random_datetime():
    start = datetime(2024, 7, 1)
    end = datetime(2026, 7, 1)
    total = int((end - start).total_seconds())
    seconds = random.randint(0, total)
    return start + timedelta(seconds=seconds)


def format_date(dt, bad_format):
    if bad_format:
        return dt.strftime("%d-%m-%Y")
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


def generate_orders(customer_ids):
    rows = []
    bad_customer_rows = set(random.sample(range(number_of_orders), int(number_of_orders * 0.05)))
    bad_date_rows = set(random.sample(range(number_of_orders), int(number_of_orders * 0.08)))

    for i in range(number_of_orders):
        order_id = i + 1

        if i in bad_customer_rows:
            customer_id = ""
        else:
            customer_id = random.choice(customer_ids)

        dt = random_datetime()
        bad_format = i in bad_date_rows
        order_date_text = format_date(dt, bad_format)
        status = random.choices(status_list, weights=status_weights)[0]
        region = random.choice(region_codes)

        rows.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date_text,
            "status": status,
            "region_code": region
        })

    return rows


def save_orders(rows, file_path):
    f = open(file_path, "w", newline="", encoding="utf-8")
    fields = ["order_id", "customer_id", "order_date", "status", "region_code"]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in rows:
        writer.writerow(row)

    f.close()


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))

    customer_path = os.path.join(root_dir, "data", "raw", "customers.csv")
    output_path = os.path.join(root_dir, "data", "raw", "orders.csv")

    customer_ids = read_customer_ids(customer_path)
    order_rows = generate_orders(customer_ids)
    save_orders(order_rows, output_path)
    print("Created", len(order_rows), "orders at", output_path)
