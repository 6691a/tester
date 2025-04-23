from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Submission(SQLModel, table=True):
    """사용자 제출 정보를 저장하는 모델

    사용자가 제출한 코드와 평가 결과를 저장합니다.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(description="사용자가 제출한 코드")
    score: Optional[float] = Field(default=None, description="LLM이 평가한 점수 (0-100)")
    feedback: Optional[str] = Field(default=None, description="LLM이 제공한 피드백")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    # 외래 키
    user_id: int = Field(foreign_key="user.id")
    problem_id: int = Field(foreign_key="problem.id")

    # 관계
    # user: User = Relationship(back_populates="submissions")
    # problem: Problem = Relationship(back_populates="submissions")
