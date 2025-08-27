from functools import lru_cache
import pandas as pd
from app.config import settings

@lru_cache
def get_orders_df() -> pd.DataFrame:
    return pd.read_csv(f"{settings.raw_dir}/synthetic_orders.csv")

@lru_cache
def get_warehouses_df() -> pd.DataFrame:
    return pd.read_csv(f"{settings.raw_dir}/warehouses.csv")

@lru_cache
def get_inventory_df() -> pd.DataFrame:
    return pd.read_csv(f"{settings.raw_dir}/inventory.csv")
