

import streamlit as st

def pokemon_form(pokemon=None):
    """
    Renders a form for creating or editing a Pokémon.
    - If `pokemon` is provided, the form is pre-filled for editing.
    - Otherwise, it's a creation form.
    Returns a dictionary with the form data if submitted, otherwise None.
    """
    if pokemon:
        nombre_val = pokemon.nombre
        region_val = pokemon.region or ""
        pokedex_val = pokemon.pokedex_nacional or 0
        tipo1_val = pokemon.tipo_primario or ""
        tipo2_val = pokemon.tipo_secundario or ""
        nivel_val = pokemon.nivel or 1
        ataques_val = "\n".join(f"{a.nombre}||{a.tipo}" for a in (pokemon.ataques or []))
    else:
        nombre_val = region_val = tipo1_val = tipo2_val = ataques_val = ""
        pokedex_val = 0
        nivel_val = 1

    with st.form("form_pokemon", clear_on_submit=True):
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
        return payload

    return None

