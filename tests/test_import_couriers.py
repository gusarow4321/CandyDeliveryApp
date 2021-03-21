import pytest
from tests.utils import generate_courier


@pytest.mark.asyncio
async def test_created_import_couriers(api_client):
    courier = generate_courier()

    response = await api_client.post(
        "/couriers",
        json={
            "data": [
                {
                    "courier_id": courier['id'],
                    "courier_type": courier['courier_type'],
                    "regions": courier['regions'],
                    "working_hours": courier['working_hours']
                }
            ]
        },
    )
    assert response.status_code == 201
    assert response.json() == {"couriers": [{"id": courier["id"]}]}


@pytest.mark.asyncio
async def test_bad_import_couriers(api_client):
    courier1 = generate_courier(working_hours=["54:78-abc"])
    courier2 = generate_courier()

    response = await api_client.post(
        "/couriers",
        json={
            "data": [
                {
                    "courier_id": courier1['id'],
                    "courier_type": courier1['courier_type'],
                    "regions": courier1['regions'],
                    "working_hours": courier1['working_hours']
                },
                {
                    "courier_id": courier2['id'],
                    "courier_type": courier2['courier_type'],
                    "regions": courier2['regions'],
                    "working_hours": courier2['working_hours'],
                    "additional": "property"
                }
            ],
            "additional": "property"
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "validation_error": {
            "couriers": [
                {
                    "id": courier1["id"]
                },
                {
                    "id": courier2["id"],
                    "additional": "property"
                }
            ],
            "additional": "property"
        }
    }
