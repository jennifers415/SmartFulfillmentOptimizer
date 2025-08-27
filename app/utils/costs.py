def shipping_cost(distance_km: float, weight_kg: float) -> float:
    base = 2.0
    per_km = 0.003
    per_kg = 0.4
    return base + per_km * distance_km + per_kg * weight_kg
