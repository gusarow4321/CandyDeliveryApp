from sqlalchemy.orm import Session
from candy.api.schema import Order as Order_schema, Courier as Courier_schema
from candy.db.models import Order as Order_model, Courier as Courier_model


def create_courier(db: Session, courier: Courier_schema):
    courier_db = Courier_model(
        courier_type=courier.courier_type,
        regions=courier.regions,
        working_hours=courier.working_hours
    )
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


def get_courier(db: Session, courier_id: int):
    return db.query(Courier_model).filter(Courier_model.id == courier_id).first()


def update_courier(db: Session, courier: Courier_schema):
    courier_db: Courier_model = db.query(Courier_model).filter(Courier_model.id == courier.id).first()
    courier_db.type = courier.courier_type
    courier_db.regions = courier.regions
    courier_db.working_hours = courier.working_hours
    db.commit()
    return courier_db


def create_order(db: Session, order: Order_schema):
    order_db = Order_model(
        weight=order.weight,
        region=order.region,
        delivery_hours=order.delivery_hours
    )
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


def get_order(db: Session, order_id: int):
    return db.query(Order_model).filter(Order_model.id == order_id).first()


# def update_order(db: Session, order: Order_schema):
#     order_db: Order_model = db.query(Order_model).filter(Order_model.id == order.id).first()
