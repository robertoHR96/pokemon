# -*- coding: utf-8 -*-
"""
Módulo principal para pruebas y ejecución de scripts.

Este módulo se utiliza para realizar pruebas rápidas y ejecutar scripts
relacionados con la base de datos de Pokémon.
"""

from db import get_db
from controller import PokemonController

# Nombre de la colección en la base de datos
COLLECTION_NAME = "pokemons"

# Obtiene la instancia de la base de datos y la colección
db = get_db()
col = db[COLLECTION_NAME]

# Crea una instancia del controlador de Pokémon
controller = PokemonController(col)

# Ejemplo de uso: busca Pokémon por nombre y muestra el resultado
result = controller.find_by_name("a")
print(result)