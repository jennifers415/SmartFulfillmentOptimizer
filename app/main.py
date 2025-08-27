from fastapi import FastAPI
from app.routers import health, orders, forecast, plan

app = FastAPI(title="Smart Fulfillment Optimizer", version="0.1.0")

app.include_router(health.router)
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(forecast.router, prefix="/forecast", tags=["forecast"])
app.include_router(plan.router, prefix="/plan", tags=["plan"])
