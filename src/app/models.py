from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, Boolean
import uuid


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(nullable=False)  # 'student' or 'teacher'

    # Связь с папками пользователя
    folders: Mapped[list["Folder"]] = relationship(
        "Folder", back_populates="owner", cascade="all, delete-orphan"
    )

    # Связь с доступами (когда пользователь имеет доступ к чужим папкам)
    shared_access: Mapped[list["SharedAccess"]] = relationship(
        "SharedAccess", back_populates="user"
    )

    # Связь с учителями и студентами
    teacher: Mapped["Teacher"] = relationship(
        "Teacher", back_populates="user", uselist=False,
        primaryjoin="User.id == Teacher.user_id"
    )

    student: Mapped["Student"] = relationship(
        "Student", back_populates="user", uselist=False,
        primaryjoin="User.id == Student.user_id"
    )


class Folder(Base):
    __tablename__ = "folders"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
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
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # К какой папке есть доступ
    folder_id: Mapped[UUID] = mapped_column(
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


class Teacher(Base):
    __tablename__ = "teachers"

    # Уникальный ID препода
    id: Mapped[int] = mapped_column(primary_key=True)

    # Внешний ключ на таблицу users
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="teacher")

    # Связь с доступами (права редактирования)
    access_rights: Mapped[list["SharedAccess"]] = relationship(
        "SharedAccess",
        primaryjoin="Teacher.user_id == SharedAccess.user_id",
        foreign_keys="[SharedAccess.user_id]",
        viewonly=True
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Внешний ключ на таблицу users
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    education_programm: Mapped[str] = mapped_column()
    course: Mapped[int] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="student")

    # Связь с доступами (права на скачивание)
    access_rights: Mapped[list["SharedAccess"]] = relationship(
        "SharedAccess",
        primaryjoin="Student.user_id == remote(SharedAccess.user_id)",
        foreign_keys="[SharedAccess.user_id]",
        viewonly=True
    )
