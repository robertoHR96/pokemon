# -*- coding: utf-8 -*-
"""
Página de listado de Pokémon.

Esta página de la aplicación Streamlit muestra una lista de los Pokémon
almacenados en la base de datos. Permite filtrar los Pokémon por nombre,
región y número de Pokedex, y también permite eliminar Pokémon.
"""

import streamlit as st
from db import get_db, DB_NAME
from controller import PokemonController


def format_ataques(ataques):
    """
    Formatea la lista de ataques de un Pokémon para su visualización.

    Args:
        ataques (list): Una lista de objetos de ataque.

    Returns:
        str: Una cadena con los ataques formateados, o "-" si no hay ataques.
    """
    if not ataques:
        return "-"
    return ", ".join([f"{a.nombre} ({a.tipo})" for a in ataques])


# Configuración de la página
st.set_page_config(page_title="Listado de Pokémon", layout="wide")

st.header("Listado de Pokémon")

try:
    # Conexión a la base de datos y al controlador
    db = get_db()
    controller = PokemonController(db["pokemons"])

    # Filtros de búsqueda
    with st.expander("Filtros de búsqueda", expanded=True):
        nombre_filtro = st.text_input("Nombre contiene")
        region_filtro = st.text_input("Región")
        min_pokedex = st.number_input("Pokedex mínimo", min_value=0, value=0)

    # Construcción del filtro para la consulta a la base de datos
    filtro = {}
    if nombre_filtro:
        filtro["nombre"] = {"$regex": nombre_filtro, "$options": "i"}
    if region_filtro:
        filtro["region"] = {"$regex": region_filtro, "$options": "i"}
    if min_pokedex > 0:
        filtro["pokedex_nacional"] = {"$gte": min_pokedex}

    # Búsqueda de Pokémon con los filtros aplicados
    pokemons = controller.find(filtro, limit=200)

    if not pokemons:
        st.info("No se encontraron Pokémon con esos filtros.")
    else:
        # Selección y eliminación de Pokémon
        delete_button_key = "delete_pokemon_button"
        pokemon_to_delete_id = st.selectbox(
            "Selecciona un Pokémon para eliminar",
            options=[""] + [p.id for p in pokemons],
            format_func=lambda x: next(
                (p.nombre for p in pokemons if p.id == x), "Seleccionar..."
            ),
        )

        if st.button("Eliminar Pokémon Seleccionado", key=delete_button_key):
            if pokemon_to_delete_id:
                ok = controller.delete(str(pokemon_to_delete_id))
                if ok:
                    st.success("Pokémon eliminado correctamente.")
                    st.rerun()
                else:
                    st.error("Error al eliminar el Pokémon.")
            else:
                st.warning("Por favor, selecciona un Pokémon para eliminar.")

        # Preparación de los datos para la tabla
        data = [
            {
                "Imagen": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{p.pokedex_nacional}.png",
                "ID": str(p.id),
                "Nombre": p.nombre,
                "Región": p.region,
                "Pokedex": p.pokedex_nacional,
                "Tipo 1": p.tipo_primario,
                "Tipo 2": p.tipo_secundario,
                "Nivel": p.nivel,
                "Ataques": format_ataques(p.ataques),
            }
            for p in pokemons
        ]

        # Visualización de los datos en una tabla
        st.dataframe(
            data,
            use_container_width=True,
            row_height=90,
            column_config={
                "Imagen": st.column_config.ImageColumn("Imagen", width="medium")
            },
        )


except Exception as e:
    st.error(
        f"No se pudo conectar a la base de datos. Verifica que la base de datos '{DB_NAME}' exista y esté cargada. Error: {e}"
    )