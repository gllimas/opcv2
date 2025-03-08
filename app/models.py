from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship

from sqlmodel import SQLModel, Field


class FaceBase (SQLModel):
    pass

# class Face (FaceBase, table=True):
#     id : int = Field(default_factory=int, primary_key=True)
#     name : str = Field(max_length=20, nullable=False, ge=3, unique=True)
#     fale_name : Optional[str] = Field(nullable=True, default=None, unique=True)
#     signatur : str = Field(nullable=False, unique=True)
#     data_add : datetime = Field(default_factory=datetime.now)
#     is_active : bool = Field(default=True)
#     data_end : Optional[datetime] = Field(default=None, nullable=True)

class UserFace (FaceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name : str = Field(max_length=20, nullable=False, unique=True)
    name_encod : bytes = Field(nullable=False)

class Photo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    filename: str


Base = SQLModel


# class UserIn(SQLModel, table=True):
#     """Модель для хранения информации о пользователе."""
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(max_length=20, nullable=False, unique=True)
#     data: datetime = Field(default_factory=datetime.now)

class UserIn(SQLModel, table=True):
    """Модель для хранения информации о пользователе."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=20, nullable=False, unique=True)
    data: datetime = Field(default_factory=lambda: datetime.now().replace(second=0, microsecond=0))

    def update_data(self):
        """Метод для обновления поля data без секунд и микросекунд."""
        self.data = datetime.now().replace(second=0, microsecond=0)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)

    def __repr__(self):
        return f"<User (username={self.username})>"