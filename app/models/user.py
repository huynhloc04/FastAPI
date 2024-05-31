from sqlmodel import Field, SQLModel
from app.models.base import IdMixin, TimestampMixin


class UserBase(SQLModel):
    first_name: str = None
    last_name: str = None
    email: str = Field(
        nullable=False, index=True, sa_column_kwargs={"unique": True}
    )
    is_active: bool = True


class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    first_name: str = None
    last_name: str = None
    email: str = None
    is_active: bool = None


class User(IdMixin, TimestampMixin, UserBase, table=True):
    __tablename__ = "users"


class UserResponse(User, table=False):
    ...


