# Kurios Visits API

Backend de la plataforma **Kurios** para gestionar las visitas que se realizan a los colegios. Expone una API REST construida con **FastAPI** sobre **PostgreSQL** (Supabase) y sigue una arquitectura por *features* (vertical slices) con capas separadas: rutas, casos de uso, repositorios, datasources y modelos.

- **Versión:** 1.0.1
- **Recursos actuales:** `/schools`, `/teachers` y `/visits`
- **Documentación interactiva:** `/docs` (Swagger UI) y `/redoc`

---

## Stack

| Componente | Tecnología |
|---|---|
| Framework HTTP | FastAPI 0.115 |
| Servidor ASGI | Uvicorn 0.34 |
| ORM | SQLAlchemy 2.0 (modo sincrónico) |
| Driver | psycopg2-binary |
| Validación / settings | Pydantic 2 + pydantic-settings |
| Base de datos | PostgreSQL (Supabase) |
| Tests | pytest + httpx |

---

## Arquitectura

Cada *feature* (`schools`, `teachers`, `visits`) es una rebanada vertical con las mismas capas. El flujo de una petición es siempre el mismo:

```
HTTP Request
    │
    ▼
routes/schools_routes.py               Valida query params / body y arma la respuesta
    │  Depends(get_school_use_case)
    ▼
use_cases/schools_use_cases.py         Reglas de negocio y orquestación
    │  SchoolsRepositoryInterface  (contrato)
    ▼
repository/school_repository_impl.py   Implementación del contrato de acceso a datos
    │
    ▼
datasources/bd/schools_datasource.py   Consultas con SQLAlchemy
    │
    ▼
models/schools_models.py  ──────────►  PostgreSQL (Supabase)
```

Puntos clave:

- **Inyección de dependencias** en `features/<feature>/dependencies.py`: FastAPI resuelve la cadena `Session → Datasource → Repository → UseCase` con `Depends`.
- **Interfaces** (`repository/*_interface.py`) para que el caso de uso no dependa de SQLAlchemy.
- **Schemas** (`schemas/*_schemas.py`) separados de los modelos ORM: la API nunca expone la tabla tal cual.
- Los imports son siempre absolutos desde la raíz del paquete: `from app.core...`, `from app.features...`. Ejecuta siempre desde `back/` para que `app` sea importable.

### Estructura de carpetas

```
back/
├── app/
│   ├── main.py                     # creación de la app FastAPI, CORS, lifespan
│   ├── core/
│   │   ├── config.py               # Settings (pydantic-settings) + VERSION
│   │   ├── database.py             # engine, SessionLocal, Base, get_db
│   │   └── logger.py               # logger compartido
│   ├── routes/
│   │   └── routes.py               # init_routes(): registra todos los routers
│   └── features/
│       ├── schools/
│       │   ├── routes/schools_routes.py
│       │   ├── use_cases/schools_use_cases.py
│       │   ├── repository/school_repository_interface.py
│       │   ├── repository/school_repository_impl.py
│       │   ├── datasources/bd/schools_datasource.py
│       │   ├── models/schools_models.py
│       │   ├── schemas/schools_schemas.py
│       │   └── dependencies.py
│       ├── teachers/
│       │   ├── routes/teachers_routes.py
│       │   ├── use_cases/teachers_use_cases.py
│       │   ├── repository/teachers_repository_interface.py
│       │   ├── repository/teachers_repository_impl.py
│       │   ├── datasources/bd/teachers_datasource.py
│       │   ├── models/teachers_models.py
│       │   ├── schemas/teachers_schemas.py
│       │   └── dependencies.py
│       ├── visits/
│       │   ├── enums.py
│       │   ├── routes/visits_routes.py
│       │   ├── use_cases/visits_use_cases.py
│       │   ├── repository/visits_repository_interface.py
│       │   ├── repository/visits_repository_impl.py
│       │   ├── datasources/bd/visits_datasource.py
│       │   ├── models/visits_models.py
│       │   ├── schemas/visits_schemas.py
│       │   └── dependencies.py
├── .env                            # variables locales (NO se versiona)
├── .env.example                    # plantilla de variables
├── requirements.txt
└── README.md
```

---

## Requisitos

- **Python 3.12+** (probado con 3.12.3)
- **PostgreSQL 14+** accesible por red, o un proyecto de **Supabase**
- Git (opcional, para clonar)

Verifica tu versión:

```powershell
python --version
```

---

## Instalación

### 1. Ubicarse en la raíz del backend

```powershell
cd C:\Users\User\Desktop\projects\kurios\back
```

### 2. Crear el entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación de scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sabrás que está activo porque el prompt empieza con `(.venv)`.

### 3. Instalar dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Comprobar que quedó todo:

```powershell
python -c "import fastapi, sqlalchemy, psycopg2; print('deps OK')"
```

En VS Code: `Ctrl+Shift+P` → **Python: Select Interpreter** → elige `.\.venv\Scripts\python.exe`.

---

## Configuración (`.env`)

Crea un archivo `.env` en la raíz del backend (`back/.env`). **No lo subas al repositorio**: ya está en `.gitignore`.

```dotenv
# development | production
ENV=development

# Conexión a PostgreSQL (Supabase)
# Formato: postgresql+psycopg2://USUARIO:PASSWORD@HOST:PUERTO/BASE
DATABASE_URL=postgresql+psycopg2://postgres:tu_password@localhost:5432/kurios
DATABASE_TYPE=postgresql
DATABASE_ECHO=False

# Cliente HTTP saliente
HTTP_TIMEOUT_SECONDS=10
HTTP_MAX_RETRIES=3
```

Variables reconocidas por `app/core/config.py`:

| Variable | Tipo | Default | Descripción |
|---|---|---|---|
| `ENV` | `str` | `development` | Entorno de ejecución |
| `DATABASE_URL` | `str` | — | DSN de SQLAlchemy para PostgreSQL |
| `DATABASE_TYPE` | `str` | `postgresql` | Motor usado (`postgresql`, `sqlite`, …) |
| `DATABASE_ECHO` | `bool` | `False` | Loguea el SQL generado (útil en desarrollo) |
| `HTTP_TIMEOUT_SECONDS` | `int` | `10` | Timeout de clientes HTTP salientes |
| `HTTP_MAX_RETRIES` | `int` | `3` | Reintentos de clientes HTTP salientes |

Notas:

- El `.env` se lee **relativo al directorio desde donde ejecutas Uvicorn**, así que arranca siempre desde `back/`.
- Si `DATABASE_TYPE=postgresql`, `app/core/database.py` fuerza `sslmode=require`, que es lo que Supabase necesita.
- El `.env.example` incluye variables de módulos que aún no existen (`SECRET_KEY_JWT`, `FETCH_INTERVAL_MINUTES`, …). `Settings` está configurado con `extra="ignore"`, así que sobran sin romper nada, pero no hace falta copiarlas.
- **Nunca** commitees `.env` con credenciales reales. Si una credencial se filtró, rótala en el panel de Supabase.

---

## Ejecución

Desde `back/`, con el venv activo:

```powershell
python -m uvicorn app.main:app --reload
```

La API queda en <http://127.0.0.1:8000>.

| Opción | Para qué sirve |
|---|---|
| `--reload` | Reinicia al guardar archivos (solo desarrollo) |
| `--host 0.0.0.0` | Expone la API a la red local |
| `--port 8001` | Cambia el puerto |
| `--log-level debug` | Más detalle en consola |

En el arranque, el `lifespan` de `app/main.py` ejecuta `Base.metadata.create_all()`, que **crea las tablas que falten** (por ejemplo `schools`). Es cómodo en desarrollo, pero no reemplaza a las migraciones: si la tabla ya existe, no se le agregan columnas nuevas.

---

## Documentación y endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Health check básico |
| `GET` | `/schools` | Lista escuelas, con filtro opcional por nombre y paginación |
| `GET` | `/teachers` | Maestros de un colegio (`school_id` obligatorio), con búsqueda por nombre |
| `GET` | `/visits` | Visitas visibles, con filtros por colegio y tipo, nombres y paginación |
| `POST` | `/visits` | Crea una visita (fecha no futura, profesor libre a esa hora) |
| `PATCH` | `/visits/{id}` | Edita parcialmente una visita visible |
| `GET` | `/visits/types` | Tipos de visita disponibles (`type_visits_enum`) |
| `DELETE` | `/visits/{id}` | Oculta una visita (`visit_status = 'hide'`), no la borra |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc |
| `GET` | `/openapi.json` | Esquema OpenAPI |

### `GET /schools`

Query params:

| Param | Tipo | Default | Descripción |
|---|---|---|---|
| `name` | `string` (2–20) | — | Filtro parcial por nombre (case-insensitive) |
| `limit` | `int` (1–100) | `20` | Tamaño de página |
| `offset` | `int` (≥ 0) | `0` | Resultados a omitir |

Respuesta:

```json
{
  "schools": [
    { "id": 1, "name": "U.E Maria Auxiliadora", "address": "El Rosal, Caracas" }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

Ejemplos:

```powershell
# PowerShell
Invoke-RestMethod "http://127.0.0.1:8000/"
Invoke-RestMethod "http://127.0.0.1:8000/schools?limit=10"
Invoke-RestMethod "http://127.0.0.1:8000/schools?name=san"
```

```bash
# curl
curl "http://127.0.0.1:8000/schools?limit=10"
curl "http://127.0.0.1:8000/schools?name=san"
```

### `GET /teachers`

Maestros **de un colegio**: `school_id` es obligatorio, así que no existe el caso "todos los maestros". El filtro `name` busca en nombre, apellido y nombre completo, sin distinguir mayúsculas ni acentos.

| Param | Tipo | Default | Descripción |
|---|---|---|---|
| `school_id` | `int` (≥ 1) | **requerido** | Colegio a consultar |
| `name` | `string` (2–100) | — | Busca en nombre, apellido o nombre completo |
| `limit` | `int` (1–100) | `20` | Tamaño de página |
| `offset` | `int` (≥ 0) | `0` | Resultados a omitir |

```json
{
  "teachers": [
    { "id": 1, "name": "Ana", "last_name": "Pérez", "id_school": 1 }
  ],
  "total": 2,
  "limit": 20,
  "offset": 0
}
```

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/teachers?school_id=1"
Invoke-RestMethod "http://127.0.0.1:8000/teachers?school_id=1&name=perez"
Invoke-RestMethod "http://127.0.0.1:8000/teachers?school_id=1&name=ana%20perez"
```

`name=perez` encuentra "Pérez" gracias a la extensión `unaccent`. `GET /teachers` sin `school_id` responde `422`.

### Visitas

Una visita **nunca se elimina físicamente**: el borrado es lógico y cambia `visit_status` de `visible` a `hide`, para conservar la transacción histórica. Todas las consultas excluyen las visitas ocultas.

#### `GET /visits`

Devuelve las visitas visibles de la más reciente a la más antigua, con el nombre del colegio y del profesor resueltos por JOIN.

| Param | Tipo | Default | Descripción |
|---|---|---|---|
| `school_id` | `int` (≥ 1) | — | Filtra por colegio |
| `type_visit` | `En Aula` \| `Encuentro` | — | Filtra por tipo |
| `limit` | `int` (1–100) | `20` | Tamaño de página |
| `offset` | `int` (≥ 0) | `0` | Resultados a omitir |

```json
{
  "visits": [
    {
      "id": 1,
      "id_school": 1,
      "id_teacher": 1,
      "date_visit": "2026-11-22",
      "time_visit": "09:00:00",
      "notes": "Visita de ejemplo",
      "visit_status": "visible",
      "type_visit": "En Aula",
      "created_at": "2026-11-22T21:49:51.070424Z",
      "updated_at": null,
      "school_name": "U.E. Colegio San Ignacio de Loyola",
      "teacher_name": "Ana Pérez"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/visits?school_id=1"
Invoke-RestMethod "http://127.0.0.1:8000/visits?type_visit=En%20Aula&limit=10"
```

#### `POST /visits`

```json
{
  "id_school": 1,
  "id_teacher": 1,
  "date_visit": "2026-11-20",
  "time_visit": "09:00:00",
  "notes": "Visita de seguimiento",
  "type_visit": "En Aula"
}
```

Validaciones:

- `date_visit` + `time_visit` no pueden ser futuras. La comparación se hace en `America/Caracas`, no en la zona del servidor.
- El colegio y el profesor deben existir (`404`).
- El profesor debe pertenecer al colegio indicado (`422`).
- Un profesor no puede tener dos visitas visibles a la misma fecha y hora (`409`). Varias visitas al mismo colegio y hora están permitidas si son profesores distintos.
- `notes` se recorta y, si queda vacío, se guarda `NULL`.

#### `PATCH /visits/{id}`

Edición parcial: envía solo los campos que quieres cambiar (`id_school`, `id_teacher`, `date_visit`, `time_visit`, `notes`, `type_visit`). El cuerpo vacío responde `422`. Las validaciones de fecha, profesor y disponibilidad se aplican sobre los valores finales. Una visita oculta responde `404`.

```powershell
Invoke-RestMethod -Method Patch "http://127.0.0.1:8000/visits/1" `
  -ContentType "application/json" -Body '{"notes":"Reprogramada"}'
```

#### `GET /visits/types`

Devuelve los valores del enum `type_visits_enum` en el orden definido en la base de datos.

```json
["En Aula", "Encuentro"]
```

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/visits/types"
```

#### `DELETE /visits/{id}`

Oculta la visita y responde `204` sin cuerpo. Es idempotente: si ya estaba oculta sigue devolviendo `204`. Si el id no existe responde `404`.

```powershell
Invoke-RestMethod -Method Delete "http://127.0.0.1:8000/visits/1"
```

---

## Tests

```powershell
python -m pytest
```

> El directorio `tests/` todavía no existe; los primeros tests de humo de `schools`, `teachers` y `visits` están pendientes.

---

## Estado del proyecto

- [x] Esqueleto de la app, configuración, logger y capa de base de datos
- [x] Estructura por *features* con inyección de dependencias
- [x] `GET /schools` con filtro por nombre y paginación
- [x] `GET /teachers` con `school_id` obligatorio, búsqueda sin acentos y `total` real
- [x] `GET /visits/types` y `DELETE /visits/{id}` (soft delete con `visit_status`)
- [x] `GET /visits` con filtros por colegio/tipo, nombres por JOIN y `total` real
- [x] `POST /visits` con validación de fecha no futura y disponibilidad del profesor
- [x] `PATCH /visits/{id}` para editar cualquier dato de la visita
- [ ] `total` real en `/schools` (`count_schools` en lugar de `len(pagina)`)
- [ ] Normalizar `teachers`: `name` y `last_name` deberían ser `NOT NULL` y sin el default `'John '`
- [ ] Índices `ix_school_visits_id_school` e `ix_school_visits_id_teacher`
- [ ] Migraciones con Alembic en lugar de `create_all`
- [ ] Tests y CI

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'app'`**
Estás ejecutando desde dentro de `app/`. Vuelve a `back/` y usa `python -m uvicorn app.main:app --reload`.

**`ModuleNotFoundError: No module named 'core' / 'features'`**
Quedó un import relativo al directorio en lugar de `from app...`. Todos los imports internos deben empezar por `app.`.

**`ValidationError: Extra inputs are not permitted`**
Una clave del `.env` no está declarada en `Settings`. Añádela como campo o confía en `extra="ignore"` (ya configurado).

**La app tarda ~10 s y falla al conectar**
`sslmode=require` es obligatorio en Supabase, pero el host directo `db.<ref>.supabase.co:5432` normalmente resuelve **solo IPv6**. En redes sin IPv6 usa el *pooler* (`aws-0-<region>.pooler.supabase.com:5432`, usuario `postgres.<ref>`).

**`psycopg2` no compila al instalar**
Estás usando el wheel equivocado de Python. Este proyecto está probado con Python 3.12; verifica con `python --version` y reinstala el venv con esa versión.
