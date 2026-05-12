# architecture.md - Arquitectura técnica #

## 1. Visión general
La aplicación sigue una **arquitectura en capas** (Layered Architecture) para separar la lógica de presentación de la persistencia de datos con tres niveles bien diferenciados. La comunicación entre capas es siempre descendente: la capa superior llama a la inferior; nunca al revés.

```
┌─────────────────────────────────────────────────────────┐
│                   CAPA DE PRESENTACIÓN                  │
│                   cli/  (cli_agent)                     │
│   main.py  ·  menu.py  ·  formatters.py                 │
└───────────────────────┬─────────────────────────────────┘
                        │  llama a
┌───────────────────────▼─────────────────────────────────┐
│                 CAPA DE LÓGICA DE NEGOCIO               │
│                logic/  (logic_agent)                    │
│   ecoroute_service.py  ·  validators.py  ·  models.py   │
└───────────────────────┬─────────────────────────────────┘
                        │  llama a
┌───────────────────────▼─────────────────────────────────┐
│                   CAPA DE DATOS                         │
│                   db/  (db_agent)                       │
│            connection.py  ·  migrations/                │
└───────────────────────┬─────────────────────────────────┘
                        │
                    ┌───▼───┐
                    │ MySQL │
                    └───────┘
```

## 2. Estructura de directorios

```
agenda_contactos/
│── .env                    # Variables de entorno (excluido de control de versiones)
│── .gitignore              # Ignora archivos sensibles y de entorno
│── README.md               # Documentación general del proyecto
├── main.py                 # Punto de entrada de la aplicación
│
├── cli/                    # Capa de presentación
│   ├── __init__.py
│   ├── menu.py             # Menú principal y submenús
│   └── formatters.py       # Formateo de tablas y mensajes
│
├── logic/                  # Capa de lógica de negocio
│   ├── __init__.py
│   ├── models.py           # Definición de la entidad `Vehículo`, `Rutas`, `Entregas`.
|   ├── services.py         # Orquesta los casos de use. Es el único punto de contacto entre CLI y repositorio.
│   └── validators.py       # Validación de campos
│
├── db/                     # Capa de acceso a datos
│   ├── __init__.py
│   ├── connection.py       # Clase encargada de la conexión y cierre de sesión.
│   └── contact_repo.py     # Repositorio de acceso a datos. Funciones específicas para sentencias SQL (INSERT, SELECT, UPDATE, DELETE).
|
|── migrations/              # Scripts SQL para crear tablas y esquemas
    ├── create_tables.sql
```
## 3. Descripción de módulos
### 3.1 `main.py`
Punto de entrada. Inicializa la conexión a la base de datos, instancia los
componentes de las capas y lanza el bucle principal del menú CLI.
### 3.2 `cli/menu.py`
Controla el flujo de navegación de la interfaz de usuario.

 ---
### 3.3 `cli/formatters.py`
Funciones de presentación puras (sin lógica de negocio).

---
### 3.4 `logic/models.py`
Define la estructura de datos del dominio. En este caso, las clases `Vehiculo`, `Entrega` y `Ruta` con sus atributos y métodos.
---
### 3.5 `logic/validators.py`
Funciones de validación sin efectos secundarios. Devuelven `True` o lanzan `ValidationError` con el código de error correspondiente.

---
### 3.6 `logic/services.py`
Orquesta los casos de uso. Es el único punto de contacto entre CLI y repositorio.

---
### 3.7 `db/connection.py`
Gestiona la conexión a MySQL.
Carga la configuración desde variables de entorno:
`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.

---
### 3.8 `db/contact_repo.py`
Repositorio de acceso a datos. Todas las consultas usan parámetros (`%s`).

---

### 3.9 `exceptions.py`
Jerarquía de excepciones del proyecto.

---

## 4. Dependencias externas (Opcional)

| Paquete                    | Versión  | Uso                            |
|----------------------------|----------|--------------------------------|
| `mysql-connector-python`   | >=8.3.0  | Conexión a MySQL               |
| `python-dotenv`            | >=1.0.0  | Carga de variables de entorno  |
| `tabulate`                 | >=0.9.0  | Formateo de tablas en consola  |

---
