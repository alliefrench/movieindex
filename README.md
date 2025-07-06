# movieindex

App for friend-sourcing movie reviews

## Project Structure

- `api/` — FastAPI Python server
- `app/` — React web frontend

## Getting Started

### Running the Services Locally

#### 1. Backend (FastAPI)

```bash
cd api
python -m venv venv
source .env
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The FastAPI server will run at [http://localhost:8000](http://localhost:8000).

#### 2. Frontend (React)

You’ll need Node.js installed.

```bash
cd app
# If you have a full React setup (e.g., with Vite or Create React App), run:
npm install
npm start
```

The React app will typically run at [http://localhost:3000](http://localhost:3000) (or as specified in your setup).

---

Update these instructions as you add more dependencies or change your project setup.
