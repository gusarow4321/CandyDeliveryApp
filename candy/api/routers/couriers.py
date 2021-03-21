from fastapi import APIRouter, status
from fastapi.responses import Response
from fastapi_sqlalchemy import db
from candy.api.crud import create_courier, get_courier, update_courier, get_uncompleted_orders, cancel_order
from candy.api.schema import (
    ImportCouriersReq,
    ImportCouriersCreatedRes,
    ItemId,
    CourierGetRes,
    CourierPatch,
    CourierItem,
)
from candy.utils.utils import get_max_weight, is_ranges_crossing

router = APIRouter(
    prefix="/couriers",
    tags=["couriers"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def import_couriers(req: ImportCouriersReq):
    res = ImportCouriersCreatedRes()
    for courier in req.data:
        if await get_courier(db.session, courier.courier_id) is None:
            courier_db = await create_courier(db.session, courier)
            res.couriers.append(ItemId(id=courier_db.id))
    return res


@router.get("/{courier_id}")
async def get_courier_by_id(courier_id: int):
    courier = await get_courier(db.session, courier_id)
    if courier is None:
        return Response(status_code=404)
    res = CourierGetRes(
        courier_id=courier.id,
        courier_type=courier.courier_type,
        regions=courier.regions,
        working_hours=courier.working_hours,
        rating=courier.rating,
        earnings=courier.earnings,
    )
    return res.dict(exclude={} if res.rating != 0 else {'rating'})


@router.patch("/{courier_id}")
async def update_courier_by_id(courier_id: int, courier: CourierPatch):
    res = await update_courier(db.session, courier_id, courier)
    if res is None:
        return Response(status_code=404)

    uncompleted = await get_uncompleted_orders(db.session, courier_id)
    for order in uncompleted:
        weight_check = order.weight > get_max_weight(res.courier_type)
        regions_check = order.region not in res.regions
        hours_check = not is_ranges_crossing(res.working_hours, order.delivery_hours)
        if weight_check or regions_check or hours_check:
            await cancel_order(db.session, order.id)

    return CourierItem(
        courier_id=res.id,
        courier_type=res.courier_type,
        regions=res.regions,
        working_hours=res.working_hours,
    )
