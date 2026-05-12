"""
logic_agent.py - Capa de lógica de negocio
Responsabilidades:
- Validar datos de entrada
- Calcular distancias y consumo de batería
- Validar viabilidad de rutas
- Optimizar orden de entregas
"""

import math
import re
from datetime import datetime


# ==================== EXCEPCIONES PERSONALIZADAS ====================

class ValidationError(Exception):
    """Error de validación de datos"""
    pass


class CalculationError(Exception):
    """Error en cálculos"""
    pass


# ==================== VALIDADORES ====================

class VehicleValidator:
    """Valida datos de vehículos"""
    
    @staticmethod
    def validate_id(id_vehiculo):
        """Valida que el ID siga el formato VAN-NNN"""
        pattern = r'^[A-Z]{3}-\d{3}$'
        if not re.match(pattern, id_vehiculo):
            raise ValidationError(f"ID inválido: {id_vehiculo}. Formato: VAN-NNN")
        return True
    
    @staticmethod
    def validate_modelo(modelo):
        """Valida que el modelo tenga al menos 2 caracteres"""
        if not modelo or len(modelo) < 2:
            raise ValidationError("El modelo debe tener al menos 2 caracteres")
        return True
    
    @staticmethod
    def validate_bateria(capacidad_total, nivel_actual):
        """Valida que la batería sea válida"""
        if capacidad_total <= 0:
            raise ValidationError("La capacidad de batería debe ser > 0")
        if nivel_actual < 0 or nivel_actual > 100:
            raise ValidationError("El nivel de batería debe estar entre 0 y 100")
        return True
    
    @staticmethod
    def validate_autonomia(autonomia_km):
        """Valida autonomía máxima"""
        if autonomia_km <= 0:
            raise ValidationError("La autonomía debe ser > 0 km")
        return True
    
    @staticmethod
    def validate_estado(estado):
        """Valida que el estado sea válido"""
        estados_validos = ['disponible', 'en ruta', 'cargando', 'mantenimiento']
        if estado.lower() not in estados_validos:
            raise ValidationError(f"Estado inválido. Válidos: {', '.join(estados_validos)}")
        return True


class DeliveryValidator:
    """Valida datos de entregas"""
    
    @staticmethod
    def validate_id(id_entrega):
        """Valida que el ID de entrega sea válido"""
        pattern = r'^ENT-\d{4}$'
        if not re.match(pattern, id_entrega):
            raise ValidationError(f"ID entrega inválido: {id_entrega}. Formato: ENT-NNNN")
        return True
    
    @staticmethod
    def validate_coordenadas(lat, lon):
        """Valida coordenadas GPS"""
        if lat < -90 or lat > 90:
            raise ValidationError(f"Latitud inválida: {lat}. Debe estar entre -90 y 90")
        if lon < -180 or lon > 180:
            raise ValidationError(f"Longitud inválida: {lon}. Debe estar entre -180 y 180")
        return True
    
    @staticmethod
    def validate_peso(peso_kg):
        """Valida peso (máx 100 kg)"""
        if peso_kg <= 0 or peso_kg > 100:
            raise ValidationError(f"Peso inválido: {peso_kg}. Debe estar entre 0 y 100 kg")
        return True
    
    @staticmethod
    def validate_prioridad(prioridad):
        """Valida prioridad (1-3)"""
        if prioridad not in [1, 2, 3]:
            raise ValidationError(f"Prioridad inválida: {prioridad}. Debe ser 1, 2 o 3")
        return True
    
    @staticmethod
    def validate_ventana_horaria(ventana):
        """Valida formato HH:MM - HH:MM"""
        pattern = r'^\d{2}:\d{2}\s*-\s*\d{2}:\d{2}$'
        if not re.match(pattern, ventana):
            raise ValidationError(f"Ventana horaria inválida: {ventana}. Formato: HH:MM - HH:MM")
        return True


# ==================== CALCULADORES ====================

class RouteCalculator:
    """Calcula distancias y consumo de batería"""
    
    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Calcula distancia Haversine entre dos puntos GPS
        Retorna distancia en km
        """
        R = 6371  # Radio de la Tierra en km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    @staticmethod
    def calculate_battery_consumption(distancia_km, peso_kg_total, autonomia_maxima_km):
        """
        Calcula consumo estimado de batería
        - Consumo base: (distancia / autonomía) * 100
        - Factor peso: peso_kg * 0.05 (cada kg adicional = 0.05% extra)
        """
        if autonomia_maxima_km <= 0:
            raise CalculationError("Autonomía inválida")
        
        consumo_base = (distancia_km / autonomia_maxima_km) * 100
        consumo_peso = peso_kg_total * 0.05
        
        consumo_total = consumo_base + consumo_peso
        
        # No puede exceder 100%
        return min(consumo_total, 100.0)
    
    @staticmethod
    def calculate_total_distance(coordenadas_list):
        """
        Calcula distancia total entre puntos
        coordenadas_list: [(lat1, lon1), (lat2, lon2), ...]
        """
        if len(coordenadas_list) < 2:
            return 0.0
        
        distancia_total = 0.0
        for i in range(len(coordenadas_list) - 1):
            lat1, lon1 = coordenadas_list[i]
            lat2, lon2 = coordenadas_list[i + 1]
            distancia_total += RouteCalculator.haversine_distance(lat1, lon1, lat2, lon2)
        
        return distancia_total
    
    @staticmethod
    def calculate_total_weight(entregas):
        """Suma el peso total de entregas"""
        return sum(entrega.get('peso_kg', 0) for entrega in entregas)


# ==================== VALIDADORES DE RUTAS ====================

class RouteValidator:
    """Valida viabilidad de rutas"""
    
    @staticmethod
    def validate_battery_capacity(bateria_actual, consumo_estimado, capacidad_total):
        """
        Valida que la batería sea suficiente
        - Consumo no puede ser > 80% de la batería actual
        """
        if bateria_actual < consumo_estimado:
            raise ValidationError(
                f"Batería insuficiente: necesita {consumo_estimado}%, dispone de {bateria_actual}%"
            )
        
        if consumo_estimado > 80:
            raise ValidationError(
                f"Consumo muy alto ({consumo_estimado}%). "
                "Se recomienda recargar antes de realizar la ruta."
            )
        
        return True
    
    @staticmethod
    def validate_weight_capacity(peso_total_entregas, capacidad_carga):
        """Valida que el peso no exceda la capacidad de carga"""
        if peso_total_entregas > capacidad_carga:
            raise ValidationError(
                f"Peso total ({peso_total_entregas} kg) excede capacidad ({capacidad_carga} kg)"
            )
        return True
    
    @staticmethod
    def validate_no_duplicate_deliveries(lista_entregas):
        """Valida que no haya entregas duplicadas"""
        if len(lista_entregas) != len(set(lista_entregas)):
            raise ValidationError("No se pueden añadir entregas duplicadas a la ruta")
        return True


# ==================== OPTIMIZADORES ====================

class RouteOptimizer:
    """Optimiza el orden de entregas en rutas"""
    
    @staticmethod
    def sort_by_priority(entregas):
        """Ordena entregas por prioridad (1 = más urgente)"""
        return sorted(entregas, key=lambda x: x['prioridad'])
    
    @staticmethod
    def sort_by_window_time(entregas):
        """Ordena entregas por ventana horaria"""
        def parse_time(ventana_str):
            # Extrae HH:MM del inicio de la ventana (ej: "09:00 - 11:00" -> 09:00)
            tiempo_inicio = ventana_str.split('-')[0].strip()
            return datetime.strptime(tiempo_inicio, '%H:%M').time()
        
        return sorted(entregas, key=lambda x: parse_time(x['ventana_horaria']))
    
    @staticmethod
    def optimize_route(entregas, vehiculo_autonomia):
        """
        Optimiza ruta combinando prioridad y ventana horaria
        Retorna entregas ordenadas
        """
        # Primero por prioridad, luego por ventana horaria
        sorted_by_priority = RouteOptimizer.sort_by_priority(entregas)
        return RouteOptimizer.sort_by_window_time(sorted_by_priority)
