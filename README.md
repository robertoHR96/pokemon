
# Pokedex Profesional - Aplicación con Streamlit y MongoDB

Este proyecto es una aplicación web construida con Streamlit que sirve como un "Pokedex Profesional". Permite a los usuarios administrar una base de datos de Pokémon alojada en MongoDB. La aplicación ofrece funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) completas a través de una interfaz de usuario interactiva.

## Características Principales

- **Interfaz Intuitiva**: Construida con Streamlit para una experiencia de usuario limpia y reactiva.
- **Base de Datos NoSQL**: Utiliza MongoDB para almacenar y gestionar los datos de los Pokémon.
- **Gestión de Datos**:
    - **Crear**: Añadir nuevos Pokémon a la base de datos a través de un formulario.
    - **Leer**: Listar todos los Pokémon con opciones de filtrado y búsqueda.
    - **Actualizar**: Buscar y modificar Pokémon existentes.
    - **Eliminar**: Borrar Pokémon de la base de datos.
- **Administración de la Base de Datos**:
    - Cargar la colección de Pokémon desde un archivo `pokemons.json`.
    - Eliminar por completo la base de datos para empezar de cero.
- **Visualización de Estadísticas**: Muestra métricas básicas sobre los datos, como el número total de Pokémon y su distribución por tipo.
- **Contenerización**: Usa Docker y `docker-compose` para gestionar la base de datos MongoDB y una interfaz de administración web (Mongo Express).

## Estructura del Proyecto

```
.
├── docker-compose.yml      # Define los servicios de MongoDB y Mongo Express.
├── requirements.txt        # Dependencias de Python.
├── python/
│   ├── app.py              # Punto de entrada principal de la aplicación Streamlit (página de inicio).
│   ├── controller.py       # Lógica de negocio para interactuar con la base de datos.
│   ├── db.py               # Lógica de conexión a la base de datos.
│   ├── models.py           # Modelos de datos Pydantic para los Pokémon.
│   ├── pokemon_form.py     # Componente de formulario reutilizable para crear/editar.
│   ├── data/
│   │   └── pokemons.json   # Datos iniciales de los Pokémon.
│   └── pages/              # Directorio de páginas de la aplicación Streamlit.
│       ├── 1_Listado.py
│       ├── 2_Crear_Pokémon.py
│       ├── 3_Editar_Pokémon.py
│       ├── 4_Estadísticas.py
│       └── 5_Administración.py
└── README.md               # Este archivo.
```

## Requisitos Previos

- [Docker](https://www.docker.com/get-started) y [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.8+](https://www.python.org/downloads/) y `pip`
- Un entorno virtual de Python (recomendado).

## Instalación y Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### 1. Iniciar la Base de Datos

El `docker-compose.yml` levantará dos servicios: `mongo` (la base de datos) y `mongo-express` (un visor web para la base de datos).

```bash
# Inicia los contenedores en segundo plano
docker-compose up -d
```

- La base de datos MongoDB estará disponible en `localhost:27017`.
- Mongo Express estará accesible en `http://localhost:8081`.

### 2. Configurar el Entorno de Python

Es una buena práctica usar un entorno virtual para aislar las dependencias del proyecto.

```bash
# 1. Crea un entorno virtual
python -m venv .venv

# 2. Activa el entorno virtual
# En macOS y Linux:
source .venv/bin/activate
# En Windows:
# .venv\Scripts\activate

# 3. Instala las dependencias de Python
pip install -r requirements.txt
```

### 3. Ejecutar la Aplicación Streamlit

Una vez que la base de datos esté en funcionamiento y las dependencias instaladas, puedes iniciar la aplicación.

```bash
streamlit run python/app.py
```

La aplicación se abrirá automáticamente en tu navegador web.

## Uso de la Aplicación

1.  **Página de Inicio**: Al ejecutar la aplicación, verás una página de bienvenida que te guiará sobre cómo usar las diferentes secciones.
2.  **Administración**:
    - **Cargar Datos**: Haz clic en este botón para poblar la base de datos con los datos de `python/data/pokemons.json`. Es el primer paso que debes realizar.
    - **Eliminar Base de Datos**: Esta opción borrará todos los datos. Úsala con precaución.
3.  **Listado**:
    - Muestra una tabla con todos los Pokémon.
    - Usa los filtros para buscar por nombre, región o número de Pokedex.
    - Selecciona un Pokémon de la lista desplegable y haz clic en "Eliminar Pokémon Seleccionado" para borrarlo.
4.  **Crear Pokémon**:
    - Rellena el formulario con los datos del nuevo Pokémon.
    - Haz clic en "Guardar Pokémon" para añadirlo a la base de datos.
5.  **Editar Pokémon**:
    - Usa la barra de búsqueda para encontrar el Pokémon que deseas modificar por su nombre.
    - Selecciónalo de la lista de resultados.
    - El formulario se rellenará con sus datos actuales. Modifica lo que necesites y guarda los cambios.
6.  **Estadísticas**:
    - Visualiza un recuento total de Pokémon y un desglose por tipo primario.
