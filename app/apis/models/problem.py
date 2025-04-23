from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import JSON, Column, DateTime
from sqlmodel import Field, SQLModel


class Problem(SQLModel, table=True):
    """문제 정보를 저장하는 모델

    각 코딩 테스트 문제의 정보를 저장합니다.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, description="문제 제목")
    description: str = Field(description="문제 설명")
    constraints: List[str] = Field(sa_type=JSON, description="문제 제약 조건")
    input_example: str = Field(description="입력 예시")
    output_example: str = Field(description="출력 예시")
    explanation: str = Field(description="문제 설명")
    concepts: List[str] = Field(sa_type=JSON, description="문제에서 다루는 개념")
    code_skeleton: str = Field(description="코드 스켈레톤")
    level: int = Field(description="문제 난이도")
    code_lang: str = Field(default="python", description="코드 언어")
    text_lang: str = Field(default="kr", description="문제 언어")
    test_case: str = Field(description="문제 테스트")
    approach_hints: List[str] = Field(sa_type=JSON, description="문제 접근 힌트")
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now(timezone.utc)),
    )

    # 관계
    # submissions: List["Submission"] = Relationship(
    #     back_populates="problem",
    # )
