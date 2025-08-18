from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from . import database, models
from .utils import get_password_hash, verify_password, SECRET_KEY, ALGORITHM, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------------- Schemas ---------------- #
class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# ---------------- HTTP Bearer ---------------- #
bearer_scheme = HTTPBearer()

# ---------------- Routes ---------------- #
@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.AdminUser).filter(models.AdminUser.email == payload.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed = get_password_hash(payload.password)
    new_user = models.AdminUser(email=payload.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully", "user_id": new_user.id}

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.AdminUser).filter(models.AdminUser.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# ---------------- Dependency ---------------- #
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Extract user ID from Bearer token.
    Used as a dependency for protected routes.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
