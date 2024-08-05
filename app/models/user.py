from uuid import UUID
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, Field
from app.models.base import IdMixin, TimestampMixin


class UserBase(SQLModel):
    first_name: str = None
    last_name: str = None
    email: str = Field(nullable=False, index=True, sa_column_kwargs={"unique": True})


class UserCreate(UserBase): ...


class UserUpdate(UserBase):
    first_name: str = None
    last_name: str = None
    email: str = None
    is_active: bool = None


class User(IdMixin, TimestampMixin, UserBase, table=True):
    __tablename__ = "users"

    is_active: bool = True
    password: str


class UserInput(UserBase):
    password: str = Field(min_length=5, max_length=24, description="user password")


class UserResponse(UserBase):
    id: UUID


class TokenSchema(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
