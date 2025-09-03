from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware  
import os  # ⬅️ ADD THIS IMPORT

from .limiter import limiter
from .auth import router as auth_router
from .media import router as media_router
from . import database, models
from .redis_client import redis_client

app = FastAPI(title="Media Platform Backend")
router = APIRouter()

# ---------------- Rate Limiter ----------------
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Database ----------------
models.Base.metadata.create_all(bind=database.engine)

# ---------------- Routers ----------------
app.include_router(auth_router)
app.include_router(media_router)

# ---------------- Root ----------------
@app.get("/")
def root():
    return {"message": "BackendMedia API is running"}

@app.get("/ping-redis")
def ping_redis():
    try:
        if redis_client.ping():
            return {"message": "Pong! Redis is connected."}  # Changed response format
    except Exception as e:
        return {"status": "Redis connection failed", "error": str(e)}

# ---------------- Debug Endpoint ----------------
@app.get("/debug-env")  # ⬅️ Add directly to app, not router
async def debug_env():
    return {
        "redis_url": os.getenv("REDIS_URL"),
        "redis_url_exists": bool(os.getenv("REDIS_URL")),
        "jwt_secret_exists": bool(os.getenv("JWT_SECRET_KEY")),
        "database_url_exists": bool(os.getenv("DATABASE_URL")),
        "all_environment_variables": list(os.environ.keys())
    }