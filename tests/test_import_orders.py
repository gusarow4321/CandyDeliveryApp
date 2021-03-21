import pytest
from tests.utils import generate_order


@pytest.mark.asyncio
async def test_created_import_orders(api_client):
    order = generate_order()

    response = await api_client.post(
        "/orders",
        json={
            "data": [
                {
                    "order_id": order['id'],
                    "weight": order['weight'],
                    "region": order['region'],
                    "delivery_hours": order['delivery_hours']
                }
            ]
        },
    )
    assert response.status_code == 201
    assert response.json() == {"orders": [{"id": order["id"]}]}


@pytest.mark.asyncio
async def test_bad_import_orders(api_client):
    order1 = generate_order(delivery_hours=["54:78-abc"])
    order2 = generate_order()

    response = await api_client.post(
        "/orders",
        json={
            "data": [
                {
                    "order_id": order1['id'],
                    "weight": order1['weight'],
                    "region": order1['region'],
                    "delivery_hours": order1['delivery_hours']
                },
                {
                    "order_id": order2['id'],
                    "weight": order2['weight'],
                    "region": order2['region'],
                    "delivery_hours": order2['delivery_hours'],
                    "additional": "property"
                }
            ],
            "additional": "property"
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "validation_error": {
            "orders": [
                {
                    "id": order1["id"]
                },
                {
                    "id": order2["id"],
                    "additional": "property"
                }
            ],
            "additional": "property"
        }
    }
