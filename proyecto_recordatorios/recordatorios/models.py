from django.db import models

class Recordatorio(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    prioridad = models.CharField(max_length=20)

    def __str__(self):
        return self.titulo