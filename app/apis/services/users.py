from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.apis.models.user import User
from app.database import get_async_session


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.session = session

    async def get_user_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_user(self, username: str, password: str, language: str) -> User:
        if await self.get_user_by_username(username):
            raise HTTPException(status_code=400, detail="Username already exists")

        db_user: User = User(
            username=username,
            password=self.pwd_context.hash(password),
            is_active=True,
            language=language,
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
