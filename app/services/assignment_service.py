from typing import List
import pandas as pd
from app.schemas.order_schemas import OrderIn
from app.schemas.plan_schemas import Assignment, KPIs, PlanResponse
from app.deps import get_warehouses_df, get_inventory_df
from app.services.optimization_service import assign_order_nearest

def plan_assignments(orders: List[OrderIn]) -> PlanResponse:
    wh = get_warehouses_df()
    inv = get_inventory_df().copy()

    assignments = []
    stockouts = 0

    for o in orders:
        # flatten order items to per-item orders
        for item in o.items:
            order_row = {
                "order_id": o.order_id,
                "region": o.region,
                "postal_code": o.postal_code,
                "sku": item.sku,
                "qty": item.qty,
            }
            wid, dist_km = assign_order_nearest(order_row, wh, inv)
            eta_days = 1.0 if dist_km < 800 else 2.5
            if wid == "UNASSIGNED":
                stockouts += 1
                eta_days = 3.0
            else:
                # decrement inventory
                inv_idx = (inv["warehouse_id"] == wid) & (inv["sku"] == item.sku)
                inv.loc[inv_idx, "on_hand"] = inv.loc[inv_idx, "on_hand"] - item.qty

            assignments.append(
                Assignment(
                    order_id=o.order_id,
                    warehouse_id=wid,
                    distance_km=dist_km,
                    eta_days=float(eta_days),
                )
            )

    avg_dist = sum(a.distance_km for a in assignments) / max(len(assignments), 1)
    sla_hit = sum(1 for a in assignments if a.eta_days <= 2.0) / max(len(assignments), 1)
    stockout_rate = stockouts / max(len(assignments), 1)

    kpis = KPIs(
        avg_distance_km=avg_dist,
        sla_2day_hit_rate=sla_hit,
        stockout_rate=stockout_rate,
        cost_per_order_usd=5.0,
    )
    return PlanResponse(assignments=assignments, kpis=kpis)
