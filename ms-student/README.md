# Student Service

Microservicio para la gestión de estudiantes del sistema SysAcad.

## 📋 Descripción

Este servicio maneja toda la información relacionada con estudiantes, incluyendo sus datos personales, documentos de identidad, y vinculación con especialidades. Es parte de una arquitectura de microservicios para un sistema académico.

## 🚀 Tecnologías

- **Python 3.14**
- **Django 6.0**
- **Django REST Framework 3.16.1**
- **PostgreSQL 17**
- **Redis 7-alpine** (caché distribuida con persistencia AOF)
- **Traefik v3.5** (reverse proxy y load balancer)
- **Docker & Docker Compose**
- **pytest 9.0.1** (testing framework)

## 📦 Estructura del Proyecto

```
student_management/
├── app/                      # Aplicación principal
│   ├── models/              # Modelos de datos
│   │   ├── student.py       # Modelo Student
│   │   └── document_type.py # Modelo DocumentType
│   ├── repositories/        # Capa de acceso a datos
│   ├── serializers/         # Serializadores DRF
│   ├── services/            # Lógica de negocio
│   └── views/               # ViewSets de la API
├── config/                  # Configuración Django
├── tests/                   # Tests unitarios
└── manage.py               # CLI de Django
```

## 🗄️ Modelos de Datos

### Student (Estudiante)
- `first_name`: Nombre
- `last_name`: Apellido
- `document_number`: Número de documento
- `document_type`: Tipo de documento (FK)
- `birth_date`: Fecha de nacimiento
- `gender`: Género (M/F/O)
- `student_number`: Legajo (único)
- `enrollment_date`: Fecha de inscripción
- `specialty_id`: ID de la especialidad (referencia externa)

### DocumentType (Tipo de Documento)
- `name`: Tipo (DNI, LC, LE, PASAPORTE)
- `description`: Descripción del tipo

## 🔌 API Endpoints

**Base URL (Producción):** `http://alumnos.universidad.localhost/api/v1/`  
**Base URL (Desarrollo):** `http://localhost:8000/api/v1/`

### Estudiantes (Full CRUD)
- `GET /api/v1/students/` - Listar todos los estudiantes (paginado)
- `POST /api/v1/students/` - Crear un nuevo estudiante
- `GET /api/v1/students/{id}/` - Obtener un estudiante específico
- `PUT /api/v1/students/{id}/` - Actualizar un estudiante
- `PATCH /api/v1/students/{id}/` - Actualización parcial
- `DELETE /api/v1/students/{id}/` - Eliminar un estudiante (soft delete)

#### Ejemplo JSON - Crear Estudiante
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "document_number": "12345678",
  "document_type_id": 1,
  "birth_date": "2000-01-15",
  "gender": "M",
  "student_number": 50001,
  "enrollment_date": "2024-03-01",
  "specialty_id": 1
}
```

### Tipos de Documento (Read-Only Catalog)
- `GET /api/v1/document-types/` - Listar tipos de documento
- `GET /api/v1/document-types/{id}/` - Obtener un tipo específico

**Nota:** Los tipos de documento son un catálogo fijo (DNI, LC, LE, PASAPORTE) y solo permiten operaciones de lectura.

### Health Check
- `GET /health/` - Estado del servicio y conectividad de base de datos

```json
{
  "status": "healthy",
  "database": "connected"
}
```

## ⚙️ Configuración

### Variables de Entorno

#### Desarrollo (`docker-compose.yml`)
```env
# Django
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=*

# Base de datos
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sysacad
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Servicios externos
GESTION_ACADEMICA_URL=http://mock-gestion-academica:8080
```

#### Producción (`docker-compose.prod.yml`)
```env
# Django
SECRET_KEY=production-secret-key-use-secrets-manager
DEBUG=False
ALLOWED_HOSTS=alumnos.universidad.localhost

# Base de datos
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sysacad_alumnos_prod
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432

# Redis (con persistencia AOF)
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Servicios externos
GESTION_ACADEMICA_URL=http://mock-gestion-academica:8080

# Traefik
TRAEFIK_DOMAIN=alumnos.universidad.localhost
```

## 🛠️ Instalación y Ejecución

### Requisitos Previos
- Docker & Docker Compose
- Python 3.14+ (para desarrollo local sin Docker)
- uv (gestor de paquetes Python)

### Ejecución con Docker (Recomendado)

#### Modo Desarrollo
```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ejecutar migraciones
docker-compose exec alumnos-service uv run python manage.py migrate

# Crear superusuario
docker-compose exec alumnos-service uv run python manage.py createsuperuser

# Acceder al servicio
# API: http://localhost:8000/api/v1/
# Health: http://localhost:8000/health/
```

#### Modo Producción
```bash
# Levantar con Traefik y configuración de producción
docker-compose -f docker-compose.prod.yml up -d --build

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Ejecutar migraciones
docker-compose -f docker-compose.prod.yml exec alumnos-service uv run python manage.py migrate

# Acceder al servicio (vía Traefik)
# HTTP: http://alumnos.universidad.localhost/api/v1/
# HTTPS: https://alumnos.universidad.localhost/api/v1/
# Health: http://alumnos.universidad.localhost/health/
```

### Desarrollo Local (sin Docker)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd sysacad-microservices/ms-student
```

2. **Instalar dependencias**
```bash
uv sync
```

3. **Configurar variables de entorno**
Crear archivo `.env` con las variables necesarias

4. **Ejecutar migraciones**
```bash
uv run python manage.py migrate
```

5. **Iniciar el servidor**
```bash
uv run python manage.py runserver
```

La API estará disponible en `http://127.0.0.1:8000/api/v1/`

## 🧪 Testing

El proyecto incluye una suite completa de tests con **100% de cobertura** en las capas principales.

### Ejecutar Tests

#### Con Docker (Producción)
```bash
# Instalar pytest en el contenedor
docker exec ms-student-alumnos-service-1 uv pip install pytest pytest-django pytest-cov

# Ejecutar todos los tests
docker exec ms-student-alumnos-service-1 pytest tests/ -v

# Ejecutar tests con cobertura
docker exec ms-student-alumnos-service-1 pytest tests/ --cov=app --cov-report=html

# Ejecutar tests específicos
docker exec ms-student-alumnos-service-1 pytest tests/views/ -v
```

#### Desarrollo Local
```bash
# Ejecutar todos los tests
uv run pytest tests/ -v

# Con cobertura
uv run pytest tests/ --cov=app --cov-report=html

# Tests específicos
uv run pytest tests/models/ -v
```

### Estructura de Tests
```
tests/
├── models/              # Tests de modelos (31 tests)
├── repositories/        # Tests de repositorios (27 tests)
├── serializers/         # Tests de serializers (43 tests)
├── services/            # Tests de servicios (27 tests)
└── views/               # Tests de views/ViewSets (24 tests)

Total: 152 tests ✅
```

## 🏗️ Arquitectura

### Patrón de Capas
```
Views (API) → Services (Business Logic) → Repositories (Data Access) → Models (ORM)
```

- **Views**: ViewSets de DRF que exponen endpoints REST
- **Services**: Lógica de negocio, validaciones, y orquestación
- **Repositories**: Abstracción de acceso a datos
- **Models**: Modelos Django ORM

### Caché con Redis
- **Document Types**: Caché de 10 minutos (datos estáticos)
- **Students**: Caché individual por ID (5 minutos)
- **Invalidación**: Automática en operaciones CREATE/UPDATE/DELETE

### Traefik (Producción)
- **Reverse Proxy**: Enrutamiento HTTP/HTTPS
- **Load Balancer**: Sticky sessions habilitadas
- **Circuit Breaker**: Protección contra servicios caídos
- **Rate Limiting**: 100 req/seg por IP
- **Health Checks**: Verificación automática cada 10s

## 🔒 Validaciones

### Estudiantes
- ✅ Nombre y apellido: Solo letras, espacios, guiones (title case automático)
- ✅ Número de documento: Alfanumérico, 5-20 caracteres, único
- ✅ Fecha de nacimiento: Entre 14 y 100 años
- ✅ Edad al inscribirse: Entre 16 y 90 años
- ✅ Fecha de inscripción: Entre 1900 y 10 años en el futuro
- ✅ Legajo: Número positivo único
- ✅ Género: M, F, O (Masculino, Femenino, Otro)
- ✅ Especialidad: Validación contra servicio de gestión académica

### Tipos de Documento
- ✅ Nombre: Único (DNI, LC, LE, PASAPORTE)
- ✅ Solo lectura vía API (catálogo fijo)

## 📊 Monitoreo

### Logs Estructurados
El servicio genera logs en formato JSON con la siguiente información:
- Timestamp
- Nivel (INFO, WARNING, ERROR)
- Mensaje
- Contexto (request_id, user, etc.)

### Métricas Disponibles
- Health check endpoint para monitoring
- Redis cache hit/miss rates (en logs)
- Tiempos de respuesta por endpoint

## 🛠️ Comandos Útiles

### Docker
```bash
# Rebuild completo
docker-compose -f docker-compose.prod.yml up -d --build

# Ver logs en tiempo real
docker-compose -f docker-compose.prod.yml logs -f alumnos-service

# Acceder al contenedor
docker exec -it ms-student-alumnos-service-1 bash

# Limpiar volúmenes y rebuild
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
```

### Django Management
```bash
# Crear migraciones
docker exec ms-student-alumnos-service-1 uv run python manage.py makemigrations

# Aplicar migraciones
docker exec ms-student-alumnos-service-1 uv run python manage.py migrate

# Crear superusuario
docker exec -it ms-student-alumnos-service-1 uv run python manage.py createsuperuser

# Shell interactivo
docker exec -it ms-student-alumnos-service-1 uv run python manage.py shell
```

### Testing en Producción
```bash
# Test endpoints con curl
curl http://alumnos.universidad.localhost/health/
curl http://alumnos.universidad.localhost/api/v1/document-types/
curl http://alumnos.universidad.localhost/api/v1/students/

# Con datos
curl -X POST http://alumnos.universidad.localhost/api/v1/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Usuario",
    "document_number": "99999999",
    "document_type_id": 1,
    "birth_date": "2000-01-01",
    "gender": "M",
    "student_number": 99999,
    "enrollment_date": "2024-03-01",
    "specialty_id": 1
  }'
```

## 📝 Notas Técnicas

### Soft Delete
Los estudiantes eliminados no se borran físicamente de la base de datos. Se marcan con:
- `is_active = False`
- `deleted_at = timestamp`

Esto permite auditoría y recuperación de datos si es necesario.

### Integración con Gestión Académica
El servicio valida `specialty_id` contra el microservicio de gestión académica:
- URL: `http://mock-gestion-academica:8080/api/v1/especialidades/{id}`
- Circuit breaker activado después de 3 fallos consecutivos
- Timeout: 5 segundos

### Caché Strategy
- **Write-Through**: Los datos se escriben en DB y caché simultáneamente
- **Cache-Aside**: Lectura desde caché, si miss → DB → guardar en caché
- **TTL**: 10 min para document types, 5 min para students

## 🚀 Roadmap / Mejoras Futuras

- [ ] Implementar paginación cursor-based para mejor performance
- [ ] Agregar validación de edad mínima en inscripción (actualmente permite cualquier edad >= 16)
- [ ] Crear ForeignKey real para `specialty_id` con sincronización event-driven
- [ ] Implementar estados de ciclo de vida del estudiante (Activo, Inactivo, Graduado)
- [ ] Agregar audit trail completo (quién modificó qué y cuándo)
- [ ] Validación de formato de documento según tipo (DNI: 8 dígitos, etc.)
- [ ] Soporte para nombres con apóstrofes y caracteres internacionales
- [ ] Implementar rate limiting por usuario (además de por IP)
- [ ] Agregar métricas con Prometheus/Grafana
- [ ] CI/CD pipeline con GitHub Actions

## 📄 Licencia

Este proyecto es parte del sistema SysAcad y está protegido por los términos de licencia correspondientes.

## 👥 Equipo de Desarrollo

Desarrollado por **Zapallo Code** para el sistema de gestión académica SysAcad.

---

**Última actualización:** Diciembre 2025  
**Versión:** 1.0.0  
**Status:** ✅ Producción Ready (152/152 tests passing)

