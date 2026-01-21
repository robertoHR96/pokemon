from typing import List, Optional, Dict, Any
from pymongo.collection import Collection
from pymongo import ReturnDocument
from datetime import datetime
from bson import ObjectId
from models import Pokemon, PyObjectId


class PokemonController:
    """
    Controller para manejar la colección 'pokemons' en MongoDB.
    Proporciona CRUD completo y búsqueda por nombre.
    """

    def __init__(self, collection: Collection):
        """
        Inicializa el controller con una colección de PyMongo.
        Crea índices recomendados para consultas frecuentes.
        """
        self.col = collection

        # Índices recomendados
        self.col.create_index("nombre", unique=False)
        self.col.create_index("pokedex_nacional", unique=False)

    def _now(self) -> datetime:
        """
        Retorna la fecha y hora UTC actual.
        """
        return datetime.utcnow()

    # -------------------
    # CREATE
    # -------------------
    def insert(self, payload: Dict[str, Any]) -> Pokemon:
        """
        Inserta un nuevo Pokémon en la base de datos.
        Agrega campos 'created_at' y 'updated_at'.
        Devuelve el objeto Pokemon insertado.
        """
        now = self._now()
        payload.update({"created_at": now, "updated_at": now})

        res = self.col.insert_one(payload)
        doc = self.col.find_one({"_id": res.inserted_id})
        return Pokemon.model_validate(doc)  # Pydantic v2

    # -------------------
    # READ
    # -------------------
    def find_by_id(self, id_str: str) -> Optional[Pokemon]:
        """
        Busca un Pokémon por su ObjectId.
        Retorna None si no existe o el id no es válido.
        """
        try:
            oid = PyObjectId.validate(id_str)
        except Exception:
            return None

        doc = self.col.find_one({"_id": oid})
        return Pokemon.model_validate(doc) if doc else None

    def find(
        self, filter: Optional[Dict[str, Any]] = None, limit: int = 50, skip: int = 0
    ) -> List[Pokemon]:
        """
        Busca Pokémon con filtro opcional.
        - filter: Diccionario de consulta MongoDB.
        - limit: número máximo de documentos a retornar.
        - skip: número de documentos a saltar (paginación).
        Retorna lista de instancias Pokemon.
        """
        f = filter or {}
        cursor = self.col.find(f).skip(skip).limit(limit)
        return [Pokemon.model_validate(d) for d in cursor]

    def find_by_name(self, name: str, exact: bool = False) -> List[Pokemon]:
        """
        Busca Pokémon por nombre.
        - exact=True -> nombre exacto
        - exact=False -> búsqueda parcial (regex, case-insensitive)
        """
        if exact:
            filter_query = {"nombre": name}
        else:
            filter_query = {"nombre": {"$regex": name, "$options": "i"}}

        return self.find(filter_query, limit=200)

    # -------------------
    # UPDATE
    # -------------------
    def update(self, id_str: str, update_fields: Dict[str, Any]) -> Optional[Pokemon]:
        """
        Actualiza un Pokémon por su ObjectId.
        Retorna el objeto actualizado o None si no existe.
        """
        try:
            oid = PyObjectId.validate(id_str)
        except Exception:
            return None

        update_fields["updated_at"] = self._now()

        doc = self.col.find_one_and_update(
            {"_id": oid}, {"$set": update_fields}, return_document=ReturnDocument.AFTER
        )
        return Pokemon.model_validate(doc) if doc else None

    # -------------------
    # DELETE
    # -------------------
    def delete(self, id_str: str) -> bool:
        """
        Borra un Pokémon por su ObjectId.
        Retorna True si se eliminó, False si no existía.
        """
        try:
            oid = PyObjectId.validate(id_str)
        except Exception:
            return False

        res = self.col.delete_one({"_id": oid})
        return res.deleted_count == 1

    def delete_many(self, filter: Dict[str, Any]) -> int:
        """
        Borra múltiples Pokémon según un filtro.
        Retorna la cantidad de documentos eliminados.
        """
        res = self.col.delete_many(filter)
        return res.deleted_count
