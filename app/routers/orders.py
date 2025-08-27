from fastapi import APIRouter
from app.deps import get_orders_df

router = APIRouter()

@router.get("/")
def list_orders(limit: int = 50):
    df = get_orders_df().head(limit)
    return {"count": len(df), "orders": df.to_dict(orient="records")}
