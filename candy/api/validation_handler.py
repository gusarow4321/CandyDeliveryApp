from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from schema import (
    CourierItem,
    OrderItem,
    ItemId,
    ImportCouriersCreatedRes,
    ImportCouriersBadRes,
    ImportOrdersCreatedRes,
    ImportOrdersBadRes
)


async def validation_exc_handler(request: Request, exc: RequestValidationError):
    if "/couriers/" in request.url.path and request.method == "POST":
        invalid = ImportCouriersCreatedRes(couriers=[])
        for courier in exc.body["data"]:
            try:
                CourierItem(**courier)
            except ValidationError:
                invalid.couriers.append(ItemId(id=courier["courier_id"] if type(courier["courier_id"]) is int else 0))

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=ImportCouriersBadRes(validation_error=invalid).dict())
    elif "/orders/" in request.url.path and request.method == "POST":
        invalid = ImportOrdersCreatedRes(orders=[])
        for order in exc.body["data"]:
            try:
                OrderItem(**order)
            except ValidationError:
                invalid.orders.append(ItemId(id=order["order_id"] if type(order["order_id"]) is int else 0))

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=ImportOrdersBadRes(validation_error=invalid).dict())
    else:
        await request_validation_exception_handler(request, exc)
