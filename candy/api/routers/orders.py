from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)
