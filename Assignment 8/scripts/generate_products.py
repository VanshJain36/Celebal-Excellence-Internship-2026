"""
generate_products.py
"""

import csv
import os
import random

random.seed(42)

category_data = {
    "Electronics": {
        "subcategories": ["Mobiles", "Laptops", "Accessories", "Cameras"],
        "products": [
            "Smartphone X1", "Smartphone Z2", "Laptop Pro", "Laptop Air",
            "Wireless Mouse", "Bluetooth Headphones", "USB Cable", "Power Bank",
            "DSLR Camera", "Action Camera", "Smart Watch", "Tablet Mini"
        ]
    },
    "Clothing": {
        "subcategories": ["Men", "Women", "Kids", "Footwear"],
        "products": [
            "Cotton T-Shirt", "Denim Jeans", "Formal Shirt", "Summer Dress",
            "Winter Jacket", "Running Shoes", "Casual Sneakers", "Kids T-Shirt",
            "Leather Belt", "Woolen Sweater"
        ]
    },
    "Home": {
        "subcategories": ["Kitchen", "Furniture", "Decor", "Bedding"],
        "products": [
            "Non Stick Pan", "Dinner Set", "Wooden Chair", "Study Table",
            "Wall Clock", "Table Lamp", "Cotton Bedsheet", "Pillow Set",
            "Curtain Set", "Storage Box"
        ]
    },
    "Books": {
        "subcategories": ["Fiction", "Non-Fiction", "Children", "Academic"],
        "products": [
            "Mystery Novel", "Self Help Guide", "Fairy Tales Collection",
            "History Textbook", "Science Textbook", "Cook Book",
            "Biography", "Poetry Collection", "Comic Book", "Travel Guide"
        ]
    }
}


def messy_name(name):
    kind = random.choice(["extra_spaces", "upper", "lower", "mixed"])

    if kind == "extra_spaces":
        return "   " + name + "   "
    elif kind == "upper":
        return name.upper()
    elif kind == "lower":
        return name.lower()
    else:
        words = name.split(" ")
        mixed_words = []
        for word in words:
            if random.random() < 0.5:
                mixed_words.append(word.upper())
            else:
                mixed_words.append(word.lower())
        return " ".join(mixed_words)


def generate_products():
    rows = []
    product_id = 1
    target_rows = 520

    all_combinations = []
    for category, info in category_data.items():
        for product_name in info["products"]:
            subcategory = random.choice(info["subcategories"])
            all_combinations.append((category, subcategory, product_name))

    messy_count = int(target_rows * 0.15)

    while len(rows) < target_rows:
        category, subcategory, base_name = random.choice(all_combinations)
        number = random.randint(1, 999)
        product_name = base_name + " " + str(number)
        cost_price = round(random.uniform(50, 5000), 2)

        rows.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "subcategory": subcategory,
            "cost_price": cost_price
        })
        product_id += 1

    messy_indexes = random.sample(range(len(rows)), messy_count)
    for index in messy_indexes:
        rows[index]["product_name"] = messy_name(rows[index]["product_name"])

    return rows


def save_products(rows, file_path):
    f = open(file_path, "w", newline="", encoding="utf-8")
    fields = ["product_id", "product_name", "category", "subcategory", "cost_price"]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in rows:
        writer.writerow(row)

    f.close()


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    output_path = os.path.join(root_dir, "data", "raw", "products.csv")

    product_rows = generate_products()
    save_products(product_rows, output_path)
    print("Created", len(product_rows), "products at", output_path)
