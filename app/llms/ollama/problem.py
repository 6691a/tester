from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.constants import END, START
from langgraph.graph import StateGraph

from app.apis.schemas.problem import ProblemSchema
from app.config import settings
from app.llms.base import BaseAgent, BaseProblemAgentState
from app.utils.parsers import parse_json_from_llm_response


class ProblemAgentState(BaseProblemAgentState):
    pass


class ProblemAgent(BaseAgent):
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            temperature=settings.OLLAMA_TEMPERATURE,
            base_dir=settings.OLLAMA_BASE_URL,
        )
        self.graph_builder = StateGraph(ProblemAgentState)
        self.parser_pydantic_class = ProblemSchema
        self.parser = PydanticOutputParser(pydantic_object=self.parser_pydantic_class)

    def setup_graph_node(self):
        self.graph_builder.add_node("create_problem", self.create_random_problem)

    def setup_graph_edge(self):
        self.graph_builder.add_edge(START, "create_problem")
        self.graph_builder.add_edge("create_problem", END)

    def _get_create_problem_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                당신은 코딩 테스트 문제를 출제하는 전문가입니다. 
                사용자(학생)가 코딩 테스트를 준비하는데 도움을 주기 위해 코딩 테스트 문제를 출제해야 합니다.
                코딩 테스트 레벨은 1 ~ 10까지 있으며, 숫자가 작을수록 높은 수준을 의미합니다.
                레벨 1은 구글, 페이스북 등 IT 대기업의 코딩 테스트 문제를 풀 수 있는 최고 수준입니다.
                레벨 10은 처음 코딩을 시작한 입문자 수준입니다.

                사용자가 지정한 프로그래밍 언어와 설명 언어로 문제를 생성해주세요.

                마지막에는 다음 형식에 맞게 JSON 형태로 데이터를 출력해주세요:
                {format}
                """,
                ),
                (
                    "user",
                    """
                {code_lang} 언어로 코딩 테스트 문제를 출제해 주세요.
                문제는 {text_lang} 언어로 설명해주세요.
                레벨 {level}에 해당하는 문제를 출제해주세요.
                """,
                ),
            ]
        )

    async def format_to_pydantic(self, state):
        """텍스트 응답을 Pydantic 객체로 변환합니다."""
        problem_text = state.get("problem_text", "")

        try:
            # JSON 형식으로 출력된 경우 직접 파싱
            problem_schema = self.parser.parse(problem_text)
        except Exception:
            # JSON 형식이 아닌 경우 텍스트 파싱 메소드 사용
            problem_schema = ProblemSchema.parse_problem_text(problem_text)

        return {"problem": problem_schema, "raw_text": problem_text}

    async def create_problem(self, state: ProblemAgentState) -> ProblemSchema:
        """LLM을 통해 문제를 생성합니다."""

        prompt = self._get_create_problem_prompt()
        level = state.get("level")
        code_lang = state.get("code_lang")
        text_lang = state.get("text_lang")
        chain = prompt | self.llm

        response = await chain.ainvoke(
            {
                "code_lang": code_lang,
                "text_lang": text_lang,
                "level": level,
                "format": self.parser.get_format_instructions(),
            }
        )

        json_content = parse_json_from_llm_response(response.content)
        return ProblemSchema.model_validate(json_content)

    async def create_random_problem(self, state: ProblemAgentState):
        """문제를 생성하고 상태에 저장합니다."""
        problem_text = await self.create_problem(state)
        state["problem_text"] = problem_text
        return state
