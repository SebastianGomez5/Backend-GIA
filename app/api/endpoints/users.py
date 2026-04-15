from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import user_schema
from app.services import user_service
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)