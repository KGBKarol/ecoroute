"""
cli_agent.py - Capa de presentación: Interfaz CLI interactiva
Responsabilidades:
- Mostrar menús
- Capturar entrada del usuario
- Mostrar resultados formateados
- Llamar a lógica_agent para procesar
"""

import sys
from tabulate import tabulate
from src.db_agent import VehicleRepository, DeliveryRepository, RouteRepository, DatabaseConnection
from src.logic_agent import (
    VehicleValidator, DeliveryValidator, RouteValidator, RouteCalculator, 
    RouteOptimizer, ValidationError, CalculationError
)
import json


class CLIAgent:
    """Interfaz CLI interactiva"""
    
    # Configuración de paginación
    ITEMS_PER_PAGE = 20
    
    def __init__(self):
        self.running = True
    
    # ==================== MENÚ PRINCIPAL ====================
    
    def show_main_menu(self):
        """Muestra menú principal"""
        while self.running:
            print("\n" + "="*60)
            print("           ECOROUTE - GESTOR DE FURGONETAS ELÉCTRICAS")
            print("="*60)
            print("\n1. Gestión de Vehículos")
            print("2. Gestión de Entregas")
            print("3. Gestión de Rutas")
            print("4. Salir")
            print("\n" + "-"*60)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.show_vehicle_menu()
            elif choice == '2':
                self.show_delivery_menu()
            elif choice == '3':
                self.show_route_menu()
            elif choice == '4':
                print("\n✓ ¡Hasta luego!")
                self.running = False
            else:
                print("\n✗ Opción inválida")
    
    # ==================== MENÚ VEHÍCULOS ====================
    
    def show_vehicle_menu(self):
        """Menú de gestión de vehículos"""
        while True:
            print("\n" + "="*60)
            print("GESTIÓN DE VEHÍCULOS")
            print("="*60)
            print("\n1. Registrar vehículo (CU-01)")
            print("2. Listar vehículos (CU-04)")
            print("3. Ver datos de vehículo (CU-03)")
            print("4. Editar vehículo (CU-05)")
            print("5. Eliminar vehículo (CU-02)")
            print("6. Volver")
            print("-"*60)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.register_vehicle()
            elif choice == '2':
                self.list_vehicles()
            elif choice == '3':
                self.view_vehicle()
            elif choice == '4':
                self.edit_vehicle()
            elif choice == '5':
                self.delete_vehicle()
            elif choice == '6':
                break
            else:
                print("✗ Opción inválida")
    
    def register_vehicle(self):
        """CU-01: Registrar vehículo"""
        print("\n" + "-"*60)
        print("REGISTRAR VEHÍCULO")
        print("-"*60)
        
        try:
            id_vehiculo = input("ID del vehículo (ej: VAN-001): ").strip()
            VehicleValidator.validate_id(id_vehiculo)
            
            # Verificar que no exista
            if VehicleRepository.read_by_id(id_vehiculo):
                print("✗ El vehículo ya existe")
                return
            
            modelo = input("Modelo: ").strip()
            VehicleValidator.validate_modelo(modelo)
            
            capacidad = float(input("Capacidad de batería (kWh): "))
            nivel_actual = float(input("Nivel de batería actual (%): "))
            VehicleValidator.validate_bateria(capacidad, nivel_actual)
            
            autonomia = float(input("Autonomía máxima (km): "))
            VehicleValidator.validate_autonomia(autonomia)
            
            print("\nEstados disponibles: disponible, en ruta, cargando, mantenimiento")
            estado = input("Estado: ").strip()
            VehicleValidator.validate_estado(estado)
            
            VehicleRepository.create(id_vehiculo, modelo, capacidad, nivel_actual, autonomia, estado)
            print("\n✓ Vehículo registrado correctamente")
            print(f"  ID: {id_vehiculo}")
            print(f"  Modelo: {modelo}")
            
        except ValidationError as e:
            print(f"\n✗ Error de validación: {e}")
        except ValueError:
            print("\n✗ Error: Los valores numéricos son inválidos")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def list_vehicles(self):
        """CU-04: Listar vehículos con paginación"""
        try:
            vehicles = VehicleRepository.read_all()
            
            if not vehicles:
                print("\n✗ No hay vehículos registrados")
                return
            
            self._paginate_list(vehicles, "VEHÍCULOS", 
                              ['id_vehiculo', 'modelo', 'nivel_bateria_actual', 'estado'])
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def view_vehicle(self):
        """CU-03: Ver datos de vehículo"""
        try:
            vehicles = VehicleRepository.read_all()
            if not vehicles:
                print("\n✗ No hay vehículos")
                return
            
            id_vehiculo = input("ID del vehículo: ").strip()
            vehicle = VehicleRepository.read_by_id(id_vehiculo)
            
            if not vehicle:
                print("✗ Vehículo no encontrado")
                return
            
            print("\n" + "="*60)
            print(f"DATOS DEL VEHÍCULO: {id_vehiculo}")
            print("="*60)
            data = [
                ["ID", vehicle['id_vehiculo']],
                ["Modelo", vehicle['modelo']],
                ["Capacidad (kWh)", vehicle['capacidad_bateria_total']],
                ["Nivel actual (%)", vehicle['nivel_bateria_actual']],
                ["Autonomía (km)", vehicle['autonomia_maxima_km']],
                ["Estado", vehicle['estado']],
            ]
            print(tabulate(data, tablefmt="grid"))
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def edit_vehicle(self):
        """CU-05: Editar vehículo"""
        try:
            id_vehiculo = input("ID del vehículo a editar: ").strip()
            vehicle = VehicleRepository.read_by_id(id_vehiculo)
            
            if not vehicle:
                print("✗ Vehículo no encontrado")
                return
            
            print(f"\nEditando vehículo {id_vehiculo} (deja en blanco para no cambiar)")
            
            modelo = input(f"Modelo ({vehicle['modelo']}): ").strip() or None
            if modelo:
                VehicleValidator.validate_modelo(modelo)
            
            nivel = input(f"Nivel batería ({vehicle['nivel_bateria_actual']}): ").strip()
            if nivel:
                nivel = float(nivel)
                VehicleValidator.validate_bateria(vehicle['capacidad_bateria_total'], nivel)
            else:
                nivel = None
            
            estado = input(f"Estado ({vehicle['estado']}): ").strip() or None
            if estado:
                VehicleValidator.validate_estado(estado)
            
            VehicleRepository.update(id_vehiculo, modelo=modelo, 
                                    nivel_bateria_actual=nivel, estado=estado)
            print("\n✓ Vehículo actualizado")
            
        except ValidationError as e:
            print(f"\n✗ Error de validación: {e}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def delete_vehicle(self):
        """CU-02: Eliminar vehículo"""
        try:
            id_vehiculo = input("ID del vehículo a eliminar: ").strip()
            vehicle = VehicleRepository.read_by_id(id_vehiculo)
            
            if not vehicle:
                print("✗ Vehículo no encontrado")
                return
            
            confirm = input(f"¿Confirmas eliminar {id_vehiculo}? (s/n): ").strip().lower()
            if confirm != 's':
                print("✗ Operación cancelada")
                return
            
            VehicleRepository.soft_delete(id_vehiculo)
            print("✓ Vehículo eliminado")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    # ==================== MENÚ ENTREGAS ====================
    
    def show_delivery_menu(self):
        """Menú de gestión de entregas"""
        while True:
            print("\n" + "="*60)
            print("GESTIÓN DE ENTREGAS")
            print("="*60)
            print("\n1. Crear entrega (CU-06)")
            print("2. Listar entregas (CU-09)")
            print("3. Ver datos de entrega (CU-08)")
            print("4. Editar entrega (CU-10)")
            print("5. Eliminar entrega (CU-07)")
            print("6. Volver")
            print("-"*60)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.create_delivery()
            elif choice == '2':
                self.list_deliveries()
            elif choice == '3':
                self.view_delivery()
            elif choice == '4':
                self.edit_delivery()
            elif choice == '5':
                self.delete_delivery()
            elif choice == '6':
                break
            else:
                print("✗ Opción inválida")
    
    def create_delivery(self):
        """CU-06: Crear entrega"""
        print("\n" + "-"*60)
        print("CREAR ENTREGA")
        print("-"*60)
        
        try:
            id_entrega = input("ID de entrega (ej: ENT-0001): ").strip()
            DeliveryValidator.validate_id(id_entrega)
            
            if DeliveryRepository.read_by_id(id_entrega):
                print("✗ La entrega ya existe")
                return
            
            lat = float(input("Latitud de destino: "))
            lon = float(input("Longitud de destino: "))
            DeliveryValidator.validate_coordenadas(lat, lon)
            
            peso = float(input("Peso (kg): "))
            DeliveryValidator.validate_peso(peso)
            
            prioridad = int(input("Prioridad (1=urgente, 2=normal, 3=baja): "))
            DeliveryValidator.validate_prioridad(prioridad)
            
            ventana = input("Ventana horaria (ej: 09:00 - 11:00): ").strip()
            DeliveryValidator.validate_ventana_horaria(ventana)
            
            DeliveryRepository.create(id_entrega, lat, lon, peso, prioridad, ventana)
            print("\n✓ Entrega creada correctamente")
            print(f"  ID: {id_entrega}")
            print(f"  Destino: ({lat}, {lon})")
            
        except ValidationError as e:
            print(f"\n✗ Error de validación: {e}")
        except ValueError:
            print("\n✗ Error: Los valores son inválidos")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def list_deliveries(self):
        """CU-09: Listar entregas"""
        try:
            deliveries = DeliveryRepository.read_all()
            
            if not deliveries:
                print("\n✗ No hay entregas")
                return
            
            self._paginate_list(deliveries, "ENTREGAS",
                              ['id_entrega', 'destino_lat', 'destino_lon', 'peso_kg', 'prioridad'])
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def view_delivery(self):
        """CU-08: Ver datos de entrega"""
        try:
            id_entrega = input("ID de entrega: ").strip()
            delivery = DeliveryRepository.read_by_id(id_entrega)
            
            if not delivery:
                print("✗ Entrega no encontrada")
                return
            
            print("\n" + "="*60)
            print(f"DATOS DE ENTREGA: {id_entrega}")
            print("="*60)
            data = [
                ["ID", delivery['id_entrega']],
                ["Destino", f"({delivery['destino_lat']}, {delivery['destino_lon']})"],
                ["Peso (kg)", delivery['peso_kg']],
                ["Prioridad", delivery['prioridad']],
                ["Ventana horaria", delivery['ventana_horaria']],
            ]
            print(tabulate(data, tablefmt="grid"))
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def edit_delivery(self):
        """CU-10: Editar entrega"""
        try:
            id_entrega = input("ID de entrega a editar: ").strip()
            delivery = DeliveryRepository.read_by_id(id_entrega)
            
            if not delivery:
                print("✗ Entrega no encontrada")
                return
            
            print(f"\nEditando entrega {id_entrega}")
            
            peso = input(f"Peso ({delivery['peso_kg']}): ").strip()
            if peso:
                peso = float(peso)
                DeliveryValidator.validate_peso(peso)
            else:
                peso = None
            
            prioridad = input(f"Prioridad ({delivery['prioridad']}): ").strip()
            if prioridad:
                prioridad = int(prioridad)
                DeliveryValidator.validate_prioridad(prioridad)
            else:
                prioridad = None
            
            DeliveryRepository.update(id_entrega, peso_kg=peso, prioridad=prioridad)
            print("\n✓ Entrega actualizada")
            
        except ValidationError as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def delete_delivery(self):
        """CU-07: Eliminar entrega"""
        try:
            id_entrega = input("ID de entrega a eliminar: ").strip()
            delivery = DeliveryRepository.read_by_id(id_entrega)
            
            if not delivery:
                print("✗ Entrega no encontrada")
                return
            
            confirm = input(f"¿Confirmas eliminar {id_entrega}? (s/n): ").strip().lower()
            if confirm != 's':
                print("✗ Operación cancelada")
                return
            
            DeliveryRepository.soft_delete(id_entrega)
            print("✓ Entrega eliminada")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    # ==================== MENÚ RUTAS ====================
    
    def show_route_menu(self):
        """Menú de gestión de rutas"""
        while True:
            print("\n" + "="*60)
            print("GESTIÓN DE RUTAS")
            print("="*60)
            print("\n1. Crear ruta (CU-11)")
            print("2. Listar rutas (CU-14)")
            print("3. Ver datos de ruta (CU-13)")
            print("4. Editar ruta (CU-15)")
            print("5. Eliminar ruta (CU-12)")
            print("6. Volver")
            print("-"*60)
            
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self.create_route()
            elif choice == '2':
                self.list_routes()
            elif choice == '3':
                self.view_route()
            elif choice == '4':
                self.edit_route()
            elif choice == '5':
                self.delete_route()
            elif choice == '6':
                break
            else:
                print("✗ Opción inválida")
    
    def create_route(self):
        """CU-11: Crear ruta"""
        print("\n" + "-"*60)
        print("CREAR RUTA")
        print("-"*60)
        
        try:
            id_ruta = input("ID de ruta (ej: RUTA-001): ").strip()
            
            # Seleccionar vehículo
            vehicles = VehicleRepository.read_all()
            if not vehicles:
                print("✗ No hay vehículos disponibles")
                return
            
            print("\nVehículos disponibles:")
            for v in vehicles:
                print(f"  {v['id_vehiculo']}: {v['modelo']} ({v['nivel_bateria_actual']}%)")
            
            id_vehiculo = input("ID del vehículo: ").strip()
            vehicle = VehicleRepository.read_by_id(id_vehiculo)
            if not vehicle:
                print("✗ Vehículo no encontrado")
                return
            
            # Seleccionar entregas
            deliveries = DeliveryRepository.read_all()
            if not deliveries:
                print("✗ No hay entregas disponibles")
                return
            
            print("\nEntregas disponibles:")
            for d in deliveries:
                print(f"  {d['id_entrega']}: ({d['destino_lat']}, {d['destino_lon']}) - Prioridad {d['prioridad']}")
            
            entregas_input = input("IDs de entregas separados por coma (ej: ENT-0001,ENT-0002): ").strip().split(',')
            entregas_seleccionadas = [e.strip() for e in entregas_input]
            
            entregas = []
            for ent_id in entregas_seleccionadas:
                ent = DeliveryRepository.read_by_id(ent_id)
                if not ent:
                    print(f"✗ Entrega {ent_id} no encontrada")
                    return
                entregas.append(ent)
            
            # Validar peso total
            peso_total = RouteCalculator.calculate_total_weight(entregas)
            try:
                RouteValidator.validate_weight_capacity(peso_total, 500)  # Capacidad estándar
            except ValidationError as e:
                print(f"✗ {e}")
                return
            
            # Calcular distancia y consumo
            coords = [(d['destino_lat'], d['destino_lon']) for d in entregas]
            distancia = RouteCalculator.calculate_total_distance(coords)
            consumo = RouteCalculator.calculate_battery_consumption(
                distancia, peso_total, vehicle['autonomia_maxima_km']
            )
            
            # Validar batería
            try:
                RouteValidator.validate_battery_capacity(
                    vehicle['nivel_bateria_actual'], consumo, vehicle['capacidad_bateria_total']
                )
            except ValidationError as e:
                print(f"\n⚠ Advertencia: {e}")
                proceed = input("¿Deseas proceder de todas formas? (s/n): ").strip().lower()
                if proceed != 's':
                    return
            
            # Guardar ruta
            lista_entregas_json = json.dumps(entregas_seleccionadas)
            RouteRepository.create(id_ruta, id_vehiculo, lista_entregas_json, distancia, consumo)
            
            print("\n✓ Ruta creada correctamente")
            print(f"  ID: {id_ruta}")
            print(f"  Vehículo: {id_vehiculo}")
            print(f"  Entregas: {len(entregas_seleccionadas)}")
            print(f"  Distancia estimada: {distancia:.2f} km")
            print(f"  Consumo estimado: {consumo:.2f}%")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def list_routes(self):
        """CU-14: Listar rutas"""
        try:
            routes = RouteRepository.read_all()
            
            if not routes:
                print("\n✗ No hay rutas")
                return
            
            self._paginate_list(routes, "RUTAS",
                              ['id_ruta', 'id_vehiculo', 'distancia_total_estimada', 'consumo_estimado_bateria'])
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def view_route(self):
        """CU-13: Ver datos de ruta"""
        try:
            id_ruta = input("ID de ruta: ").strip()
            route = RouteRepository.read_by_id(id_ruta)
            
            if not route:
                print("✗ Ruta no encontrada")
                return
            
            entregas_list = json.loads(route['lista_entregas'])
            
            print("\n" + "="*60)
            print(f"DATOS DE RUTA: {id_ruta}")
            print("="*60)
            data = [
                ["ID", route['id_ruta']],
                ["Vehículo", route['id_vehiculo']],
                ["Entregas", ', '.join(entregas_list)],
                ["Distancia (km)", route['distancia_total_estimada']],
                ["Consumo (%)", route['consumo_estimado_bateria']],
            ]
            print(tabulate(data, tablefmt="grid"))
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def edit_route(self):
        """CU-15: Editar ruta"""
        print("✗ Funcionalidad en desarrollo")
    
    def delete_route(self):
        """CU-12: Eliminar ruta"""
        try:
            id_ruta = input("ID de ruta a eliminar: ").strip()
            route = RouteRepository.read_by_id(id_ruta)
            
            if not route:
                print("✗ Ruta no encontrada")
                return
            
            confirm = input(f"¿Confirmas eliminar {id_ruta}? (s/n): ").strip().lower()
            if confirm != 's':
                print("✗ Operación cancelada")
                return
            
            RouteRepository.soft_delete(id_ruta)
            print("✓ Ruta eliminada")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    # ==================== UTILIDADES ====================
    
    def _paginate_list(self, items, title, columns):
        """Muestra lista paginada"""
        total_items = len(items)
        total_pages = (total_items + self.ITEMS_PER_PAGE - 1) // self.ITEMS_PER_PAGE
        current_page = 1
        
        while True:
            start = (current_page - 1) * self.ITEMS_PER_PAGE
            end = start + self.ITEMS_PER_PAGE
            page_items = items[start:end]
            
            print("\n" + "="*60)
            print(f"{title} - Página {current_page}/{total_pages} ({total_items} total)")
            print("="*60)
            
            table_data = [[item[col] for col in columns] for item in page_items]
            print(tabulate(table_data, headers=columns, tablefmt="grid"))
            
            if total_pages > 1:
                print(f"\nOpciones: [N]próxima, [A]anterior, [S]alir")
                choice = input("Opción: ").strip().lower()
                
                if choice == 'n' and current_page < total_pages:
                    current_page += 1
                elif choice == 'a' and current_page > 1:
                    current_page -= 1
                else:
                    break
            else:
                input("\nPresiona Enter para volver...")
                break
