from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas import decision_history_schema
from app.services import decision_history_service
from app.db.session import get_db
from app.api import deps
from app.db import models

router = APIRouter()

@router.post("/", response_model=decision_history_schema.DecisionHistoryResponse)
def log_decision(
    decision: decision_history_schema.DecisionHistoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Registra una nueva decisión. La app móvil llamará a esta ruta
    cuando el usuario modifique la agenda generada por la IA.
    """
    return decision_history_service.create_decision_record(db, decision, current_user.id)

@router.get("/", response_model=List[decision_history_schema.DecisionHistoryResponse])
def get_history(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Devuelve el historial de decisiones del usuario."""
    return decision_history_service.get_user_decisions(db, current_user.id, skip, limit)