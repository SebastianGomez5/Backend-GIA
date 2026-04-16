from sqlalchemy.orm import Session
from app.db import models
from app.schemas import time_block_schema
from uuid import UUID
from datetime import datetime

def get_user_agenda(db: Session, user_id: UUID, start_date: datetime, end_date: datetime):
    """
    Busca todos los bloques de tiempo del usuario en un rango de fechas específico,
    ordenados cronológicamente.
    """
    return db.query(models.TimeBlock).filter(
        models.TimeBlock.user_id == user_id,
        models.TimeBlock.start_time >= start_date,
        models.TimeBlock.end_time <= end_date
    ).order_by(models.TimeBlock.start_time.asc()).all()

def create_time_block(db: Session, block: time_block_schema.TimeBlockCreate, user_id: UUID):
    """
    Esta función será usada principalmente por el motor de IA para guardar
    la agenda calculada en la base de datos.
    """
    db_block = models.TimeBlock(**block.model_dump(), user_id=user_id)
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block