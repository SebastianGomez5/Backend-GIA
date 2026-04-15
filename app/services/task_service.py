from sqlalchemy.orm import Session
from app.db import models
from app.schemas import task_schema

# Esta función recibe la sesión de la base de datos y los datos ya validados por el esquema
def create_task(db: Session, task: task_schema.TaskCreate):
    
    # task.model_dump() convierte el esquema validado en un diccionario de Python.
    # Los asteriscos (**) desempaquetan ese diccionario para que coincida exactamente 
    # con las columnas de tu modelo en PostgreSQL.
    db_task = models.Task(**task.model_dump())
    
    # Preparamos la tarea en la sesión temporal
    db.add(db_task)
    
    # commit() es el equivalente a presionar Ctrl+S, guarda físicamente en la base de datos
    db.commit()
    
    # refresh() actualiza nuestro objeto db_task para traer los datos que PostgreSQL 
    # generó automáticamente, como el UUID (id)
    db.refresh(db_task)
    
    return db_task