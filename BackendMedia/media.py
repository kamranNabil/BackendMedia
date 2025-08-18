from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt

import database
import models
from schemas import MediaAssetCreate as MediaCreate
from auth import get_current_user, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/media", tags=["media"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
