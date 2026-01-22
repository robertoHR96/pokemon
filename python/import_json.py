# -*- coding: utf-8 -*-
"""
Script para importar datos de un archivo JSON a la base de datos.

Este script se utiliza para leer un archivo JSON que contiene datos de Pokémon
y los inserta en la colección 'pokemons' de la base de datos MongoDB.
"""

import json
from db import get_db
from controller import PokemonController


def import_file(path="./"):
    """
    Importa un archivo JSON de Pokémon a la base de datos.

    Args:
        path (str, optional): La ruta al archivo JSON. Defaults to "./".
    """
    db = get_db()
    c = PokemonController(db["pokemons"])
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    inserted = 0
    for doc in data:
        c.insert(doc)
        inserted += 1
    print(f"{inserted} documentos insertados")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python import_json.py data/pokemons.json")
    else:
        import_file(sys.argv[1])