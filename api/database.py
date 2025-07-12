import ssl
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

import api.settings as settings

SYNCPG_PREFIX = "postgresql://"
ASYNC_PG_PREFIX = "postgresql+asyncpg://"
SSL_PREFIX = "sslmode="
SPLIT_CHARS = "://"

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


def clean_database_url_for_asyncpg(database_url: str) -> str:
    cleaned_url = database_url
    if SSL_PREFIX in cleaned_url:
        # Split the URL to remove unsupported parameters. For Neon, we need SSL but asyncpg handles it differently
        base_url = cleaned_url.split("?")[0]
        cleaned_url = base_url

    if cleaned_url.startswith(ASYNC_PG_PREFIX):
        return cleaned_url

    # Ensure the URL uses asyncpg driver
    if cleaned_url.startswith(SYNCPG_PREFIX):
        return cleaned_url.replace(SYNCPG_PREFIX, ASYNC_PG_PREFIX, 1)

    if SPLIT_CHARS in cleaned_url:
        parts = cleaned_url.split(SPLIT_CHARS, 1)
        cleaned_url = f"{ASYNC_PG_PREFIX}{parts[1]}"

    return cleaned_url


# Create SSL context for asyncpg
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

# Create async engine with SSL context
engine = create_async_engine(
    clean_database_url_for_asyncpg(settings.DATABASE_URL),
    echo=True,
    connect_args={
        "ssl": SSL_CONTEXT,
        "server_settings": {
            "application_name": "movieindex_app",
        },
    },
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


# Dependency to get database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
