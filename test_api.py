"""
Archivo de pruebas de la API con ejemplos de uso.
Este archivo demuestra cómo interactuar con la API REST.
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:8000/api"
HEADERS = {"Content-Type": "application/json"}


class TaskAPIClient:
    """Cliente para interactuar con la API de tareas."""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
    
    def set_auth_headers(self):
        """Actualizar headers con token de autenticación."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
    
    def register(self, username, email, password, first_name="", last_name=""):
        """Registrar un nuevo usuario."""
        url = f"{self.base_url}/auth/register/"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
        
        response = requests.post(url, json=data, headers=HEADERS)
        print(f"\n📝 Registro:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            self.access_token = data.get('access')
            self.refresh_token = data.get('refresh')
            self.user_id = data.get('user', {}).get('id')
            print(f"✅ Usuario registrado exitosamente")
            print(f"Username: {data.get('user', {}).get('username')}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def login(self, username, password):
        """Login y obtener tokens."""
        url = f"{self.base_url}/auth/login/"
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, json=data, headers=HEADERS)
        print(f"\n🔐 Login:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access')
            self.refresh_token = data.get('refresh')
            print(f"✅ Login exitoso")
            print(f"Token: {self.access_token[:50]}...")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def create_task(self, title, description="", priority="medium", status="pending", due_date=None):
        """Crear una nueva tarea."""
        url = f"{self.base_url}/tasks/"
        data = {
            "title": title,
            "description": description,
            "priority": priority,
            "status": status,
        }
        
        if due_date:
            data["due_date"] = due_date
        
        response = requests.post(url, json=data, headers=self.set_auth_headers())
        print(f"\n✏️ Crear tarea:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            task = response.json()
            print(f"✅ Tarea creada: {task.get('title')}")
            print(f"ID: {task.get('id')}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def get_tasks(self):
        """Obtener todas las tareas del usuario."""
        url = f"{self.base_url}/tasks/"
        response = requests.get(url, headers=self.set_auth_headers())
        
        print(f"\n📋 Listar tareas:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            tasks = response.json()
            if isinstance(tasks, dict) and 'results' in tasks:
                tasks = tasks['results']
            print(f"✅ Se encontraron {len(tasks)} tareas")
            for task in tasks:
                print(f"  - [{task.get('id')}] {task.get('title')} (Status: {task.get('status')})")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def get_task_detail(self, task_id):
        """Obtener detalles de una tarea específica."""
        url = f"{self.base_url}/tasks/{task_id}/"
        response = requests.get(url, headers=self.set_auth_headers())
        
        print(f"\n🔍 Detalle de tarea #{task_id}:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            task = response.json()
            print(f"✅ Tarea encontrada")
            print(f"Título: {task.get('title')}")
            print(f"Descripción: {task.get('description')}")
            print(f"Estado: {task.get('status')}")
            print(f"Prioridad: {task.get('priority')}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def update_task(self, task_id, title=None, description=None, status=None, priority=None):
        """Actualizar una tarea."""
        url = f"{self.base_url}/tasks/{task_id}/"
        data = {}
        
        if title:
            data['title'] = title
        if description is not None:
            data['description'] = description
        if status:
            data['status'] = status
        if priority:
            data['priority'] = priority
        
        response = requests.patch(url, json=data, headers=self.set_auth_headers())
        print(f"\n✏️ Actualizar tarea #{task_id}:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            task = response.json()
            print(f"✅ Tarea actualizada")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def mark_completed(self, task_id):
        """Marcar una tarea como completada."""
        url = f"{self.base_url}/tasks/{task_id}/mark_completed/"
        response = requests.patch(url, headers=self.set_auth_headers())
        
        print(f"\n✔️ Marcar tarea #{task_id} como completada:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            task = response.json()
            print(f"✅ Tarea marcada como {task.get('status')}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def delete_task(self, task_id):
        """Eliminar una tarea."""
        url = f"{self.base_url}/tasks/{task_id}/"
        response = requests.delete(url, headers=self.set_auth_headers())
        
        print(f"\n🗑️ Eliminar tarea #{task_id}:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 204:
            print(f"✅ Tarea eliminada")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def filter_by_status(self, status):
        """Filtrar tareas por estado."""
        url = f"{self.base_url}/tasks/by_status/?status={status}"
        response = requests.get(url, headers=self.set_auth_headers())
        
        print(f"\n🔍 Tareas filtradas por estado '{status}':")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Se encontraron {len(tasks)} tareas")
            for task in tasks:
                print(f"  - [{task.get('id')}] {task.get('title')}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def filter_by_priority(self, priority):
        """Filtrar tareas por prioridad."""
        url = f"{self.base_url}/tasks/by_priority/?priority={priority}"
        response = requests.get(url, headers=self.set_auth_headers())
        
        print(f"\n🔍 Tareas filtradas por prioridad '{priority}':")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Se encontraron {len(tasks)} tareas")
            for task in tasks:
                print(f"  - [{task.get('id')}] {task.get('title')}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response
    
    def get_user_info(self):
        """Obtener información del usuario autenticado."""
        url = f"{self.base_url}/users/me/"
        response = requests.get(url, headers=self.set_auth_headers())
        
        print(f"\n👤 Información del usuario:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Usuario: {user.get('username')}")
            print(f"Email: {user.get('email')}")
            print(f"Nombre: {user.get('first_name')} {user.get('last_name')}")
            print(f"Tareas: {len(user.get('tasks', []))}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response


def run_demo():
    """Ejecutar una demostración de la API."""
    print("=" * 60)
    print("DEMOSTRACIÓN DE API - SISTEMA DE GESTIÓN DE TAREAS")
    print("=" * 60)
    
    # Crear cliente
    client = TaskAPIClient()
    
    # 1. Registrar usuario
    print("\n1️⃣ REGISTRANDO NUEVO USUARIO")
    print("-" * 60)
    client.register(
        username="usuario_demo",
        email="usuario@example.com",
        password="password123",
        first_name="Usuario",
        last_name="Demo"
    )
    
    # 2. Obtener información del usuario
    print("\n2️⃣ INFORMACIÓN DEL USUARIO")
    print("-" * 60)
    client.get_user_info()
    
    # 3. Crear tareas
    print("\n3️⃣ CREANDO TAREAS")
    print("-" * 60)
    client.create_task(
        title="Implementar autenticación JWT",
        description="Agregar autenticación JWT al proyecto",
        priority="high",
        status="in_progress"
    )
    client.create_task(
        title="Crear endpoints de tareas",
        description="Desarrollar CRUD de tareas",
        priority="high",
        status="in_progress"
    )
    client.create_task(
        title="Escribir documentación",
        description="Documentar la API",
        priority="medium",
        status="pending"
    )
    client.create_task(
        title="Testing de la API",
        description="Realizar pruebas de la API",
        priority="medium",
        status="pending"
    )
    
    # 4. Listar todas las tareas
    print("\n4️⃣ LISTANDO TODAS LAS TAREAS")
    print("-" * 60)
    client.get_tasks()
    
    # 5. Filtrar por estado
    print("\n5️⃣ FILTRANDO TAREAS POR ESTADO")
    print("-" * 60)
    client.filter_by_status("pending")
    
    # 6. Filtrar por prioridad
    print("\n6️⃣ FILTRANDO TAREAS POR PRIORIDAD")
    print("-" * 60)
    client.filter_by_priority("high")
    
    # 7. Obtener detalle de una tarea
    print("\n7️⃣ DETALLE DE UNA TAREA")
    print("-" * 60)
    client.get_task_detail(1)
    
    # 8. Actualizar una tarea
    print("\n8️⃣ ACTUALIZANDO UNA TAREA")
    print("-" * 60)
    client.update_task(
        task_id=1,
        status="completed",
        description="Autenticación JWT completada"
    )
    
    # 9. Marcar tarea como completada
    print("\n9️⃣ MARCAR TAREA COMO COMPLETADA")
    print("-" * 60)
    client.mark_completed(2)
    
    # 10. Listar tareas nuevamente
    print("\n🔟 LISTANDO TAREAS DESPUÉS DE CAMBIOS")
    print("-" * 60)
    client.get_tasks()
    
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    print("\n⚠️ Asegúrate de que el servidor está corriendo: python manage.py runserver\n")
    input("Presiona Enter para continuar...")
    run_demo()
