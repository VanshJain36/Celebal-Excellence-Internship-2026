"""
generate_order_items.py
"""

import csv
import os
import random

random.seed(42)

number_of_items = 500


def read_ids(file_path, id_column):
    ids = []
    with open(file_path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            ids.append(row[id_column])
    return ids


def make_items(order_ids, product_ids):
    rows = []

    bad_rows = set(random.sample(range(number_of_items), int(number_of_items * 0.03)))
    bad_order_links = set(random.sample(range(number_of_items), max(5, int(number_of_items * 0.01))))
    max_real_order_id = max(int(o) for o in order_ids)

    for i in range(number_of_items):
        item_id = i + 1

        if i in bad_order_links:
            order_id = max_real_order_id + random.randint(1000, 2000)
        else:
            order_id = random.choice(order_ids)

        product_id = random.choice(product_ids)

        if i in bad_rows:
            quantity = -random.randint(1, 5)
        else:
            quantity = random.randint(1, 10)

        price = round(random.uniform(50, 6000), 2)
        discount = round(random.uniform(0, 100), 2)

        rows.append({
            "item_id": item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": price,
            "discount_percent": discount
        })

    return rows


def save_items(rows, file_path):
    f = open(file_path, "w", newline="", encoding="utf-8")
    fields = ["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent"]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in rows:
        writer.writerow(row)

    f.close()


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))

    order_path = os.path.join(root_dir, "data", "raw", "orders.csv")
    product_path = os.path.join(root_dir, "data", "raw", "products.csv")
    output_path = os.path.join(root_dir, "data", "raw", "order_items.csv")

    order_ids = read_ids(order_path, "order_id")
    product_ids = read_ids(product_path, "product_id")

    item_rows = make_items(order_ids, product_ids)
    save_items(item_rows, output_path)
    print("Created", len(item_rows), "order items at", output_path)
