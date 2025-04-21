from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=30, unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    language: str = Field(default="kr", max_length=2)




