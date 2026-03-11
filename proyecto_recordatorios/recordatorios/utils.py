# utils.py
# ESP: Módulo de utilidades matemáticas y lógicas para CRONOX
# ENG: Mathematical and logical utilities module for CRONOX

from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, List
import math


# =============================================================================
# G1: PROCESOS MATEMÁTICOS Y LÓGICOS / MATHEMATICAL AND LOGICAL PROCESSES
# =============================================================================

def calcular_tiempo_restante(fecha_objetivo: datetime) -> Tuple[int, int, int, int]:
    """
    ESP: Calcula el tiempo restante hasta una fecha objetivo.
    ENG: Calculates remaining time until a target date.
    """
    try:
        ahora = datetime.now()
        diferencia = fecha_objetivo - ahora
        
        if diferencia.total_seconds() < 0:
            return (0, 0, 0, 0)
        
        dias = diferencia.days
        segundos_totales = diferencia.seconds
        horas = segundos_totales // 3600
        minutos = (segundos_totales % 3600) // 60
        segundos = segundos_totales % 60
        
        return (dias, horas, minutos, segundos)
    
    except Exception as e:
        print(f"[ERROR] calcular_tiempo_restante: {str(e)}")
        return (0, 0, 0, 0)


def calcular_urgencia(dias_restantes: int, prioridad: str) -> float:
    """
    ESP: Calcula índice de urgencia basado en tiempo y prioridad.
    ENG: Calculates urgency index based on time and priority.
    """
    try:
        pesos = {'Alta': 3.0, 'Media': 2.0, 'Baja': 1.0}
        peso_prioridad = pesos.get(prioridad, 1.0)
        
        if dias_restantes <= 0:
            urgencia_base = 100.0
        else:
            urgencia_base = 100.0 * math.exp(-dias_restantes / 7.0)
        
        indice_urgencia = min(urgencia_base * peso_prioridad, 100.0)
        return round(indice_urgencia, 2)
    
    except Exception as e:
        print(f"[ERROR] calcular_urgencia: {str(e)}")
        return 0.0


def calcular_porcentaje_progreso(fecha_creacion: datetime, fecha_objetivo: datetime) -> float:
    """
    ESP: Calcula el porcentaje de progreso hacia una fecha objetivo.
    ENG: Calculates progress percentage towards a target date.
    """
    try:
        ahora = datetime.now()
        duracion_total = (fecha_objetivo - fecha_creacion).total_seconds()
        tiempo_transcurrido = (ahora - fecha_creacion).total_seconds()
        
        if duracion_total <= 0:
            return 100.0 if ahora >= fecha_objetivo else 0.0
        
        porcentaje = (tiempo_transcurrido / duracion_total) * 100
        return round(max(0.0, min(100.0, porcentaje)), 2)
    
    except Exception as e:
        print(f"[ERROR] calcular_porcentaje_progreso: {str(e)}")
        return 0.0


# =============================================================================
# G2: VALIDACIÓN DE DATOS / DATA VALIDATION
# =============================================================================

def validar_fecha(fecha_str: str, formato: str = '%Y-%m-%dT%H:%M') -> Tuple[bool, Optional[datetime], str]:
    """
    ESP: Valida y convierte una cadena de fecha.
    ENG: Validates and converts a date string.
    """
    try:
        if not fecha_str:
            return (False, None, "La fecha no puede estar vacía / Date cannot be empty")
        
        fecha = datetime.strptime(fecha_str, formato)
        
        if fecha < datetime.now():
            return (False, None, "El destino no puede estar en el pasado / Destiny cannot be in the past")
        
        if fecha > datetime.now() + timedelta(days=3650):
            return (False, None, "El destino está demasiado lejos / Destiny is too far")
        
        return (True, fecha, "Fecha válida / Valid date")
    
    except ValueError:
        return (False, None, f"Formato inválido / Invalid format: {formato}")
    
    except Exception as e:
        return (False, None, f"Error: {str(e)}")


def validar_prioridad(prioridad: str) -> Tuple[bool, str]:
    """
    ESP: Valida que la prioridad sea una de las opciones permitidas.
    ENG: Validates that priority is one of the allowed options.
    """
    try:
        prioridades_validas = ['Alta', 'Media', 'Baja']
        
        if prioridad not in prioridades_validas:
            return (False, f"Prioridad inválida. Use / Invalid priority. Use: {prioridades_validas}")
        
        return (True, "Prioridad válida / Valid priority")
    
    except Exception as e:
        return (False, f"Error: {str(e)}")


# =============================================================================
# G4: PASO DE PARÁMETROS / PARAMETER PASSING
# =============================================================================

def procesar_recordatorio(datos: Dict) -> Dict:
    """
    ESP: Procesa un recordatorio aplicando todas las validaciones y cálculos.
    ENG: Processes a reminder applying all validations and calculations.
    
    Args:
        datos (Dict): Diccionario con titulo, descripcion, fecha, prioridad
    
    Returns:
        Dict: Resultado procesado con métricas calculadas
    """
    try:
        # ESP: Validar fecha / ENG: Validate date
        es_fecha_valida, fecha_obj, msg_fecha = validar_fecha(datos.get('fecha', ''))
        
        if not es_fecha_valida:
            return {'exito': False, 'error': msg_fecha}
        
        # ESP: Validar prioridad / ENG: Validate priority
        es_prio_valida, msg_prio = validar_prioridad(datos.get('prioridad', ''))
        
        if not es_prio_valida:
            return {'exito': False, 'error': msg_prio}
        
        # ESP: Calcular métricas / ENG: Calculate metrics
        dias, horas, minutos, segundos = calcular_tiempo_restante(fecha_obj)
        urgencia = calcular_urgencia(dias, datos['prioridad'])
        
        # ESP: Retornar resultado procesado / ENG: Return processed result
        return {
            'exito': True,
            'titulo': datos['titulo'],
            'descripcion': datos['descripcion'],
            'fecha': fecha_obj,
            'prioridad': datos['prioridad'],
            'tiempo_restante': {
                'dias': dias,
                'horas': horas,
                'minutos': minutos,
                'segundos': segundos
            },
            'urgencia': urgencia,
            'mensaje': 'Destino procesado correctamente / Destiny processed successfully'
        }
    
    except Exception as e:
        return {'exito': False, 'error': f"Error de procesamiento / Processing error: {str(e)}"}


def analizar_recordatorios(recordatorios: List) -> Dict:
    """
    ESP: Analiza una lista de recordatorios y genera estadísticas.
    ENG: Analyzes a list of reminders and generates statistics.
    """
    try:
        if not recordatorios:
            return {
                'total': 0,
                'por_prioridad': {'Alta': 0, 'Media': 0, 'Baja': 0},
                'urgencia_promedio': 0.0,
                'mensaje': 'No hay destinos forjados / No destinies forged'
            }
        
        # ESP: Contar por prioridad / ENG: Count by priority
        por_prioridad = {'Alta': 0, 'Media': 0, 'Baja': 0}
        urgencias = []
        
        for rec in recordatorios:
            prio = getattr(rec, 'prioridad', 'Baja')
            por_prioridad[prio] = por_prioridad.get(prio, 0) + 1
            
            # ESP: Calcular urgencia si tiene fecha / ENG: Calculate urgency if it has date
            fecha = getattr(rec, 'fecha', None)
            if fecha:
                dias, _, _, _ = calcular_tiempo_restante(fecha)
                urg = calcular_urgencia(dias, prio)
                urgencias.append(urg)
        
        urgencia_promedio = sum(urgencias) / len(urgencias) if urgencias else 0.0
        
        return {
            'total': len(recordatorios),
            'por_prioridad': por_prioridad,
            'urgencia_promedio': round(urgencia_promedio, 2),
            'mensaje': 'Análisis completado / Analysis completed'
        }
    
    except Exception as e:
        return {'error': f"Error en análisis / Analysis error: {str(e)}"}