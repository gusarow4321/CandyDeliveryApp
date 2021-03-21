import pytest
from datetime import datetime

from sqlalchemy.orm import Session
from tests.utils import generate_courier
from candy.db.models import Courier, Order


@pytest.mark.asyncio
async def test_successful_patch_courier(api_client, migrated_postgres_connection):
    courier = generate_courier()

    db = Session(migrated_postgres_connection)
    courier_db = Courier(
        id=courier["id"],
        courier_type=courier["courier_type"],
        regions=courier["regions"],
        working_hours=courier["working_hours"],
        rating=courier["rating"],
        earnings=courier["earnings"]
    )
    db.add(courier_db)
    db.commit()

    response = await api_client.patch(
        "/couriers/" + str(courier["id"]),
        json={
            "courier_type": "foot",
            "regions": [69],
            "working_hours": ["00:00-23:59"]
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "courier_id": courier["id"],
        "courier_type": "foot",
        "regions": [69],
        "working_hours": ["00:00-23:59"],
    }


@pytest.mark.asyncio
async def test_not_found_patch_courier(api_client):
    response = await api_client.patch(
        "/couriers/0",
        json={
            "courier_type": "foot",
            "regions": [69],
            "working_hours": ["00:00-23:59"]
        }
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_cancel_orders(api_client, migrated_postgres_connection):
    db = Session(migrated_postgres_connection)
    courier_db = Courier(
        id=1,
        courier_type="car",
        regions=[1, 2, 3],
        working_hours=["10:00-12:00"],
    )
    db.add(courier_db)

    order1 = Order(
        id=1,
        weight=40,
        region=1,
        delivery_hours=["10:30-11:30"],
        assign_time=datetime.utcnow(),
        courier_id=1
    )
    order2 = Order(
        id=2,
        weight=1,
        region=2,
        delivery_hours=["10:30-11:30"],
        assign_time=datetime.utcnow(),
        courier_id=1
    )
    order3 = Order(
        id=3,
        weight=1,
        region=3,
        delivery_hours=["10:30-11:30"],
        assign_time=datetime.utcnow(),
        courier_id=1
    )

    db.add(order1)
    db.add(order2)
    db.add(order3)
    db.commit()

    response = await api_client.patch(
        "/couriers/1",
        json={
            "courier_type": "foot",
            "regions": [1, 3],
            "working_hours": ["15:00-16:00"]
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "courier_id": 1,
        "courier_type": "foot",
        "regions": [1, 3],
        "working_hours": ["15:00-16:00"],
    }

    orders_ids = [order.id for order in db.query(Order).filter(Order.assign_time == None)]
    assert orders_ids == [1, 2, 3]
