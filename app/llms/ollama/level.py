from langchain_ollama import ChatOllama
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langchain_core.prompts import ChatPromptTemplate

from app.config import settings
from app.llms.base import LevelAgentState

class LevelAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            temperature=settings.OLLAMA_TEMPERATURE,
            base_dir=settings.OLLAMA_BASE_URL,
        )
        self.graph_builder = StateGraph(LevelAgentState)

    def __call__(self, *args, **kwargs):
        self.setup_graph_node()
        self.setup_graph_edge()
        self.compile_graph = self.graph_builder.compile()

    def setup_graph_node(self):
        self.graph_builder.add_node("test", self.test)

    def setup_graph_edge(self):
        self.graph_builder.add_edge(START, "test")
        self.graph_builder.add_edge("test", END)

    async def test(self, state: LevelAgentState):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            당신은 코딩 테스트 문제를 출제하는 전문가 입니다. 
            사용자(학생)가 코딩 테스트를 준비하는데 도움을 주기 위해,
            코딩 테스트 문제를 출제해야 합니다.
            코딩 테스트 레벨은 1 ~ 10까지 있으며, 1이 높은 수준을 갖고 있는 사용자(학생)입니다.
            레벨 1은 구글, 페이스북 등 IT 대기업의 코딩 테스트 문제를 풀 수 있는 수준입니다.
            레벨 10은 처음 코딩을 시작한 사용자(학생)입니다.
            먼저 사용자(학생)의 코딩 테스트의 레벨 측정을 위한 문제가 필요합니다.
            """),
        ])

        chain = prompt | self.llm

        response = chain.astream()
        return response["messages"]