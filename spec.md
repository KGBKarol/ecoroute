## 1. Descripción general 
La aplicación es una herramienta de línea de comandos (CLI) escrita en lenguaje Python que permite gestionar su nueva flota de furgonetas eléctricas

## 2. Funcionalidades

- Registrar vehiculos
- Gestionar Entregas
- Logica de seguridad

## 3. Modelo de datos

### Entidad: Vehiculo

| Campo | Tipo | Descripcion |
| ----- | ---- | ----------- |
| id_vehiculo | string |  Identificador único (ej: "VAN-001"). Debe seguir un patrón alfanumérico. |
| modelo | string | Nombre del modelo |
| capacidad_bateria_total | float | Capacidad maxima en kWh |
| nivel_bateria_actual | float | porcentaje de carga (0 a 100) |
| autonomia_maxima_km | int | Cuantos km puede recorrer con 100% carga |
| estado | enum(disponible, en ruta, Cargando, Mantenimeinto) | Estado del vehiculo |

### Entidad: Entrega

| Campo | Tipo | Descripcion |
| ----- | ---- | ----------- |
| id_entrega | string |   Identificador único del paquete. |
| destino_coordenadas | tuple(lat,lon) | Ubicacion exacta de la entrega |
| peso_kg | float | Influye en el consumo |
| prioridad | int | Nivel de urgencia (1-3) |
| ventana_horaria | string | ej: (09:00 - 11:00) |

### Entidad: Ruta

| Campo | Tipo | Descripcion |
| ----- | ---- | ----------- |
| id_ruta | string |   Identificador único |
| Vehiculo asignado | FK | Referencia vehiculo |
| lista_entregas | List | Lisa ordenada de IDs de entregas |
| distancia_total_estimada | float | suma de los trayectos |
| consumo_estimado_bateria | float | porcentaje que se restara al acabar la ruta |

## 4. Casos de uso

### CU-01: Registrar vehiculos

1. El usuario selecciona añadir vehiculo
2. El sistema pide: Modelo, capacidad_bateria_total, nivel_bateria_actual, autonomia_maxima_km, estado
3. El usuario introduce los datos
4. El sistema valida los datos
5. El sistema inserta el vehiculo en la BBDD y te muestra la informacion

**Flujo alternativo A**  (validación falla)
   - El sistema muestra un mensaje de error y solicta corregir el error

**Flujo Alternativo B** (validacion correcta)
  - El sistema inserta los datos en la base de datos

### CU-02: Eliminar vehiculo

1. El usuario selecciona eliminar vehiculo
2. El sistema muestra todos los vehiculos junto con id
3. El sistema le pide al usuario que introduzca el id del vehiculo a eliminar
4. El sistema valida que el id sea correcto y exista
5. El sistema hace la pregunta de confirmacion para saber si quiere eliminarlo
6. Si el usuario confirma el borrado elimina el vehiculo de la BBDD
7. El sistema confirma la eliminacion

### CU-03: Mostrar datos de vehiculo

1. El usuario selecciona mostrar datos de vehiculo
2. El usuario muestra todos los vehiculos (modelos e id)
3. El sistema le pide al usuario que introduzca el id del vehiculo que quiera ver los datos
4. El sistema valida que el id sea correcto
5. El sistema muestra todos los datos de ese vehiculo

### CU-04 Mostrar todos los vehiculos

1. El usuario selecionna mostrar vehiculos
2. El sistema muestra todos los vehiculos
3. Si hay mas de 10 vehiculos paginarlos en listas de 20 en 20
4. El usuario puede navegar entre dichas paginas o volver al menu

### CU-05 Editar vehiculo
1. El usuario selecciona editar vehiculo
2. El sistema le muestra los vehiculos que puede editar mostrando modelo e id
3. 
