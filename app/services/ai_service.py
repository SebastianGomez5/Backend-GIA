from sqlalchemy.orm import Session
from datetime import date
from uuid import UUID
from app.db import models
from app.ai_engine.csp_solver import CSPSolver
from app.schemas.time_block_schema import TimeBlockCreate
from app.services import time_block_service, user_settings_service

def generate_daily_schedule(db: Session, user_id: UUID, target_date: date):
    # 1. Obtenemos las reglas del juego (Preferencias)
    settings = user_settings_service.get_user_settings(db, user_id)
    if not settings:
        raise ValueError("El usuario no tiene preferencias configuradas. Por favor, configúralas primero.")

    # 2. Buscamos la materia prima (Tareas Pendientes)
    tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.status == "Pendiente"
    ).all()

    if not tasks:
        return {"mensaje": "No hay tareas pendientes para agendar en este momento."}

    # 3. Le pasamos el trabajo pesado a nuestra Inteligencia Artificial
    solver = CSPSolver(tasks=tasks, user_settings=settings, target_date=target_date)
    best_schedule = solver.solve()

    if not best_schedule:
        return {"mensaje": "El algoritmo no pudo encontrar una agenda viable con el tiempo disponible."}

    # 4. Traducimos la respuesta matemática a datos físicos en PostgreSQL
    created_blocks = []
    for task_id, (start_time, end_time) in best_schedule.items():
        
        # Armamos el esquema para el nuevo bloque de tiempo
        block_data = TimeBlockCreate(
            task_id=task_id,
            start_time=start_time,
            end_time=end_time,
            is_locked=False
        )
        
        # Lo guardamos en la base de datos
        db_block = time_block_service.create_time_block(db, block=block_data, user_id=user_id)
        created_blocks.append(db_block)

        # 5. Actualizamos el estado de la tarea para que no se vuelva a agendar mañana
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task:
            db_task.status = "Agendada"
    
    # Confirmamos los cambios en la base de datos
    db.commit()

    return {
        "mensaje": "Agenda generada exitosamente.",
        "tareas_agendadas": len(best_schedule)
    }