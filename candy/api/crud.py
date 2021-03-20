from sqlalchemy.orm import Session
from candy.api.schema import CourierItem, CourierPatch, OrderItem
from candy.db.models import Order as Order_model, Courier as Courier_model
from typing import List
from datetime import datetime


async def create_courier(db: Session, courier: CourierItem):
    courier_db = Courier_model(
        id=courier.courier_id,
        courier_type=courier.courier_type,
        regions=courier.regions,
        working_hours=courier.working_hours
    )
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


async def get_courier(db: Session, courier_id: int) -> Courier_model:
    return db.query(Courier_model).filter(Courier_model.id == courier_id).first()


async def update_courier(db: Session, courier_id: int, courier: CourierPatch):
    courier_db: Courier_model = db.query(Courier_model).filter(Courier_model.id == courier_id).first()
    if courier_db is None:
        return None
    if courier.courier_type is not None:
        courier_db.courier_type = courier.courier_type
    if courier.regions is not None:
        courier_db.regions = courier.regions
    if courier.working_hours is not None:
        courier_db.working_hours = courier.working_hours
    db.commit()
    return courier_db


async def update_earnings_and_rating(db: Session, courier_id: int, val: int, rating: float):
    courier_db: Courier_model = db.query(Courier_model).filter(Courier_model.id == courier_id).first()
    courier_db.earning += val
    courier_db.rating = rating
    db.commit()
    return courier_db


async def create_order(db: Session, order: OrderItem):
    order_db = Order_model(
        id=order.order_id,
        weight=order.weight,
        region=order.region,
        delivery_hours=order.delivery_hours
    )
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


async def get_order(db: Session, order_id: int):
    return db.query(Order_model).filter(Order_model.id == order_id).first()


async def get_vacant_orders(db: Session, regions: List[int], max_weight: int):
    return db.query(Order_model).filter(Order_model.region in regions,
                                        Order_model.assign_time is None,
                                        Order_model.weight <= max_weight)


async def get_uncompleted_orders(db: Session, courier_id: int) -> List[Order_model]:
    return db.query(Order_model).filter(Order_model.courier_id == courier_id, Order_model.completed is False)


async def get_completed_orders(db: Session, courier_id: int) -> List[Order_model]:
    return db.query(Order_model).filter(Order_model.courier_id == courier_id,
                                        Order_model.completed is True).order_by(Order_model.completed_time)


async def cancel_order(db: Session, order_id: int):
    order_db: Order_model = db.query(Order_model).filter(Order_model.id == order_id).first()
    order_db.assign_time = None
    order_db.courier_id = None
    db.commit()
    return order_db


async def update_assign_time(db: Session, order_id: int, dt: datetime, courier_id: int):
    order_db: Order_model = db.query(Order_model).filter(Order_model.id == order_id).first()
    order_db.assign_time = dt
    order_db.courier_id = courier_id
    db.commit()
    return order_db


async def complete_order(db: Session, order_id: int, courier_id: int, complete_time: datetime):
    order_db: Order_model = db.query(Order_model).filter(Order_model.id == order_id).first()
    if order_db is None or order_db.courier_id is None or order_db.courier_id != courier_id:
        return None
    order_db.completed_time = complete_time
    order_db.completed = True
    db.commit()
    return order_db


# def update_order(db: Session, order: Order_schema):
#     order_db: Order_model = db.query(Order_model).filter(Order_model.id == order.id).first()
