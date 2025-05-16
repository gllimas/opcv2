from datetime import datetime, time
from typing import Optional, List

from sqlmodel import SQLModel, Field


class FaceBase (SQLModel):
    pass


class UserFace (FaceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name : str = Field(max_length=20, nullable=False, unique=True)
    name_encod : bytes = Field(nullable=False)

class Photo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    filename: str


Base = SQLModel


class UserIn(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=20, nullable=False, unique=True)
    data: datetime = Field(default_factory=lambda: datetime.now().replace(second=0, microsecond=0))

    def update_data(self):
        self.data = datetime.now().replace(second=0, microsecond=0)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)

    def __repr__(self):
        return f"<User (username={self.username})>"

class UserButton(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, nullable=False)
    data: datetime = Field(default_factory=lambda: datetime.now().replace(second=0, microsecond=0))



class SetingHeated(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    temperature: float = Field(default=None, nullable=False)

class SetingAutomaticWatering(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    time: time

class SetingAutomaticWateringOff(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    time: time