import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from api import route_constants
from api.auth import router as auth_router
from api.database import get_db

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=route_constants.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# async def startup_event():
#     """Initialize permissions on app startup"""
#     await initialize_default_permissions()
#     logging.info("Default permissions initialized")


app.include_router(auth_router)


@app.get(route_constants.API_ROOT)
def read_root() -> dict:
    return {"message": "Welcome to movieindex API"}


@app.get(route_constants.SCARY_ROUTE)
def get_scary() -> dict:
    get_db()
    return {
        "message": "🎃 BOO! This is a scary response from the server! 👻",
        "scary_level": "moderate",
    }


# @app.get(route_constants.MOVIES_ROUTE)
# @require_permission(PermissionType.ADD_MOVIES)
# async def create_movie_endpoint(user_id: str, movie_data: dict):
#     """Create a new movie - requires ADD_MOVIES permission"""
#     # Movie creation logic here
#     return {"message": "Movie created successfully"}
