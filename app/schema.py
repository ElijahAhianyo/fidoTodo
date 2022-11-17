from enum import Enum
from typing import Dict, Optional, List
from datetime import datetime

from pydantic import BaseModel, root_validator


class TimeStampBaseModel(BaseModel):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values

class UserCreate(TimeStampBaseModel):
    email: str
    user_name: str


class User(UserCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Task(TimeStampBaseModel):
    id: int
    title: str
    description: str
    status: str
    created_by: User
    assigned_to: User


class TaskAssign:
    assigned_to: User