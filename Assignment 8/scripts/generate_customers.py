"""
generate_customers.py
"""

import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)
number_of_customers = 500

first_names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Krishna",
    "Ishaan", "Rohan", "Ananya", "Diya", "Isha", "Kavya", "Meera", "Priya",
    "Riya", "Saanvi", "Tara", "Zara", "John", "Emma", "Olivia",
    "William", "Sophia", "James"
]

last_names = [
    "Sharma", "Verma", "Gupta", "Patel", "Reddy", "Nair", "Iyer", "Singh",
    "Kumar", "Das", "Mehta", "Joshi", "Kapoor", "Malhotra", "Chopra",
    "Smith", "Johnson", "Taylor", "Wilson"
]

customer_types = ["REGULAR", "PREMIUM", "VIP"]
weights = [0.65, 0.25, 0.10]
email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]


def random_date():
    start = datetime(2023, 1, 1)
    end = datetime(2026, 7, 1)
    total = (end - start).days
    days = random.randint(0, total)
    d = start + timedelta(days=days)
    return d.strftime("%Y-%m-%d")


def make_email(name, bad):
    clean_name = name.lower().replace(" ", ".")
    domain = random.choice(email_domains)

    if bad == True:
        x = random.choice(["no_at", "no_domain"])
        if x == "no_at":
            return clean_name + domain
        else:
            return clean_name + "@"
    else:
        return clean_name + "@" + domain


def generate_customers():
    rows = []
    bad_rows = set(random.sample(range(number_of_customers), int(number_of_customers * 0.02)))

    for x in range(number_of_customers):
        first = random.choice(first_names)
        last = random.choice(last_names)
        full_name = first + " " + last

        if x in bad_rows:
            bad = True
        else:
            bad = False

        email = make_email(full_name, bad)
        date = random_date()
        c_type = random.choices(customer_types, weights=weights)[0]

        rows.append({
            "customer_id": x + 1,
            "customer_name": full_name,
            "email": email,
            "registration_date": date,
            "customer_type": c_type
        })

    return rows


def save_to_csv(rows, file_path):
    f = open(file_path, "w", newline="", encoding="utf-8")
    fields = ["customer_id", "customer_name", "email", "registration_date", "customer_type"]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in rows:
        writer.writerow(row)

    f.close()


if __name__ == "__main__":
    data = generate_customers()
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "customers.csv"))
    save_to_csv(data, output_path)
    print("Created", len(data), "customers at", output_path)
