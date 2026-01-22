# -*- coding: utf-8 -*-
"""
Módulo de conexión a la base de datos MongoDB.

Este módulo se encarga de establecer la conexión con la base de datos
MongoDB, utilizando las variables de entorno para la configuración.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import streamlit as st

# Carga las variables de entorno desde un archivo .env
load_dotenv()

# Obtiene la URI de MongoDB y el nombre de la base de datos de las variables de entorno,
# con valores por defecto si no se encuentran.
MONGO_URI = os.getenv(
    "MONGO_URI", "mongodb://admin:admin123@localhost:27017/?authSource=admin"
)
DB_NAME = os.getenv("DB_NAME", "appdb")


@st.cache_resource
def get_client() -> MongoClient:
    """
    Establece y devuelve una conexión con el cliente de MongoDB.

    Utiliza el decorador `@st.cache_resource` de Streamlit para asegurar que
    la conexión se establezca una sola vez y se reutilice en toda la aplicación.

    Returns:
        MongoClient: Una instancia del cliente de MongoDB.
    """
    client = MongoClient(MONGO_URI)
    # Realiza un "ping" a la base de datos para comprobar la conexión
    client.admin.command("ping")
    return client


def get_db():
    """
    Devuelve una instancia de la base de datos.

    Returns:
        Database: Una instancia de la base de datos de MongoDB.
    """
    return get_client()[DB_NAME]