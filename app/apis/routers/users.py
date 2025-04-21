from fastapi import APIRouter, Depends, HTTPException

from app.apis.schemas.users import CreateUserRequestSchema, CreateUserResponseSchema
from app.apis.services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=CreateUserResponseSchema)
async def create_user(
    user: CreateUserRequestSchema,
    service: UserService = Depends(UserService)
) -> CreateUserResponseSchema:
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    if user.password != user.re_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    user = await service.create_user(user.username, user.password, user.language)

    return CreateUserResponseSchema(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
        language=user.language,
    )