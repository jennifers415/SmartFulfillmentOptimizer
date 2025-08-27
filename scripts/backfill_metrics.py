import pandas as pd

try:
    assignments = pd.read_csv("data/processed/assignments.csv")
except FileNotFoundError:
    print("No assignments file found. Run the optimizer first.")
    exit(0)

# Compute KPIs
kpis = {
    "avg_distance_km": assignments["distance_km"].mean(),
    "sla_2day_hit_rate": (assignments["eta_days"] <= 2).mean(),
    "stockout_rate": (assignments["stockout_flag"] == 1).mean() if "stockout_flag" in assignments else 0.0,
    "cost_per_order_usd": assignments["cost_usd"].mean() if "cost_usd" in assignments else 0.0,
}

# Save KPIs
df_kpis = pd.DataFrame([kpis])
df_kpis.to_csv("data/processed/kpis.csv", index=False)

print("Metrics backfilled → data/processed/kpis.csv")
print(df_kpis)
