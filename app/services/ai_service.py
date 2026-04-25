from sqlalchemy.orm import Session
from datetime import date
from uuid import UUID
from app.db import models
from app.ai_engine.csp_solver import CSPSolver
from app.schemas.time_block_schema import TimeBlockCreate
from app.services import time_block_service, user_settings_service

# IMPORTACIÓN NUEVA: Traemos nuestra función para hablar con Google
from app.services.google_calendar_service import create_google_event

def generate_daily_schedule(db: Session, user_id: UUID, target_date: date):
    settings = user_settings_service.get_user_settings(db, user_id)
    if not settings:
        raise ValueError("El usuario no tiene preferencias configuradas. Por favor, configúralas primero.")

    tasks = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.status == "Pendiente"
    ).all()

    if not tasks:
        return {"mensaje": "No hay tareas pendientes para agendar en este momento."}

    solver = CSPSolver(tasks=tasks, user_settings=settings, target_date=target_date)
    best_schedule = solver.solve()

    if not best_schedule:
        return {"mensaje": "El algoritmo no pudo encontrar una agenda viable con el tiempo disponible."}

    created_blocks = []
    for task_id, (start_time, end_time) in best_schedule.items():
        
        # 1. Buscamos la tarea para saber su nombre (Google lo necesita para el título)
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        
        # 2. LLAMAMOS A GOOGLE CALENDAR (La magia sucede aquí)
        # Esto va a crear el evento real y nos devolverá el ID que Google le asigne.
        g_event_id = create_google_event(db_task.title, start_time, end_time)
        
        # 3. Armamos el bloque de tiempo, inyectándole el ID de Google
        block_data = TimeBlockCreate(
            task_id=task_id,
            start_time=start_time,
            end_time=end_time,
            google_event_id=g_event_id, # Ahora esto ya no será null
            is_locked=False
        )
        
        db_block = time_block_service.create_time_block(db, block=block_data, user_id=user_id)
        created_blocks.append(db_block)

        if db_task:
            db_task.status = "Agendada"
    
    db.commit()

    return {
        "mensaje": "Agenda generada y sincronizada con Google Calendar exitosamente.",
        "tareas_agendadas": len(best_schedule)
    }