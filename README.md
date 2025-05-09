# ChessTournament - Manual de Usuario

ChessTournament es una aplicación web para la gestión de torneos de ajedrez. Consiste en un backend desarrollado en Django (API REST) y un frontend desarrollado en Vue.js.

## Estructura del Proyecto

El proyecto está dividido en dos componentes principales:

- **Backend (Django)**: Directorio `chesstournament` - API REST que gestiona los datos de torneos, jugadores y partidas.
- **Frontend (Vue.js)**: Directorio `chesstournament-client` - Interfaz de usuario que permite visualizar y gestionar los torneos.

## Configuración del Entorno

### Variables de Entorno

El proyecto utiliza un archivo `env` en la raíz del directorio `chesstournament` que contiene las URLs de despliegue tanto para el backend como para el frontend en Render.com. Este archivo también incluye la configuración de la base de datos.

```
# URLs de Render.com
RENDER_URL = https://psi-p3-chess.onrender.com
RENDER_URL_FRONTEND = https://tournamentmaster-ale-clau.onrender.com
```

### Configuración del Backend

El backend puede utilizar dos bases de datos diferentes dependiendo de la variable de entorno `TESTING`:

- Si `export TESTING=true`: Utiliza PostgreSQL local
- Si no está configurado: Utiliza la base de datos de Neon configurada en el archivo `env`

## Instalación y Ejecución

### Requisitos Previos

- Python 3.8 o superior
- Node.js 14 o superior
- npm 6 o superior
- PostgreSQL (opcional, para entorno de desarrollo/testing)

### Instalación del Backend (Django)

1. Crear un entorno virtual de Python:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Navegar al directorio del backend:

```bash
cd chesstournament
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:

Para usar PostgreSQL local (modo testing):
```bash
export TESTING=true
```

Para usar la base de datos Neon:
```bash
# No es necesario configurar nada, usará por defecto la URL en el archivo env
```

5. Realizar las migraciones:

```bash
python manage.py migrate
```

6. Crear un superusuario (opcional):

```bash
python manage.py createsuperuser
```

7. Iniciar el servidor:

```bash
python manage.py runserver 8001
```

El backend estará disponible en: http://localhost:8001/

### Instalación del Frontend (Vue.js)

1. Navegar al directorio del frontend:

```bash
cd chesstournament-client
```

2. Instalar las dependencias:

```bash
npm install
```

3. Configurar las variables de entorno para el desarrollo:


Para usar la URL de Render en lugar de la local:
```
export VITE_TESTING=true
```

4. Iniciar el servidor de desarrollo:

```bash
npm run dev
```

Alternativamente, puede exportar la variable TESTING directamente:
```bash
VITE_TESTING=true npm run dev
```

El frontend estará disponible en: http://localhost:5173/

## Funcionalidades Principales

La aplicación ofrece las siguientes funcionalidades:

### Para Todos los Usuarios

- **Página de inicio**: Visualizar listado de torneos con paginación
- **Búsqueda de torneos**: Filtrar torneos por nombre
- **Visualización de detalles de torneo**: Ver clasificación, rondas y juegos
- **FAQ**: Consultar preguntas frecuentes

### Para Jugadores

- **Actualizar resultados**: Introducir el resultado de sus partidas

### Para Administradores

- **Login/Logout**: Iniciar y cerrar sesión
- **Crear torneos**: Crear nuevos torneos con diferentes configuraciones
- **Gestionar torneos**: Modificar resultados de cualquier partida

## Tipos de Tableros

El sistema admite dos tipos de torneos:

- **OTB (Over The Board)**: Torneos presenciales
- **LIC (Lichess)**: Torneos en línea utilizando Lichess como plataforma

## Pruebas

Para ejecutar las pruebas de Cypress:

```bash
# En el directorio chesstournament-client
npx cypress open
```

Asegúrese de que tanto el servidor backend como el frontend estén en ejecución antes de ejecutar las pruebas.

## Acceso a la Aplicación Desplegada

Para acceder al panel de administración de Django, utilice:
- **URL**: `URL/admin/`
- **Usuario**: `alumnodb`
- **Contraseña**: `alumnodb`