from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    UserViewSet,
    TaskViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView

# Crear router para los viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')

app_name = 'tasks'

urlpatterns = [
    # Rutas del router
    path('', include(router.urls)),
    
    # Rutas de autenticación
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
