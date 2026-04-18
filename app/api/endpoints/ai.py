from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import get_db
from app.api import deps
from app.db import models
from app.services import ai_service

router = APIRouter()

@router.post("/generate-schedule")
def generate_schedule(
    target_date: date,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Activa el motor de Inteligencia Artificial para agendar las tareas pendientes.
    """
    try:
        # Llamamos al servicio que acabamos de crear
        result = ai_service.generate_daily_schedule(db, current_user.id, target_date)
        return result
    except ValueError as e:
        # Errores predecibles (ej. falta de configuraciones)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Errores inesperados del servidor o de la matemática
        raise HTTPException(status_code=500, detail=f"Error interno en el motor de IA: {str(e)}")