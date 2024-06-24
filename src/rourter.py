from fastapi import APIRouter, Request, Depends, Query
from converter import Converter
from typing import Annotated


router = APIRouter(
    prefix="/api",
)


@router.get("/rates")
async def get_result(from_: str = Query(..., alias="from"), to_: str = Query(..., alias="to"), value_: float = Query(..., alias="value")):
    conveter = Converter(currency_from=from_, currency_to=to_, amount=value_)
    result = await conveter.get_amount("https://www.xe.com/currencyconverter/convert/")
    return result