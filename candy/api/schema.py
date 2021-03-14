from typing import List
from pydantic import BaseModel

from candy.db.models import CourierType


class Order(BaseModel):
    id: int
    weight: float
    region: int
    delivery_hours: List[str]
    assign_time: str
    completed: bool = False
    completed_time: str
    courier_id = int

    class Config:
        orm_mode = True


class Courier(BaseModel):
    id: int
    courier_type: CourierType
    regions: List[int]
    working_hours: List[str]
    rating: float
    earning: int
    busy: bool = False
    orders: List[Order]

    class Config:
        orm_mode = True
