import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set")

if not DATABASE_URL.startswith("postgresql+asyncpg://"):
    # Convert postgresql:// to postgresql+asyncpg://
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        raise ValueError("DATABASE_URL must be a PostgreSQL URL for asyncpg")

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Dependency to get an async DB session for each request
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session 