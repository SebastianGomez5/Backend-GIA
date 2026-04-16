from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import time

class UserSettingsBase(BaseModel):
    current_mode: Optional[str] = "Normal"
    work_start_time: Optional[time] = time(8, 0)  # 8:00 AM por defecto
    work_end_time: Optional[time] = time(20, 0) # 8:00 PM por defecto
    preferences: Optional[Dict[str, Any]] = {} # Un diccionario para cosas extra (JSONB)

class UserSettingsCreate(UserSettingsBase):
    pass

class UserSettingsUpdate(UserSettingsBase):
    pass

class UserSettingsResponse(UserSettingsBase):
    id: UUID
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)