<<<<<<< HEAD
# views.py
# ESP: Vistas del sistema CRONOX - Señor del Tiempo
# ENG: Views for CRONOX system - Lord of Time

from django.shortcuts import render, redirect, get_object_or_404
from .models import Recordatorio

# G4: IMPORTACIÓN MODULAR / MODULAR IMPORT
# ESP: Importamos funciones utilitarias desde módulo externo
# ENG: We import utility functions from external module
from .utils import (
    calcular_tiempo_restante,
    calcular_urgencia,
    calcular_porcentaje_progreso,
    validar_fecha,
    validar_prioridad,
    procesar_recordatorio,
    analizar_recordatorios
)


# =============================================================================
# G3/G4: FUNCIONES VISTA CON DELEGACIÓN A MÓDULOS
# VIEW FUNCTIONS WITH MODULE DELEGATION
# =============================================================================

def inicio(request):
    """
    ESP: Vista principal - Muestra todos los destinos forjados con métricas calculadas.
    ENG: Main view - Shows all forged destinies with calculated metrics.
    """
    try:
        # ESP: Obtener todos los recordatorios ordenados por fecha / ENG: Get all reminders ordered by date
        recordatorios = Recordatorio.objects.all().order_by('fecha')
        
        # G4: PASO DE PARÁMETROS A FUNCIÓN EXTERNA / PASSING PARAMETERS TO EXTERNAL FUNCTION
        # ESP: Analizar recordatorios para estadísticas / ENG: Analyze reminders for statistics
        estadisticas = analizar_recordatorios(recordatorios)
        
        # ESP: Enriquecer cada recordatorio con cálculos matemáticos / ENG: Enrich each reminder with mathematical calculations
        recordatorios_enriquecidos = []
        
        for rec in recordatorios:
            # G1: CÁLCULOS MATEMÁTICOS / MATHEMATICAL CALCULATIONS
            dias, horas, minutos, segundos = calcular_tiempo_restante(rec.fecha)
            urgencia = calcular_urgencia(dias, rec.prioridad)
            
            # ESP: Crear objeto enriquecido / ENG: Create enriched object
            rec_enriquecido = {
                'id': rec.id,
                'titulo': rec.titulo,
                'descripcion': rec.descripcion,
                'fecha': rec.fecha,
                'prioridad': rec.prioridad,
                'tiempo_restante': {
                    'dias': dias,
                    'horas': horas,
                    'minutos': minutos,
                    'segundos': segundos
                },
                'urgencia': urgencia,
                'esta_vencido': dias == 0 and horas == 0 and minutos == 0
            }
            recordatorios_enriquecidos.append(rec_enriquecido)
        
        # ESP: Contexto para la plantilla / ENG: Context for template
        contexto = {
            'recordatorios': recordatorios_enriquecidos,
            'estadisticas': estadisticas,
            'titulo': 'CRONOX | Señor del Tiempo'
        }
        
        return render(request, 'recordatorios/inicio.html', contexto)
    
    except Exception as e:
        # G2: VALIDACIÓN - MANEJO DE ERRORES SIN CERRAR / VALIDATION - ERROR HANDLING WITHOUT CRASHING
        print(f"[ERROR] inicio: {str(e)}")
        return render(request, 'recordatorios/inicio.html', {
            'recordatorios': [],
            'error': 'Error al cargar los destinos / Error loading destinies'
        })


def crear_recordatorio(request):
    """
    ESP: Vista para forjar nuevos destinos - incluye validación completa.
    ENG: View for forging new destinies - includes complete validation.
    """
    # ESP: Inicializar contexto con datos vacíos / ENG: Initialize context with empty data
    contexto = {
        'datos': {},
        'error': None,
        'exito': None
    }
    
    if request.method == 'POST':
        # ESP: Recopilar datos del formulario / ENG: Collect form data
        datos_formulario = {
            'titulo': request.POST.get('titulo', '').strip(),
            'descripcion': request.POST.get('descripcion', '').strip(),
            'fecha': request.POST.get('fecha', ''),
            'prioridad': request.POST.get('prioridad', '')
        }
        
        contexto['datos'] = datos_formulario
        
        # G2: VALIDACIÓN DE DATOS / DATA VALIDATION
        # ESP: Validar que los campos no estén vacíos / ENG: Validate that fields are not empty
        if not datos_formulario['titulo']:
            contexto['error'] = 'El nombre del destino es obligatorio / Destiny name is required'
            return render(request, 'recordatorios/crear.html', contexto)
        
        if not datos_formulario['descripcion']:
            contexto['error'] = 'La profecía es obligatoria / Prophecy is required'
            return render(request, 'recordatorios/crear.html', contexto)
        
        # G4: DELEGACIÓN A FUNCIÓN CON PASO DE PARÁMETROS / DELEGATION TO FUNCTION WITH PARAMETER PASSING
        # ESP: Procesar con validaciones y cálculos del módulo utils / ENG: Process with validations and calculations from utils module
        resultado = procesar_recordatorio(datos_formulario)
        
        if not resultado['exito']:
            # ESP: Mostrar error específico sin cerrar el sistema / ENG: Show specific error without crashing the system
            contexto['error'] = resultado['error']
            return render(request, 'recordatorios/crear.html', contexto)
        
        # G1: LÓGICA DE NEGOCIO / BUSINESS LOGIC
        # ESP: Crear el recordatorio en base de datos / ENG: Create reminder in database
        try:
            Recordatorio.objects.create(
                titulo=resultado['titulo'],
                descripcion=resultado['descripcion'],
                fecha=resultado['fecha'],
                prioridad=resultado['prioridad']
            )
            
            contexto['exito'] = '¡Destino forjado con éxito! / Destiny forged successfully!'
            return redirect('inicio')
            
        except Exception as e:
            contexto['error'] = f'Error al sellar el destino / Error sealing destiny: {str(e)}'
            return render(request, 'recordatorios/crear.html', contexto)
    
    # ESP: GET - Mostrar formulario vacío / ENG: GET - Show empty form
    return render(request, 'recordatorios/crear.html', contexto)


def editar_recordatorio(request, id):
    """
    ESP: Vista para alterar destinos existentes - reescribir el tiempo.
    ENG: View for altering existing destinies - rewriting time.
    
    Args:
        id (int): Identificador del destino a alterar / Identifier of destiny to alter
    """
    # G4: PASO DE PARÁMETRO POR VALOR / PASSING PARAMETER BY VALUE
    # ESP: Obtener el recordatorio o mostrar 404 / ENG: Get reminder or show 404
    recordatorio = get_object_or_404(Recordatorio, id=id)
    
    # ESP: Calcular métricas actuales para mostrar cambios / ENG: Calculate current metrics to show changes
    dias_actual, horas_actual, minutos_actual, _ = calcular_tiempo_restante(recordatorio.fecha)
    urgencia_actual = calcular_urgencia(dias_actual, recordatorio.prioridad)
    
    contexto = {
        'recordatorio': recordatorio,
        'metricas_actuales': {
            'dias': dias_actual,
            'horas': horas_actual,
            'minutos': minutos_actual,
            'urgencia': urgencia_actual
        },
        'error': None,
        'exito': None
    }
    
    if request.method == 'POST':
        # ESP: Recopilar nuevos datos / ENG: Collect new data
        datos_nuevos = {
            'titulo': request.POST.get('titulo', '').strip(),
            'descripcion': request.POST.get('descripcion', '').strip(),
            'fecha': request.POST.get('fecha', ''),
            'prioridad': request.POST.get('prioridad', '')
        }
        
        # G2: VALIDACIÓN DE DATOS / DATA VALIDATION
        # ESP: Validar campos obligatorios / ENG: Validate required fields
        if not datos_nuevos['titulo'] or not datos_nuevos['descripcion']:
            contexto['error'] = 'Todos los campos son obligatorios / All fields are required'
            return render(request, 'recordatorios/editar.html', contexto)
        
        # ESP: Validar fecha con función utilitaria / ENG: Validate date with utility function
        es_fecha_valida, fecha_obj, msg_fecha = validar_fecha(datos_nuevos['fecha'])
        
        if not es_fecha_valida:
            contexto['error'] = msg_fecha
            return render(request, 'recordatorios/editar.html', contexto)
        
        # ESP: Validar prioridad / ENG: Validate priority
        es_prio_valida, msg_prio = validar_prioridad(datos_nuevos['prioridad'])
        
        if not es_prio_valida:
            contexto['error'] = msg_prio
            return render(request, 'recordatorios/editar.html', contexto)
        
        # G1: CÁLCULOS MATEMÁTICOS PARA COMPARACIÓN / MATHEMATICAL CALCULATIONS FOR COMPARISON
        # ESP: Calcular nuevas métricas / ENG: Calculate new metrics
        dias_nuevo, horas_nuevo, minutos_nuevo, _ = calcular_tiempo_restante(fecha_obj)
        urgencia_nueva = calcular_urgencia(dias_nuevo, datos_nuevos['prioridad'])
        
        # ESP: Guardar cambios / ENG: Save changes
        try:
            recordatorio.titulo = datos_nuevos['titulo']
            recordatorio.descripcion = datos_nuevos['descripcion']
            recordatorio.fecha = fecha_obj
            recordatorio.prioridad = datos_nuevos['prioridad']
            recordatorio.save()
            
            contexto['exito'] = '¡Destino alterado con éxito! / Destiny altered successfully!'
            contexto['metricas_nuevas'] = {
                'dias': dias_nuevo,
                'horas': horas_nuevo,
                'minutos': minutos_nuevo,
                'urgencia': urgencia_nueva
            }
            
            return redirect('inicio')
            
        except Exception as e:
            contexto['error'] = f'Error al alterar el destino / Error altering destiny: {str(e)}'
            return render(request, 'recordatorios/editar.html', contexto)
    
    # ESP: GET - Mostrar formulario con datos actuales / ENG: GET - Show form with current data
    return render(request, 'recordatorios/editar.html', contexto)


def eliminar_recordatorio(request, id):
    """
    ESP: Vista para destruir destinos - acción permanente como la muerte.
    ENG: View for destroying destinies - permanent action like death.
    
    Args:
        id (int): Identificador del destino a destruir / Identifier of destiny to destroy
    """
    # G4: PASO DE PARÁMETRO / PARAMETER PASSING
    recordatorio = get_object_or_404(Recordatorio, id=id)
    
    # ESP: Calcular métricas finales antes de destruir / ENG: Calculate final metrics before destroying
    dias, horas, minutos, _ = calcular_tiempo_restante(recordatorio.fecha)
    urgencia = calcular_urgencia(dias, recordatorio.prioridad)
    
    contexto = {
        'recordatorio': recordatorio,
        'metricas_finales': {
            'dias': dias,
            'horas': horas,
            'minutos': minutos,
            'urgencia': urgencia,
            'tiempo_restante_str': f'{dias}d {horas}h {minutos}m' if dias > 0 else f'{horas}h {minutos}m'
        },
        'error': None
    }
    
    if request.method == 'POST':
        # ESP: Verificar que se confirmó la destrucción / ENG: Verify destruction was confirmed
        confirmacion = request.POST.get('confirmacion', '')
        
        if confirmacion != 'DESTRUIR':
            contexto['error'] = 'Debe escribir DESTRUIR para confirmar / You must type DESTRUIR to confirm'
            return render(request, 'recordatorios/eliminar.html', contexto)
        
        # G1/G2: LÓGICA DE NEGOCIO CON VALIDACIÓN / BUSINESS LOGIC WITH VALIDATION
        try:
            # ESP: Destruir el destino permanentemente / ENG: Destroy destiny permanently
            titulo_destruido = recordatorio.titulo  # ESP: Guardar para mensaje / ENG: Save for message
            recordatorio.delete()
            
            # ESP: Redirigir con mensaje de éxito / ENG: Redirect with success message
            return redirect('inicio')
            
        except Exception as e:
            # G2: MANEJO DE ERRORES SIN CERRAR / ERROR HANDLING WITHOUT CRASHING
            contexto['error'] = f'Error al destruir el destino / Error destroying destiny: {str(e)}'
            return render(request, 'recordatorios/eliminar.html', contexto)
    
    # ESP: GET - Mostrar pantalla de confirmación / ENG: GET - Show confirmation screen
    return render(request, 'recordatorios/eliminar.html', contexto)
=======
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
>>>>>>> 8a43f58e1a5f1830e569e9e2839cc476a79d1c85
