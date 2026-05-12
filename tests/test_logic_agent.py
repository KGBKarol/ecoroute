"""
test_logic_agent.py - Tests unitarios para la lógica de negocio
Ejecutar: python -m pytest tests/
"""

import pytest
from src.logic_agent import (
    ValidationError, CalculationError,
    VehicleValidator, DeliveryValidator,
    RouteCalculator, RouteValidator, RouteOptimizer
)


# ==================== TESTS VEHICLEVALIDATOR ====================

class TestVehicleValidator:
    
    def test_validate_id_valid(self):
        """Valida ID correcto"""
        assert VehicleValidator.validate_id("VAN-001")
        assert VehicleValidator.validate_id("BUS-999")
    
    def test_validate_id_invalid(self):
        """Rechaza ID incorrecto"""
        with pytest.raises(ValidationError):
            VehicleValidator.validate_id("van-001")  # minúscula
        with pytest.raises(ValidationError):
            VehicleValidator.validate_id("VAN001")  # sin guion
    
    def test_validate_modelo_valid(self):
        """Valida modelo válido"""
        assert VehicleValidator.validate_modelo("Tesla Model 3")
    
    def test_validate_modelo_invalid(self):
        """Rechaza modelo vacío"""
        with pytest.raises(ValidationError):
            VehicleValidator.validate_modelo("")
        with pytest.raises(ValidationError):
            VehicleValidator.validate_modelo("V")
    
    def test_validate_bateria_valid(self):
        """Valida batería válida"""
        assert VehicleValidator.validate_bateria(100, 50)
        assert VehicleValidator.validate_bateria(100, 0)
        assert VehicleValidator.validate_bateria(100, 100)
    
    def test_validate_bateria_invalid(self):
        """Rechaza batería inválida"""
        with pytest.raises(ValidationError):
            VehicleValidator.validate_bateria(0, 50)  # capacidad 0
        with pytest.raises(ValidationError):
            VehicleValidator.validate_bateria(100, 150)  # nivel > 100
    
    def test_validate_estado_valid(self):
        """Valida estado válido"""
        assert VehicleValidator.validate_estado("disponible")
        assert VehicleValidator.validate_estado("en ruta")
        assert VehicleValidator.validate_estado("cargando")
    
    def test_validate_estado_invalid(self):
        """Rechaza estado inválido"""
        with pytest.raises(ValidationError):
            VehicleValidator.validate_estado("roto")


# ==================== TESTS DELIVERYVALIDATOR ====================

class TestDeliveryValidator:
    
    def test_validate_coordenadas_valid(self):
        """Valida coordenadas válidas"""
        assert DeliveryValidator.validate_coordenadas(40.0, -3.0)
        assert DeliveryValidator.validate_coordenadas(-90, 180)
    
    def test_validate_coordenadas_invalid(self):
        """Rechaza coordenadas inválidas"""
        with pytest.raises(ValidationError):
            DeliveryValidator.validate_coordenadas(91, 0)  # lat > 90
        with pytest.raises(ValidationError):
            DeliveryValidator.validate_coordenadas(0, 181)  # lon > 180
    
    def test_validate_peso_valid(self):
        """Valida peso válido"""
        assert DeliveryValidator.validate_peso(10.5)
        assert DeliveryValidator.validate_peso(100)
    
    def test_validate_peso_invalid(self):
        """Rechaza peso inválido"""
        with pytest.raises(ValidationError):
            DeliveryValidator.validate_peso(0)
        with pytest.raises(ValidationError):
            DeliveryValidator.validate_peso(101)  # > 100 kg
    
    def test_validate_prioridad_valid(self):
        """Valida prioridad válida"""
        assert DeliveryValidator.validate_prioridad(1)
        assert DeliveryValidator.validate_prioridad(2)
        assert DeliveryValidator.validate_prioridad(3)
    
    def test_validate_prioridad_invalid(self):
        """Rechaza prioridad inválida"""
        with pytest.raises(ValidationError):
            DeliveryValidator.validate_prioridad(0)
        with pytest.raises(ValidationError):
            DeliveryValidator.validate_prioridad(4)
    
    def test_validate_ventana_horaria_valid(self):
        """Valida ventana horaria válida"""
        assert DeliveryValidator.validate_ventana_horaria("09:00 - 11:00")
        assert DeliveryValidator.validate_ventana_horaria("14:30-16:45")
    
    def test_validate_ventana_horaria_invalid(self):
        """Rechaza ventana horaria inválida"""
        with pytest.raises(ValidationError):
            DeliveryValidator.validate_ventana_horaria("9:00 - 11:00")
        with pytest.raises(ValidationError):
            DeliveryValidator.validate_ventana_horaria("09:00-11")


# ==================== TESTS ROUTECALCULATOR ====================

class TestRouteCalculator:
    
    def test_haversine_distance_simple(self):
        """Calcula distancia Haversine correctamente"""
        # Madrid a Barcelona (aprox 600 km)
        dist = RouteCalculator.haversine_distance(40.4168, -3.7038, 41.3851, 2.1734)
        assert 550 < dist < 650  # Rango aproximado
    
    def test_haversine_distance_same_point(self):
        """Distancia entre el mismo punto es 0"""
        dist = RouteCalculator.haversine_distance(40.0, -3.0, 40.0, -3.0)
        assert dist == 0.0
    
    def test_calculate_battery_consumption_basic(self):
        """Calcula consumo de batería"""
        # 100 km, 50 kg, autonomía 500 km
        # Base: (100/500)*100 = 20%
        # Peso: 50*0.05 = 2.5%
        # Total: 22.5%
        consumption = RouteCalculator.calculate_battery_consumption(100, 50, 500)
        assert 20 < consumption < 25
    
    def test_calculate_battery_consumption_max(self):
        """Consumo no puede ser > 100%"""
        consumption = RouteCalculator.calculate_battery_consumption(1000, 100, 100)
        assert consumption == 100.0
    
    def test_calculate_total_weight(self):
        """Calcula peso total de entregas"""
        entregas = [
            {'peso_kg': 10},
            {'peso_kg': 20},
            {'peso_kg': 15}
        ]
        weight = RouteCalculator.calculate_total_weight(entregas)
        assert weight == 45


# ==================== TESTS ROUTEVALIDATOR ====================

class TestRouteValidator:
    
    def test_validate_battery_capacity_sufficient(self):
        """Valida que la batería sea suficiente"""
        assert RouteValidator.validate_battery_capacity(100, 50, 100)
    
    def test_validate_battery_capacity_insufficient(self):
        """Rechaza batería insuficiente"""
        with pytest.raises(ValidationError):
            RouteValidator.validate_battery_capacity(30, 50, 100)
    
    def test_validate_battery_capacity_high_consumption(self):
        """Rechaza consumo > 80%"""
        with pytest.raises(ValidationError):
            RouteValidator.validate_battery_capacity(100, 85, 100)
    
    def test_validate_weight_capacity_ok(self):
        """Valida peso dentro de capacidad"""
        assert RouteValidator.validate_weight_capacity(300, 500)
    
    def test_validate_weight_capacity_exceeded(self):
        """Rechaza peso que excede capacidad"""
        with pytest.raises(ValidationError):
            RouteValidator.validate_weight_capacity(600, 500)
    
    def test_validate_no_duplicate_deliveries_ok(self):
        """Valida sin duplicados"""
        assert RouteValidator.validate_no_duplicate_deliveries(["ENT-001", "ENT-002"])
    
    def test_validate_no_duplicate_deliveries_duplicates(self):
        """Rechaza duplicados"""
        with pytest.raises(ValidationError):
            RouteValidator.validate_no_duplicate_deliveries(["ENT-001", "ENT-001"])


# ==================== TESTS ROUTEOPTIMIZER ====================

class TestRouteOptimizer:
    
    def test_sort_by_priority(self):
        """Ordena entregas por prioridad"""
        entregas = [
            {'id_entrega': 'E1', 'prioridad': 3},
            {'id_entrega': 'E2', 'prioridad': 1},
            {'id_entrega': 'E3', 'prioridad': 2},
        ]
        sorted_entregas = RouteOptimizer.sort_by_priority(entregas)
        assert sorted_entregas[0]['prioridad'] == 1
        assert sorted_entregas[1]['prioridad'] == 2
        assert sorted_entregas[2]['prioridad'] == 3
    
    def test_sort_by_window_time(self):
        """Ordena entregas por ventana horaria"""
        entregas = [
            {'id_entrega': 'E1', 'ventana_horaria': '14:00 - 16:00'},
            {'id_entrega': 'E2', 'ventana_horaria': '09:00 - 11:00'},
            {'id_entrega': 'E3', 'ventana_horaria': '12:00 - 13:00'},
        ]
        sorted_entregas = RouteOptimizer.sort_by_window_time(entregas)
        assert sorted_entregas[0]['id_entrega'] == 'E2'
        assert sorted_entregas[1]['id_entrega'] == 'E3'
        assert sorted_entregas[2]['id_entrega'] == 'E1'
