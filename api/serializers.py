from rest_framework import serializers
from django.contrib.auth.models import User
from tasks.models import Task


class UserSimpleSerializer(serializers.ModelSerializer):
    """Serializador simple de usuario."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    """Serializador de tareas con usuario."""
    user = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'status', 'priority', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
