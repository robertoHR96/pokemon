# -*- coding: utf-8 -*-
"""
Página para editar un Pokémon existente.

Esta página de la aplicación Streamlit permite a los usuarios buscar un Pokémon
por su nombre, seleccionarlo de una lista de resultados y luego editar
sus datos a través de un formulario.
"""

import streamlit as st
from pokemon_form import pokemon_form
from controller import PokemonController
from db import get_db

# Configuración de la página
st.set_page_config(page_title="Editar Pokémon", layout="wide")

st.header("Editar Pokémon")

# Conexión a la base de datos y al controlador
db = get_db()
controller = PokemonController(db["pokemons"])

# --- Búsqueda del Pokémon a editar ---
search_term = st.text_input("Buscar Pokémon por nombre para editar", key="edit_search")

if search_term:
    results = controller.find_by_name(search_term)
    if results:
        # Muestra una lista de resultados para que el usuario elija
        pokemon_to_edit = st.selectbox(
            "Selecciona un Pokémon",
            options=results,
            format_func=lambda p: f"{p.nombre} (ID: {p.id})",
        )

        if pokemon_to_edit:
            # Guarda el ID del Pokémon seleccionado en el estado de la sesión
            st.session_state.edit_id = pokemon_to_edit.id
    else:
        st.info(f"No se encontraron Pokémon con el nombre '{search_term}'.")
        if "edit_id" in st.session_state:
            del st.session_state["edit_id"]

# --- Formulario de edición ---
edit_id = st.session_state.get("edit_id")

if not edit_id:
    st.warning("Busca y selecciona un Pokémon para empezar a editar.")
else:
    pokemon_obj = controller.find_by_id(str(edit_id))
    if not pokemon_obj:
        st.error("El Pokémon seleccionado ya no existe o el ID es inválido.")
        if "edit_id" in st.session_state:
            del st.session_state.edit_id
    else:
        st.subheader(f"Editando a: **{pokemon_obj.nombre}**")

        # Muestra la imagen del Pokémon
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_obj.pokedex_nacional}.png",
                width=200,
            )

        # Renderiza el formulario de edición y obtiene los datos
        payload = pokemon_form(pokemon=pokemon_obj)

        if payload:
            # Actualiza el Pokémon en la base de datos
            updated = controller.update(str(edit_id), payload)
            if updated:
                st.success(f"Pokémon '{updated.nombre}' actualizado correctamente.")
                # Limpia el estado de la sesión para la siguiente edición
                if "edit_id" in st.session_state:
                    del st.session_state.edit_id
                st.rerun()
            else:
                st.error("Error al actualizar el Pokémon.")

        if st.button("Cancelar Edición"):
            # Limpia el estado de la sesión si se cancela la edición
            if "edit_id" in st.session_state:
                del st.session_state.edit_id
            st.rerun()