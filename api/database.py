import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load .env file from the repo root (parent directory)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    print("⚠️  DATABASE_URL environment variable not set!")
    print("Please create a .env file in the repo root with:")
    print("DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/movieindex")
    print("Using a dummy URL for now - database operations will fail until properly configured.")
    DATABASE_URL = "postgresql+asyncpg://dummy:dummy@localhost:5432/dummy"

# For asyncpg, ensure your DATABASE_URL uses postgresql+asyncpg://
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
        print(DATABASE_URL)
        yield session 