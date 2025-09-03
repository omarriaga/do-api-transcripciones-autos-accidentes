
# do-api-transcripciones-autos-accidentes

API para consultar transcripciones de conversaciones relacionadas con autos y accidentes. Permite obtener información detallada de las interacciones, participantes y análisis de sentimiento.

## Descripción

Esta API expone endpoints para consultar transcripciones almacenadas en una base de datos PostgreSQL. Utiliza FastAPI como framework principal y está diseñada para integrarse con sistemas de gestión y análisis de llamadas. El modelo principal es `Transcripcion`, que contiene atributos relevantes de cada conversación.

## Características

- **Framework**: FastAPI
- **Base de datos**: PostgreSQL (con SQLAlchemy y asyncpg)
- **Arquitectura**: Asíncrona, Monolítica
- **Documentación**: Swagger UI, ReDoc
- **Autenticación**: (No implementada, pero preparado para integración con Google Cloud Secret Manager)

## Estructura del Proyecto

```
do-api-transcripciones-autos-accidentes/
├── main.py                 # Punto de entrada FastAPI
├── requirements.txt        # Dependencias
├── Dockerfile              # Contenedor
├── cloudbuild.yaml         # CI/CD
├── models/
│   └── models.py           # Modelos de datos (Transcripcion, DataRequest, DataResponse)
├── utils/
│   ├── connect_sql.py      # Conexión y helpers para base de datos
│   └── request_postgres.py # Lógica de consulta a la base de datos
└── helpers/
        └── credentials_helper.py # Obtención de credenciales
```

## Modelo de Datos

Modelo principal: `Transcripcion`

```python
class Transcripcion(BaseModel):
        id_conversacion: Optional[str]
        dnis: str
        id_cola: str
        nombre_cola: str
        id_usuario: str
        nombre_usuario: str
        username: str
        emisor: str
        fecha_inicio_participante: datetime
        fecha_fin_participante: datetime
        equipo: str
        sentimiento: float
        tendencia_sentimiento: str
        transcripcion: str
        confianza: float
        tipo_direccion: str
        hora_transcripciones_mil: int
        fecha_cargue: datetime
```

## Endpoints

### GET /api/transcripciones/autos-accidentes

Consulta transcripciones de conversaciones.


**Parámetros (en el body):**
- `dni` (str): DNI del participante
- `fecha` (datetime): Fecha de referencia
- `gestor` (str): Nombre del gestor

**Ejemplo de request body:**
```json
{
    "dni": "123456789",
    "fecha": "2025-09-02T00:00:00",
    "gestor": "Juan Perez"
}
```

**Respuesta exitosa (200):**
```json
{
    "data": [
        {
            "id_conversacion": "abc123",
            "dnis": "123456789",
            "id_cola": "1",
            "nombre_cola": "Accidentes",
            "id_usuario": "u001",
            "nombre_usuario": "Juan Perez",
            "username": "jperez",
            "emisor": "cliente",
            "fecha_inicio_participante": "2025-09-02T10:00:00",
            "fecha_fin_participante": "2025-09-02T10:30:00",
            "equipo": "Soporte",
            "sentimiento": 0.85,
            "tendencia_sentimiento": "Positivo",
            "transcripcion": "Texto de la conversación...",
            "confianza": 0.95,
            "tipo_direccion": "Entrante",
            "hora_transcripciones_mil": 1693651200000,
            "fecha_cargue": "2025-09-02T11:00:00"
        }
    ]
}
```

**Respuesta cuando no se encuentra (404):**
```json
{
    "error": "No hay conversaciones para mostrar"
}
```

### GET /

Redirige a la documentación de la API (`/docs`).

## Instalación y Configuración

### Prerrequisitos

- Python 3.x
- Acceso a la base de datos PostgreSQL
- Variables de entorno configuradas (credenciales en Google Cloud Secret Manager)

### Instalación local

1. Clonar el repositorio:
```bash
git clone <URL-del-repositorio>
cd do-api-transcripciones-autos-accidentes
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
set VARIABLE=valor
```

4. Ejecutar la aplicación:
```bash
python main.py
```

### Despliegue con Docker

1. Construir la imagen:
```bash
docker build -t do-api-transcripciones-autos-accidentes .
```

2. Ejecutar el contenedor:
```bash
docker run -p 8080:8080 do-api-transcripciones-autos-accidentes
```

## Uso de la API

### Ejemplo con cURL

```bash
curl -X GET "http://localhost:8080/api/transcripciones/autos-accidentes" -H "accept: application/json"
```

### Ejemplo con Python

```python
import requests

url = "http://localhost:8080/api/transcripciones/autos-accidentes"
response = requests.get(url)
print(response.json())
```

## Documentación Interactiva

Accede a la documentación en:

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

## Tecnologías Utilizadas

- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Pydantic
- Google Cloud Secret Manager
- Uvicorn




