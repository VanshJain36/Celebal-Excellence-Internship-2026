"""
load_sqlite.py

This script reads the cleaned CSV files from data/cleaned and loads
them into a SQLite database file at database/ecommerce.db
"""

import os
import sqlite3
import pandas as pd

SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

CLEANED_FOLDER = os.path.join(PROJECT_DIR, "data", "cleaned")
DATABASE_PATH = os.path.join(PROJECT_DIR, "database", "ecommerce.db")


def load_table(connection, csv_file_name, table_name):
    """Read a cleaned CSV file and load it into a SQLite table."""
    file_path = os.path.join(CLEANED_FOLDER, csv_file_name)
    data_frame = pd.read_csv(file_path)

    data_frame.to_sql(table_name, connection, if_exists="replace", index=False)
    print("Loaded", len(data_frame), "rows into table:", table_name)


def create_indexes(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id)")
    connection.commit()
    print("Indexes created.")


def main():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)

    load_table(connection, "customers.csv", "customers")
    load_table(connection, "products.csv", "products")
    load_table(connection, "orders.csv", "orders")
    load_table(connection, "order_items.csv", "order_items")

    create_indexes(connection)

    connection.close()
    print("\nAll tables loaded into", DATABASE_PATH)


if __name__ == "__main__":
    main()
