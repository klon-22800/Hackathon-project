from pydantic import BaseModel, EmailStr
from datetime import date


class SUserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str #teacher or student 
    education_programm: str
    course: int

    class Config:
        orm_mode = True


class SUserOutput(BaseModel):
    name: str
    email: str
    role: str #тут скорее всего тоже нужна роль


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
    education_programm: str #шарим папку для студентов с определенной образовательной программой и курсом 
    course: int
