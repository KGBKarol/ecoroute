# decisions.md — Registro de Decisiones de Diseño
Este documento registra las decisiones técnicas y de diseño significativas tomadas durante el desarrollo de la aplicación de ecoroute. Cada entrada sigue el formato ADR (Architecture Decision Record).
---

## ADR-001: Elección de base de datos — MySQL
**Fecha:** 2026-05-12  

**Estado:** Aceptado

**Contexto:**  
Se necesita un motor de base de datos relacional para persistir los datos con soporte para consultas de búsqueda, integridad de datos y fácil despliegue local.

**Opciones consideradas:**
- MySQL 8.0
- PostgreSQL 16
- SQLite 3

**Decisión:**  
Se elige **MySQL 8.0**.

**Justificación:**
- Es el requisito explícito del proyecto.
- Amplia documentación, soporte en hosting compartido y herramientas de administración
  maduras (phpMyAdmin, MySQL Workbench).
- Compatible con MariaDB, lo que facilita migraciones a entornos alternativos.

**Consecuencias:**
- Se requiere un servidor MySQL corriendo localmente o accesible en red.
- El driver elegido es `mysql-connector-python` (oficial de Oracle, sin dependencias C).

---

## ADR-002: Interfaz de usuario — CLI interactiva

**Fecha:** 2026-05-12  

**Estado:** Aceptado

**Contexto:**  
La aplicación necesita una interfaz de usuario. Las opciones principales son CLI, GUI de escritorio o aplicación web.

**Opciones consideradas:**
- CLI con menús interactivos
- GUI con Tkinter
- API REST + frontend web

**Decisión:**  
Se implementa una **CLI interactiva** (menús en bucle).

**Justificación:**
- Menor complejidad de implementación y mantenimiento.
- No requiere dependencias adicionales de UI pesadas.
- Se alinea con el objetivo de "aplicación simple".
- Facilita el testing automatizado (entrada/salida estándar).

**Consecuencias:**
- La experiencia de usuario está limitada a terminal.
- Si en v2.0 se desea GUI/Web, la separación en capas (CLI → lógica → DB) facilita
  sustituir el `cli_agent` sin tocar la lógica de negocio.

---

## ADR-003: Librería de conexión a MySQL — `mysql-connector-python`

**Fecha:** 2026-05-12  
**Estado:** Aceptado

**Opciones consideradas:**
- `mysql-connector-python` (oficial Oracle)
- `PyMySQL` (puro Python, sin compilación)
- `SQLAlchemy` (ORM completo)

**Decisión:**  
Se usa **`mysql-connector-python`**.

**Justificación:**
- Driver oficial, mantenido activamente por Oracle.
- API directa: conexión → cursor → execute → fetchall. Sin abstracción ORM que añada
  complejidad innecesaria para una aplicación simple.
- Soporte nativo para prepared statements parametrizados.

**Consecuencias:**
- Las consultas SQL son explícitas en el código (ventaja para legibilidad en un
  proyecto educativo).
- Si se desea añadir soporte multi-DB en el futuro, habría que refactorizar hacia
  SQLAlchemy o un patrón Repository más abstracto.

---

## ADR-004: Estrategia de borrado — Soft Delete

**Fecha:** 2026-05-12  
**Estado:** Aceptado

**Contexto:**  
Al eliminar un dato, ¿se borra físicamente el registro o se marca como eliminado?

**Opciones consideradas:**
- Hard delete (DELETE FROM contactos WHERE id = ?)
- Soft delete (UPDATE contactos SET deleted_at = NOW() WHERE id = ?)

**Decisión:**  
**Soft delete** mediante columna `deleted_at DATETIME`.

**Justificación:**
- Permite recuperar contactos eliminados accidentalmente.
- Conserva el historial de datos para auditoría.
- Las consultas de listado y búsqueda filtran `WHERE deleted_at IS NULL` de forma
  transparente.

**Consecuencias:**
- Todas las consultas de lectura deben incluir el filtro `deleted_at IS NULL`.
- Si en el futuro se desea implementar "papelera de reciclaje", la base ya está puesta.

---

## ADR-005: Gestión de configuración — Variables de entorno con `.env`

**Fecha:** 2026-05-12  
**Estado:** Aceptado

**Contexto:**  
Las credenciales de MySQL (host, puerto, usuario, contraseña, nombre de base de datos)
deben estar disponibles en tiempo de ejecución sin hardcodearlas en el código.

**Opciones consideradas:**
- Archivo de configuración `config.ini`
- Variables de entorno puras (sin archivo)
- Archivo `.env` cargado con `python-dotenv`

**Decisión:**  
**Archivo `.env`** cargado mediante `python-dotenv`.

**Justificación:**
- Estándar de facto en proyectos Python modernos.
- El archivo `.env` se excluye del control de versiones (`.gitignore`).
- Se incluye un `.env.example` con claves sin valores para documentar las variables
  necesarias.
- Compatible con entornos CI/CD que inyectan variables de entorno nativas.

**Variables requeridas:**
```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecoroute_db
DB_USER=ecoroute_db
DB_PASSWORD=tu_contraseña_segura
```

---

## ADR-006: Formato de presentación de tablas — `tabulate`

**Fecha:** 2026-04-27  
**Estado:** Aceptado

**Opciones consideradas:**
- Formateo manual con `str.ljust()`
- Librería `tabulate`
- Librería `rich`

**Decisión:**  
**`tabulate`** con formato `grid` o `simple`.

**Justificación:**
- Librería ligera y sin subdependencias relevantes.
- API de una sola línea: `tabulate(rows, headers=..., tablefmt="grid")`.
- `rich` es más potente pero excesivo para las necesidades actuales.

**Consecuencias:**
- Añadir `tabulate` a `requirements.txt`.
- Si en el futuro se desea colorear la salida, se puede combinar con `colorama` o
  migrar a `rich` de forma localizada en el `cli_agent`.

---

## ADR-007: Patrón de arquitectura — Capas (Layered Architecture)

**Fecha:** 2026-05-12
**Estado:** Aceptado

**Decisión:**  
Se aplica una arquitectura en tres capas estrictas:

```
Presentación (cli_agent)  →  Lógica de negocio (logic_agent)  →  Datos (db_agent)
```

**Justificación:**
- Permite testear la lógica de negocio de forma aislada con mocks.
- Facilita el reemplazo de cualquier capa sin afectar a las demás.
- Consistente con los principios de `constitution.md`.

**Consecuencias:**  
Ver `architecture.md` para detalle de módulos y dependencias.
