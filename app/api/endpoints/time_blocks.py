from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.schemas import time_block_schema
from app.services import time_block_service
from app.db.session import get_db
from app.api import deps
from app.db import models

router = APIRouter()

# Nota: response_model=List[...] indica que vamos a devolver una lista de bloques, no solo uno.
@router.get("/agenda", response_model=List[time_block_schema.TimeBlockResponse])
def get_agenda(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Ruta para que la aplicación móvil consulte cómo quedó organizada su agenda.
    """
    return time_block_service.get_user_agenda(db, current_user.id, start_date, end_date)