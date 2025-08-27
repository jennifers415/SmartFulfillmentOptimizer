from pydantic import BaseModel

class ForecastQuery(BaseModel):
    sku: str
    region: str
    horizon_days: int = 7

class ForecastResponse(BaseModel):
    sku: str
    region: str
    horizon_days: int
    daily_demand: list
