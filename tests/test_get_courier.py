import pytest
from sqlalchemy.orm import Session
from tests.utils import generate_courier
from candy.db.models import Courier


@pytest.mark.asyncio
async def test_successful_get_courier(api_client, migrated_postgres_connection):
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

    response = await api_client.get("/couriers/" + str(courier["id"]))
    assert response.status_code == 200
    assert response.json() == {
        "courier_id": courier["id"],
        "courier_type": courier["courier_type"],
        "regions": courier["regions"],
        "working_hours": courier["working_hours"],
        "rating": courier["rating"],
        "earnings": courier["earnings"]
    }


@pytest.mark.asyncio
async def test_not_found_courier(api_client):
    response = await api_client.get("/couriers/0")
    assert response.status_code == 404
