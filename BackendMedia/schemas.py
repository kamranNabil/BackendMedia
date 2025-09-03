from pydantic import BaseModel, Field
from datetime import datetime

class AdminUserCreate(BaseModel):
    email: str
    password: str

class AdminUserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True   

class MediaAssetCreate(BaseModel):
    title: str 
    type: str
    file_url: str 

    class Config:
        from_attributes = True

class MediaAssetOut(BaseModel):
    id: int
    title: str
    type: str
    file_url: str
    created_at: datetime

    class Config:
        from_attributes = True   
