import streamlit as st
from pokemon_form import pokemon_form
from controller import PokemonController
from db import get_db

st.set_page_config(
    page_title="Crear Pokémon",
    layout="wide"
)

st.header("Crear un Nuevo Pokémon")

# Obtener el controlador
db = get_db()
controller = PokemonController(db["pokemons"])

# Renderizar el formulario y obtener el payload
payload = pokemon_form()

# Si el formulario fue enviado y tiene datos, insertar
if payload:
    # Validar que el nombre no esté vacío
    if not payload.get("nombre"):
        st.error("El nombre del Pokémon es obligatorio.")
    else:
        # Comprobar si ya existe un Pokémon con ese nombre
        existing = controller.find_by_name(payload["nombre"], exact=True)
        if existing:
            st.warning(f"Ya existe un Pokémon llamado '{payload['nombre']}'.")
        else:
            created = controller.insert(payload)
            st.success(f"Pokémon '{created.nombre}' creado con ID: {created.id}")