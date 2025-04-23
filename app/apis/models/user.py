from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func
from sqlalchemy.testing.schema import Column
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=30, unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    language: str = Field(default="kr", max_length=2)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))

    # submissions: list["Submission"] = Relationship(back_populates="user")
