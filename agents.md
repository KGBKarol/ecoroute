# agents.md — Agenda de Contactos

## Visión general

Este documento describe los agentes (roles de IA o automatizados) que pueden operar sobre la aplicación de ecoroute. Cada agente tiene un propósito concreto, un conjunto de herramientas permitidas y restricciones explícitas.

| Rol | Responsabilidad |
| :--- | :--- |
| **db_agent** | Gestionar todas las operaciones de lectura y escritura sobre la base de datos MySQL. Es el único agente con acceso directo a la capa de persistencia. |
| **logic_agent** | Contener toda la lógica de negocio de las rutas etc...: validaciones, normalización de datos y orquestación de operaciones. |
| **cli_agent** | Proporcionar la interfaz de usuario en línea de comandos (CLI) para interactuar con la agenda. |
---
## Diagrama de interacción

```
Usuario
  │
  ▼
cli_agent  ──►  logic_agent  ──►  db_agent  ──►  MySQL
                                                   │
test_agent   ◄─────────────────────────────────────┘
            (entorno de pruebas aislado)
```

---