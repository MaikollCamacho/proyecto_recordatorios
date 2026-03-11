from django.shortcuts import render, redirect, get_object_or_404
from .models import Recordatorio

def inicio(request):
    recordatorios = Recordatorio.objects.all().order_by('fecha')
    return render(request, 'recordatorios/inicio.html', {
        'recordatorios': recordatorios,
        'titulo': 'Mis Recordatorios'
    })

def crear_recordatorio(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        prioridad = request.POST.get('prioridad')
        
        Recordatorio.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha=fecha,
            prioridad=prioridad
        )
        return redirect('inicio')
    
    return render(request, 'recordatorios/crear.html')

def editar_recordatorio(request, id):
    recordatorio = get_object_or_404(Recordatorio, id=id)
    
    if request.method == 'POST':
        recordatorio.titulo = request.POST.get('titulo')
        recordatorio.descripcion = request.POST.get('descripcion')
        recordatorio.fecha = request.POST.get('fecha')
        recordatorio.prioridad = request.POST.get('prioridad')
        recordatorio.save()
        return redirect('inicio')
    
    return render(request, 'recordatorios/editar.html', {
        'recordatorio': recordatorio
    })

def eliminar_recordatorio(request, id):
    recordatorio = get_object_or_404(Recordatorio, id=id)
    
    if request.method == 'POST':
        recordatorio.delete()
        return redirect('inicio')
    
    return render(request, 'recordatorios/eliminar.html', {
        'recordatorio': recordatorio
    })