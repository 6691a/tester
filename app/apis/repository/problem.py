from typing import Optional

from fastapi import Depends
from sqlmodel import select

from app.apis.models.problem import Problem
from app.apis.schemas.problem import ProblemSchema
from app.database import get_async_session


class ProblemRepository:
    def __init__(self, session=Depends(get_async_session)):
        self.session = session

    async def get_problem_by_title(self, title: str) -> Optional[Problem]:
        statement = select(Problem).where(Problem.title == title)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_problem_by_id(self, problem_id: int) -> Optional[Problem]:
        statement = select(Problem).where(Problem.id == problem_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_problem(self, data: ProblemSchema, code_lang: str, text_lang: str) -> Problem:
        problem = Problem(
            title=data.title,
            description=data.description,
            constraints=data.constraints,
            input_example=data.input_example,
            output_example=data.output_example,
            explanation=data.explanation,
            concepts=data.concepts,
            code_skeleton=data.code_skeleton,
            level=data.level,
            code_lang=code_lang,
            text_lang=text_lang,
            test_case=data.test_case,
            approach_hints=data.approach_hints,
        )
        self.session.add(problem)
        await self.session.commit()
        await self.session.refresh(problem)
        return problem
