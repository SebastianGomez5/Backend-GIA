from sqlalchemy.orm import Session
from app.db import models
from app.schemas import decision_history_schema
from uuid import UUID

def create_decision_record(db: Session, decision: decision_history_schema.DecisionHistoryCreate, user_id: UUID):
    """Guarda un registro de la acción del usuario respecto a una sugerencia de la IA."""
    
    db_decision = models.DecisionHistory(
        **decision.model_dump(),
        user_id=user_id
    )
    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)
    return db_decision

def get_user_decisions(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    """Obtiene el historial para que el futuro algoritmo de ML lo pueda analizar."""
    return db.query(models.DecisionHistory).filter(
        models.DecisionHistory.user_id == user_id
    ).order_by(models.DecisionHistory.created_at.desc()).offset(skip).limit(limit).all()