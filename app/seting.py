from fastapi import APIRouter, HTTPException, Depends, Request
import serial
import re
from datetime import time, datetime
from pydantic import BaseModel, conint
from sqlmodel import Session, select
from starlette.responses import Response
from starlette.status import HTTP_202_ACCEPTED

from models import SetingHeated, SetingAutomaticWatering, SetingAutomaticWateringOff
from kontrol import selected_port, heated_port, heated_port_off, \
    automatic_watering_port, automatic_watering_port_off  
from database import get_session

router = APIRouter()



# включение подогрева пола
@router.post("/seting_heated")
async def read_temperature():
    try:
        with serial.Serial(selected_port, baudrate=9600, timeout=1) as ser:
            data = ser.readline()

            if data:
                decoded_data = data.decode('utf-8').strip()
                match = re.search(r'TEMP:([\d.]+)', decoded_data)

                if match:
                    temperature = float(match.group(1))
                    return {"temperature": temperature}
                else:
                    raise HTTPException(status_code=400, detail="Temperature data not found in response")
            else:
                raise HTTPException(status_code=404, detail="No data received")
    except serial.SerialException as e:
        raise HTTPException(status_code=500, detail=f"Serial error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



class TemperatureModel(BaseModel):
    temperature: float

class TimeInputModel(BaseModel):
    hour: conint(ge=0, le=23)  # Часы от 0 до 23
    minute: conint(ge=0, le=59)

# добавление в базу данных температуры
@router.post("/add_temperature")
async def add_temperature(temp: TemperatureModel, session: Session = Depends(get_session)):
    new_temperature = SetingHeated(temperature=temp.temperature)
    session.add(new_temperature)
    session.commit()
    session.refresh(new_temperature)
    return Response(status_code=202)


# Сравнение температуры с датчик с температурой с базы данных
@router.get("/compare_temperature", response_model=dict)
async def compare_temperature(session: Session = Depends(get_session)):
    try:
        # Получаем температуру с микроконтроллера
        microcontroller_temp = await read_temperature()  # Вызов функции для получения температуры

        # Получаем последнюю сохраненную температуру из базы данных
        last_record = await session.execute(select(SetingHeated).order_by(SetingHeated.id.desc()))
        last_record = last_record.scalars().first()

        if last_record is None:
            raise HTTPException(status_code=404, detail="No temperature records found in the database")

        if microcontroller_temp["temperature"] < last_record.temperature:
            await heated_port()
        else:
            await heated_port_off()

        return {
            "microcontroller_temperature": microcontroller_temp["temperature"],
            "database_temperature": last_record.temperature,
            "is_equal": microcontroller_temp["temperature"] == last_record.temperature,
            "difference": microcontroller_temp["temperature"] - last_record.temperature,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Добавление времени включение автополива
@router.post("/clock_water")
async def clock_water(time_input: TimeInputModel, session: Session = Depends(get_session)):
    time_to_save = time(hour=time_input.hour, minute=time_input.minute)
    new_automat = SetingAutomaticWatering(time=time_to_save)
    session.add(new_automat)
    session.commit()
    session.refresh(new_automat)

    return {"message": "Time saved successfully", "saved_time": time_to_save}


# Добавление времени отключения автополива
@router.post("/clock_water_off")
async def clock_water_off(time_input: TimeInputModel, session: Session = Depends(get_session)):
    time_to_save = time(hour=time_input.hour, minute=time_input.minute)

    new_automat = SetingAutomaticWateringOff(time=time_to_save)
    session.add(new_automat)
    session.commit()
    session.refresh(new_automat)

    return {"message": "Time saved successfully", "saved_time": time_to_save}



# Сравниваем время с базы данных с настоящим временем для включения автополива
@router.post("/water_on")
async def water_on(session: Session = Depends(get_session)):
    current_time = datetime.now().time()
    watering_settings = session.execute(select(SetingAutomaticWatering))
    watering_settings = watering_settings.scalars().all()

    should_water = any(setting.time == current_time for setting in watering_settings)

    if should_water:
        await automatic_watering_port()
        await water_off()
    else:
        pass


# Сравниваем время с базы данных с настоящим временем для отключения автополива
@router.post("/water_off")
async def water_off(session: Session = Depends(get_session)):
    current_time = datetime.now().time()
    watering_settings = session.execute(select(SetingAutomaticWateringOff))
    watering_settings = watering_settings.scalars().all()

    should_water = any(setting.time == current_time for setting in watering_settings)

    if should_water:
        await automatic_watering_port_off()
        await water_on()
    else:
        pass


# Выводим прследнюю запись в базе данных температуры
@router.get("/last_temperature")
async def get_last_temperature(session: Session = Depends(get_session)):
    last_temperature = session.query(SetingHeated).order_by(SetingHeated.id.desc()).first()

    if last_temperature:
        return {"temperature": last_temperature.temperature}
    else:
        return {"message": "No temperature records found"}



# Выводим прследнюю запись в базе данных включения автополива
@router.get("/last_clock_water")
async def get_last_clock_water(session: Session = Depends(get_session)):
    last_clock_water = session.query(SetingAutomaticWatering).order_by(SetingAutomaticWatering.id.desc()).first()

    if last_clock_water:
        return {"time": str(last_clock_water.time)}
    else:
        return {"message": "No clock water records found"}



# Выводим прследнюю запись в базе данных отключения автополива
@router.get("/last_clock_water_off")
async def get_last_clock_water(session: Session = Depends(get_session)):
    last_clock_water = session.query(SetingAutomaticWateringOff).order_by(SetingAutomaticWateringOff.id.desc()).first()

    if last_clock_water:
        return {"time": str(last_clock_water.time)}
    else:
        return {"message": "No clock water records found"}