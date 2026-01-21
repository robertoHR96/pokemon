
import streamlit as st
from db import get_db, DB_NAME

st.set_page_config(
    page_title="Estadísticas", 
    layout="wide"
)

st.header("Estadísticas Generales")

try:
    db = get_db()
    col = db["pokemons"]
    total = col.count_documents({})
    st.metric("Total de Pokémon", total)

    tipos_primarios = col.aggregate(
        [{"$group": {"_id": "$tipo_primario", "count": {"$sum": 1}}}]
    )
    st.subheader("Pokémon por Tipo Primario")
    for t in tipos_primarios:
        st.write(f"{t['_id'] or 'Desconocido'}: {t['count']}")
        
except Exception as e:
    st.error(f"No se pudo conectar a la base de datos para cargar estadísticas. Verifica que la base de datos '{DB_NAME}' esté cargada. Error: {e}")
