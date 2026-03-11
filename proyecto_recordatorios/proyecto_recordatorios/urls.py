from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Aquí le decimos a Django que mande el tráfico a las rutas de tu aplicación
    path('', include('recordatorios.urls')), 
]
