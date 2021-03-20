from fastapi import APIRouter
from fastapi.responses import Response
from fastapi_sqlalchemy import db
from candy.api.crud import (
    create_order,
    get_order,
    get_courier,
    get_vacant_orders,
    update_assign_time,
    complete_order,
    get_completed_orders,
    update_earnings_and_rating
)
from candy.api.schema import (
    ImportOrdersReq,
    ImportOrdersCreatedRes,
    ItemId,
    AssignOrder,
    AssignRes,
    CompleteOrder,
    OrderCompleteRes,
)
from candy.utils.utils import is_ranges_crossing, get_max_weight, get_earning_coef
from datetime import datetime

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/")
async def import_orders(req: ImportOrdersReq):
    res = ImportOrdersCreatedRes()
    for order in req.data:
        if await get_order(db.session, order.order_id) is None:
            order_db = await create_order(db.session, order)
            res.orders.append(ItemId(id=order_db.id))
    return res


@router.post("/assign")
async def assign_orders(req: AssignOrder):
    res = AssignRes(orders=[])
    courier = await get_courier(db.session, req.courier_id)
    if courier is None:
        return Response(status_code=400)

    max_weight = get_max_weight(courier.courier_type)

    vacant_orders = await get_vacant_orders(db.session, courier.regions, max_weight)
    for order in vacant_orders:
        if is_ranges_crossing(courier.working_hours, order.delivery_hours):
            res.orders.append(ItemId(id=order.id))

    assign_time = datetime.utcnow()
    assign_time_str = assign_time.isoformat() + 'Z'
    for order_id in res.orders:
        await update_assign_time(db.session, order_id.id, assign_time, courier.id)

    res.assign_time = assign_time_str

    return res.dict(exclude={} if len(res.orders) > 0 else {'assign_time'})


@router.post("/complete")
async def complete(req: CompleteOrder):
    if (await complete_order(db.session, req.order_id, req.courier_id, req.complete_time)) is None:
        return Response(status_code=400)
    courier = await get_courier(db.session, req.courier_id)
    if courier is None:
        return Response(status_code=400)
    orders = await get_completed_orders(db.session, courier.id)

    rating = 0
    if len(orders) != 0:
        tds = dict()
        tds[orders[0].region] = [round(orders[0].completed_time.timestamp()) - round(orders[0].assign_time.timestamp())]
        for i, order in enumerate(orders[1:]):
            tds.setdefault(order.region, [])
            tds[order.region].append(
                round(order.completed_time.timestamp()) - round(orders[i-1].completed_time.timestamp())
            )
        tds = [sum(td) / len(td) for td in tds]
        t = min(tds)
        rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
    earning_val = 500 * get_earning_coef(courier.courier_type)
    await update_earnings_and_rating(db.session, courier.id, earning_val, rating)

    return OrderCompleteRes(order_id=req.order_id)
