from fastapi import APIRouter
from app.schemas.order_schemas import OrdersBatchIn
from app.schemas.plan_schemas import PlanResponse
from app.services.assignment_service import plan_assignments

router = APIRouter()

@router.post("/", response_model=PlanResponse)
def plan(req: OrdersBatchIn):
    return plan_assignments(req.orders)
