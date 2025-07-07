import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dotenv import load_dotenv
import ssl

# Load environment variables (working directory is project root)
load_dotenv('.env')

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Parse and clean the DATABASE_URL for asyncpg
# Remove sslmode and channel_binding parameters as they're not supported by asyncpg
if "sslmode=" in DATABASE_URL:
    # Split the URL to remove unsupported parameters
    base_url = DATABASE_URL.split('?')[0]
    # For Neon, we need SSL but asyncpg handles it differently
    cleaned_url = base_url
else:
    cleaned_url = DATABASE_URL

# Ensure the URL uses asyncpg driver
if cleaned_url.startswith("postgresql://"):
    cleaned_url = cleaned_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif not cleaned_url.startswith("postgresql+asyncpg://"):
    # If it doesn't start with postgresql://, add the asyncpg driver
    if "://" in cleaned_url:
        parts = cleaned_url.split("://", 1)
        cleaned_url = f"postgresql+asyncpg://{parts[1]}"

# Create SSL context for asyncpg
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create async engine with SSL context
engine = create_async_engine(
    cleaned_url,
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