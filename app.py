"""
app.py — Interfaz principal de Johto Pokédex Admin
Ejecutar con: streamlit run app.py
"""

import streamlit as st
import database as db
import index as m

# ─────────────────────────────────────────────
# CONFIGURACIÓN INICIAL
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Johto Pokédex Admin",
    page_icon="🏆",
    layout="wide",
)

db.inicializar_base()

# ─────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #e63946;
        letter-spacing: -1px;
    }
    .section-badge {
        background: #e63946;
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .stat-box {
        background: #f8f9fa;
        border-left: 4px solid #e63946;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<p class="main-title">🏆 Johto Pokédex Admin</p>', unsafe_allow_html=True)
st.caption("Sistema de gestión del Laboratorio del Profesor Elm — Región Johto")
st.divider()

# ─────────────────────────────────────────────
# NAVEGACIÓN
# ─────────────────────────────────────────────
seccion = st.sidebar.radio(
    "Navegación",
    ["🏥 Centro Pokémon", "🎒 Registro de Entrenadores", "🏟️ Red de Gimnasios"],
    index=0,
)

# ═══════════════════════════════════════════════════════
# SECCIÓN 1 — CENTRO POKÉMON
# ═══════════════════════════════════════════════════════
if seccion == "🏥 Centro Pokémon":
    st.subheader("🏥 Centro Pokémon — Gestión de Especímenes")

    tab_lista, tab_nuevo, tab_editar, tab_borrar = st.tabs(
        ["📋 Ver Pokémon", "➕ Registrar", "✏️ Editar", "🗑️ Eliminar"]
    )

    # ── Listar ──────────────────────────────────────────
    with tab_lista:
        tipos = ["Todos"] + db.obtener_tipos_pokemon_unicos()
        filtro_tipo = st.selectbox("Filtrar por tipo", tipos)

        filas = db.obtener_pokemon(None if filtro_tipo == "Todos" else filtro_tipo)
        pokemon_list = m.filas_a_pokemon(filas)

        if not pokemon_list:
            st.info("No hay Pokémon registrados con ese filtro.")
        else:
            for p in pokemon_list:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 2])
                    col1.markdown(f"**{p.nombre_especie}** `#{p.id}`")
                    col2.write(f"🔖 {p.tipo_principal}")
                    col3.write(f"Nv. {p.nivel}")
                    entrenador_txt = p.entrenador if p.entrenador else "Libre 🌿"
                    col4.write(f"👤 {entrenador_txt}")
                    st.caption(f"Categoría: {p.categoria()}  |  Legendario: {'✅' if p.es_legendario() else '❌'}")
                    st.divider()

    # ── Crear ────────────────────────────────────────────
    with tab_nuevo:
        st.markdown("#### Nuevo espécimen")
        with st.form("form_nuevo_pokemon"):
            nombre_esp = st.text_input("Nombre de la especie")
            tipo = st.selectbox("Tipo principal", m.TIPOS_POKEMON)
            nivel = st.number_input("Nivel", min_value=1, max_value=100, value=5)

            entrenadores = db.obtener_entrenadores()
            opciones_ent = {"Sin entrenador": None}
            opciones_ent.update({e[1]: e[0] for e in entrenadores})
            seleccion_ent = st.selectbox("Asignar a entrenador", list(opciones_ent.keys()))

            submitted = st.form_submit_button("Registrar Pokémon")
            if submitted:
                if not nombre_esp.strip():
                    st.error("El nombre de la especie no puede estar vacío.")
                else:
                    id_ent = opciones_ent[seleccion_ent]
                    db.crear_pokemon(nombre_esp.strip(), tipo, nivel, id_ent)
                    st.success(f"✅ {nombre_esp} registrado en la Pokédex.")
                    st.rerun()

    # ── Editar ───────────────────────────────────────────
    with tab_editar:
        st.markdown("#### Editar espécimen existente")
        filas_todos = db.obtener_pokemon()
        if not filas_todos:
            st.info("No hay Pokémon registrados.")
        else:
            opciones_pk = {f"{f[1]} (#{f[0]})": f[0] for f in filas_todos}
            seleccion_pk = st.selectbox("Seleccionar Pokémon", list(opciones_pk.keys()), key="edit_pk_sel")
            id_pk = opciones_pk[seleccion_pk]
            fila = db.obtener_pokemon_por_id(id_pk)

            with st.form("form_editar_pokemon"):
                nombre_esp_e = st.text_input("Nombre de la especie", value=fila[1])
                tipo_e = st.selectbox("Tipo principal", m.TIPOS_POKEMON,
                                      index=m.TIPOS_POKEMON.index(fila[2]) if fila[2] in m.TIPOS_POKEMON else 0)
                nivel_e = st.number_input("Nivel", min_value=1, max_value=100, value=fila[3] or 1)

                entrenadores_e = db.obtener_entrenadores()
                opciones_ent_e = {"Sin entrenador": None}
                opciones_ent_e.update({e[1]: e[0] for e in entrenadores_e})
                ent_actual = next((e[1] for e in entrenadores_e if e[0] == fila[4]), "Sin entrenador")
                seleccion_ent_e = st.selectbox("Entrenador", list(opciones_ent_e.keys()),
                                               index=list(opciones_ent_e.keys()).index(ent_actual))

                submitted_e = st.form_submit_button("Guardar cambios")
                if submitted_e:
                    if not nombre_esp_e.strip():
                        st.error("El nombre no puede estar vacío.")
                    else:
                        db.actualizar_pokemon(id_pk, nombre_esp_e.strip(), tipo_e, nivel_e,
                                              opciones_ent_e[seleccion_ent_e])
                        st.success("✅ Pokémon actualizado.")
                        st.rerun()

    # ── Eliminar ─────────────────────────────────────────
    with tab_borrar:
        st.markdown("#### Eliminar espécimen")
        filas_d = db.obtener_pokemon()
        if not filas_d:
            st.info("No hay Pokémon registrados.")
        else:
            opciones_d = {f"{f[1]} (#{f[0]})": f[0] for f in filas_d}
            sel_d = st.selectbox("Seleccionar Pokémon a eliminar", list(opciones_d.keys()), key="del_pk")
            if st.button("🗑️ Eliminar Pokémon", type="primary"):
                db.eliminar_pokemon(opciones_d[sel_d])
                st.success("Pokémon eliminado del registro.")
                st.rerun()

# ═══════════════════════════════════════════════════════
# SECCIÓN 2 — ENTRENADORES
# ═══════════════════════════════════════════════════════
elif seccion == "🎒 Registro de Entrenadores":
    st.subheader("🎒 Registro de Entrenadores")

    tab_lista, tab_nuevo, tab_editar, tab_borrar = st.tabs(
        ["📋 Ver Entrenadores", "➕ Registrar", "✏️ Editar", "🗑️ Eliminar"]
    )

    # ── Listar ──────────────────────────────────────────
    with tab_lista:
        ciudades = ["Todas"] + db.obtener_ciudades_unicas()
        filtro_ciudad = st.selectbox("Filtrar por ciudad de origen", ciudades)

        filas = db.obtener_entrenadores(None if filtro_ciudad == "Todas" else filtro_ciudad)
        entrenadores = m.filas_a_entrenadores(filas)

        if not entrenadores:
            st.info("No hay entrenadores con ese filtro.")
        else:
            for e in entrenadores:
                col1, col2, col3 = st.columns([3, 2, 3])
                col1.markdown(f"**{e.nombre}** `#{e.id}`")
                col2.write(f"📍 {e.ciudad_origen}")
                col3.write(f"🎖️ {e.medallas_ganadas} medallas — {e.rango()}")
                st.divider()

    # ── Crear ────────────────────────────────────────────
    with tab_nuevo:
        st.markdown("#### Nuevo entrenador")
        with st.form("form_nuevo_ent"):
            nombre_ent = st.text_input("Nombre del entrenador")
            ciudad_ent = st.text_input("Ciudad de origen")
            medallas_ent = st.number_input("Medallas ganadas", min_value=0, max_value=8, value=0)

            submitted_ent = st.form_submit_button("Registrar Entrenador")
            if submitted_ent:
                if not nombre_ent.strip():
                    st.error("El nombre no puede estar vacío.")
                elif not ciudad_ent.strip():
                    st.error("La ciudad de origen no puede estar vacía.")
                else:
                    db.crear_entrenador(nombre_ent.strip(), ciudad_ent.strip(), medallas_ent)
                    st.success(f"✅ Entrenador {nombre_ent} registrado.")
                    st.rerun()

    # ── Editar ───────────────────────────────────────────
    with tab_editar:
        st.markdown("#### Editar entrenador")
        filas_e = db.obtener_entrenadores()
        if not filas_e:
            st.info("No hay entrenadores registrados.")
        else:
            opciones_ent_ed = {f"{f[1]} (#{f[0]})": f[0] for f in filas_e}
            sel_ent_ed = st.selectbox("Seleccionar entrenador", list(opciones_ent_ed.keys()), key="edit_ent_sel")
            id_ent_ed = opciones_ent_ed[sel_ent_ed]
            fila_ent = db.obtener_entrenador_por_id(id_ent_ed)

            with st.form("form_editar_ent"):
                nombre_ed = st.text_input("Nombre", value=fila_ent[1])
                ciudad_ed = st.text_input("Ciudad de origen", value=fila_ent[2] or "")
                medallas_ed = st.number_input("Medallas ganadas", min_value=0, max_value=8,
                                              value=fila_ent[3] or 0)
                submitted_ed = st.form_submit_button("Guardar cambios")
                if submitted_ed:
                    if not nombre_ed.strip():
                        st.error("El nombre no puede estar vacío.")
                    elif not ciudad_ed.strip():
                        st.error("La ciudad no puede estar vacía.")
                    else:
                        db.actualizar_entrenador(id_ent_ed, nombre_ed.strip(), ciudad_ed.strip(), medallas_ed)
                        st.success("✅ Entrenador actualizado.")
                        st.rerun()

    # ── Eliminar ─────────────────────────────────────────
    with tab_borrar:
        st.markdown("#### Eliminar entrenador")
        filas_del = db.obtener_entrenadores()
        if not filas_del:
            st.info("No hay entrenadores registrados.")
        else:
            opciones_del = {f"{f[1]} (#{f[0]})": f[0] for f in filas_del}
            sel_del = st.selectbox("Seleccionar entrenador a eliminar", list(opciones_del.keys()), key="del_ent")
            st.warning("⚠️ Sus Pokémon quedarán sin entrenador asignado.")
            if st.button("🗑️ Eliminar Entrenador", type="primary"):
                db.eliminar_entrenador(opciones_del[sel_del])
                st.success("Entrenador eliminado del registro.")
                st.rerun()

# ═══════════════════════════════════════════════════════
# SECCIÓN 3 — GIMNASIOS
# ═══════════════════════════════════════════════════════
elif seccion == "🏟️ Red de Gimnasios":
    st.subheader("🏟️ Red de Gimnasios de Johto")

    tab_lista, tab_nuevo, tab_editar, tab_borrar = st.tabs(
        ["📋 Ver Gimnasios", "➕ Registrar", "✏️ Editar", "🗑️ Eliminar"]
    )

    # ── Listar ──────────────────────────────────────────
    with tab_lista:
        filas_gym = db.obtener_gimnasios()
        gimnasios = m.filas_a_gimnasios(filas_gym)

        if not gimnasios:
            st.info("No hay gimnasios registrados.")
        else:
            for g in gimnasios:
                col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
                col1.markdown(f"**{g.nombre_ciudad}** `#{g.id}`")
                col2.write(f"👑 {g.lider_nombre}")
                col3.write(f"🔖 {g.tipo_especialidad}")
                retador_txt = g.retador if g.tiene_retador() else "Sin retador"
                col4.write(f"⚔️ {retador_txt}")
                st.caption(f"Debilidades: {', '.join(g.debilidades())}")
                st.divider()

    # ── Crear ────────────────────────────────────────────
    with tab_nuevo:
        st.markdown("#### Nuevo gimnasio")
        with st.form("form_nuevo_gym"):
            ciudad_gym = st.text_input("Ciudad")
            lider_gym = st.text_input("Nombre del líder")
            tipo_gym = st.selectbox("Tipo de especialidad", m.TIPOS_POKEMON)

            entrenadores_gym = db.obtener_entrenadores()
            opciones_retador = {"Sin retador": None}
            opciones_retador.update({e[1]: e[0] for e in entrenadores_gym})
            sel_retador = st.selectbox("Entrenador retador actual", list(opciones_retador.keys()))

            submitted_gym = st.form_submit_button("Registrar Gimnasio")
            if submitted_gym:
                if not ciudad_gym.strip():
                    st.error("La ciudad no puede estar vacía.")
                elif not lider_gym.strip():
                    st.error("El nombre del líder no puede estar vacío.")
                else:
                    db.crear_gimnasio(ciudad_gym.strip(), lider_gym.strip(), tipo_gym,
                                      opciones_retador[sel_retador])
                    st.success(f"✅ Gimnasio de {ciudad_gym} registrado.")
                    st.rerun()

    # ── Editar ───────────────────────────────────────────
    with tab_editar:
        st.markdown("#### Editar gimnasio")
        filas_gym_e = db.obtener_gimnasios()
        if not filas_gym_e:
            st.info("No hay gimnasios registrados.")
        else:
            opciones_gym_e = {f"{f[1]} (#{f[0]})": f[0] for f in filas_gym_e}
            sel_gym_e = st.selectbox("Seleccionar gimnasio", list(opciones_gym_e.keys()), key="edit_gym_sel")
            id_gym_e = opciones_gym_e[sel_gym_e]
            fila_gym = db.obtener_gimnasio_por_id(id_gym_e)

            with st.form("form_editar_gym"):
                ciudad_ge = st.text_input("Ciudad", value=fila_gym[1])
                lider_ge = st.text_input("Líder", value=fila_gym[2] or "")
                tipo_ge = st.selectbox("Tipo especialidad", m.TIPOS_POKEMON,
                                       index=m.TIPOS_POKEMON.index(fila_gym[3]) if fila_gym[3] in m.TIPOS_POKEMON else 0)

                entrenadores_ge = db.obtener_entrenadores()
                opciones_ret_ge = {"Sin retador": None}
                opciones_ret_ge.update({e[1]: e[0] for e in entrenadores_ge})
                ret_actual_ge = next((e[1] for e in entrenadores_ge if e[0] == fila_gym[4]), "Sin retador")
                sel_ret_ge = st.selectbox("Retador", list(opciones_ret_ge.keys()),
                                          index=list(opciones_ret_ge.keys()).index(ret_actual_ge))

                submitted_ge = st.form_submit_button("Guardar cambios")
                if submitted_ge:
                    if not ciudad_ge.strip() or not lider_ge.strip():
                        st.error("Ciudad y líder son obligatorios.")
                    else:
                        db.actualizar_gimnasio(id_gym_e, ciudad_ge.strip(), lider_ge.strip(), tipo_ge,
                                               opciones_ret_ge[sel_ret_ge])
                        st.success("✅ Gimnasio actualizado.")
                        st.rerun()

    # ── Eliminar ─────────────────────────────────────────
    with tab_borrar:
        st.markdown("#### Eliminar gimnasio")
        filas_gym_d = db.obtener_gimnasios()
        if not filas_gym_d:
            st.info("No hay gimnasios registrados.")
        else:
            opciones_gym_d = {f"{f[1]} (#{f[0]})": f[0] for f in filas_gym_d}
            sel_gym_d = st.selectbox("Seleccionar gimnasio a eliminar", list(opciones_gym_d.keys()), key="del_gym")
            if st.button("🗑️ Eliminar Gimnasio", type="primary"):
                db.eliminar_gimnasio(opciones_gym_d[sel_gym_d])
                st.success("Gimnasio eliminado del registro.")
                st.rerun()