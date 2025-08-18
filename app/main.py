from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware  


from .limiter import limiter
from .auth import router as auth_router
from .media import router as media_router
from . import database, models
from .redis_client import redis_client

app = FastAPI(title="Media Platform Backend")

# ---------------- Rate Limiter ----------------
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)  # <-- Use SlowAPIMiddleware, not limiter.middleware

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
            return {"status": "Redis is alive!"}
    except Exception as e:
        return {"status": "Redis connection failed", "error": str(e)}

