# Proyecto Kurios - Gestión de Escuelas, Profesores y Visitas

Aplicación Full-Stack dividida en dos directorios principales (`back/` y `front/`), diseñada para la gestión integral de instituciones educativas, docentes y el seguimiento de visitas. 

## 📁 Estructura del Repositorio

```
kurios/
├── back/                   # API REST construida con FastAPI (Clean Architecture)
└── front/                  # Aplicación web construida con React, TypeScript y Tailwind CSS
    └── Kurios-template-ts/

```

## 🚀 Instalación y Ejecución Local

### 1. Base de Datos (PostgreSQL - Supabase)

El proyecto utiliza una base de datos PostgreSQL alojada en Supabase (entorno de pruebas/desarrollo). Si deseas inspeccionar la estructura o conectarte directamente mediante un cliente SQL (como DBeaver, pgAdmin o TablePlus), puedes utilizar la siguiente cadena de conexión:

```
postgresql://postgres.eqfmwiwguzmwpbumqnbx:kurios-test-db-2026@aws-1-us-east-2.pooler.supabase.com:5432/postgres

host=aws-1-us-east-2.pooler.supabase.com
port=5432
database=postgres
user=postgres.eqfmwiwguzmwpbumqnbx

```

### 2. Backend (FastAPI)

#### Ubicarse en la raíz del backend

Abre una terminal y navega hasta la carpeta `back` del repositorio:

```
cd back

```

#### Crear y activar el entorno virtual

**Windows (PowerShell):**

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1

```

*(Si PowerShell bloquea la activación de scripts, ejecuta primero: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y vuelve a activar).*

**Windows (CMD):**

```
python -m venv .venv
.venv\Scripts\activate.bat

```

**Linux / macOS:**

```
python3 -m venv .venv
source .venv/bin/activate

```

*(Sabrás que está activo porque el prompt comenzará con `(.venv)`).*

#### Instalar dependencias

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

```

Para comprobar que las dependencias principales se instalaron correctamente:

```
python -c "import fastapi, sqlalchemy, psycopg2; print('deps OK')"

```

> **Tip para VS Code:** Presiona `Ctrl+Shift+P` → **Python: Select Interpreter** → selecciona `.\.venv\Scripts\python.exe`.

#### Configuración (`.env`)

Crea un archivo `.env` en la raíz del backend (`back/.env`). Puedes guiarte y copiar directamente las credenciales incluidas en el archivo `env.example`.

#### Ejecución del servidor

Desde `back/`, con el entorno virtual activo:

```
python -m uvicorn app.main:app --reload

```

La API quedará disponible en `http://127.0.0.1:8000` (y su documentación interactiva en `http://127.0.0.1:8000/docs`).

| Opción | Descripción | 
| ----- | ----- | 
| `--reload` | Reinicia el servidor automáticamente al guardar cambios (solo desarrollo). | 
| `--host 0.0.0.0` | Expone la API a la red local. | 
| `--port 8001` | Cambia el puerto de ejecución. | 
| `--log-level debug` | Muestra mayor nivel de detalle en la consola. | 

### 3. Frontend (React + TypeScript)

Abre una nueva terminal, navega al directorio del frontend, instala las dependencias y levanta el entorno de desarrollo:

```
cd front/Kurios-template-ts
npm install
npm run dev

```

La aplicación web estará disponible en la URL local indicada por Vite (generalmente `http://localhost:5173`).

## 🛠️ Decisiones Técnicas

* **Backend inspirado en Clean Architecture:** Se optó por estructurar la API en FastAPI separando responsabilidades por capas (casos de uso, repositorios y controladores/rutas). Aunque este enfoque requiere escribir más código inicial, garantiza un sistema desacoplado, altamente escalable y fácil de mantener a largo plazo.

* **Diseño de Base de Datos Relacional con Tipos Enumerados (PostgreSQL):** El modelado de la base de datos se realizó desde cero priorizando la integridad de los datos. En la tabla `schools_visits` se implementaron tipos `ENUM` nativos de PostgreSQL para controlar estrictamente los estados (`status`) y tipos de visitas (`visit_type`), evitando inconsistencias desde la capa de persistencia, y evitando tablas donde solo se guardan tipos de estatos ya que esto generaba para este proyecto, mas interacciones en la BD a la hora de realizar consultas.

* **Frontend Pragmático con React y Tailwind CSS:** Dado que llevaba tiempo sin profundizar en el ecosistema actual de React y priorizando cumplir con los tiempos de entrega, se optó por una estructura más directa y funcional utilizando una plantilla nativa con TypeScript y Tailwind CSS para agilizar la maquetación y el consumo de los endpoints. con plantilla me refiero a el diseño que genere usando IA para armar un maqueta inicial.

## ⏳ Funcionalidades Fuera de Alcance y Mejoras Futuras

### Qué quedó fuera por falta de tiempo

* **Arquitectura Modular en el Frontend:** La intención original era segmentar el frontend por módulos independientes (similar al backend), pero por limitaciones de tiempo se consolidó de una manera más directa.

* **Autenticación y Control de Roles:** Gestión de sesiones de usuario (JWT) y permisos diferenciados entre administradores y personal de campo.

* **Pruebas Automatizadas:** Implementación de tests unitarios y de integración tanto para los casos de uso en FastAPI como para los componentes en React.

### Qué mejoraría en una siguiente iteración

* **Refactorización integral del Frontend:** Reestructurar completamente la aplicación en React bajo una arquitectura modular (Feature-based architecture), implementando manejo de estado global más robusto y optimización de renderizado para lograr un producto más sólido y elaborado.

* **Evolución del Backend:** La base actual del backend es muy sólida, organizada y escalable; en una siguiente fase me enfocaría en añadir paginación avanzada en los listados y contenedores con Docker para facilitar el despliegue.

## 🤖 Uso de inteligencia artificial

En el desarrollo de este proyecto utilicé herramientas de inteligencia artificial de manera estratégica y supervisada para acelerar tareas repetitivas y refrescar conceptos técnicos:

### Herramientas utilizadas

* **OpenCode** (utilizando modelos abiertos/gratuitos como *Big Pickle* y *DeepSeek* como agentes de programación).

* **Google Gemini** (apoyo en estructura de código, maquetación y resolución de dudas mas que todo para el front).

* **NotebookLM** (investigación y síntesis de conceptos modernos de React a partir de diversas fuentes y documentación web).

### Partes del desarrollo asistidas por IA

* **Base de Datos (0% IA):** El diseño, modelado relacional, creación de tablas y definición de tipos enumerados (`ENUM`) en PostgreSQL/Supabase fue un trabajo **100% manual y propio**, sin intervención de IA.

* **Backend (Apoyo en replicación de patrones):** Diseñé y programé manualmente el primer módulo completo (`schools`) siguiendo los principios de Clean Architecture. Dado que replicar esa misma estructura de carpetas, interfaces y repositorios para los demás módulos era una tarea mecánicamente repetitiva, utilicé agentes en OpenCode bajo mis propios parámetros y arquitectura base para generar el *boilerplate* de los módulos `teacher` y `visit`, siempre bajo estricta supervisión.

* **Frontend (Apoyo en maquetación e integración):** Al tener tiempo sin profundizar en React y contar con poco tiempo de desarrollo, me apoyé en NotebookLM para repasar conceptos clave, y en Gemini junto con OpenCode para diseñar una maqueta visual inicial antes de escribir el código final, estilizar componentes con Tailwind CSS y conectar las llamadas a los endpoints respetando las reglas de negocio.

### Correcciones y ajustes realizados sobre lo generado por IA

* **Alineación con Clean Architecture (Backend):** Al duplicar los módulos `teacher` y `visit`, los agentes tendían a mezclar lógica de negocio dentro de los controladores o acoplar demasiado los esquemas de Pydantic con los modelos de SQLAlchemy. Tuve que refactorizar manualmente las inyecciones de dependencias y las interfaces de los repositorios para mantener la pureza de las capas establecidas en el módulo `schools`.

* **Manejo de tipos `ENUM` y validaciones:** Ajusté manualmente la serialización y validación entre FastAPI y PostgreSQL para asegurar que los valores enviados desde el frontend coincidieran exactamente con los tipos enumerados definidos en la tabla `schools_visits`.

* **Lógica de negocio y limpieza en React (Frontend):** La IA generó inicialmente componentes muy extensos con estados locales redundantes y llamadas desordenadas a la API. Tuve que limpiar el código, corregir errores de tipado en TypeScript, ajustar el manejo de estados asíncronos (carga y errores) y adaptar las vistas para que cumplieran fielmente con las reglas de negocio del proyecto.