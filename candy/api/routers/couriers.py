from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from candy.api.crud import create_courier
from candy.api.schema import ImportCouriersReq

router = APIRouter(
    prefix="/couriers",
    tags=["couriers"],
)


@router.post("/")
async def import_couriers(req: ImportCouriersReq):
    # await create_courier()
    # res = db.session.execute("SELECT 1").first()[0]
    return {"YEP": req}
