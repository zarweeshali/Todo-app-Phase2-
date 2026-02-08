"""
SQLModel database models for Phase II Todo App
"""

from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    """Base user model for common fields"""
    email: str = Field(index=True, unique=True)
    name: Optional[str] = None


class User(UserBase, table=True):
    """User model for database"""
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    todos: List["Todo"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str


class UserRead(UserBase):
    """Schema for reading a user"""
    id: UUID
    created_at: datetime
    updated_at: datetime


from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoBase(SQLModel):
    """Base todo model for common fields"""
    title: str = Field(min_length=1, max_length=500)
    completed: bool = False
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = Priority.MEDIUM


class Todo(TodoBase, table=True):
    """Todo model for database"""
    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: Optional[User] = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    """Schema for creating a todo"""
    pass


class TodoUpdate(SQLModel):
    """Schema for updating a todo"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None


class TodoRead(TodoBase):
    """Schema for reading a todo"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class TodoReadWithUser(TodoRead):
    """Schema for reading a todo with user info"""
    user: Optional[UserRead] = None
