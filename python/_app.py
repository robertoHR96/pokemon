import streamlit as st
from db import get_db
from controller import PokemonController
from models import Pokemon
from bson import ObjectId

# Setup
COLLECTION_NAME = "pokemons"
db = get_db()
col = db[COLLECTION_NAME]
controller = PokemonController(col)

st.set_page_config(page_title="Pokedex CRUD", layout="wide")

st.title("Pokedex — CRUD con MongoDB")

# Sidebar: búsqueda / filtros
st.sidebar.header("Buscar / Filtros")
q_nombre = st.sidebar.text_input("Nombre contiene")
q_region = st.sidebar.text_input("Región")
min_pokedex = st.sidebar.number_input("Pokedex mínimo", min_value=0, value=0)
buscar = st.sidebar.button("Buscar")

# Main layout: list + formulario
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Listado")
    # build filter
    f = {}
    if q_nombre:
        f["nombre"] = {"$regex": q_nombre, "$options": "i"}
    if q_region:
        f["region"] = {"$regex": q_region, "$options": "i"}
    if min_pokedex:
        f["pokedex_nacional"] = {"$gte": int(min_pokedex)}

    pokemons = controller.find(f, limit=200)
    if not pokemons:
        st.info("No se encontraron pokemons con esos filtros.")
    else:
        # show table
        rows = []
        for p in pokemons:
            rows.append(
                {
                    "_id": str(p.id) if p.id else "",
                    "nombre": p.nombre,
                    "region": p.region,
                    "pokedex": p.pokedex_nacional,
                    "tipo1": p.tipo_primario,
                    "tipo2": p.tipo_secundario,
                    "nivel": p.nivel,
                    "ataques": ", ".join(a.nombre for a in (p.ataques or [])),
                }
            )
        st.dataframe(rows)

        # acciones por fila (editar / borrar)
        st.markdown("### Acciones")
        to_edit = st.selectbox(
            "Selecciona ID para editar", [r["_id"] for r in rows] + [""]
        )
        if to_edit:
            st.session_state.edit_id = to_edit

        if st.button("Borrar seleccionado"):
            if "edit_id" in st.session_state and st.session_state.edit_id:
                ok = controller.delete(st.session_state.edit_id)
                if ok:
                    st.success("Borrado OK")
                    del st.session_state["edit_id"]
                else:
                    st.error("Error borrando")
            else:
                st.warning("Selecciona un ID para borrar")

with col2:
    st.subheader("Crear / Editar Pokemon")
    edit_id = st.session_state.get("edit_id", "")
    if edit_id:
        st.info(f"Editando ID: {edit_id}")
        p = controller.find_by_id(edit_id)
        if p:
            nombre_val = p.nombre
            region_val = p.region or ""
            pokedex_val = p.pokedex_nacional or 0
            tipo1_val = p.tipo_primario or ""
            tipo2_val = p.tipo_secundario or ""
            nivel_val = p.nivel or 1
            ataques_val = "\n".join(f"{a.nombre}||{a.tipo}" for a in (p.ataques or []))
        else:
            st.error("No se encontró el documento seleccionado.")
            nombre_val = region_val = tipo1_val = tipo2_val = ""
            pokedex_val = 0
            nivel_val = 1
            ataques_val = ""
    else:
        nombre_val = ""
        region_val = ""
        pokedex_val = 0
        tipo1_val = ""
        tipo2_val = ""
        nivel_val = 1
        ataques_val = ""

    nombre = st.text_input("Nombre", value=nombre_val)
    region = st.text_input("Región", value=region_val)
    pokedex_nacional = st.number_input(
        "Pokedex nacional", min_value=0, value=int(pokedex_val)
    )
    tipo_primario = st.text_input("Tipo primario", value=tipo1_val)
    tipo_secundario = st.text_input("Tipo secundario", value=tipo2_val)
    nivel = st.number_input("Nivel", min_value=1, max_value=100, value=int(nivel_val))
    st.markdown("**Ataques** (una línea por ataque, formato: nombre||tipo)")
    ataques_raw = st.text_area("Ataques", value=ataques_val, height=120)

    def parse_ataques(text: str):
        items = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if "||" in line:
                nombre_a, tipo_a = line.split("||", 1)
            else:
                nombre_a, tipo_a = line, "Normal"
            items.append({"nombre": nombre_a.strip(), "tipo": tipo_a.strip()})
        return items

    if st.button("Guardar"):
        payload = {
            "nombre": nombre,
            "region": region or None,
            "pokedex_nacional": int(pokedex_nacional) if pokedex_nacional else None,
            "tipo_primario": tipo_primario or None,
            "tipo_secundario": tipo_secundario or None,
            "nivel": int(nivel),
            "ataques": parse_ataques(ataques_raw),
        }
        if edit_id:
            updated = controller.update(edit_id, payload)
            if updated:
                st.success("Actualizado correctamente")
                del st.session_state["edit_id"]
            else:
                st.error("Error al actualizar")
        else:
            created = controller.insert(payload)
            st.success(f"Creado con ID {created.id}")

    if st.button("Limpiar formulario"):
        if "edit_id" in st.session_state:
            del st.session_state["edit_id"]
        st.experimental_rerun()
