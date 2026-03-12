<<<<<<< HEAD
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Aquí le decimos a Django que mande el tráfico a las rutas de tu aplicación
    path('', include('recordatorios.urls')), 
]
=======
"""
URL configuration for proyecto_recordatorios project.
"""

from django.contrib import admin
from django.urls import path, include  # ✅ Agregamos include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recordatorios.urls')),  # ✅ Incluye todas las URLs de la app
]
>>>>>>> 8a43f58e1a5f1830e569e9e2839cc476a79d1c85
