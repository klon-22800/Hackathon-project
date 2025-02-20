import uuid
from typing import List

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()

    # Связь с папками пользователя
    folders: Mapped[List["Folder"]] = relationship(
        "Folder", back_populates="owner", cascade="all, delete-orphan"
    )

    # Связь с доступами (когда пользователь имеет доступ к чужим папкам)
    shared_access: Mapped[List["SharedAccess"]] = relationship(
        "SharedAccess", back_populates="user"
    )

    role: Mapped[str] = mapped_column(nullable=False, default='student')  # 'student' or 'teacher'

    education_programm: Mapped[str] = mapped_column(nullable=True) #Make nullable in case a teacher is also in the students table
    course: Mapped[int] = mapped_column(nullable=True) #Make nullable in case a teacher is also in the students table


class Folder(Base):
    __tablename__ = "folders"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=lambda: uuid.uuid4())
    name: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    # Связь с владельцем папки
    owner: Mapped["User"] = relationship(back_populates="folders")

    # Связь с доступами для других пользователей (включая преподавателей и студентов)
    shared_users: Mapped[list["SharedAccess"]] = relationship(
        "SharedAccess", back_populates="folder"
    )


class SharedAccess(Base):
    __tablename__ = "shared_access"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=lambda: uuid.uuid4())

    # К какой папке есть доступ
    folder_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("folders.id"), nullable=False
    )

    # У какого пользователя есть этот доступ
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    # Уровень разрешений: "edit" для учителей, "download" для студентов
    permissions: Mapped[str] = mapped_column(nullable=False)

    # Связь с папкой
    folder: Mapped["Folder"] = relationship(back_populates="shared_users")

    # Связь с пользователем, которому предоставлен доступ
    user: Mapped["User"] = relationship(back_populates="shared_access")
