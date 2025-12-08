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

## 🔗 Dependencias Externas

Este microservicio requiere de servicios externos en ejecución para funcionar correctamente:

### 1. Traefik (Reverse Proxy & Load Balancer)

**Descripción:** Traefik gestiona el enrutamiento, TLS, circuit breaker, retry y rate limiting para todos los microservicios del sistema.

**Repositorio:** El servicio de Traefik debe estar corriendo en un repositorio/proyecto separado (típicamente `traefik-gateway` o similar).

**Red Docker:** `mired` (external network)

**Configuración requerida:**
- Traefik debe estar conectado a la red Docker `mired`
- Debe tener los entrypoints `http` (puerto 80) y `https` (puerto 443) configurados
- Debe tener el provider Docker habilitado para leer labels de los contenedores

**Verificar Traefik:**
```bash
# Verificar que Traefik está corriendo
docker ps | grep traefik

# Verificar que la red mired existe
docker network ls | grep mired

# Crear la red si no existe
docker network create mired
```

**Endpoints expuestos por Traefik para este servicio:**
- **HTTP:** `http://alumnos.universidad.localhost/api/v1/`
- **HTTPS:** `https://alumnos.universidad.localhost/api/v1/`
- **Health:** `http://alumnos.universidad.localhost/health/`

### 2. Mock de Gestión Académica

**Descripción:** Servicio mock que simula el sistema de gestión académica (especialidades, validaciones, etc.).

**Repositorio:** Debe estar corriendo en un repositorio/proyecto separado (típicamente `mock-gestion-academica` o similar).

**Puerto:** 8080 (configurable via `ACADEMIC_SERVICE_URL`)

**Red Docker:** `mired` (debe estar en la misma red que ms-student)

**Configuración requerida:**
- El mock debe estar corriendo y accesible en `http://host.docker.internal:8001` (desarrollo) o en la red `mired` (producción)
- Debe exponer endpoints para validar especialidades y tipos de documento

**Verificar Mock Académico:**
```bash
# Verificar que el mock está corriendo
docker ps | grep mock-gestion-academica

# O si corre en host local
curl http://localhost:8001/health
```

**Variables de entorno relacionadas:**
```env
# En .env o .env.prod
ACADEMIC_SERVICE_URL=http://host.docker.internal:8001  # Desarrollo
ACADEMIC_SERVICE_URL=http://mock-gestion-academica:8080  # Producción con Docker
```

### 🎯 Guía Completa: Cómo Hacer Funcionar el Proyecto

Esta sección explica **paso a paso** cómo levantar todo el ecosistema de microservicios para que funcione correctamente.

#### 📚 Entendiendo la Arquitectura

El proyecto `ms-student` **no funciona de manera aislada**. Es parte de un ecosistema de microservicios que se comunican entre sí:

```
┌─────────────────┐
│   Navegador     │
└────────┬────────┘
         │ HTTP/HTTPS
         ↓
┌─────────────────────────────────────────┐
│         Traefik (Reverse Proxy)         │
│  - Enrutamiento por Host                │
│  - TLS/SSL                              │
│  - Circuit Breaker                      │
│  - Rate Limiting                        │
│  - Retry Logic                          │
└────────┬────────────────────────────────┘
         │ Red: mired
         ↓
┌─────────────────────────────────────────┐
│      ms-student (Este Servicio)         │
│  - API REST de estudiantes              │
│  - Gestión de documentos                │
│  - Caché con Redis                      │
└────────┬────────────────────────────────┘
         │ HTTP interno
         ↓
┌─────────────────────────────────────────┐
│    Mock Gestión Académica               │
│  - Validación de especialidades         │
│  - Catálogo de tipos de documento       │
└─────────────────────────────────────────┘
```

#### 🔧 Configuración de Conectividad: Paso a Paso

##### Paso 1: Crear la red Docker compartida

Todos los servicios deben estar en la misma red Docker para poder comunicarse.

```bash
# Crear la red 'mired' (si no existe)
docker network create mired

# Verificar que se creó correctamente
docker network ls | grep mired
```

**¿Por qué?** Docker aísla los contenedores por defecto. La red `mired` actúa como un "puente" que permite que Traefik, ms-student y el mock académico se vean entre sí.

##### Paso 2: Configurar y levantar Traefik (Servicio 1/3)

Traefik es el **punto de entrada** de todas las peticiones. Debe estar corriendo primero.

```bash
# Navegar al repositorio de Traefik (ajusta la ruta según tu estructura)
cd ../traefik-gateway  # o la ruta donde tengas Traefik

# Verificar que el docker-compose.yml de Traefik incluya:
# networks:
#   mired:
#     external: true

# Levantar Traefik
docker-compose up -d

# Verificar que está corriendo
docker ps | grep traefik

# Verificar que está en la red mired
docker network inspect mired
```

**¿Qué hace Traefik?**
- Escucha en los puertos 80 (HTTP) y 443 (HTTPS)
- Lee las **labels** de los contenedores Docker para configurar rutas automáticamente
- Cuando recibe una petición a `alumnos.universidad.localhost`, la redirige al contenedor `ms-student`
- Aplica circuit breaker, retry y rate limiting según las labels configuradas

**Endpoints de Traefik:**
- Dashboard: `http://localhost:8080` (si está habilitado)
- API: `http://localhost:8080/api/rawdata` (muestra configuración dinámica)

##### Paso 3: Configurar y levantar el Mock Académico (Servicio 2/3)

El mock simula el sistema de gestión académica real.

```bash
# Navegar al repositorio del mock (ajusta la ruta según tu estructura)
cd ../mock-gestion-academica  # o donde esté tu mock

# Verificar que el docker-compose.yml del mock incluya:
# networks:
#   mired:
#     external: true

# Levantar el mock
docker-compose up -d

# Verificar que está corriendo
docker ps | grep mock-gestion-academica

# Probar el endpoint de salud
curl http://localhost:8001/health
# Debería responder con: {"status": "healthy"}
```

**¿Qué hace el Mock?**
- Provee endpoints para validar que una especialidad existe (por ID)
- Provee endpoints para validar tipos de documento
- Simula tiempos de respuesta y posibles errores del servicio real

**Configuración en ms-student:**
```env
# En .env o .env.prod
ACADEMIC_SERVICE_URL=http://host.docker.internal:8001  # Desarrollo (acceso desde container al host)
# o
ACADEMIC_SERVICE_URL=http://mock-gestion-academica:8080  # Producción (ambos en red mired)
```

##### Paso 4: Configurar y levantar ms-student (Servicio 3/3)

Ahora sí, levantamos nuestro microservicio de estudiantes.

```bash
# Navegar al directorio de ms-student
cd ../sysacad-microservices/ms-student

# Verificar que existe el archivo .env (desarrollo) o .env.prod (producción)
ls -la .env*

# Verificar que docker-compose.yml incluya:
# networks:
#   mired:
#     external: true
# y las labels de Traefik estén configuradas

# Levantar el servicio (desarrollo)
docker-compose up -d

# O para producción:
docker-compose -f docker-compose.prod.yml up -d --build

# Ver los logs en tiempo real
docker-compose logs -f alumnos-service

# Verificar que está corriendo
docker ps | grep alumnos-service
```

**¿Qué hace ms-student?**
- Expone la API REST en el puerto 8000 **dentro del contenedor**
- Se registra automáticamente en Traefik mediante las **labels** del docker-compose
- Se conecta a PostgreSQL (contenedor `postgres`) para almacenar datos
- Se conecta a Redis (contenedor `redis`) para caché
- Se conecta al mock académico para validar especialidades

##### Paso 5: Ejecutar migraciones y datos iniciales

```bash
# Ejecutar migraciones de Django
docker-compose exec alumnos-service uv run python manage.py migrate

# Crear superusuario (opcional, para Django Admin)
docker-compose exec alumnos-service uv run python manage.py createsuperuser

# Cargar datos iniciales de tipos de documento (si tienes fixtures)
docker-compose exec alumnos-service uv run python manage.py loaddata document_types
```

##### Paso 6: Verificar la conectividad completa

Ahora probamos que todo el flujo funciona:

**A) Verificar que Traefik puede alcanzar ms-student:**
```bash
# Petición HTTP a través de Traefik (usa el Host configurado)
curl http://alumnos.universidad.localhost/health/

# Debería responder:
# {"status":"healthy","database":"connected"}
```

**B) Verificar que ms-student puede alcanzar el mock académico:**
```bash
# Desde dentro del contenedor de ms-student
docker exec ms-student-alumnos-service-1 curl http://host.docker.internal:8001/health

# Debería responder:
# {"status":"healthy"}
```

**C) Probar un flujo completo (crear un estudiante):**
```bash
# Crear un estudiante (esto validará la especialidad con el mock)
curl -X POST http://alumnos.universidad.localhost/api/v1/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan",
    "last_name": "Pérez",
    "document_number": "12345678",
    "document_type_id": 1,
    "birth_date": "2000-01-15",
    "gender": "M",
    "student_number": 50001,
    "enrollment_date": "2024-03-01",
    "specialty_id": 1
  }'

# Si todo funciona correctamente:
# - Traefik enruta la petición a ms-student
# - ms-student valida la especialidad consultando al mock académico
# - ms-student guarda el estudiante en PostgreSQL
# - ms-student cachea el resultado en Redis
# - Responde con el estudiante creado (201 Created)
```

#### 🐛 Troubleshooting: Problemas Comunes

##### Problema 1: "Connection refused" al acceder vía Traefik

**Síntoma:**
```bash
curl http://alumnos.universidad.localhost/health/
# curl: (7) Failed to connect to alumnos.universidad.localhost port 80: Connection refused
```

**Solución:**
1. Verificar que Traefik está corriendo: `docker ps | grep traefik`
2. Verificar que ms-student está en la red `mired`: `docker network inspect mired`
3. Verificar los logs de Traefik: `docker logs <traefik-container-id>`
4. Asegurar que `/etc/hosts` (Linux/Mac) o `C:\Windows\System32\drivers\etc\hosts` (Windows) contiene:
   ```
   127.0.0.1 alumnos.universidad.localhost
   ```

##### Problema 2: "Cannot reach academic service"

**Síntoma:**
```bash
# Al crear un estudiante, error 500 con mensaje sobre conectividad
```

**Solución:**
1. Verificar que el mock está corriendo: `docker ps | grep mock`
2. Probar acceso directo al mock: `curl http://localhost:8001/health`
3. Revisar la variable `ACADEMIC_SERVICE_URL` en el `.env`:
   ```env
   # Desarrollo (desde container a host)
   ACADEMIC_SERVICE_URL=http://host.docker.internal:8001
   
   # Producción (ambos en red mired)
   ACADEMIC_SERVICE_URL=http://mock-gestion-academica:8080
   ```
4. Verificar logs de ms-student: `docker-compose logs alumnos-service`

##### Problema 3: "Network mired not found"

**Síntoma:**
```bash
docker-compose up -d
# ERROR: Network mired declared as external, but could not be found
```

**Solución:**
```bash
# Crear la red manualmente
docker network create mired

# Volver a levantar el servicio
docker-compose up -d
```

##### Problema 4: Base de datos no conecta

**Síntoma:**
```bash
# Logs muestran: "could not connect to server: Connection refused"
```

**Solución:**
1. Verificar que PostgreSQL está corriendo: `docker ps | grep postgres`
2. Esperar a que el healthcheck pase (puede tardar 10-30s en el primer inicio)
3. Verificar logs de PostgreSQL: `docker-compose logs postgres`
4. Verificar credenciales en `.env`:
   ```env
   DB_HOST=postgres  # Nombre del servicio en docker-compose
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=sysacad
   ```

#### 📊 Resumen: Orden de Inicio

Para que todo funcione correctamente, el orden importa:

```bash
# 1️⃣ Crear red compartida (una sola vez)
docker network create mired

# 2️⃣ Levantar Traefik (primer servicio)
cd ../traefik-gateway
docker-compose up -d

# 3️⃣ Levantar Mock Académico (segundo servicio)
cd ../mock-gestion-academica
docker-compose up -d

# 4️⃣ Levantar ms-student (tercer servicio)
cd ../sysacad-microservices/ms-student
docker-compose up -d

# 5️⃣ Ejecutar migraciones
docker-compose exec alumnos-service uv run python manage.py migrate

# 6️⃣ Verificar
curl http://alumnos.universidad.localhost/health/
```

#### 🔄 Detener Todo el Ecosistema

```bash
# Detener ms-student
cd sysacad-microservices/ms-student
docker-compose down

# Detener mock académico
cd ../../mock-gestion-academica
docker-compose down

# Detener Traefik
cd ../traefik-gateway
docker-compose down

# (Opcional) Eliminar la red
docker network rm mired
```

## 🛠️ Instalación y Ejecución

### Requisitos Previos
- Docker & Docker Compose
- Python 3.14+ (para desarrollo local sin Docker)
- uv (gestor de paquetes Python)
- **Traefik corriendo** (ver sección Dependencias Externas)
- **Mock de Gestión Académica corriendo** (ver sección Dependencias Externas)
- **Red Docker `mired` creada** (ver sección Dependencias Externas)

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
Integrantes:
Pablo Geyer
Valentin Rubio
Santiago Calzolari
Luciano Castro
Santiago Oses

---

**Última actualización:** Diciembre 2025  
**Versión:** 1.0.0  
**Status:** ✅ Producción Ready (152/152 tests passing)

