"""
URL configuration for proyecto_recordatorios project.
"""

from django.contrib import admin
from django.urls import path, include  # ✅ Agregamos include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recordatorios.urls')),  # ✅ Incluye todas las URLs de la app
]