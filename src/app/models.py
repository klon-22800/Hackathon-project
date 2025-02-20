import uuid

from typing import List

from sqlalchemy import ForeignKey, UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from src.app.schemas.shemas import Role


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()

    folders: Mapped[List["Folder"]] = relationship(
        "Folder", back_populates="owner", cascade="all, delete-orphan"
    )

    shared_access: Mapped[List["SharedAccess"]] = relationship(
        "SharedAccess", back_populates="user"
    )

    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.student)

    education_programm: Mapped[str] = mapped_column(nullable=True)
    course: Mapped[int] = mapped_column(nullable=True)


class Folder(Base):
    __tablename__ = "folders"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=lambda: uuid.uuid4())
    name: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    owner: Mapped["User"] = relationship(back_populates="folders")

    shared_users: Mapped[list["SharedAccess"]] = relationship(
        "SharedAccess", back_populates="folder"
    )


class SharedAccess(Base):
    __tablename__ = "shared_access"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=lambda: uuid.uuid4())

    folder_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("folders.id"), nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    # Уровень разрешений: "edit" для учителей, "download" для студентов
    permissions: Mapped[str] = mapped_column(nullable=False)

    folder: Mapped["Folder"] = relationship(back_populates="shared_users")

    user: Mapped["User"] = relationship(back_populates="shared_access")
