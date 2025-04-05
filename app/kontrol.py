import asyncio


import serial

from fastapi import APIRouter
from pydantic import BaseModel
import serial.tools.list_ports
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_202_ACCEPTED


router = APIRouter()

selected_port = None

Name_user_in = []

@router.get("/usb_ports", response_class=JSONResponse)
async def get_usb_ports():
    ports = serial.tools.list_ports.comports()
    port_list = [{"device": port.device, "description": port.description} for port in ports]
    return {"ports": port_list}

class SelectedPort(BaseModel):
    port: str


@router.post("/select_port", response_class=JSONResponse)
async def select_port(selected: SelectedPort):
    global selected_port
    selected_port = selected.port
    return {"message": f"Порт {selected.port} успешно выбран"}

async def com_port():
    global selected_port
    if selected_port is None:
        return

    ser = None
    try:

        ser = serial.Serial(selected_port, 9600, timeout=1)
        await asyncio.sleep(2)


        if ser.is_open:
            ser.write(b'1')  #
        else:
            pass

    except serial.SerialException as e:
        print(f"Ошибка при подключении к порту: {e}")

    finally:
        if ser is not None and ser.is_open:
            ser.close()



@router.get("/button_on")
async def button_on():
    await com_port()
    return Response(status_code=HTTP_202_ACCEPTED)

