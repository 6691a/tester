from datetime import UTC, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.apis.models.user import User
from app.llms.base import Level as LevelEnum


class Level(SQLModel, table=True):
    """사용자 레벨 정보를 저장하는 모델

    사용자의 현재 레벨과 레벨 평가 기록을 저장합니다.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    level: int = Field(default=LevelEnum.BEGINNER)  # 기본값은 중간 레벨
    assessment_result: str  # LLM이 제공한 레벨 평가 결과
    assessed_at: datetime = Field(default_factory=datetime.now(UTC))

    # 외래 키
    user_id: int = Field(foreign_key="user.id", unique=True)

    # 관계
    user: User = Relationship()
