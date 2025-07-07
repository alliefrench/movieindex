# movieindex

App for friend-sourcing movie reviews with Google OAuth authentication

## Project Structure

- `api/` — FastAPI Python server with Google OAuth
- `app/` — React web frontend with Vite
- `vercel.json` — Vercel deployment configuration

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL (Neon), Google OAuth
- **Frontend**: React, TypeScript, Vite
- **Database**: Neon (PostgreSQL)
- **Authentication**: Google OAuth 2.0 + JWT
- **Deployment**: Vercel

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- A Neon database (PostgreSQL)
- Google OAuth credentials

### Environment Setup

1. **Create environment files:**

   Create `api/.env` with:

   ```bash
   DATABASE_URL=your_neon_database_url
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   SECRET_KEY=your_jwt_secret_key
   API_URL=http://localhost:8000
   FRONTEND_URL=http://localhost:5173
   ```

   Create `app/.env` with:

   ```bash
   VITE_API_URL=http://localhost:8000
   ```

### Running the Services Locally

#### 1. Backend (FastAPI)

```bash
# Install dependencies
pip install -r requirements.txt

# Run from the ROOT directory (important for imports)
uvicorn api.main:app --reload --port 8000
```

**Alternative method (if you prefer running from api directory):**

```bash
cd api
source venv/bin/activate  # if using virtual environment
uvicorn main:app --reload --port 8000
```

The FastAPI server will run at [http://localhost:8000](http://localhost:8000).

#### 2. Frontend (React + Vite)

```bash
cd app
npm install
npm start  # or npm run dev
```

The React app will run at [http://localhost:5173](http://localhost:5173).

### Important Notes

#### Backend Import Structure

- The project uses **absolute imports** (`from api.database import get_db`)
- When running from root: `uvicorn api.main:app --reload --port 8000`
- When running from api/: `uvicorn main:app --reload --port 8000`

#### Common Issues & Solutions

1. **Port 8000 already in use:**

   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

2. **Import errors:**

   - Make sure you're running from the correct directory
   - Root directory: `uvicorn api.main:app --reload --port 8000`
   - API directory: `cd api && uvicorn main:app --reload --port 8000`

3. **Database connection issues:**

   - Ensure your `DATABASE_URL` is correct in `api/.env`
   - Check that your Neon database is running

4. **CORS errors:**
   - Make sure `VITE_API_URL=http://localhost:8000` in `app/.env`
   - Backend should be running on port 8000

## API Endpoints

- `GET /` - Health check
- `GET /scary` - Test endpoint
- `GET /auth/google` - Google OAuth login
- `GET /auth/google/callback` - OAuth callback
- `GET /auth/me` - Get current user info

## Database Schema

The application uses these main tables:

- `users` - User profiles with Google OAuth data
- `movies` - Movie information
- `reviews` - User movie reviews

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:8000/auth/google/callback` (local)
   - `https://yourdomain.com/api/auth/google/callback` (production)

## Deployment

The app is configured for Vercel deployment:

1. **Push to GitHub**
2. **Connect to Vercel**
3. **Set environment variables** in Vercel dashboard
4. **Deploy**

### Vercel Environment Variables

Set these in your Vercel project settings:

- `DATABASE_URL`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `SECRET_KEY`
- `API_URL` (your production API URL)
- `FRONTEND_URL` (your production frontend URL)

## Project Files

- `api/main.py` - FastAPI application
- `api/auth.py` - Google OAuth endpoints
- `api/database.py` - Database configuration
- `api/models.py` - SQLAlchemy models
- `api/handler.py` - Vercel serverless handler
- `app/src/index.tsx` - React frontend
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel deployment config

## Development Workflow

1. **Start backend**: `uvicorn api.main:app --reload --port 8000`
2. **Start frontend**: `cd app && npm start`
3. **Access app**: [http://localhost:5173](http://localhost:5173)
4. **Test Google login**: Click "Login with Google" button
5. **API docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

For any issues, check the console logs and ensure all environment variables are set correctly.
