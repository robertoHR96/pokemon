# -*- coding: utf-8 -*-
"""
Módulo del controlador de Pokémon.

Este módulo define la clase `PokemonController`, que se encarga de
la interacción con la base de datos de MongoDB para realizar
operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los Pokémon.
"""

from typing import List, Optional, Dict, Any
from pymongo.collection import Collection
from pymongo import ReturnDocument
from datetime import datetime
from bson import ObjectId
from models import Pokemon, PyObjectId


class PokemonController:
    """
    Controlador para manejar la colección 'pokemons' en MongoDB.

    Proporciona un conjunto completo de métodos para realizar operaciones
    CRUD (Crear, Leer, Actualizar, Eliminar) y búsqueda por nombre.
    """

    def __init__(self, collection: Collection):
        """
        Inicializa el controlador con una colección de PyMongo.

        Además, crea índices en la colección para mejorar el rendimiento
        de las consultas más frecuentes.

        Args:
            collection (Collection): La colección de MongoDB a utilizar.
        """
        self.col = collection

        # Índices recomendados para optimizar las búsquedas
        self.col.create_index("nombre", unique=False)
        self.col.create_index("pokedex_nacional", unique=False)

    def _now(self) -> datetime:
        """
        Retorna la fecha y hora actual en formato UTC.

        Returns:
            datetime: La fecha y hora actual en UTC.
        """
        return datetime.utcnow()

    # -------------------
    # CREATE
    # -------------------
    def insert(self, payload: Dict[str, Any]) -> Pokemon:
        """
        Inserta un nuevo Pokémon en la base de datos.

        Agrega automáticamente los campos 'created_at' y 'updated_at'
        con la fecha y hora actual.

        Args:
            payload (Dict[str, Any]): Un diccionario con los datos del Pokémon.

        Returns:
            Pokemon: El objeto Pokémon insertado, validado con Pydantic.
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

        Args:
            id_str (str): El ID del Pokémon en formato de cadena.

        Returns:
            Optional[Pokemon]: El objeto Pokémon si se encuentra, o None si no existe
                               o el ID no es válido.
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
        Busca Pokémon con un filtro opcional y paginación.

        Args:
            filter (Optional[Dict[str, Any]], optional): Diccionario de consulta de MongoDB.
                                                        Defaults to None.
            limit (int, optional): Número máximo de documentos a retornar. Defaults to 50.
            skip (int, optional): Número de documentos a saltar (para paginación).
                                  Defaults to 0.

        Returns:
            List[Pokemon]: Una lista de instancias de Pokémon.
        """
        f = filter or {}
        cursor = self.col.find(f).skip(skip).limit(limit)
        return [Pokemon.model_validate(d) for d in cursor]

    def find_by_name(self, name: str, exact: bool = False) -> List[Pokemon]:
        """
        Busca Pokémon por nombre.

        Args:
            name (str): El nombre del Pokémon a buscar.
            exact (bool, optional): Si es True, busca el nombre exacto. Si es False,
                                    realiza una búsqueda parcial (regex, case-insensitive).
                                    Defaults to False.

        Returns:
            List[Pokemon]: Una lista de Pokémon que coinciden con la búsqueda.
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

        Actualiza automáticamente el campo 'updated_at' con la fecha y hora actual.

        Args:
            id_str (str): El ID del Pokémon a actualizar.
            update_fields (Dict[str, Any]): Un diccionario con los campos a actualizar.

        Returns:
            Optional[Pokemon]: El objeto Pokémon actualizado si se encuentra, o None
                               si no existe.
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

        Args:
            id_str (str): El ID del Pokémon a borrar.

        Returns:
            bool: True si se eliminó correctamente, False si no existía.
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

        Args:
            filter (Dict[str, Any]): El filtro de MongoDB para seleccionar los
                                     documentos a eliminar.

        Returns:
            int: La cantidad de documentos eliminados.
        """
        res = self.col.delete_many(filter)
        return res.deleted_count