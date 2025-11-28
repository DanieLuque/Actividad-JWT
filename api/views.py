from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from tasks.models import Task
from .serializers import UserSimpleSerializer, TaskSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver usuarios.
    Permite ver información de usuarios autenticados.
    """
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener información del usuario autenticado."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar tareas.
    Permite CRUD completo de tareas del usuario autenticado.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna solo las tareas del usuario autenticado."""
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Asigna el usuario autenticado como propietario de la tarea."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_status(self, request):
        """Filtrar tareas por estado."""
        status_filter = request.query_params.get('status')
        if not status_filter:
            return Response(
                {'error': 'status parameter required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tasks = self.get_queryset().filter(status=status_filter)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_priority(self, request):
        """Filtrar tareas por prioridad."""
        priority_filter = request.query_params.get('priority')
        if not priority_filter:
            return Response(
                {'error': 'priority parameter required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tasks = self.get_queryset().filter(priority=priority_filter)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def mark_completed(self, request, pk=None):
        """Marcar una tarea como completada."""
        task = self.get_object()
        task.status = 'completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
