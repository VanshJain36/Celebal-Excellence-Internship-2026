"""
clean_data.py

Part 2: Data Cleaning

Functions in this file:
1. clean_orders()              - fix date formats, handle NULL customer_id
2. clean_products()             - normalize product names (trim + title case)
3. validate_emails()            - find customer_ids with invalid emails
4. check_referential_integrity() - find order_items pointing to orders
                                    that do not exist
"""

import os
import re
import pandas as pd

script_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(script_dir, ".."))

raw_folder = os.path.join(project_dir, "data", "raw")
cleaned_folder = os.path.join(project_dir, "data", "cleaned")
report_path = os.path.join(project_dir, "reports", "data_quality_report.txt")


def clean_orders(orders_df):
    """
    Clean the orders table.

    - order_date can be in two formats:
        correct:  YYYY-MM-DD HH:MM:SS
        wrong:    DD-MM-YYYY
    """

    cleaned = orders_df.copy()

    fixed_date_count = 0
    missing_customer_count = 0

    fixed_dates = []
    for value in cleaned["order_date"]:
        text_value = str(value).strip()

        # try the correct format first
        try:
            parsed_date = pd.to_datetime(text_value, format="%Y-%m-%d %H:%M:%S")
            fixed_dates.append(parsed_date)
            continue
        except ValueError:
            pass

        # try the wrong format (DD-MM-YYYY) next
        try:
            parsed_date = pd.to_datetime(text_value, format="%d-%m-%Y")
            fixed_dates.append(parsed_date)
            fixed_date_count += 1
            continue
        except ValueError:
            pass

        parsed_date = pd.to_datetime(text_value, errors="coerce")
        fixed_dates.append(parsed_date)
        if pd.isna(parsed_date):
            fixed_date_count += 1

    cleaned["order_date"] = fixed_dates

    # handle missing customer_id values
    def fix_customer_id(value):
        text_value = str(value).strip()
        if text_value == "" or text_value.upper() == "NULL" or text_value == "nan":
            return "UNKNOWN"
        return text_value

    original_customer_ids = cleaned["customer_id"].copy()
    cleaned["customer_id"] = cleaned["customer_id"].apply(fix_customer_id)
    missing_customer_count = int((cleaned["customer_id"] == "UNKNOWN").sum())

    report_lines = [
        "clean_orders(): fixed " + str(fixed_date_count) + " rows with wrong date format",
        "clean_orders(): found " + str(missing_customer_count) + " rows with missing customer_id (set to UNKNOWN)"
    ]

    return cleaned, report_lines


def clean_products(products_df):
    """
    Clean the products table.
    """
    cleaned = products_df.copy()

    messy_count = 0
    cleaned_names = []
    for name in cleaned["product_name"]:
        original_name = str(name)
        fixed_name = original_name.strip().title()
        if fixed_name != original_name:
            messy_count += 1
        cleaned_names.append(fixed_name)

    cleaned["product_name"] = cleaned_names

    report_lines = [
        "clean_products(): cleaned " + str(messy_count) + " messy product names (spaces/case fixed)"
    ]

    return cleaned, report_lines


def validate_emails(customers_df):
    """
    Check every email address in the customers table.
    A valid email must have exactly one @ symbol and a domain name
    with a dot after the @ (for example someone@gmail.com).

    Returns a list of customer_id values that have an invalid email.
    """
    email_pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    invalid_customer_ids = []
    for index, row in customers_df.iterrows():
        email = str(row["email"])
        if not email_pattern.match(email):
            invalid_customer_ids.append(row["customer_id"])

    return invalid_customer_ids


def check_referential_integrity(orders_df, order_items_df):
    valid_order_ids = set(orders_df["order_id"].astype(int).astype(str))

    broken_item_ids = []
    item_ids = order_items_df["item_id"].tolist()
    order_ids = order_items_df["order_id"].tolist()

    for item_id, order_id in zip(item_ids, order_ids):
        order_id_text = str(int(order_id))
        if order_id_text not in valid_order_ids:
            broken_item_ids.append(int(item_id))

    return broken_item_ids


def run_cleaning_pipeline():
    os.makedirs(cleaned_folder, exist_ok=True)

    print("Reading raw CSV files...")
    orders_df = pd.read_csv(os.path.join(raw_folder, "orders.csv"), dtype={"customer_id": str})
    products_df = pd.read_csv(os.path.join(raw_folder, "products.csv"))
    customers_df = pd.read_csv(os.path.join(raw_folder, "customers.csv"))
    order_items_df = pd.read_csv(os.path.join(raw_folder, "order_items.csv"))

    all_report_lines = []

    # 1. clean orders
    cleaned_orders_df, orders_report = clean_orders(orders_df)
    all_report_lines.extend(orders_report)

    # 2. clean products
    cleaned_products_df, products_report = clean_products(products_df)
    all_report_lines.extend(products_report)

    # 3. validate emails
    invalid_emails = validate_emails(customers_df)
    all_report_lines.append(
        "validate_emails(): found " + str(len(invalid_emails)) + " customers with invalid email addresses"
    )

    # 4. check referential integrity (order_items -> orders)

    broken_items = check_referential_integrity(orders_df, order_items_df)
    all_report_lines.append(
        "check_referential_integrity(): found " + str(len(broken_items)) +
        " order_items rows pointing to an order_id that does not exist"
    )

    # save the cleaned files (customers and order_items did not need
    # structural cleaning, so we save them as they are)
    cleaned_orders_df.to_csv(os.path.join(cleaned_folder, "orders.csv"), index=False)
    cleaned_products_df.to_csv(os.path.join(cleaned_folder, "products.csv"), index=False)
    customers_df.to_csv(os.path.join(cleaned_folder, "customers.csv"), index=False)
    order_items_df.to_csv(os.path.join(cleaned_folder, "order_items.csv"), index=False)

    # write the report to a text file as well as printing it
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write("DATA QUALITY REPORT\n")
        report_file.write("====================\n\n")
        for line in all_report_lines:
            report_file.write(line + "\n")

        report_file.write("\nCustomer ids with invalid emails:\n")
        report_file.write(str(invalid_emails) + "\n")

        report_file.write("\nItem ids with broken order_id reference:\n")
        report_file.write(str(broken_items) + "\n")

    print("\n".join(all_report_lines))
    print("\nCleaned files saved to", cleaned_folder)
    print("Full report saved to", report_path)


if __name__ == "__main__":
    run_cleaning_pipeline()
