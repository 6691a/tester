from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.apis.routers.level import router as level_router
from app.apis.routers.problem import router as problem_router
from app.apis.routers.users import router as user_router
from app.config import settings
from app.database import get_async_session

# Create FastAPI app
app = FastAPI(
    title="Coding Test API",
    description="AI-powered coding test generation, verification, and evaluation system",
    version="0.1.0",
)

# Include routers
app.include_router(user_router, prefix=settings.API_PREFIX)
app.include_router(level_router, prefix=settings.API_PREFIX)
app.include_router(problem_router, prefix=settings.API_PREFIX)


# Dependency to get DB session
def get_session() -> AsyncGenerator[AsyncSession, None]:
    return get_async_session()
