import pytest

from sqlalchemy.orm import Session
from candy.db.models import Courier, Order


@pytest.mark.asyncio
async def test_not_found_courier(api_client):
    response = await api_client.post("/orders/assign", json={"courier_id": 0})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_assign_orders(api_client, migrated_postgres_connection):
    db = Session(migrated_postgres_connection)
    courier_db = Courier(
        id=1,
        courier_type="bike",
        regions=[1, 2],
        working_hours=["12:00-16:00", "18:00-19:30"],
    )
    db.add(courier_db)

    order_db = Order(
        id=1,
        weight=0.6,
        region=2,
        delivery_hours=["15:30-20:30"],
    )
    db.add(order_db)
    db.commit()

    response = await api_client.post("/orders/assign", json={"courier_id": 1})
    assert response.status_code == 200
    assert response.json()["orders"] == [{"id": 1}]
    assert response.json().get("assign_time") is not None

    order = db.query(Order).filter(Order.id == 1).first()
    assert order.assign_time is not None and order.courier_id == 1


@pytest.mark.asyncio
async def test_not_assign_orders(api_client, migrated_postgres_connection):
    db = Session(migrated_postgres_connection)
    courier_db = Courier(
        id=1,
        courier_type="bike",
        regions=[1, 2],
        working_hours=["12:00-16:00", "18:00-19:30"],
    )
    db.add(courier_db)

    order_db = Order(
        id=1,
        weight=50,
        region=4,
        delivery_hours=["15:30-20:30"],
    )
    db.add(order_db)
    db.commit()

    response = await api_client.post("/orders/assign", json={"courier_id": 1})
    assert response.status_code == 200
    assert response.json()["orders"] == []
    assert response.json().get("assign_time") is None
