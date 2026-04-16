from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import user_settings_schema
from app.services import user_settings_service
from app.db.session import get_db
from app.api import deps
from app.db import models

router = APIRouter()

@router.get("/", response_model=user_settings_schema.UserSettingsResponse)
def read_settings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Obtiene las configuraciones del usuario autenticado."""
    settings = user_settings_service.get_user_settings(db, current_user.id)
    if not settings:
        # Si no tiene, creamos unas por defecto (para que no falle la IA más adelante)
        default_settings = user_settings_schema.UserSettingsCreate()
        settings = user_settings_service.upsert_user_settings(db, default_settings, current_user.id)
    return settings

@router.put("/", response_model=user_settings_schema.UserSettingsResponse)
def update_settings(
    settings: user_settings_schema.UserSettingsCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Actualiza o crea las configuraciones del usuario autenticado."""
    return user_settings_service.upsert_user_settings(db=db, settings=settings, user_id=current_user.id)