from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet

# Crear router para los viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api-user')
router.register(r'tasks', TaskViewSet, basename='api-task')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
