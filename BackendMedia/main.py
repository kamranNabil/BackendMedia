from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
import database
import models
from auth import router as auth_router
from media import router as media_router

# 1️⃣ Create the FastAPI app first
app = FastAPI(title="Media Platform Backend")

# 2️⃣ Exception handler after app exists
@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    # Print full traceback to console
    print("Exception occurred:")
    traceback.print_exc()

    # Return error in JSON response
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__
        }
    )

# 3️⃣ Create database tables
models.Base.metadata.create_all(bind=database.engine)

# 4️⃣ Include routers
app.include_router(auth_router)
app.include_router(media_router)

# 5️⃣ Root endpoint
@app.get("/")
def root():
    return {"message": "BackendMedia API is running"}

# 6️⃣ Optional: print all routes
for route in app.routes:
    print(f"Path: {route.path}, Method: {route.methods}")
