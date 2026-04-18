import time
from datetime import datetime, timedelta
from .scoring import calculate_slot_penalty

class CSPSolver:
    def __init__(self, tasks, user_settings, target_date, timeout=4.0):
        """
        Inicializa el cerebro de la IA.
        - tasks: Lista de tareas a organizar hoy.
        - user_settings: Preferencias del usuario (hora de inicio y fin del día).
        - target_date: El día específico que estamos agendando.
        - timeout: Tiempo máximo de pensamiento (en segundos) para evitar bloqueos.
        """
        self.tasks = tasks
        self.settings = user_settings
        self.target_date = target_date
        self.timeout = timeout
        
        self.start_time = None
        self.best_schedule = {}
        self.max_tasks_scheduled = 0

        # Definimos los límites del día (Restricción Dura Global)
        self.day_start = datetime.combine(target_date, self.settings.work_start_time)
        self.day_end = datetime.combine(target_date, self.settings.work_end_time)

    def solve(self):
        """Punto de entrada principal. Inicia el reloj y dispara el algoritmo."""
        self.start_time = time.time()
        
        # 1. ORDENAMIENTO INTELIGENTE (Heurística)
        # Ordenamos primero por Prioridad (descendente) y luego por Duración (descendente).
        # Tareas urgentes y largas se acomodan primero; las fáciles rellenan huecos.
        self.tasks = sorted(
            self.tasks, 
            key=lambda t: (t.priority, t.duration_minutes), 
            reverse=True
        )
        
        current_schedule = {}
        
        # 2. INICIAMOS EL BACKTRACKING (Recursividad)
        self._backtrack(task_index=0, current_schedule=current_schedule)
        
        return self.best_schedule

    def _backtrack(self, task_index, current_schedule):
        """El corazón matemático del algoritmo."""
        
        # Criterio de parada 1: El tiempo se acabó (Timeout de 4 segundos)
        if time.time() - self.start_time > self.timeout:
            return False
            
        # Criterio de parada 2: Ya revisamos todas las tareas
        if task_index == len(self.tasks):
            # Guardamos la mejor agenda encontrada
            self.best_schedule = current_schedule.copy()
            self.max_tasks_scheduled = len(current_schedule)
            return True

        # Guardamos la agenda parcial si es la mejor hasta ahora
        if len(current_schedule) > self.max_tasks_scheduled:
            self.best_schedule = current_schedule.copy()
            self.max_tasks_scheduled = len(current_schedule)

        # Tomamos la tarea que nos toca evaluar en este ciclo
        current_task = self.tasks[task_index]
        
        # DOMINIO: Buscamos todos los huecos de tiempo posibles (ej. de 15 en 15 minutos)
        possible_slots = self._get_possible_slots(current_task)

        for slot_start, slot_end in possible_slots:
            # RESTRICCIÓN DURA: Verificamos que no choque con otras tareas
            if self._is_valid(slot_start, slot_end, current_schedule):
                
                # ASIGNACIÓN: Ponemos la ficha en el tablero
                current_schedule[current_task.id] = (slot_start, slot_end)
                
                # RECURSIVIDAD: Llamamos a la función de nuevo para la siguiente tarea
                if self._backtrack(task_index + 1, current_schedule):
                    return True
                
                # RETROCESO (BACKTRACK): Si la línea de arriba falló (no cupieron las demás), 
                # quitamos esta ficha del tablero y probamos el siguiente hueco.
                del current_schedule[current_task.id]

        # Si ningún hueco sirvió para esta tarea, la saltamos y tratamos de acomodar el resto
        return self._backtrack(task_index + 1, current_schedule)

    def _get_possible_slots(self, task):
        """
        Genera franjas de tiempo disponibles en intervalos de 15 minutos.
        Ejemplo: 8:00 a 9:00, 8:15 a 9:15, etc.
        """
        slots = []
        current_time = self.day_start
        duration = timedelta(minutes=task.duration_minutes)

        while current_time + duration <= self.day_end:
            # RESTRICCIÓN DURA: Deadline. Si se pasa del límite de entrega, no sirve.
            if task.deadline and (current_time + duration) > task.deadline.replace(tzinfo=None):
                break # Ya no buscamos más tarde
                
            slots.append((current_time, current_time + duration))
            current_time += timedelta(minutes=15) # Intervalo de búsqueda
            
        return slots

    def _is_valid(self, start_time, end_time, current_schedule):
        """Verifica que el nuevo bloque no se solape con los que ya están en el tablero."""
        for scheduled_start, scheduled_end in current_schedule.values():
            # Condición de solapamiento de fechas
            if max(start_time, scheduled_start) < min(end_time, scheduled_end):
                return False # ¡Hay choque!
        return True

    def _get_possible_slots(self, task):
        """
        Genera franjas de tiempo disponibles en intervalos de 15 minutos,
        pero ahora las ORDENA de mejor a peor usando la función de Scoring.
        """
        slots_with_scores = []
        current_time = self.day_start
        duration = timedelta(minutes=task.duration_minutes)

        while current_time + duration <= self.day_end:
            if task.deadline and (current_time + duration) > task.deadline.replace(tzinfo=None):
                break 
                
            # Calculamos la penalización para este hueco de tiempo específico
            penalty = calculate_slot_penalty(task, current_time)
            
            slots_with_scores.append({
                "start": current_time,
                "end": current_time + duration,
                "penalty": penalty
            })
            
            current_time += timedelta(minutes=15)
            
        # MAGIA DE IA: Ordenamos los huecos de menor a mayor penalización.
        # Así, el Backtracking probará siempre los horarios más saludables primero.
        slots_with_scores.sort(key=lambda x: x["penalty"])
        
        # Devolvemos solo las tuplas de (start, end) ya ordenadas para que el algoritmo las use
        return [(slot["start"], slot["end"]) for slot in slots_with_scores]