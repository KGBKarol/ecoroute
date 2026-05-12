# 1. Principios fundamentales

### 1.1 Privacidad por diseño
- Todos los datos son informacion personal y se tratan como tal. Es decir **no** se envian datos a terceros, ni se almacenan datos que no sean necesarios para el funcionamiento del programa.
- El accesso a la base de datos require autenticacion. Las credenciales no se almacenan ni en el codigo fuente ni el control de versiones.
  
### 1.2 Integridad de los datos
- Toda escritura en la base de datos se realiza mediante sentencias SQL parametrizadas para evitar inyecciones SQL.
- Se validan los datos introducidos por el usuario antes de ser insertados en la base de datos. Esto incluye validaciones de formato, rango y tipo de datos.

### 1.3 Separacion de responsabilidades
Ningun agente asume responsabilidades que no le corresponden.

### 1.4 Simplicidad sobre complejidad
- Soluciones simples, legibles y funcionales frente a soluciones complejas y sofisticadas. Esto se traduce en un codigo limpio, facil de entender y mantener.
- No se añadiran dependecias externas sin justificacion

## 2. Reglas de diseño de código

| Regla | Descripción |
|-------|-------------|
| R-01  | El manejo de errores usa excepciones. |
| R-02  | Las constantes de configuración se leen desde variables de entorno. |
| R-03  | Los nombres de variables y funciones están en **snake_case** en  inglés |


## 3. Restricciones de seguridad

- **SQL Injection:** Uso obligatorio de parámetros en todas las consultas.
- **Credenciales:** Cargadas desde `.env` (excluido de `.gitignore`). Nunca en código.
- **Permisos MySQL:** El usuario de la aplicación solo tiene `SELECT, INSERT, UPDATE, DELETE` sobre el esquema `ecoroute_db`. **No** tiene ningun otro permiso que no sea estrictamente necesario.