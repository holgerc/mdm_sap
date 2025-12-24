# MDM SAP - Master Data Management System

Sistema de gestión de datos maestros con arquitectura 100% parametrizable.

## Requisitos

- Docker 20.10+
- Docker Compose 2.0+

## Inicio Rápido

```bash
# 1. Construir las imágenes
make build

# 2. Iniciar los servicios
make up

# 3. Ejecutar el seed inicial (crear datos de ejemplo)
make seed
```

## URLs

| Servicio | URL |
|----------|-----|
| API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/api/v1/docs |
| API Docs (ReDoc) | http://localhost:8000/api/v1/redoc |
| Health Check | http://localhost:8000/api/v1/health |
| PgAdmin | http://localhost:5050 (con `make pgadmin`) |

## Credenciales por Defecto

### API
- **Usuario:** admin
- **Contraseña:** admin123

### PostgreSQL
- **Host:** localhost:5432
- **Database:** mdm_db
- **Usuario:** mdm
- **Contraseña:** mdm123

### PgAdmin
- **Email:** admin@mdm.local
- **Contraseña:** admin123

## Comandos Disponibles

```bash
make build      # Construir imágenes Docker
make up         # Iniciar servicios
make down       # Detener servicios
make logs       # Ver logs
make shell      # Abrir shell en backend
make seed       # Cargar datos iniciales
make clean      # Limpiar todo (contenedores + volúmenes)
make pgadmin    # Iniciar con PgAdmin
```

## Estructura del Proyecto

```
mdm_sap/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # Endpoints REST
│   │   ├── core/               # Configuración y seguridad
│   │   ├── models/             # Modelos SQLAlchemy
│   │   ├── schemas/            # Schemas Pydantic
│   │   └── main.py             # Aplicación FastAPI
│   ├── Dockerfile
│   └── requirements.txt
├── scripts/
│   ├── init-db.sql             # Script de inicialización DB
│   └── seed_data.py            # Script de datos iniciales
├── docker-compose.yml
├── Makefile
└── README.md
```

## API Endpoints Principales

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrar usuario
- `GET /api/v1/auth/me` - Usuario actual

### Entidades
- `GET /api/v1/entities` - Listar entidades
- `POST /api/v1/entities` - Crear entidad
- `GET /api/v1/entities/{id}` - Obtener entidad
- `PUT /api/v1/entities/{id}` - Actualizar entidad
- `DELETE /api/v1/entities/{id}` - Eliminar entidad

### Atributos
- `GET /api/v1/attributes` - Listar atributos
- `POST /api/v1/attributes` - Crear atributo
- `GET /api/v1/attributes/{id}` - Obtener atributo
- `PUT /api/v1/attributes/{id}` - Actualizar atributo

### Catálogos
- `GET /api/v1/catalogs` - Listar catálogos
- `POST /api/v1/catalogs` - Crear catálogo
- `GET /api/v1/catalogs/{id}/values` - Valores del catálogo
- `POST /api/v1/catalogs/{id}/values` - Agregar valor

## Módulos del Sistema

1. **Entidades** - Definición dinámica de datos maestros
2. **Atributos** - Configuración granular de campos
3. **Validaciones** - Reglas de validación por campo
4. **Transformaciones** - Pipeline de transformación
5. **Catálogos** - Gestión de valores con jerarquías
6. **Relaciones** - Configuración entre entidades
7. **Calidad de Datos** - Reglas DQ
8. **Match & Merge** - Deduplicación
9. **Workflows** - Flujos de aprobación
10. **Seguridad** - Control de acceso granular
11. **Integraciones** - Conectores configurables
12. **Auditoría** - Trazabilidad completa
13. **Notificaciones** - Sistema multicanal
14. **UI Dinámico** - Formularios configurables
15. **Multiidioma** - Soporte i18n

## Licencia

Propietario - Todos los derechos reservados.
