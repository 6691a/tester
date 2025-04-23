from abc import ABC, abstractmethod
from enum import IntEnum

from langchain_core.language_models import BaseChatModel
from langgraph.graph import Graph, MessagesState

from app.apis.models.problem import Problem


class Level(IntEnum):
    """
    # 코딩 테스트 레벨 기준

    ## 레벨 1 (최고 난이도)
    - 복잡한 알고리즘 문제 해결 능력 (DP, 그래프 알고리즘 최적화)
    - 시간/공간 복잡도 최적화 능력
    - 구글, 페이스북 등 대기업 코딩 테스트 통과 수준
    - 예: 고급 트리 알고리즘, NP-Hard 문제 근사 해법

    ## 레벨 2-3
    - 중상급 알고리즘 지식 (세그먼트 트리, 복잡한 그래프 알고리즘)
    - 효율적인 자료구조 활용 능력
    - 예: 복잡한 DP 문제, 네트워크 플로우 알고리즘

    ## 레벨 4-5
    - 중급 알고리즘 구현 능력 (DFS/BFS, 기본 DP)
    - 자료구조에 대한 깊은 이해
    - 예: 그래프 탐색, 트리 순회, 해시 테이블 활용 문제

    ## 레벨 6-7
    - 기본적인 알고리즘 지식 (정렬, 이진 탐색)
    - 자료구조 기초 (배열, 스택, 큐, 링크드리스트)
    - 예: 간단한 그리디 알고리즘, 문자열 처리

    ## 레벨 8-10 (가장 쉬운 난이도)
    - 프로그래밍 기본 문법
    - 간단한 문제 해결 능력
    - 예: 반복문으로 해결 가능한 기초 문제, 조건문 활용
    """

    EXPERT = 1
    ADVANCED = 2
    INTERMEDIATE_HIGH = 3
    INTERMEDIATE = 4
    INTERMEDIATE_LOW = 5
    BEGINNER_HIGH = 6
    BEGINNER = 7
    BEGINNER_LOW = 8
    NOVICE = 9
    STARTER = 10


class LevelAgentState(MessagesState):
    level: Level = None
    code_lang: str = None
    text_lang: str = None
    test: str = None
    user_id: int = None
    submissions: list = None
    problems: list = None
    assessment_mode: bool = False
    scoring_mode: bool = False
    recommendation_mode: bool = False


class BaseProblemAgentState(MessagesState):
    level: Level
    problem: Problem = None
    code_lang: str
    text_lang: str


class BaseAgent(ABC):
    graph_builder: Graph
    llm: BaseChatModel

    def __call__(self, *args, **kwargs):
        self.setup_graph_node()
        self.setup_graph_edge()
        self.compile_graph = self.graph_builder.compile()

    @abstractmethod
    def setup_graph_node(self):
        """
        그래프 노드 설정
        """

    @abstractmethod
    def setup_graph_edge(self):
        """
        그래프 엣지 설정
        """
