from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.llms.ollama.level import LevelAgent


class LevelService:
    def __init__(
        self,
        agent: LevelAgent = Depends(lambda: LevelAgent()),
        session: AsyncSession = Depends(get_async_session),
    ):
        self.agent = agent
        self.session = session
