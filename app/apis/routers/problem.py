from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException

from app.apis.models.problem import Problem
from app.apis.services.problem import ProblemService

router = APIRouter(prefix="/problems", tags=["problems"])


@router.post("/")
async def create_problem(
    code_lang: str = Body("python"),
    text_lang: str = Body("kr"),
    level_bounds: Optional[tuple] = Body((1, 10)),
    service: ProblemService = Depends(ProblemService),
):
    """LLM이 생성한 테스트 결과로부터 문제를 생성합니다."""
    try:
        problem = await service.create_random_problem(code_lang, text_lang, level_bounds)
        await service.save_problem(problem, code_lang, text_lang)
    except Exception:
        raise HTTPException(status_code=400, detail="다시 생성해주세요.")
    return problem


@router.get("/{problem_id}")
async def get_problem(problem_id: int, service: ProblemService = Depends(ProblemService)) -> Problem:
    problem = await service.get_problem_by_id(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="문제를 찾을 수 없습니다.")
    return problem
