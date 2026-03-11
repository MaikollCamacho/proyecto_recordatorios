from django.contrib import admin
from .models import Recordatorio

# Registra el modelo para verlo en el panel admin
@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'prioridad')  # Columnas que se ven
    list_filter = ('prioridad', 'fecha')              # Filtros laterales
    search_fields = ('titulo', 'descripcion')         # Buscador