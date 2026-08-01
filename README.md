# ⚙️ WikiPlanner - Backend (FastAPI & Motor de IA)

> **Sistema Inteligente Adaptativo para la Gestión y Optimización del Tiempo**  
> *Trabajo de Grado - Universidad del Valle (Escuela de Ingeniería de Sistemas y Computación)*

---

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Google Calendar API](https://img.shields.io/badge/Google_Calendar_API-v3-4285F4?logo=googlecalendar&logoColor=white)](https://developers.google.com/calendar)
[![License](https://img.shields.io/badge/License-Academic-blue.svg)]()

---

## 📌 Descripción del Proyecto

**WikiPlanner API** es el servidor de procesamiento y motor de Inteligencia Artificial (Backend) encargado de la optimización y asignación dinámica de horarios para actividades personales.

El núcleo de este sistema implementa un **motor de resolución de Problemas de Satisfacción de Restricciones (Constraint Satisfaction Problem - CSP)** con algoritmos de *backtracking* guiados por funciones de costo/penalización (*scoring*) y un módulo de aprendizaje a partir de la retroalimentación del usuario (*feedback loop*). Además, el backend proporciona autenticación JWT, persistencia relacional con PostgreSQL, cálculo de indicadores de rendimiento (KPIs) y sincronización bidireccional con **Google Calendar**.

---

## ✨ Características Principales

- 🧠 **Motor de IA & Algoritmo CSP (`app/ai_engine`)**:
  - **Resolución de Restricciones (CSP)**: Asignación inteligente de tareas considerando prioridades, duraciones, niveles de energía, plazos límite (*deadlines*) y franjas de preferencia.
  - **Evaluación y Penalización (`scoring.py`)**: Cálculo de costo dinámico por cada bloque de tiempo evaluado.
  - **Aprendizaje Continuo (`learning.py`)**: Construcción del perfil de penalización del usuario a partir del historial de rechazos o reprogramaciones manuales.
  - **Explicabilidad e Inferencia Transparente**: Diagnóstico automático del motivo exacto por el cual una tarea no pudo ser agendada (por falta de espacio, conflicto con jornada o incompatibilidad con la preferencia).
- 🔑 **Autenticación JWT & Seguridad**: Encriptación de contraseñas con `passlib` y tokens portadores (*Bearer tokens*) seguros.
- 📆 **Integración Bidireccional con Google Calendar**: Sincronización automática de eventos entre WikiPlanner y la cuenta Google del usuario vía OAuth2.
- 📊 **Cálculo de KPIs y Analíticas**: Medición de la Tasa de Adherencia al plan, Tasa de Aceptación de sugerencias de la IA y puntaje de confianza (*Confidence Score*).
- 🗄️ **Modelado Relacional ORM**: Esquema de base de datos relacional modelado con SQLAlchemy en PostgreSQL.

---

## 🛠️ Tecnologías y Librerías

| Categoría | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Framework Web** | FastAPI | Framework asíncrono de alto rendimiento para APIs RESTful |
| **Servidor ASGI** | Uvicorn | Servidor de producción/desarrollo rápido para FastAPI |
| **ORM / Base de Datos** | SQLAlchemy & PostgreSQL | Mapeo objeto-relacional y persistencia estructurada |
| **Seguridad** | PyJWT, Passlib (Bcrypt) | Autenticación basada en JSON Web Tokens y hashing |
| **Integración Google** | `google-api-python-client`, `google-auth` | Cliente API oficial para sincronización con Google Calendar |
| **Validación de Datos** | Pydantic | Schemas y serialización tipada de solicitudes y respuestas |

---

## 🗺️ Endpoints de la API REST

| Módulo | Prefijo | Descripción de Funcionalidad |
| :--- | :--- | :--- |
| **Autenticación** | `/api/auth` | Registro de usuarios, login y generación de tokens JWT. |
| **Usuarios** | `/api/users` | Consulta y actualización de datos del perfil de usuario. |
| **Preferencias** | `/api/settings` | Configuración de rangos laborales y descanso del usuario. |
| **Tareas** | `/api/tasks` | CRUD de tareas (pendientes, fijas, flexibles, prioridades). |
| **Bloques de Tiempo** | `/api/time-blocks` | Obtención de la agenda agendada por fecha y franjas. |
| **Inteligencia Artificial** | `/api/ai` | Disparo del motor CSP para generar la agenda diaria. |
| **Decisiones** | `/api/decisions` | Registro y consulta de acciones aceptadas/rechazadas por el usuario. |
| **Métricas KPI** | `/api/kpi` | Cálculo de tasa de adherencia y satisfacción. |
| **Google Calendar** | `/api/google` | OAuth2 flow y sincronización con Google Calendar. |

---

## 📂 Estructura del Código Fuente

```text
Backend-WikiPlanner/
├── app/
│   ├── ai_engine/           # Motor de Inteligencia Artificial (CSP & Scoring)
│   │   ├── csp_solver.py    # Algoritmo CSP Backtracking & Diagnóstico
│   │   ├── learning.py      # Modelo de aprendizaje continuo basado en decisiones
│   │   └── scoring.py       # Cálculo de penalizaciones y score de confianza
│   ├── api/
│   │   └── endpoints/       # Controladores de rutas REST por módulo
│   │       ├── ai.py
│   │       ├── auth.py
│   │       ├── decisions.py
│   │       ├── google_auth.py
│   │       ├── kpi.py
│   │       ├── tasks.py
│   │       ├── time_blocks.py
│   │       ├── user_settings.py
│   │       └── users.py
│   ├── core/                # Configuraciones globales y seguridad (JWT, envs)
│   │   ├── config.py
│   │   └── security.py
│   ├── db/                  # Modelos SQLAlchemy y sesión de base de datos
│   │   ├── models.py
│   │   └── session.py
│   ├── schemas/             # Esquemas de validación Pydantic
│   │   └── user_schema.py
│   ├── services/            # Lógica de negocio (sincronización Google, tareas)
│   └── main.py              # Punto de entrada de la aplicación FastAPI
├── .env                     # Variables de entorno de la aplicación
├── credentials.json         # Credenciales OAuth2 para Google Calendar API
├── requirements.txt         # Dependencias del proyecto Python
└── README.md                # Documentación del backend
```

---

## 🚀 Requisitos Previos e Instalación

### Requisitos Técnicos
- **Python**: `v3.10` o superior
- **PostgreSQL**: Servidor de base de datos PostgreSQL en ejecución
- **Virtualenv**: Entorno virtual de Python

### Pasos de Instalación

1. **Clonar el repositorio e ingresar a la carpeta**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd TG/Backend-WikiPlanner
   ```

2. **Crear y activar el entorno virtual**:
   - En Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - En Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar el archivo `.env`**:
   Crea o edita el archivo `.env` en la raíz del backend con la configuración de tu base de datos y secretos:
   ```env
   PROJECT_NAME="WikiPlanner API"
   DATABASE_URL="postgresql://postgres:tu_password@localhost:5432/wikiplanner_db"
   SECRET_KEY="TuClaveSuperSecretaDePrueba"
   GOOGLE_CLIENT_ID="tu_google_client_id.apps.googleusercontent.com"
   GOOGLE_CLIENT_SECRET="tu_google_client_secret"
   GOOGLE_REDIRECT_URI="http://localhost:8000/api/google/callback"
   ```

5. **Iniciar el servidor backend (Uvicorn)**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Documentación Interactiva Swagger UI**:
   Una vez iniciado el servidor, accede a la interfaz interactiva OpenAPI en:
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🎓 Información Académica del Proyecto

- **Título del Trabajo de Grado**: *Implementación de un sistema inteligente adaptativo para la gestión y optimización del tiempo.*
- **Autor**: Juan Sebastián Gómez Agudelo (*Código: 2259474*)
- **Director**: MSc. Joshua David Triana Madrid, Ing.
- **Institución**: Universidad del Valle - Sede Tuluá
- **Facultad**: Facultad de Ingeniería
- **Escuela**: Escuela de Ingeniería de Sistemas y Computación
- **Año**: 2025 - 2026

---

## 📄 Licencia

Este proyecto ha sido desarrollado con fines exclusivamente académicos e investigativos en el marco del programa de Ingeniería de Sistemas y Computación de la **Universidad del Valle**.
