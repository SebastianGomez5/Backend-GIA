from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import task_schema
from app.services import task_service
from app.db.session import get_db

# Creamos un enrutador (Router) exclusivo para gestionar tareas.
# Esto mantiene el código ordenado y evita que el main.py se llene de miles de líneas.
router = APIRouter()

# Definimos una ruta POST (usada para crear recursos).
# response_model garantiza que la salida pase por el filtro de TaskResponse, 
# ocultando datos sensibles y formateando la respuesta.
@router.post("/", response_model=task_schema.TaskResponse)
def create_task(task: task_schema.TaskCreate, db: Session = Depends(get_db)):
    
    # Delegamos el trabajo pesado a la capa de servicios.
    # La API solo actúa como un puente limpio y seguro.
    return task_service.create_task(db=db, task=task)