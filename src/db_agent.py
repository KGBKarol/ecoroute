"""
db_agent.py - Capa de datos: acceso a MySQL
Responsabilidades:
- Gestionar conexión a BD
- Implementar repositorios CRUD
- Usar sentencias parametrizadas para prevenir SQL injection
- Aplicar soft delete
"""

import mysql.connector
from mysql.connector import Error as MySQLError
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()


class DatabaseConnection:
    """Gestiona la conexión a MySQL"""
    
    @staticmethod
    def get_connection():
        """Obtiene conexión a la BD desde variables de entorno"""
        try:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            return conn
        except MySQLError as e:
            raise Exception(f"Error conectando a BD: {e}")


class VehicleRepository:
    """Repositorio para gestionar vehículos"""
    
    @staticmethod
    def create(id_vehiculo, modelo, capacidad_bateria_total, 
               nivel_bateria_actual, autonomia_maxima_km, estado):
        """Inserta un nuevo vehículo"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO vehiculos 
                (id_vehiculo, modelo, capacidad_bateria_total, 
                 nivel_bateria_actual, autonomia_maxima_km, estado, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                id_vehiculo, modelo, capacidad_bateria_total,
                nivel_bateria_actual, autonomia_maxima_km, estado, datetime.now()
            ))
            conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error al insertar vehículo: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def read_all():
        """Lee todos los vehículos no eliminados"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM vehiculos WHERE deleted_at IS NULL ORDER BY id_vehiculo"
            cursor.execute(query)
            return cursor.fetchall()
        except MySQLError as e:
            raise Exception(f"Error al leer vehículos: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def read_by_id(id_vehiculo):
        """Lee un vehículo específico por ID"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM vehiculos WHERE id_vehiculo = %s AND deleted_at IS NULL"
            cursor.execute(query, (id_vehiculo,))
            return cursor.fetchone()
        except MySQLError as e:
            raise Exception(f"Error al leer vehículo: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(id_vehiculo, **kwargs):
        """Actualiza campos de un vehículo"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            fields = []
            values = []
            for key, value in kwargs.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if not fields:
                return True
            
            values.append(id_vehiculo)
            query = f"UPDATE vehiculos SET {', '.join(fields)}, updated_at = %s WHERE id_vehiculo = %s AND deleted_at IS NULL"
            values.insert(-1, datetime.now())
            
            cursor.execute(query, values)
            conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error al actualizar vehículo: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def soft_delete(id_vehiculo):
        """Marca un vehículo como eliminado (soft delete)"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            query = "UPDATE vehiculos SET deleted_at = %s WHERE id_vehiculo = %s"
            cursor.execute(query, (datetime.now(), id_vehiculo))
            conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error al eliminar vehículo: {e}")
        finally:
            cursor.close()
            conn.close()


class DeliveryRepository:
    """Repositorio para gestionar entregas"""
    
    @staticmethod
    def create(id_entrega, destino_lat, destino_lon, peso_kg, prioridad, ventana_horaria):
        """Inserta una nueva entrega"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO entregas 
                (id_entrega, destino_lat, destino_lon, peso_kg, prioridad, ventana_horaria, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                id_entrega, destino_lat, destino_lon, peso_kg, prioridad, ventana_horaria, datetime.now()
            ))
            conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error al insertar entrega: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def read_all():
        """Lee todas las entregas no eliminadas"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM entregas WHERE deleted_at IS NULL ORDER BY prioridad, ventana_horaria"
            cursor.execute(query)
            return cursor.fetchall()
        except MySQLError as e:
            raise Exception(f"Error al leer entregas: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def read_by_id(id_entrega):
        """Lee una entrega específica por ID"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM entregas WHERE id_entrega = %s AND deleted_at IS NULL"
            cursor.execute(query, (id_entrega,))
            return cursor.fetchone()
        except MySQLError as e:
            raise Exception(f"Error al leer entrega: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(id_entrega, **kwargs):
        """Actualiza campos de una entrega"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            fields = []
            values = []
            for key, value in kwargs.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if not fields:
                return True
            
            values.append(id_entrega)
            query = f"UPDATE entregas SET {', '.join(fields)}, updated_at = %s WHERE id_entrega = %s AND deleted_at IS NULL"
            values.insert(-1, datetime.now())
            
            cursor.execute(query, values)
            conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error al actualizar entrega: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def soft_delete(id_entrega):
        """Marca una entrega como eliminada (soft delete)"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            query = "UPDATE entregas SET deleted_at = %s WHERE id_entrega = %s"
            cursor.execute(query, (datetime.now(), id_entrega))
            conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error al eliminar entrega: {e}")
        finally:
            cursor.close()
            conn.close()


class RouteRepository:
    """Repositorio para gestionar rutas"""
    
    @staticmethod
    def create(id_ruta, id_vehiculo, lista_entregas_json, distancia_total_estimada, consumo_estimado_bateria):
        """Inserta una nueva ruta"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO rutas 
                (id_ruta, id_vehiculo, lista_entregas, distancia_total_estimada, 
                 consumo_estimado_bateria, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                id_ruta, id_vehiculo, lista_entregas_json, distancia_total_estimada,
                consumo_estimado_bateria, datetime.now()
            ))
            conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error al insertar ruta: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def read_all():
        """Lee todas las rutas no eliminadas"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM rutas WHERE deleted_at IS NULL ORDER BY created_at DESC"
            cursor.execute(query)
            return cursor.fetchall()
        except MySQLError as e:
            raise Exception(f"Error al leer rutas: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def read_by_id(id_ruta):
        """Lee una ruta específica por ID"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM rutas WHERE id_ruta = %s AND deleted_at IS NULL"
            cursor.execute(query, (id_ruta,))
            return cursor.fetchone()
        except MySQLError as e:
            raise Exception(f"Error al leer ruta: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(id_ruta, **kwargs):
        """Actualiza campos de una ruta"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            fields = []
            values = []
            for key, value in kwargs.items():
                if value is not None:
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if not fields:
                return True
            
            values.append(id_ruta)
            query = f"UPDATE rutas SET {', '.join(fields)}, updated_at = %s WHERE id_ruta = %s AND deleted_at IS NULL"
            values.insert(-1, datetime.now())
            
            cursor.execute(query, values)
            conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error al actualizar ruta: {e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def soft_delete(id_ruta):
        """Marca una ruta como eliminada (soft delete)"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            query = "UPDATE rutas SET deleted_at = %s WHERE id_ruta = %s"
            cursor.execute(query, (datetime.now(), id_ruta))
            conn.commit()
            return True
        except MySQLError as e:
            raise Exception(f"Error al eliminar ruta: {e}")
        finally:
            cursor.close()
            conn.close()
