from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Date, String, Float, Integer, Column
from pydantic import BaseModel
import datetime

DATABASE_URL = "sqlite+aiosqlite:///expenses_.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    ...


class UserRegister(BaseModel):
    username: str
    password: str


class TransactionCreate(BaseModel):
    user_id: int
    date: str
    type: str
    amount: float
    category: str


class users(Base):
    __tablename__="users"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    username: Column[str] = Column(String, unique=True, index=True)
    password: Column[str] = Column(String)
    role: Column[str] = Column(String, default="user")


class Transaction(Base):
    __tablename__="transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date)
    type: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(50))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


