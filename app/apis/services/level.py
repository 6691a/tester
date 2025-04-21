from fastapi import Depends

from app.llms.ollama.level import LevelAgent


class LevelService:
    def __init__(self, agent: LevelAgent = Depends(lambda: LevelAgent())):
        self.agent = agent


