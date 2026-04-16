from sqlalchemy.orm import Session
from app.db import models
from app.schemas import user_settings_schema
from uuid import UUID

def get_user_settings(db: Session, user_id: UUID):
    # Busca si el usuario ya tiene configuraciones guardadas
    return db.query(models.UserSettings).filter(models.UserSettings.user_id == user_id).first()

def upsert_user_settings(db: Session, settings: user_settings_schema.UserSettingsCreate, user_id: UUID):
    """
    Upsert = Update or Insert (Actualiza si existe, o crea si no existe).
    Así evitamos tener múltiples configuraciones para un mismo usuario.
    """
    db_settings = get_user_settings(db, user_id)
    
    if db_settings:
        # Si existe, actualizamos los valores
        for key, value in settings.model_dump(exclude_unset=True).items():
            setattr(db_settings, key, value)
    else:
        # Si no existe, creamos uno nuevo
        db_settings = models.UserSettings(**settings.model_dump(), user_id=user_id)
        db.add(db_settings)
        
    db.commit()
    db.refresh(db_settings)
    return db_settings