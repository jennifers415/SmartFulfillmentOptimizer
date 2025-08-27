import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)

n_orders = 500
skus = ["SKU123", "SKU456", "SKU789"]
regions = ["NE", "MW", "SC", "W"]
warehouses = pd.read_csv("data/raw/warehouses.csv")

# Generate synthetic orders
orders = []
start_date = datetime(2025, 8, 1)

for i in range(n_orders):
    order_id = f"ORD{i+1}"
    created_at = start_date + timedelta(minutes=random.randint(0, 10000))
    sku = random.choice(skus)
    qty = random.randint(1, 5)
    weight = round(random.uniform(0.2, 3.0), 2)
    postal_code = fake.postcode()
    region = random.choice(regions)

    orders.append([order_id, postal_code, region, created_at.isoformat(), sku, qty, weight])

df_orders = pd.DataFrame(
    orders, columns=["order_id", "postal_code", "region", "created_at", "sku", "qty", "weight_kg"]
)
df_orders.to_csv("data/raw/synthetic_orders.csv", index=False)

# Generate synthetic inventory
inventory = []
for _, wh in warehouses.iterrows():
    for sku in skus:
        on_hand = random.randint(200, 1200)
        safety = int(on_hand * 0.1)
        inventory.append([wh["warehouse_id"], sku, on_hand, safety])

df_inv = pd.DataFrame(inventory, columns=["warehouse_id", "sku", "on_hand", "safety_stock"])
df_inv.to_csv("data/raw/inventory.csv", index=False)

print("Synthetic orders & inventory generated.")
