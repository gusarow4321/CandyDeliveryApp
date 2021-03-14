from typing import List
from pydantic import BaseModel
from typing import ForwardRef

from candy.db.models import CourierType

courier_item = ForwardRef('Courier')


class Order(BaseModel):
    id: int
    weight: float
    region: int
    delivery_hours: List[str]
    assign_time: str
    completed: bool = False
    completed_time: str
    courier_id = int
    courier: courier_item

    class Config:
        orm_mode = True


class Courier(BaseModel):
    id: int
    courier_type: CourierType
    regions: List[int]
    working_hours: List[str]
    rating: float = 0
    earning: int = 0
    busy: bool = False
    orders: List[Order] = []

    class Config:
        orm_mode = True
