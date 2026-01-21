# scripts/import_json.py
import json
from db import get_db
from controller import PokemonController


def import_file(path="./"):
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
        print("Usage: python import_json.py data/pokemons.json")
    else:
        import_file(sys.argv[1])
