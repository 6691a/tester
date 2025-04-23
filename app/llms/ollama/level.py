from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph

from app.config import settings
from app.llms.base import BaseAgent, LevelAgentState


class LevelAgent(BaseAgent):
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            temperature=settings.OLLAMA_TEMPERATURE,
            base_dir=settings.OLLAMA_BASE_URL,
        )
        self.graph_builder = StateGraph(LevelAgentState)
