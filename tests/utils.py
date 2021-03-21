from typing import List
from random import choice, randint
from datetime import datetime

from candy.api.schema import CourierType


def generate_courier(
        courier_id: int = None,
        courier_type: CourierType = None,
        regions: List[int] = None,
        working_hours: List[str] = None,
        rating: float = None,
        earnings: int = None
):
    if courier_id is None:
        courier_id = randint(1, 1000)

    if courier_type is None:
        courier_type = choice(["foot", "bike", "car"])

    if regions is None:
        regions = [randint(1, 100) for _ in range(10)]

    if working_hours is None:
        working_hours = ["10:30-13:45", "15:00-18:00"]

    if rating is None:
        rating = randint(1, 10000) / 100

    if earnings is None:
        earnings = randint(1, 1000000)

    return {
        'id': courier_id,
        'courier_type': courier_type,
        'regions': regions,
        'working_hours': working_hours,
        'rating': rating,
        'earnings': earnings
    }


def generate_order(
        order_id: int = None,
        weight: float = None,
        region: int = None,
        delivery_hours: List[str] = None,
        assign_time: datetime = None,
        completed: bool = False,
        completed_time: datetime = None,
        courier_id: int = None
):
    if order_id is None:
        order_id = randint(1, 1000)

    if weight is None:
        weight = randint(1, 5000) / 100

    if region is None:
        region = randint(1, 100)

    if delivery_hours is None:
        delivery_hours = ["10:30-13:45", "15:00-18:00"]

    return {
        'id': order_id,
        'weight': weight,
        'region': region,
        'delivery_hours': delivery_hours,
        'assign_time': assign_time,
        'completed': completed,
        'completed_time': completed_time,
        'courier_id': courier_id
    }
