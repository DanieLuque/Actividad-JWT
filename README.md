# Actividad-JWT - Sistema de Gestión de Tareas con JWT

Sistema de gestión de tareas RESTful implementado con Django REST Framework (DRF) y autenticación JWT (Simple JWT), sin templates HTML. Proyecto con dos apps: `tasks` (autenticación) y `api` (CRUD de tareas).

## Características

- ✅ Autenticación JWT con tokens de acceso y refresco
- ✅ Registro de usuarios con validación de contraseñas
- ✅ Sistema completo de gestión de tareas (CRUD)
- ✅ Filtrado de tareas por estado y prioridad
- ✅ Base de datos MySQL
- ✅ Permiso de usuario para acceder solo sus propias tareas
- ✅ API RESTful completa sin templates
- ✅ Panel de administración Django
- ✅ Documentación interactiva con Swagger y ReDoc
- ✅ Dos apps: `tasks` (autenticación) y `api` (gestión de tareas)

## Requisitos

- Python 3.8+
- MySQL Server
- pip (gestor de paquetes de Python)

## Instalación y Setup

### 1. Crear la base de datos MySQL

Debes crear la base de datos manualmente en MySQL:

```sql
CREATE DATABASE task_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Edita el archivo `.env.example` con tus credenciales MySQL:

```env
DEBUG=True
SECRET_KEY=

# MySQL Configuration
DB_ENGINE=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# JWT Configuration
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### 4. Ejecutar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario (opcional, para panel admin)

```bash
python manage.py createsuperuser
```

### 6. Iniciar servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

## Estructura del Proyecto

```
Actividad-JWT/
├── config/                    # Configuración principal del proyecto
│   ├── settings.py           # Configuración de Django, DRF, JWT
│   ├── urls.py               # URLs principales
│   ├── asgi.py               # ASGI
│   └── wsgi.py               # WSGI
├── tasks/                     # App de Autenticación
│   ├── models.py             # Modelos (Task, User)
│   ├── views.py              # ViewSets de autenticación
│   ├── serializers.py        # Serializadores
│   ├── urls.py               # URLs de autenticación
│   ├── admin.py              # Panel de administración
│   └── migrations/           # Migraciones de base de datos
├── api/                       # App de Gestión de Tareas
│   ├── views.py              # ViewSets (UserViewSet, TaskViewSet)
│   ├── serializers.py        # Serializadores (UserSerializer, TaskSerializer)
│   ├── urls.py               # URLs de la API
│   ├── apps.py               # Configuración de la app
│   └── migrations/           # Migraciones
├── .env                       # Variables de entorno
├── manage.py                  # Script de gestión de Django
├── requirements.txt           # Dependencias
└── README.md                  # Este archivo
```

## Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Registrar nuevo usuario |
| POST | `/api/auth/login/` | Obtener tokens JWT |
| POST | `/api/auth/refresh/` | Refrescar token de acceso |

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/users/me/` | Obtener información del usuario actual |
| GET | `/api/users/{id}/` | Obtener información de un usuario |
| POST | `/api/users/logout/` | Logout del usuario |

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks/` | Listar todas las tareas del usuario |
| POST | `/api/tasks/` | Crear nueva tarea |
| GET | `/api/tasks/{id}/` | Obtener detalle de una tarea |
| PUT | `/api/tasks/{id}/` | Actualizar una tarea |
| PATCH | `/api/tasks/{id}/` | Actualización parcial |
| DELETE | `/api/tasks/{id}/` | Eliminar una tarea |
| GET | `/api/tasks/by_status/?status=pending` | Filtrar por estado |
| GET | `/api/tasks/by_priority/?priority=high` | Filtrar por prioridad |
| PATCH | `/api/tasks/{id}/mark_completed/` | Marcar como completada |

## Dependencias

| Paquete | Versión | Función |
|---------|---------|---------|
| Django | 5.2.8 | Framework web principal |
| djangorestframework | 3.16.1 | Framework para crear APIs REST |
| djangorestframework-simplejwt | 5.5.1 | Autenticación JWT |
| drf-spectacular | 0.27.0 | Documentación OpenAPI (Swagger, ReDoc) |
| mysqlclient | 2.2.7 | Driver MySQL |
| python-decouple | 3.8 | Lector de variables de entorno (.env) |
| PyJWT | 2.10.1 | Manejo de tokens JWT |

## Ejemplo de Uso con cURL

### 1. Registrar un usuario

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "email": "juan@example.com",
    "password": "securepass123",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

Respuesta:
```json
{
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 1,
    "username": "juan",
    "email": "juan@example.com",
    "first_name": "Juan",
    "last_name": "Pérez"
  },
  "refresh": "eyJhbGc...",
  "access": "eyJhbGc..."
}
```

### 2. Login (obtener tokens)

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "password": "securepass123"
  }'
```

Respuesta:
```json
{
  "refresh": "eyJhbGc...",
  "access": "eyJhbGc...",
  "user": {
    "id": 1,
    "username": "juan",
    "email": "juan@example.com"
  }
}
```

### 3. Crear una tarea (usando token)

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{
    "title": "Implementar autenticación JWT",
    "description": "Agregar autenticación JWT al proyecto",
    "priority": "high",
    "status": "in_progress"
  }'
```

### 4. Listar tareas

```bash
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer eyJhbGc..."
```

### 5. Filtrar tareas por estado

```bash
curl -X GET http://localhost:8000/api/tasks/by_status/?status=pending \
  -H "Authorization: Bearer eyJhbGc..."
```

### 6. Marcar tarea como completada

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/mark_completed/ \
  -H "Authorization: Bearer eyJhbGc..."
```

## Modelos de Datos

### Usuario (User)

Modelo estándar de Django con campos:
- `id`: ID único
- `username`: Nombre de usuario único
- `email`: Email del usuario
- `first_name`: Nombre
- `last_name`: Apellido
- `password`: Contraseña encriptada

### Tarea (Task)

```python
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "juan",
    "email": "juan@example.com"
  },
  "title": "Tarea ejemplo",
  "description": "Descripción de la tarea",
  "status": "pending",  # pending, in_progress, completed
  "priority": "high",   # low, medium, high
  "due_date": "2024-12-31T23:59:59Z",
  "created_at": "2024-11-28T10:00:00Z",
  "updated_at": "2024-11-28T10:00:00Z"
}
```

## Configuración de JWT

La configuración se encuentra en `config/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
}
```

### Tokens JWT

- **Access Token**: Token de corta duración (24 horas por defecto) para acceder a la API
- **Refresh Token**: Token de larga duración (1 día por defecto) para obtener nuevo access token

## Autenticación en Requests

Incluir el token JWT en la cabecera de autorización:

```
Authorization: Bearer <access_token>
```

Ejemplo con Python requests:

```python
import requests

token = "eyJhbGc..."
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.get(
    "http://localhost:8000/api/tasks/",
    headers=headers
)
print(response.json())
```

## App `tasks` vs App `api`

### App `tasks`
- **Responsabilidad:** Autenticación de usuarios
- **Endpoints:** `/api/tasks-auth/auth/register/`, `/api/tasks-auth/auth/login/`
- **ViewSets:** Login, Registro, Refresh Token
- **Modelos:** User, Task

### App `api`
- **Responsabilidad:** Gestión de tareas (CRUD)
- **Endpoints:** `/api/users/`, `/api/tasks/`
- **ViewSets:** UserViewSet, TaskViewSet
- **Modelos:** Importa de `tasks`

**Ambas apps coexisten:** `tasks` maneja autenticación, `api` maneja datos



