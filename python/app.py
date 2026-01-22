# -*- coding: utf-8 -*-
"""
Módulo principal de la aplicación de Streamlit.

Este módulo configura la página principal de la aplicación,
mostrando un mensaje de bienvenida y una guía de uso.
"""

import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Pokedex Profesional - Inicio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título de la página principal
st.title("¡Bienvenido al Pokedex Profesional!")

# Contenido de la página principal en formato Markdown
st.markdown(
    """
    Esta es una aplicación de Streamlit para gestionar una base de datos de Pokémon en MongoDB.

    ### ¿Cómo empezar?
    
    1.  **Navega por las páginas en el menú de la izquierda.**
    2.  **Administración**: Si es la primera vez que usas la app, ve a esta página para cargar la base de datos desde el archivo JSON. También puedes eliminar la base de datos aquí.
    3.  **Listado**: Muestra todos los Pokémon en la base de datos. Puedes filtrar y eliminar Pokémon desde aquí.
    4.  **Crear Pokémon**: Añade un nuevo Pokémon a la base de datos.
    5.  **Editar Pokémon**: Busca un Pokémon existente por su nombre y modifica sus datos.
    6.  **Estadísticas**: Muestra algunas estadísticas básicas sobre los Pokémon en la base de datos.

    ---
    
    **¡Disfruta de la aplicación!**
    """
)
