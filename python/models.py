from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime
from bson import ObjectId

from bson import ObjectId


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        """
        Validador de ObjectId para Pydantic v2
        info: información adicional que Pydantic pasa, se puede ignorar
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
    nombre: str
    tipo: str


class Pokemon(BaseModel):
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
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

    @validator("nombre")
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("nombre no puede estar vacío")
        return v.strip()
