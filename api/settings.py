import os


DATABASE_URL = os.getenv("DATABASE_URL")
APP_ENV = os.getenv("APP_ENV", "development")

API_URL = os.getenv("API_URL", "http://localhost:8000")