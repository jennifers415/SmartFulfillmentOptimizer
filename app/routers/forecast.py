from fastapi import APIRouter
from app.schemas.forecast_schemas import ForecastQuery, ForecastResponse
from app.services.forecasting_service import forecast_sku_region

router = APIRouter()

@router.post("/", response_model=ForecastResponse)
def do_forecast(req: ForecastQuery):
    values = forecast_sku_region(req.sku, req.region, req.horizon_days)
    return ForecastResponse(
        sku=req.sku, region=req.region, horizon_days=req.horizon_days, daily_demand=values
    )
