from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class DecisionHistoryBase(BaseModel):
    conflict_context: Dict[str, Any] # Ej: {"tarea": "gym", "hora_sugerida": "6:00 AM"}
    ai_suggested_action: str         # Ej: "Agendar en la mañana"
    user_final_action: Optional[str] = None # Ej: "Movido a la noche"
    is_accepted: Optional[bool] = None      # True si aceptaste la sugerencia de la IA
    confidence_score: Optional[float] = None # Con cuánta seguridad la IA hizo esta sugerencia

class DecisionHistoryCreate(DecisionHistoryBase):
    pass

class DecisionHistoryResponse(DecisionHistoryBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)