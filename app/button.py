from fastapi import APIRouter
from sqlalchemy.testing import db
from starlette.responses import Response
from starlette.status import HTTP_202_ACCEPTED

from api import get_users
from kontrol import light_port, socket_port, heated_port, blinds_port, automatic_watering_port

router = APIRouter()

# Кнопка включить свет
@router.get("/light_on")
async def light_on():
    await light_port()
    return Response(status_code=HTTP_202_ACCEPTED)


# Кнопка вкючить розетку
@router.get("/socket_on")
async def socket_on():
    await socket_port()
    return Response(status_code=HTTP_202_ACCEPTED)


# кнопка вывести кто входил
@router.get("/inbox_list")
async def inbox_list():
    users = await get_users(db=db)
    return users


#кнопка включить тёплый пол
@router.get("/heated_floor")
async def heated_floor():
    await heated_port()
    return Response(status_code=HTTP_202_ACCEPTED)


# кнопка открыть жалюзи
@router.get("/blinds")
async def blinds():
    await blinds_port()
    return Response(status_code=HTTP_202_ACCEPTED)


# кнопка включить автополив
@router.get("/automatic_watering")
async def automatic_watering():
    await automatic_watering_port()
    return Response(status_code=HTTP_202_ACCEPTED)