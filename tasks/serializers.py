from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo User.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """
        Crear un nuevo usuario con contraseña encriptada.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializador detallado del usuario con sus tareas.
    """
    tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tasks']
        read_only_fields = ['id']
    
    def get_tasks(self, obj):
        """Obtener las tareas del usuario."""
        tasks = obj.tasks.all()
        return TaskSerializer(tasks, many=True).data


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Task.
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'status', 'priority', 
                  'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Crear una nueva tarea asignando el usuario actual.
        """
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para actualizar tareas.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']


class TaskListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listar tareas.
    """
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority', 'due_date', 'created_at']
