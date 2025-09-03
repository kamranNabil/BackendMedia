from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import json
from .redis_client import redis_client
from . import database, models
from .schemas import MediaAssetCreate as MediaCreate
from .auth import get_current_user, SECRET_KEY, ALGORITHM
from .limiter import limiter
router = APIRouter(prefix="/media", tags=["media"])

# ---------------- Database Dependency ----------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Create Media ----------------
@router.post("", response_model=dict)
def create_media(payload: MediaCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    new_media = models.MediaAsset(
        title=payload.title,
        type=payload.type,
        file_url=payload.file_url
    )
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    return {
        "id": new_media.id,
        "title": new_media.title,
        "type": new_media.type,
        "file_url": new_media.file_url,
        "created_at": new_media.created_at
    }

# ---------------- Get Stream URL ----------------
@router.get("/{media_id}/stream-url", response_model=dict)
def get_stream_url(media_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    media = db.query(models.MediaAsset).filter(models.MediaAsset.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    expire = datetime.utcnow() + timedelta(minutes=10)
    token_payload = {
        "mid": media_id,
        "exp": expire,
        "scope": "stream"
    }
    stream_token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"stream_url": f"/stream?token={stream_token}"}

# ---------------- Analytics with Redis Caching ----------------
@router.get("/{media_id}/analytics", response_model=dict)
def get_media_analytics(media_id: int, db: Session = Depends(get_db)):
    cache_key = f"media_analytics:{media_id}"
    
    # Check Redis cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Fetch from DB
    media = db.query(models.MediaAsset).filter(models.MediaAsset.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    analytics = {
        "media_id": media.id,
        "title": media.title,
        "views": media.views if hasattr(media, "views") else 0  # placeholder
    }
    
    # Cache in Redis for 10 minutes
    redis_client.setex(cache_key, 600, json.dumps(analytics))
    
    return analytics

# ---------------- POST View with Rate Limiting ----------------
@router.post("/{media_id}/view")
@limiter.limit("5/minute")  # 5 requests per minute per IP
def post_media_view(media_id: int, db: Session = Depends(get_db), request: Request = None):
    media = db.query(models.MediaAsset).filter(models.MediaAsset.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    if not hasattr(media, "views"):
        media.views = 0
    media.views += 1
    db.commit()
    
    # Invalidate Redis cache for analytics
    cache_key = f"media_analytics:{media_id}"
    redis_client.delete(cache_key)

    return {"media_id": media_id, "views": media.views}
