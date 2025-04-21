from fastapi import APIRouter, Depends

from app.apis.services.level import LevelService

router = APIRouter(prefix="/level", tags=["level"])

@router.get("/test")
async def test_level(
    service: LevelService = Depends(LevelService)
):
    pass

