from random import randint

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.models.problem import Problem
from app.apis.repository.problem import ProblemRepository
from app.apis.schemas.problem import ProblemSchema
from app.database import get_async_session
from app.llms.ollama.problem import ProblemAgent, ProblemAgentState
from app.utils.exceptions import AlreadyExistsException


class ProblemService:
    def __init__(
        self,
        agent: ProblemAgent = Depends(ProblemAgent),
        session: AsyncSession = Depends(get_async_session),
        repository: ProblemRepository = Depends(ProblemRepository),
    ):
        self.agent = agent
        self.session = session
        self.repository = repository

    async def create_random_problem(
        self, code_lang: str, text_lang: str, level_bounds: tuple = (1, 10)
    ) -> ProblemSchema:
        """LLM을 통한 랜덤한 난이도의 문제를 생성합니다."""
        level = randint(*level_bounds)
        problem = await self.agent.create_problem(
            ProblemAgentState(
                code_lang=code_lang,
                text_lang=text_lang,
                level=level,
            )
        )
        return problem

    async def get_problem_by_id(self, problem_id: int) -> Problem:
        return await self.repository.get_problem_by_id(problem_id)

    async def save_problem(self, problem: ProblemSchema, code_lang: str, text_lang: str) -> Problem:
        if await self.repository.get_problem_by_title(problem.title):
            raise AlreadyExistsException("Problem with this title already exists.")
        return await self.repository.create_problem(problem, code_lang, text_lang)
