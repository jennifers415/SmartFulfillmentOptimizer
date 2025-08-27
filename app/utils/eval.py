from typing import List
from app.schemas.plan_schemas import Assignment

def sla_hit_rate(assignments: List[Assignment], threshold_days: float = 2.0) -> float:
    return sum(1 for a in assignments if a.eta_days <= threshold_days) / max(len(assignments), 1)
