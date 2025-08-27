from pydantic import BaseModel
from typing import List

class Assignment(BaseModel):
    order_id: str
    warehouse_id: str
    distance_km: float
    eta_days: float

class KPIs(BaseModel):
    avg_distance_km: float
    sla_2day_hit_rate: float
    stockout_rate: float
    cost_per_order_usd: float

class PlanResponse(BaseModel):
    assignments: List[Assignment]
    kpis: KPIs
