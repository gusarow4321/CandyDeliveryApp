from typing import List, Optional
from pydantic import BaseModel

from candy.db.models import CourierType


class ItemId(BaseModel):
    id: int


class AssignOrder(BaseModel):
    courier_id: int


class CompleteOrder(AssignOrder):
    order_id: int
    complete_time: str


class OrderItem(BaseModel):
    order_id: int
    weight: float
    region: int
    delivery_hours: List[str]


class ImportOrdersReq(BaseModel):
    data: List[OrderItem]


class Order(OrderItem, AssignOrder):
    assign_time: str
    completed: bool = False
    completed_time: str
    courier: 'Courier'

    class Config:
        orm_mode = True


class ImportOrdersCreatedRes(BaseModel):
    orders: List[ItemId]


class ImportOrdersBadRes(BaseModel):
    validation_error: ImportOrdersCreatedRes


class AssignRes(ImportOrdersCreatedRes):
    assign_time: str


class OrderCompleteRes(BaseModel):
    order_id: int


class CourierPatch(BaseModel):
    courier_type: CourierType
    regions: List[int]
    working_hours: List[str]


class CourierItem(CourierPatch):
    courier_id: Optional[int]


class CourierGetRes(CourierItem):
    rating: float = 0
    earning: int = 0


class Courier(CourierGetRes):
    orders: List[Order] = []

    class Config:
        orm_mode = True


class ImportCouriersReq(BaseModel):
    data: List[CourierItem]


class ImportCouriersCreatedRes(BaseModel):
    couriers: List[ItemId]


class ImportCouriersBadRes(BaseModel):
    validation_error: ImportCouriersCreatedRes


Order.update_forward_refs()
