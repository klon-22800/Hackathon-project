from enum import Enum
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class Role(Enum):
    student = 1
    teacher = 2

    def __json__(self):
        return {self.name}


class Permission(Enum):
    download = 1
    edit = 2


PositiveInt = Annotated[int, Field(strict=True, gt=0)]


class SUserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role
    education_programm: str
    course: PositiveInt

    class Config:
        orm_mode = True


class SUserOutput(BaseModel):
    name: str
    email: str
    role: Role

class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class RenameFileRequest(BaseModel):
    old_name: str
    new_name: str


class FolderCreateRequest(BaseModel):
    name: str
    path: str


class ShareFolderRequest(BaseModel):
    folder_path: str
    education_programm: str
    course: PositiveInt
