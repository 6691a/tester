from pydantic import BaseModel, Field


class CreateUserRequestSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str
    re_password: str
    language: str = Field(default="kr", max_length=2, description="AI Response Language")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "username",
                "password": "password123",
                "re_password": "password123",
                "language": "kr",
            }
        }

class CreateUserResponseSchema(BaseModel):
    id: int
    username: str
    is_active: bool
    language: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "username",
                "is_active": True,
                "language": "kr",
            }
        }