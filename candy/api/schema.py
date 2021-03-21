from typing import List, Optional
from pydantic import BaseModel, Extra, Field, PositiveInt, constr
from datetime import datetime

from candy.db.models import CourierType

hours = constr(regex="^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")


class ItemId(BaseModel):
    id: int


class AssignOrder(BaseModel, extra=Extra.forbid):
    courier_id: int


class CompleteOrder(AssignOrder):
    order_id: int
    complete_time: datetime


class OrderItem(BaseModel, extra=Extra.forbid):
    order_id: int
    weight: float = Field(ge=0.01, le=50)
    region: PositiveInt
    delivery_hours: List[hours]


class ImportOrdersReq(BaseModel, extra=Extra.forbid):
    data: List[OrderItem]


class Order(OrderItem, AssignOrder):
    assign_time: str
    completed: bool = False
    completed_time: str
    courier: 'Courier'

    class Config:
        orm_mode = True


class ImportOrdersCreatedRes(BaseModel):
    orders: List[ItemId] = []


class ImportOrdersBadRes(BaseModel):
    validation_error: ImportOrdersCreatedRes


class AssignRes(ImportOrdersCreatedRes):
    assign_time: str = ''


class OrderCompleteRes(BaseModel):
    order_id: int


class CourierPatch(BaseModel, extra=Extra.forbid):
    courier_type: Optional[CourierType]
    regions: Optional[List[PositiveInt]]
    working_hours: Optional[List[hours]]


class CourierItem(BaseModel, extra=Extra.forbid):
    courier_id: Optional[int]
    courier_type: CourierType
    regions: List[PositiveInt]
    working_hours: List[hours]


class CourierGetRes(CourierItem):
    rating: Optional[float] = 0
    earnings: int = 0


class Courier(CourierGetRes):
    orders: List[Order] = []

    class Config:
        orm_mode = True


class ImportCouriersReq(BaseModel, extra=Extra.forbid):
    data: List[CourierItem]


class ImportCouriersCreatedRes(BaseModel):
    couriers: List[ItemId] = []


class ImportCouriersBadRes(BaseModel):
    validation_error: ImportCouriersCreatedRes


Order.update_forward_refs()
