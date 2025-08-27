from pydantic import BaseModel, Field
from typing import List, Optional

class OrderItem(BaseModel):
    sku: str
    qty: int = Field(gt=0)
    weight_kg: Optional[float] = 0.5

class OrderIn(BaseModel):
    order_id: str
    postal_code: str
    region: Optional[str] = None
    items: List[OrderItem]

class OrdersBatchIn(BaseModel):
    orders: List[OrderIn]
