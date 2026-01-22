# -*- coding: utf-8 -*-
"""
Módulo de modelos de datos Pydantic.

Este módulo define los modelos de datos utilizados en la aplicación,
incluyendo el modelo principal `Pokemon` y otros modelos auxiliares.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Clase personalizada para manejar ObjectId de MongoDB en modelos Pydantic.
    """

    @classmethod
    def __get_validators__(cls):
        """
        Define los validadores para el tipo PyObjectId.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        """
        Validador de ObjectId para Pydantic v2.

        Args:
            v: El valor a validar.
            info: Información adicional que Pydantic pasa (se puede ignorar).

        Raises:
            ValueError: Si el valor no es un ObjectId válido.

        Returns:
            ObjectId: El ObjectId validado.
        """
        if v is None:
            return None
        if isinstance(v, ObjectId):
            return v
        try:
            return ObjectId(str(v))
        except Exception:
            raise ValueError("Invalid ObjectId")


class Attack(BaseModel):
    """
    Modelo Pydantic para representar un ataque de un Pokémon.
    """
    nombre: str
    tipo: str


class Pokemon(BaseModel):
    """
    Modelo Pydantic para representar un Pokémon.
    """
    id: Optional[PyObjectId] = Field(None, alias="_id")
    nombre: str
    region: Optional[str] = None
    pokedex_nacional: Optional[int] = None
    tipo_primario: Optional[str] = None
    tipo_secundario: Optional[str] = None
    nivel: Optional[int] = None
    ataques: Optional[List[Attack]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """
        Configuración del modelo Pydantic.
        """
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

    @validator("nombre")
    def nombre_no_vacio(cls, v):
        """
        Validador para asegurar que el nombre del Pokémon no esté vacío.
        """
        if not v or not v.strip():
            raise ValueError("nombre no puede estar vacío")
        return v.strip()