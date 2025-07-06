from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import router as auth_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth router
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to movieindex API"}

@app.get("/scary")
def get_scary():
    return {"message": "🎃 BOO! This is a scary response from the server! 👻", "scary_level": "moderate"}

# Example async route using the database
@app.get("/db-test")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        # Example of how to use async database operations
        # result = await db.execute(select(SomeModel))
        # return result.scalars().all()
        return {"message": "Database connection ready for async operations!"}
    except Exception as e:
        return {"error": "Database connection failed", "details": str(e), "message": "Please set DATABASE_URL environment variable"}
