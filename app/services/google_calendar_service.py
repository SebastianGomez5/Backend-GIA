import requests
from datetime import datetime
from app.core.config import settings

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
CALENDAR_API_BASE = "https://www.googleapis.com/calendar/v3"


def get_access_token(refresh_token: str) -> str:
    """
    Intercambia el refresh_token del usuario por un access_token fresco.
    Esto se hace en CADA operación, ya que el access_token expira en 1 hora
    pero el refresh_token (en modo producción) no expira.
    """
    response = requests.post(GOOGLE_TOKEN_URL, data={
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    })

    if response.status_code != 200:
        raise Exception(f"No se pudo renovar el token de Google: {response.json()}")

    return response.json()["access_token"]


def create_google_event(user, task_title: str, start_time: datetime, end_time: datetime):
    """
    Crea un evento en el Google Calendar del USUARIO específico
    (usando su propio refresh_token, no uno global).
    """
    if not user.google_refresh_token:
        print(f"⚠️ Usuario {user.id} no tiene Google Calendar conectado. Se omite sincronización.")
        return None

    try:
        access_token = get_access_token(user.google_refresh_token)

        event = {
            "summary": task_title,
            "description": "Generado por Agenda IA inteligente",
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "America/Bogota",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "America/Bogota",
            },
        }

        response = requests.post(
            f"{CALENDAR_API_BASE}/calendars/primary/events",
            headers={"Authorization": f"Bearer {access_token}"},
            json=event
        )

        if response.status_code not in (200, 201):
            print(f"⚠️ Error creando evento en Google: {response.json()}")
            return None

        return response.json().get("id")

    except Exception as e:
        print(f"⚠️ Error de sincronización con Google Calendar: {e}")
        return None


def delete_google_event(user, event_id: str):
    """Elimina un evento del calendario del usuario específico."""
    if not event_id or not user.google_refresh_token:
        return False

    try:
        access_token = get_access_token(user.google_refresh_token)

        response = requests.delete(
            f"{CALENDAR_API_BASE}/calendars/primary/events/{event_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if response.status_code in (200, 204, 404):
            # 404 significa que ya no existe, lo tratamos como éxito
            return True

        print(f"⚠️ Error eliminando evento de Google: {response.json()}")
        return False

    except Exception as e:
        print(f"⚠️ Error al eliminar evento de Google Calendar: {e}")
        return False


def get_calendar_events(user, start_date: datetime, end_date: datetime):
    """
    Obtiene TODOS los eventos del calendario del usuario en un rango de fechas,
    incluyendo los creados externamente (por otras personas, invitaciones, u otras apps).
    Filtra los eventos que la propia IA creó, para no duplicarlos.
    """
    if not user.google_refresh_token:
        return []

    try:
        access_token = get_access_token(user.google_refresh_token)

        # CORREGIDO — Manejamos correctamente fechas con y sin zona horaria
        def to_google_format(dt):
            if dt.tzinfo is not None:
                # Ya trae zona horaria (ej. viene del frontend con "Z")
                return dt.isoformat()
            else:
                # Fecha "naive" (sin zona), asumimos UTC y lo indicamos
                return dt.isoformat() + "Z"

        params = {
            "timeMin": to_google_format(start_date),
            "timeMax": to_google_format(end_date),
            "singleEvents": True,
            "orderBy": "startTime",
        }

        response = requests.get(
            f"{CALENDAR_API_BASE}/calendars/primary/events",
            headers={"Authorization": f"Bearer {access_token}"},
            params=params
        )

        if response.status_code != 200:
            print(f"⚠️ Error obteniendo eventos de Google: {response.json()}")
            return []

        events = response.json().get("items", [])

        external_events = []
        for event in events:
            description = event.get("description", "")
            if "Generado por Agenda IA" in description:
                continue

            start = event.get("start", {}).get("dateTime")
            end = event.get("end", {}).get("dateTime")

            if start and end:
                external_events.append({
                    "title": event.get("summary", "Evento sin título"),
                    "start": datetime.fromisoformat(start.replace("Z", "+00:00")).replace(tzinfo=None),
                    "end": datetime.fromisoformat(end.replace("Z", "+00:00")).replace(tzinfo=None),
                })

        return external_events

    except Exception as e:
        print(f"⚠️ Error leyendo calendario de Google: {e}")
        return []