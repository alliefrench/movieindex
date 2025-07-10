from api.db_models import PermissionType
from api.manager import require_permission, initialize_default_permissions
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import logging

# Import with absolute paths (working directory is project root for both local and Vercel)
from api.database import get_db
from api.auth import router as auth_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",  # Vite dev server ports
        "https://www.themovieindex.club",  # Production domain (frontend)
        "https://api.themovieindex.club",  # If using API subdomain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# async def startup_event():
#     """Initialize permissions on app startup"""
#     await initialize_default_permissions()
#     logging.info("Default permissions initialized")

# Include auth router
app.include_router(auth_router)
logging.warning("Auth router included")
logging.warning("***", str(app.routes))

@app.get("/api")
def read_root():
    get_db()
    return {"message": "Welcome to movieindex API"}

@app.get("/api/scary")
def get_scary():
    return {"message": "🎃 BOO! This is a scary response from the server! 👻", "scary_level": "moderate"}

@app.get("/api/movies")
@require_permission(PermissionType.ADD_MOVIES)
async def create_movie_endpoint(user_id: str, movie_data: dict):
    """Create a new movie - requires ADD_MOVIES permission"""
    # Movie creation logic here
    return {"message": "Movie created successfully"}