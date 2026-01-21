import streamlit as st
import json
from db import get_db, get_client, DB_NAME
from controller import PokemonController

st.set_page_config(
    page_title="Administración",
    layout="wide"
)

st.header("Panel de Administración de la Base de Datos")

st.warning("ADVERTENCIA: Las siguientes acciones son destructivas y no se pueden deshacer.")

# --- Cargar Datos ---
st.subheader("Cargar Colección desde JSON")
st.markdown("Esto cargará los datos desde `python/data/pokemons.json` en la colección `pokemons`. "
            "La base de datos y la colección se crearán si no existen.")

if st.button("Cargar Datos"):
    try:
        db = get_db()
        controller = PokemonController(db["pokemons"])
        
        with open("python/data/pokemons.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        inserted_count = 0
        with st.spinner(f"Insertando {len(data)} documentos..."):
            for doc in data:
                # Evitar duplicados por nombre
                if not controller.find_by_name(doc.get("nombre"), exact=True):
                    controller.insert(doc)
                    inserted_count += 1
        
        st.success(f"¡Proceso completado! Se insertaron {inserted_count} nuevos Pokémon.")
        st.info(f"{len(data) - inserted_count} Pokémon ya existían y no se re-insertaron.")
    except Exception as e:
        st.error(f"Ocurrió un error al cargar los datos: {e}")

# --- Eliminar Datos ---
st.subheader("Eliminar Base de Datos")
st.markdown(f"Esta acción eliminará **toda** la base de datos `{DB_NAME}` del servidor MongoDB. "
            "Todos los datos se perderán permanentemente.")

if st.button("Eliminar Base de Datos y Colección"):
    try:
        client = get_client()
        with st.spinner(f"Eliminando la base de datos '{DB_NAME}'..."):
            client.drop_database(DB_NAME)
        
        # Limpiar la cache de recursos de Streamlit para forzar una nueva conexión
        st.cache_resource.clear()
        
        st.success(f"La base de datos '{DB_NAME}' ha sido eliminada correctamente.")
        st.info("La aplicación puede requerir un reinicio para reflejar los cambios completamente.")
        st.rerun()
    except Exception as e:
        st.error(f"Ocurrió un error al eliminar la base de datos: {e}")