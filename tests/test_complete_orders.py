import pytest
from datetime import datetime

from sqlalchemy.orm import Session
from candy.db.models import Courier, Order


@pytest.mark.asyncio
async def test_bad_req(api_client, migrated_postgres_connection):
    response = await api_client.post("/orders/complete", json={
        "courier_id": 0,
        "order_id": 0,
        "complete_time": "2021-01-10T10:33:01.42Z"
    })
    assert response.status_code == 400

    db = Session(migrated_postgres_connection)
    order_db = Order(
        id=1,
        weight=1,
        region=1,
        delivery_hours=["15:30-20:30"]
    )
    db.add(order_db)
    db.commit()

    response = await api_client.post("/orders/complete", json={
        "courier_id": 1,
        "order_id": 1,
        "complete_time": "2021-01-10T10:33:01.42Z"
    })
    assert response.status_code == 400

    db = Session(migrated_postgres_connection)
    courier_db = Courier(
        id=2,
        courier_type="bike",
        regions=[1, 2],
        working_hours=["12:00-16:00", "18:00-19:30"],
    )
    db.add(courier_db)

    order_db = Order(
        id=2,
        weight=1,
        region=1,
        delivery_hours=["15:30-20:30"],
        courier_id=2
    )
    db.add(order_db)
    db.commit()

    response = await api_client.post("/orders/complete", json={
        "courier_id": 1,
        "order_id": 2,
        "complete_time": "2021-01-10T10:33:01.42Z"
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_successful_req(api_client, migrated_postgres_connection):
    db = Session(migrated_postgres_connection)
    courier_db = Courier(
        id=1,
        courier_type="car",
        regions=[1, 2],
        working_hours=["12:00-19:30"],
    )
    db.add(courier_db)

    order_db = Order(
        id=1,
        weight=1,
        region=1,
        delivery_hours=["15:30-20:30"],
        assign_time=datetime.strptime("2021-01-10T10:00:00.42Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        courier_id=1
    )
    db.add(order_db)
    db.commit()

    response = await api_client.post("/orders/complete", json={
        "courier_id": 1,
        "order_id": 1,
        "complete_time": "2021-01-10T10:30:00.42Z"
    })
    assert response.status_code == 200
    assert response.json() == {"order_id": 1}

    order = db.query(Order).filter(Order.id == 1).first()
    assert order.completed_time is not None
    assert order.completed

    courier = db.query(Courier).filter(Courier.id == 1).first()
    assert courier.rating != 0
    assert courier.earnings == 4500
