import os
import uuid
import requests
import api.settings as settings
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from datetime import datetime, timedelta
import logging


from api.database import get_db
from api.db_models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

google_client_id = settings.GOOGLE_CLIENT_ID
google_client_secret = settings.GOOGLE_CLIENT_SECRET
google_oauth_url = settings.GOOGLE_OAUTH_URL
google_token_url = settings.GOOGLE_TOKEN_URL
google_user_info_url = settings.GOOGLE_USER_INFO_URL
frontend_url = settings.FRONTEND_URL
api_url = settings.API_URL
secret_key = settings.SECRET_KEY

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/google")
async def google_login():
    """Redirect to Google OAuth"""
    if not google_client_id:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    
    callback_url = f"{api_url}/auth/google/callback"
    google_auth_url = (
        f"{google_oauth_url}?"
        f"client_id={google_client_id}&"
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

    try:
        # Exchange code for token
        callback_url = f"{api_url}/auth/google/callback"
        token_data = {
            "client_id": google_client_id,
            "client_secret": google_client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": callback_url,
        }

        # Get access token from Google
        token_response = requests.post(google_token_url, data=token_data)
        token_json = token_response.json()

        if "access_token" not in token_json:
            logging.error(f"Failed to get access token: {token_json}")
            raise HTTPException(status_code=400, detail="Failed to get access token")

        # Get user info from Google
        headers = {"Authorization": f"Bearer {token_json['access_token']}"}
        user_response = requests.get(google_user_info_url, headers=headers)
        user_data = user_response.json()
        
        logging.info(f"Google user data: {user_data}")

        # Check if user exists or create new user
        result = await db.execute(select(User).where(User.google_id == user_data["id"]))
        user = result.scalar_one_or_none()

        if not user:
            # Check if user exists by email
            result = await db.execute(select(User).where(User.email == user_data["email"]))
            user = result.scalar_one_or_none()
            
            if user:
                # Update existing user with Google ID
                logging.info(f"Updating existing user with Google ID: {user.email}")
                user.google_id = user_data["id"]
                user.avatar_url = user_data.get("picture")
            else:
                # Create new user
                new_user_id = str(uuid.uuid4())
                logging.info(f"Creating new user: {user_data['email']} with ID: {new_user_id}")
                user = User(
                    id=new_user_id,
                    name=user_data["name"],
                    email=user_data["email"],
                    google_id=user_data["id"],
                    avatar_url=user_data.get("picture")
                )
                db.add(user)
        else:
            # Update existing user info
            logging.info(f"Updating existing user: {user.email}")
            user.name = user_data["name"]
            user.avatar_url = user_data.get("picture")

        # Commit the transaction
        await db.commit()
        logging.info(f"User saved successfully: {user.email} with ID: {user.id}")

        # Create JWT token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )

        # Redirect to frontend with token
        redirect_url = f"{frontend_url}?token={access_token}"
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        logging.error(f"Error in OAuth callback: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"OAuth callback failed: {str(e)}")

@router.get("/me")
async def get_current_user(token: str, db: AsyncSession = Depends(get_db)):
    """Get current user info"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token - no email")
        
        # Try to find user by email first
        try:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
        except Exception as e:
            logging.error(f"Database error when looking up user by email: {str(e)}")
            user = None
        
        # If not found by email, try by user_id as fallback
        if user is None and user_id:
            try:
                result = await db.execute(select(User).where(User.id == user_id))
                user = result.scalar_one_or_none()
            except Exception as e:
                logging.error(f"Database error when looking up user by ID: {str(e)}")
                user = None
        
        if user is None:
            # Log for debugging
            logging.error(f"User not found - email: {email}, user_id: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        # Manually commit the read transaction to prevent rollback
        await db.commit()
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "avatar_url": user.avatar_url
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except JWTError as e:
        logging.error(f"JWT decode error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(f"Unexpected error in get_current_user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/debug/db")
async def debug_database(db: AsyncSession = Depends(get_db)):
    """Debug endpoint to test database connectivity"""
    try:
        # Test basic database connection
        result = await db.execute(select(1))
        db_connected = result.scalar_one() == 1
        
        # Test user table structure
        user_count_result = await db.execute(select(User).limit(5))
        users = user_count_result.scalars().all()
        
        return {
            "database_connected": db_connected,
            "user_table_accessible": True,
            "sample_users_count": len(users)
        }
        
    except Exception as e:
        logging.error(f"Database debug error: {str(e)}")
        return {
            "database_connected": False,
            "error": str(e),
            "user_table_accessible": False
        } 