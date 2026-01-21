import streamlit as st
from db import get_db
from controller import PokemonController
from models import Pokemon

# -----------------------------
# Configuración
# -----------------------------
st.set_page_config(
    page_title="Pokedex Profesional", layout="wide", initial_sidebar_state="expanded"
)

COLLECTION_NAME = "pokemons"
db = get_db()
col = db[COLLECTION_NAME]
controller = PokemonController(col)

# -----------------------------
# Sidebar: Navegación
# -----------------------------
st.sidebar.title("Pokedex")
page = st.sidebar.radio("Menú", ["Listado", "Crear / Editar", "Estadísticas"])


# -----------------------------
# Funciones auxiliares
# -----------------------------
def format_ataques(ataques):
    if not ataques:
        return "-"
    return ", ".join([f"{a.nombre} ({a.tipo})" for a in ataques])


# -----------------------------
# Página: Listado
# -----------------------------
if page == "Listado":
    st.header("Listado de Pokémon")

    # Filtros
    with st.expander("Filtros de búsqueda", expanded=True):
        nombre_filtro = st.text_input("Nombre contiene")
        region_filtro = st.text_input("Región")
        min_pokedex = st.number_input("Pokedex mínimo", min_value=0, value=0)
        buscar_btn = st.button("Buscar")

    # Construir filtro
    filtro = {}
    if nombre_filtro:
        filtro["nombre"] = {"$regex": nombre_filtro, "$options": "i"}
    if region_filtro:
        filtro["region"] = {"$regex": region_filtro, "$options": "i"}
    if min_pokedex:
        filtro["pokedex_nacional"] = {"$gte": min_pokedex}

    pokemons = controller.find(filtro, limit=200)

    if not pokemons:
        st.info("No se encontraron Pokémon con esos filtros.")
    else:
        # Mostrar tabla profesional
        data = [
            {
                "ID": str(p.id),
                "Nombre": p.nombre,
                "Región": p.region,
                "Pokedex": p.pokedex_nacional,
                "Tipo 1": p.tipo_primario,
                "Tipo 2": p.tipo_secundario,
                "Nivel": p.nivel,
                "Ataques": format_ataques(p.ataques),
            }
            for p in pokemons
        ]
        st.dataframe(data, use_container_width=True)

        # Selección para editar
        edit_id = st.selectbox(
            "Selecciona Pokémon para editar", [""] + [str(p.id) for p in pokemons]
        )
        if edit_id:
            st.session_state.edit_id = edit_id

        if st.button("Borrar seleccionado"):
            if "edit_id" in st.session_state:
                ok = controller.delete(st.session_state.edit_id)
                if ok:
                    st.success("Pokémon eliminado correctamente")
                    del st.session_state["edit_id"]
                    st.experimental_rerun()  # type: ignore
                else:
                    st.error("Error borrando Pokémon")
            else:
                st.warning("Selecciona un Pokémon para borrar")

# -----------------------------
# Página: Crear / Editar
# -----------------------------
elif page == "Crear / Editar":
    st.header("Crear o Editar Pokémon")

    edit_id = st.session_state.get("edit_id", "")
    if edit_id:
        st.info(f"Editando Pokémon con ID: {edit_id}")
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
            st.error("No se encontró el Pokémon seleccionado.")
            nombre_val = region_val = tipo1_val = tipo2_val = ""
            pokedex_val = 0
            nivel_val = 1
            ataques_val = ""
    else:
        nombre_val = region_val = tipo1_val = tipo2_val = ataques_val = ""
        pokedex_val = 0
        nivel_val = 1

    # Formulario
    with st.form("form_pokemon", clear_on_submit=False):
        nombre = st.text_input("Nombre", value=nombre_val)
        region = st.text_input("Región", value=region_val)
        pokedex_nacional = st.number_input(
            "Pokedex nacional", min_value=0, value=int(pokedex_val)
        )
        tipo_primario = st.text_input("Tipo primario", value=tipo1_val)
        tipo_secundario = st.text_input("Tipo secundario", value=tipo2_val)
        nivel = st.number_input(
            "Nivel", min_value=1, max_value=100, value=int(nivel_val)
        )
        st.markdown("**Ataques** (una línea por ataque, formato: nombre||tipo)")
        ataques_raw = st.text_area("Ataques", value=ataques_val, height=150)

        submitted = st.form_submit_button("Guardar Pokémon")
        if submitted:
            ataques_list = []
            for line in ataques_raw.splitlines():
                if "||" in line:
                    nombre_a, tipo_a = line.split("||", 1)
                else:
                    nombre_a, tipo_a = line, "Normal"
                ataques_list.append(
                    {"nombre": nombre_a.strip(), "tipo": tipo_a.strip()}
                )

            payload = {
                "nombre": nombre.strip(),
                "region": region.strip() or None,
                "pokedex_nacional": int(pokedex_nacional) if pokedex_nacional else None,
                "tipo_primario": tipo_primario.strip() or None,
                "tipo_secundario": tipo_secundario.strip() or None,
                "nivel": int(nivel),
                "ataques": ataques_list,
            }

            if edit_id:
                updated = controller.update(edit_id, payload)
                if updated:
                    st.success("Pokémon actualizado correctamente")
                    del st.session_state["edit_id"]
                    st.experimental_rerun()  # type: ignore
                else:
                    st.error("Error al actualizar Pokémon")
            else:
                created = controller.insert(payload)
                st.success(f"Pokémon creado con ID {created.id}")

        if st.button("Limpiar formulario"):
            if "edit_id" in st.session_state:
                del st.session_state["edit_id"]
            st.experimental_rerun()  # type: ignore

# -----------------------------
# Página: Estadísticas
# -----------------------------
elif page == "Estadísticas":
    st.header("Estadísticas Generales")
    total = col.count_documents({})
    st.metric("Total de Pokémon", total)

    tipos_primarios = col.aggregate(
        [{"$group": {"_id": "$tipo_primario", "count": {"$sum": 1}}}]
    )
    st.subheader("Pokémon por Tipo Primario")
    for t in tipos_primarios:
        st.write(f"{t['_id'] or 'Desconocido'}: {t['count']}")
