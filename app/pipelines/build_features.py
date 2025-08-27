import pandas as pd
from app.config import settings

def main():
    orders = pd.read_csv(f"{settings.raw_dir}/synthetic_orders.csv", parse_dates=["created_at"])

    feats = (
        orders.groupby([orders["created_at"].dt.date, "sku", "region"])["qty"]
        .sum()
        .reset_index()
        .rename(columns={"created_at": "date", "qty": "demand"})
    )
    out = f"{settings.processed_dir}/features.parquet"
    feats.to_parquet(out, index=False)
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
