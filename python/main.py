"""
Esto es una prueba para probar cosas
    Enviar ejercicio a cosme.morales@viewnext.com
    
"""

from db import get_db
from controller import PokemonController

COLLECTION_NAME = "pokemons"
db = get_db()
col = db[COLLECTION_NAME]
controller = PokemonController(col)

result = controller.find_by_name("a")
print(result)
