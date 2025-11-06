# Student Service

Microservicio para la gestión de estudiantes del sistema SysAcad.

## 📋 Descripción

Este servicio maneja toda la información relacionada con estudiantes, incluyendo sus datos personales, documentos de identidad, y vinculación con especialidades. Es parte de una arquitectura de microservicios para un sistema académico.

## 🚀 Tecnologías

- **Python 3.14+**
- **Django 5.2.7**
- **Django REST Framework 3.16.1**
- **PostgreSQL** (producción)
- **SQLite** (desarrollo)

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

### Estudiantes
- `GET /students/` - Listar todos los estudiantes (paginado)
- `POST /students/` - Crear un nuevo estudiante
- `GET /students/{id}/` - Obtener un estudiante específico
- `PUT /students/{id}/` - Actualizar un estudiante
- `PATCH /students/{id}/` - Actualización parcial
- `DELETE /students/{id}/` - Eliminar un estudiante

### Tipos de Documento
- `GET /document-types/` - Listar tipos de documento
- `POST /document-types/` - Crear un tipo de documento
- `GET /document-types/{id}/` - Obtener un tipo específico
- `PUT /document-types/{id}/` - Actualizar un tipo
- `DELETE /document-types/{id}/` - Eliminar un tipo

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sysacad
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Para desarrollo con SQLite:
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

## 🛠️ Instalación y Ejecución

### Requisitos Previos
- Python 3.14+
- uv (gestor de paquetes Python)
- PostgreSQL (opcional, para producción)

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd student_management
```

2. **Instalar dependencias**
```bash
uv sync
```

3. **Configurar variables de entorno** .env


4. **Ejecutar migraciones**
```bash
uv run python manage.py migrate
```

5. **Crear superusuario (opcional)**
```bash
uv run python manage.py createsuperuser
```

6. **Iniciar el servidor**
```bash
uv run python manage.py runserver
```

La API estará disponible en `http://127.0.0.1:8000/`

