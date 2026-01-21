import os
from pymongo import MongoClient
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI", "mongodb://admin:admin123@localhost:27017/?authSource=admin"
)
DB_NAME = os.getenv("DB_NAME", "appdb")


@st.cache_resource
def get_client() -> MongoClient:
    client = MongoClient(MONGO_URI)
    # simple ping para comprobar
    client.admin.command("ping")
    return client


def get_db():
    return get_client()[DB_NAME]
