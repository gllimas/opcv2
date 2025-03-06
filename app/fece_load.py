from datetime import datetime

import face_recognition
import cv2
import os
import pickle

from fastapi import Depends
from sqlmodel import select, Session
from database import get_session, engine
from models import UserFace, Base, UserIn

cascPathface = os.path.join(os.path.dirname(cv2.__file__), "data/haarcascade_frontalface_alt2.xml")
faceCascade = cv2.CascadeClassifier(cascPathface)


def save_user_in(name: str='name', session: Session = Depends(get_session)):
    new_user = UserIn(name=name, data=datetime.now())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


class VideoCv():
    def load_face_encodings_from_db(session):
        """Загрузка кодировок лиц из базы данных."""
        known_encodings = []
        known_names = []

        statement = select(UserFace)
        user_faces = session.exec(statement).all()

        for user_face in user_faces:
            known_encodings.append(pickle.loads(user_face.name_encod))  # Декодируем кодировку
            known_names.append(user_face.name)

        return known_encodings, known_names

    def recognize_faces(image, known_encodings, known_names):
        """Распознавание лиц на изображении."""
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60), flags=cv2.CASCADE_SCALE_IMAGE)

        encodings = face_recognition.face_encodings(rgb)
        names = []
        face_locations = []

        for (x, y, w, h) in faces:
            face_locations.append((y, y + h, x, x + w))  # (top, bottom, left, right)

        if encodings:
            for encoding in encodings:
                matches = face_recognition.compare_faces(known_encodings, encoding)
                name = "Unknown"

                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    for i in matchedIdxs:
                        name = known_names[i]
                        counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
                save_user_in(name)
                names.append(name)

                # здесь нужно написать код для сохранения в базу данных


        else:
            names = ["Unknown"] * len(faces)

        return names, face_locations

    @staticmethod
    def generate_video_stream():
        """Генерация видеопотока с распознаванием лиц."""
        video_capture = cv2.VideoCapture(0)
        session_generator = get_session()
        session = next(session_generator)

        known_encodings, known_names = VideoCv.load_face_encodings_from_db(session)

        try:
            while True:
                ret, frame = video_capture.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)

                names, face_locations = VideoCv.recognize_faces(frame, known_encodings, known_names)

                # Отрисовка рамок и имен
                for (top, bottom, left, right), name in zip(face_locations, names):
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Кодируем кадр в JPEG
                ret, jpeg = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        finally:
            session.close()
            video_capture.release()

    # if __name__ == "__main__":
    #     Base.metadata.create_all(engine)
    #
    #     video_capture = cv2.VideoCapture(0)
    #
    #     session_generator = get_session()
    #     session = next(session_generator)
    #
    #     try:
    #         known_encodings, known_names = load_face_encodings_from_db(session)
    #
    #         while True:
    #             ret, frame = video_capture.read()
    #             if not ret:
    #                 print("Не удалось захватить кадр.")
    #                 break
    #
    #             frame = cv2.flip(frame, 1)
    #
    #             names, face_locations = recognize_faces(frame, known_encodings, known_names)
    #
    #             # Отрисовка рамок и имен
    #             for (top, bottom, left, right), name in zip(face_locations, names):
    #                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    #                 cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #
    #             # Отображение видео
    #             cv2.imshow("Video", frame)
    #
    #             # Выход при нажатии клавиши 'q'
    #             if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 break
    #     finally:
    #         session.close()
    #         video_capture.release()
    #         cv2.destroyAllWindows()
