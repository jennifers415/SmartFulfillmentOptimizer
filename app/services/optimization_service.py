from typing import Tuple
import pandas as pd
import numpy as np
from app.utils.geo import haversine_km

def assign_order_nearest(order_row, warehouses_df: pd.DataFrame, inv: pd.DataFrame) -> Tuple[str, float]:
    # geo mapping by region: pick centroid warehouse of same region if available, else nearest by lat/lon
    sku = order_row["sku"]
    qty = int(order_row["qty"])
    # candidate warehouses with stock
    stock = inv[inv["sku"] == sku].copy()
    stock["available"] = stock["on_hand"] - stock["safety_stock"]
    stock = stock[stock["available"] >= qty]
    if stock.empty:
        # fallback
        return "UNASSIGNED", 0.0

    candidates = warehouses_df.merge(stock[["warehouse_id", "available"]], on="warehouse_id")
    # If order has region, filter first
    region = order_row.get("region") or None
    if region:
        regional = candidates[candidates["region"] == region]
        if not regional.empty:
            chosen = regional.iloc[0]
        else:
            chosen = candidates.iloc[0]
    else:
        chosen = candidates.iloc[0]

    dist = 0.0 if region and chosen["region"] == region else 1000.0
    return str(chosen["warehouse_id"]), float(dist)
