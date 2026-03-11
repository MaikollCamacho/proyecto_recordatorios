from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('crear/', views.crear_recordatorio, name='crear'),
    path('editar/<int:id>/', views.editar_recordatorio, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_recordatorio, name='eliminar'),
]