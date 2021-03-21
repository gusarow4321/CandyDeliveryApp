from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from candy.api.schema import (
    CourierItem,
    OrderItem,
    ItemId,
    ImportCouriersCreatedRes,
    ImportCouriersBadRes,
    ImportOrdersCreatedRes,
    ImportOrdersBadRes,
    ImportCouriersReq,
    ImportOrdersReq,
)


async def validation_exc_handler(request: Request, exc: RequestValidationError):
    if "/couriers" in request.url.path and request.method == "POST":
        res = ImportCouriersBadRes(validation_error=ImportCouriersCreatedRes(couriers=[])).dict()

        try:
            ImportCouriersReq(**exc.body)
        except ValidationError as e:
            for error in e.errors():
                if error["type"] == 'value_error.extra' and len(error["loc"]) == 1:
                    res["validation_error"][error["loc"][0]] = exc.body[error["loc"][0]]

        for courier in (exc.body["data"] if exc.body["data"] else []):
            courier = courier if type(courier) is dict else {}
            try:
                CourierItem(**courier)
            except ValidationError as e:

                item_id = ItemId(id=courier["courier_id"] if type(courier.get("courier_id")) is int else 0).dict()
                for error in e.errors():
                    if error["type"] == 'value_error.extra':
                        item_id[error["loc"][0]] = courier[error["loc"][0]]
                res["validation_error"]["couriers"].append(item_id)

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=res)
    elif request.url.path.endswith("/orders") and request.method == "POST":
        res = ImportOrdersBadRes(validation_error=ImportOrdersCreatedRes(orders=[])).dict()

        try:
            ImportOrdersReq(**exc.body)
        except ValidationError as e:
            for error in e.errors():
                if error["type"] == 'value_error.extra' and len(error["loc"]) == 1:
                    res["validation_error"][error["loc"][0]] = exc.body[error["loc"][0]]

        for order in (exc.body["data"] if exc.body["data"] else []):
            order = order if type(order) is dict else {}
            try:
                OrderItem(**order)
            except ValidationError as e:
                item_id = ItemId(id=order["order_id"] if type(order.get("order_id")) is int else 0).dict()
                for error in e.errors():
                    if error["type"] == 'value_error.extra':
                        item_id[error["loc"][0]] = order[error["loc"][0]]
                res["validation_error"]["orders"].append(item_id)

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=res)
    else:
        return Response(status_code=400)
