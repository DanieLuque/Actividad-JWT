from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Administrador para el modelo Task.
    """
    list_display = ('title', 'user', 'status', 'priority', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información de la Tarea', {
            'fields': ('user', 'title', 'description')
        }),
        ('Estado y Prioridad', {
            'fields': ('status', 'priority')
        }),
        ('Fechas', {
            'fields': ('due_date', 'created_at', 'updated_at')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """
        Hacer readonly los campos de fecha de creación y actualización.
        """
        if obj:
            return self.readonly_fields
        return []
