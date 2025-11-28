from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Task
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
    TaskListSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    Vista para registrar nuevos usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Registrar usuario y retornar tokens JWT.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Obtener tokens con información adicional del usuario.
        """
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            user = User.objects.get(username=request.data.get('username'))
            response.data['user'] = UserSerializer(user).data
        
        return response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para obtener información de usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Obtener información del usuario autenticado.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        Logout del usuario (invalidar refresh token si es necesario).
        """
        return Response(
            {'message': 'Logout exitoso'},
            status=status.HTTP_200_OK
        )


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar tareas.
    Permite crear, listar, actualizar y eliminar tareas.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Retornar solo las tareas del usuario autenticado.
        """
        return Task.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """
        Usar diferentes serializadores según la acción.
        """
        if self.action == 'list':
            return TaskListSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        """
        Asignar el usuario actual a la tarea creada.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_status(self, request):
        """
        Filtrar tareas por estado.
        Query param: ?status=pending
        """
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = self.get_queryset().filter(status=status_filter)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Status parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_priority(self, request):
        """
        Filtrar tareas por prioridad.
        Query param: ?priority=high
        """
        priority_filter = request.query_params.get('priority')
        if priority_filter:
            queryset = self.get_queryset().filter(priority=priority_filter)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Priority parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def mark_completed(self, request, pk=None):
        """
        Marcar una tarea como completada.
        """
        task = self.get_object()
        task.status = 'completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
