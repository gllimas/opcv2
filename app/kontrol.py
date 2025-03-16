import asyncio
import serial

from fastapi import APIRouter
from pydantic import BaseModel
import serial.tools.list_ports
from starlette.responses import JSONResponse


router = APIRouter()

selected_port = None



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
        raise Exception("Сначала выберите порт")

    ser = serial.Serial(selected_port, 9600)
    await asyncio.sleep(2)
    ser.write(b'1')
    ser.close()
