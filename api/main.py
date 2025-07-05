<<<<<<< Updated upstream
from fastapi import FastAPI
=======
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
>>>>>>> Stashed changes

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to movieindex API"}
<<<<<<< Updated upstream
=======

@app.get("/scary")
def get_scary():
    return {"message": "🎃 BOO! This is a scary response from the server! 👻", "scary_level": "moderate"}

# Example async route using the database
@app.get("/db-test")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    # Example of how to use async database operations
    # result = await db.execute(select(SomeModel))
    # return result.scalars().all()
    return {"message": "Database connection ready for async operations!"}
>>>>>>> Stashed changes
