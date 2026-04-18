from datetime import datetime

def calculate_slot_penalty(task, slot_start: datetime):
    """
    Evalúa qué tan 'doloroso' o inadecuado es asignar una tarea en una hora específica.
    Entre mayor sea el puntaje (penalización), peor es la decisión.
    """
    penalty = 0
    hora_del_dia = slot_start.hour

    # 1. Evaluación de Energía y Dificultad
    # Si la tarea es pesada, el usuario debería hacerla temprano cuando tiene la mente fresca.
    if task.energy_level == "Alto" or task.difficulty_level == "Alta":
        if hora_del_dia >= 15: # Después de las 3:00 PM
            penalty += 20
        elif hora_del_dia >= 18: # Después de las 6:00 PM el cansancio es extremo
            penalty += 50

    # 2. Evaluación de Categoría
    # Si es una tarea de "Ocio" o "Salud" (como ir al gimnasio), suele ser mejor al final del día.
    if task.category in ["Ocio", "Salud"]:
        if hora_del_dia < 12: # En la mañana penalizamos un poco para priorizar trabajo
            penalty += 15

    # 3. Evaluación de Flexibilidad
    # Si la tarea NO es flexible (ej. una reunión fija), el algoritmo no debería 
    # tener penalización extra porque es una obligación inamovible.
    # Pero si ES flexible, el algoritmo tiene libertad de buscar el punto de menor estrés.
    if not task.is_flexible:
        penalty = 0 # No hay penalización por hora, tiene que hacerse sí o sí.

    return penalty