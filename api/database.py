import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import api.settings as settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import ssl

database_url = settings.DATABASE_URL
syncpg_prefix = "postgresql://"
asyncpg_prefix = "postgresql+asyncpg://"
ssl_prefix = "sslmode="
split_chars = "://"

if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

def clean_database_url_for_asyncpg(database_url):
    cleaned_url = database_url
    if ssl_prefix in cleaned_url:
        # Split the URL to remove unsupported parameters. For Neon, we need SSL but asyncpg handles it differently
        base_url = database_url.split('?')[0]
        cleaned_url = base_url

    if cleaned_url.startswith(asyncpg_prefix):
        return cleaned_url

    # Ensure the URL uses asyncpg driver
    if cleaned_url.startswith(syncpg_prefix):
        return cleaned_url.replace(syncpg_prefix, asyncpg_prefix, 1)

    if split_chars in cleaned_url:
        parts = cleaned_url.split(split_chars, 1)
        cleaned_url = f"{asyncpg_prefix}{parts[1]}"
        
    return cleaned_url

# Create SSL context for asyncpg
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create async engine with SSL context
engine = create_async_engine(
    clean_database_url_for_asyncpg(database_url),
    echo=True,
    connect_args={
        "ssl": ssl_context,
        "server_settings": {
            "application_name": "movieindex_app",
        }
    }
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()