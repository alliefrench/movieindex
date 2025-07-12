API_ROOT = "/api"

SCARY_ROUTE = f"{API_ROOT}/scary"
MOVIES_ROUTE = f"{API_ROOT}/movies"

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://www.themovieindex.club",
]

AUTH_ROOT = f"{API_ROOT}/auth"
GOOGLE_AUTH_ROOT = f"{AUTH_ROOT}/google"
GOOGLE_AUTH_CALLBACK_ROOT = f"{GOOGLE_AUTH_ROOT}/callback"
GOOGLE_AUTH_ME_ROOT = f"{GOOGLE_AUTH_ROOT}/me"
GOOGLE_AUTH_DEBUG_DB_ROOT = f"{GOOGLE_AUTH_ROOT}/debug/db"
