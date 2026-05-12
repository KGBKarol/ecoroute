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
6. Si el usuario confirma el borrado elimina el vehiculo de la BBDD con soft_delete
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
3. El usuario seleccionara el id del vehiculo que quiere editar
4. El sistema mostrara todos los datos del vehiculo selecionnado
5. El sistema ir campo por campo preguntando el nuevo valor
6. Si el usuario pone vacio se deja el valor antiguo
7. El sistema comprobara que cada dato introducido sea correcto
8. EL sistema actualizara la tabla con los nuevos datos
   
### CU-06 Añadir entrega
1. El usuario selecciona añadir entrega
2. El sistema le pide al usuario que introduzca: destino_coordenadas, peso_kg, prioridad, ventana_horaria
3. El sistema valida los datos introducidos
4. El sistema inserta la entrega en la BBDD y muestra la informacion
   
### CU-07 Eliminar entrega
1. El usuario selecciona eliminar entrega
2. El sistema muestra todas las entregas junto con id
3. El sistema le pide al usuario que introduzca el id de la entrega a eliminar
4. El sistema valida que el id sea correcto y exista
5. El sistema hace la pregunta de confirmacion para saber si quiere eliminarlo
6. Si el usuario confirma el borrado elimina la entrega de la BBDD con soft_delete
7. El sistema confirma la eliminacion
   
### CU-08 Mostrar datos de entrega
1. El usuario selecciona mostrar datos de entrega
2. El usuario muestra todas las entregas (destino e id)
3. El sistema le pide al usuario que introduzca el id de la entrega que quiera ver los datos
4. El sistema valida que el id sea correcto
5. El sistema muestra todos los datos de esa entrega
   
### CU-09 Mostrar todas las entregas
1. El usuario selecionna mostrar entregas
2. El sistema muestra todas las entregas
3. Si hay mas de 20 entregas paginarlos en listas de 20 en 20
4. El usuario puede navegar entre dichas paginas o volver al menu
5. El sistema muestra el numero total de entregas
  
### CU-10 Editar entrega
1. El usuario selecciona editar entrega
2. El sistema le muestra las entregas que puede editar mostrando destino e id
3. El usuario seleccionara el id de la entrega que quiere editar
4. El sistema mostrara todos los datos de la entrega selecionnada
5. El sistema ir campo por campo preguntando el nuevo valor
6. Si el usuario pone vacio se deja el valor antiguo
7. El sistema comprobara que cada dato introducido sea correcto
8. EL sistema actualizara la tabla con los nuevos datos
  
### CU-11 Crear ruta
1. El usuario selecciona crear ruta
2. El sistema le muestra los vehiculos disponibles (modelo e id)
3. El usuario selecciona el id del vehiculo que quiere asignar a la ruta
4. El sistema muestra las entregas disponibles (destino e id)
5. El usuario selecciona las entregas que quiere asignar a la ruta (puede seleccionar varias)
6. El sistema valida que el vehiculo tenga suficiente bateria para realizar la ruta
7.  Si el sistema detecta que la ruta va a consumir mas del 80% de la bateria actual, el sistema debe rechazar la ruta o sugerir una parada en un punto de recarga
8. El sistema valida que el peso total de las entregas no supere la capacidad de carga del vehiculo
9. El sistema calcula la distancia total estimada de la ruta
10. El sistema calcula el consumo estimado de bateria para esa ruta
11. El sistema muestra un resumen de la ruta creada (vehiculo, entregas, distancia, consumo)
12. El sistema inserta la ruta en la BBDD y muestra la informacion
  
### CU-12 Eliminar ruta
1. El usuario selecciona eliminar ruta
2. El sistema muestra todas las rutas junto con id
3. El sistema le pide al usuario que introduzca el id de la ruta a eliminar
4. El sistema valida que el id sea correcto y exista
5. El sistema hace la pregunta de confirmacion para saber si quiere eliminarlo
6. Si el usuario confirma el borrado elimina la ruta de la BBDD con soft_delete
7. El sistema confirma la eliminacion
  
### CU-13 Mostrar datos de ruta
1. El usuario selecciona mostrar datos de ruta
2. El usuario muestra todas las rutas (id y vehiculo asignado)
3. El sistema le pide al usuario que introduzca el id de la ruta que quiera ver los datos
4. El sistema valida que el id sea correcto
5. El sistema muestra todos los datos de esa ruta (vehiculo, entregas, distancia, consumo)  
   
### CU-14 Mostrar todas las rutas
1. El usuario selecionna mostrar rutas
2. El sistema muestra todas las rutas
3. Si hay mas de 20 rutas paginarlos en listas de 20 en 20
4. El usuario puede navegar entre dichas paginas o volver al menu
5. El sistema muestra el numero total de rutas
  
### CU-15 Editar ruta
1. El usuario selecciona editar ruta
2. El sistema le muestra las rutas que puede editar mostrando id y vehiculo asignado
3. El usuario seleccionara el id de la ruta que quiere editar
4. El sistema mostrara todos los datos de la ruta selecionnada
5. El sistema le pregunta si quiere cambiar el vehiculo asignado
6. Si el usuario quiere cambiar el vehiculo, el sistema muestra los vehiculos disponibles (modelo e id) y el usuario selecciona el nuevo vehiculo
7. El sistema le pregunta si quiere cambiar las entregas asignadas
8. Si el usuario quiere cambiar las entregas, el sistema muestra las entregas disponibles (destino e id) y el usuario selecciona las nuevas entregas (puede seleccionar varias)
9. El sistema valida que el nuevo vehiculo tenga suficiente bateria para realizar la ruta con las nuevas entregas
10. El sistema valida que el peso total de las nuevas entregas no supere la capacidad de carga del nuevo vehiculo
11. El sistema recalcula la distancia total estimada de la ruta
12. El sistema recalcula el consumo estimado de bateria para esa ruta
13. El sistema muestra un resumen de la ruta editada (vehiculo, entregas, distancia, consumo)
14. El sistema actualiza la ruta en la BBDD con los nuevos datos
    
