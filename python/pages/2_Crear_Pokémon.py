# -*- coding: utf-8 -*-
"""
Página para crear un nuevo Pokémon.

Esta página de la aplicación Streamlit proporciona un formulario para
añadir un nuevo Pokémon a la base de datos.
"""

import streamlit as st
from pokemon_form import pokemon_form
from controller import PokemonController
from db import get_db

# Configuración de la página
st.set_page_config(
    page_title="Crear Pokémon",
    layout="wide"
)

st.header("Crear un Nuevo Pokémon")

# Obtener el controlador de la base de datos
db = get_db()
controller = PokemonController(db["pokemons"])

# Renderizar el formulario y obtener los datos
payload = pokemon_form()

# Si el formulario fue enviado y contiene datos, procesarlos
if payload:
    # Validar que el nombre no esté vacío
    if not payload.get("nombre"):
        st.error("El nombre del Pokémon es obligatorio.")
    else:
        # Comprobar si ya existe un Pokémon con el mismo nombre
        existing = controller.find_by_name(payload["nombre"], exact=True)
        if existing:
            st.warning(f"Ya existe un Pokémon llamado '{payload['nombre']}'.")
        else:
            # Insertar el nuevo Pokémon en la base de datos
            created = controller.insert(payload)
            st.success(f"Pokémon '{created.nombre}' creado con ID: {created.id}")
