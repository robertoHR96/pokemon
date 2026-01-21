import streamlit as st
from pokemon_form import pokemon_form
from controller import PokemonController
from db import get_db

st.set_page_config(
    page_title="Editar Pokémon",
    layout="wide"
)

st.header("Editar Pokémon")

db = get_db()
controller = PokemonController(db["pokemons"])

# --- Search ---
search_term = st.text_input("Buscar Pokémon por nombre para editar", key="edit_search")

if search_term:
    results = controller.find_by_name(search_term)
    if results:
        # Usamos un selectbox para que el usuario elija a quién editar
        pokemon_to_edit = st.selectbox(
            "Selecciona un Pokémon",
            options=results,
            format_func=lambda p: f"{p.nombre} (ID: {p.id})"
        )
        
        if pokemon_to_edit:
            st.session_state.edit_id = pokemon_to_edit.id
    else:
        st.info(f"No se encontraron Pokémon con el nombre '{search_term}'.")
        if 'edit_id' in st.session_state:
            del st.session_state['edit_id']

# --- Edit Form ---
edit_id = st.session_state.get("edit_id")

if not edit_id:
    st.warning("Busca y selecciona un Pokémon para empezar a editar.")
else:
    pokemon_obj = controller.find_by_id(str(edit_id))
    if not pokemon_obj:
        st.error("El Pokémon seleccionado ya no existe o el ID es inválido.")
        if 'edit_id' in st.session_state:
            del st.session_state.edit_id
    else:
        st.subheader(f"Editando a: **{pokemon_obj.nombre}**")
        
        # Render form and get payload
        payload = pokemon_form(pokemon=pokemon_obj)

        if payload:
            updated = controller.update(str(edit_id), payload)
            if updated:
                st.success(f"Pokémon '{updated.nombre}' actualizado correctamente.")
                # Limpiar estado para la siguiente edición
                if 'edit_id' in st.session_state:
                    del st.session_state.edit_id
                st.rerun()
            else:
                st.error("Error al actualizar el Pokémon.")
        
        if st.button("Cancelar Edición"):
            if 'edit_id' in st.session_state:
                del st.session_state.edit_id
            st.rerun()