
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Depends
import os
import pickle
import face_recognition
from sqlmodel import Session



from starlette.responses import JSONResponse, StreamingResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from fece_load import VideoCv
from database import get_session
from models import Photo, UserFace, UserIn

router = APIRouter()

active_connections: List[WebSocket] = []

async def broadcast(message: str):
    """Отправка сообщения всем активным соединениям."""
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Error sending to WebSocket: {e}")
            active_connections.remove(connection) #если соединение разорвано удаляем его

@router.websocket("/ws/video")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
        #     await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        active_connections.remove(websocket)


@router.post("/upload/")
async def upload_photo(
    title: str = Form(...),
    file: UploadFile = File(...),
    user_name: str = Form(...),
    session: Session = Depends(get_session)
):

    file_location = f"static/{file.filename}"
    with open(file_location, "wb") as file_object:
        file_object.write(await file.read())


    image = face_recognition.load_image_file(file_location)
    encodings = face_recognition.face_encodings(image)

    if encodings:
        encoded_face = pickle.dumps(encodings[0])


        new_user_face = UserFace(name=user_name, name_encod=encoded_face)
        session.add(new_user_face)
        session.commit()
        session.refresh(new_user_face)
    else:
        return JSONResponse(content={"message": "No face found in the image."}, status_code=400)

    new_photo = Photo(title=title, filename=file.filename)
    session.add(new_photo)
    session.commit()
    session.refresh(new_photo)

    return JSONResponse(content={
        "id": new_photo.id,
        "title": new_photo.title,
        "filename": new_photo.filename,
        "user_face_id": new_user_face.id
    })





@router.get("/video_feed/")
async def video_feed():
    return StreamingResponse(VideoCv.generate_video_stream(), media_type="multipart/x-mixed-replace; boundary=frame")



if not os.path.exists("static"):
    os.makedirs("static")



