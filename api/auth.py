import os
import uuid
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from database import get_db
from models import User

# Load environment variables from root level .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

router = APIRouter(prefix="/auth", tags=["auth"])

# Configuration from environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
API_URL = os.getenv("API_URL", "http://localhost:8000")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Google OAuth URLs
GOOGLE_OAUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/google")
async def google_login():
    """Redirect to Google OAuth"""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    
    callback_url = f"{API_URL}/auth/google/callback"
    google_auth_url = (
        f"{GOOGLE_OAUTH_URL}?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={callback_url}&"
        f"scope=openid email profile&"
        f"response_type=code&"
        f"access_type=offline"
    )
    return RedirectResponse(url=google_auth_url)

@router.get("/google/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Handle Google OAuth callback"""
    if not code:
        raise HTTPException(status_code=400, detail="No authorization code received")

    # Exchange code for token
    callback_url = f"{API_URL}/auth/google/callback"
    token_data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": callback_url,
    }

    # Get access token from Google
    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_response.json()

    if "access_token" not in token_json:
        raise HTTPException(status_code=400, detail="Failed to get access token")

    # Get user info from Google
    headers = {"Authorization": f"Bearer {token_json['access_token']}"}
    user_response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)
    user_data = user_response.json()

    # Check if user exists or create new user
    result = await db.execute(select(User).where(User.google_id == user_data["id"]))
    user = result.scalar_one_or_none()

    if not user:
        # Check if user exists by email
        result = await db.execute(select(User).where(User.email == user_data["email"]))
        user = result.scalar_one_or_none()
        
        if user:
            # Update existing user with Google ID
            user.google_id = user_data["id"]
            user.avatar_url = user_data.get("picture")
        else:
            # Create new user
            user = User(
                id=str(uuid.uuid4()),
                name=user_data["name"],
                email=user_data["email"],
                google_id=user_data["id"],
                avatar_url=user_data.get("picture")
            )
            db.add(user)
    else:
        # Update existing user info
        user.name = user_data["name"]
        user.avatar_url = user_data.get("picture")

    await db.commit()

    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )

    # Redirect to frontend with token
    redirect_url = f"{FRONTEND_URL}?token={access_token}"
    return RedirectResponse(url=redirect_url)

@router.get("/me")
async def get_current_user(token: str, db: AsyncSession = Depends(get_db)):
    """Get current user info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "avatar_url": user.avatar_url
    } 