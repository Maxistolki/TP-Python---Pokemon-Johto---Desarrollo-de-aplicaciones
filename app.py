"""
app.py – Interfaz Streamlit para "Johto Pokédex Admin"
Ejecutar con:  streamlit run app.py
"""

import streamlit as st
import database as db
import models

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN INICIAL
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Johto Pokédex Admin",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicializar base de datos al arrancar
db.inicializar_db()

# ──────────────────────────────────────────────────────────────────────────────
# CSS PERSONALIZADO
# ──────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Nunito:wght@400;600;700&display=swap');

/* Fondo general */
.stApp { background: #0f0f1a; }
section[data-testid="stSidebar"] { background: #1a1a2e !important; }

/* Tipografía */
h1, h2, h3 { font-family: 'Press Start 2P', monospace !important; }
p, div, span, label { font-family: 'Nunito', sans-serif !important; }

/* Tarjetas */
.poke-card {
    background: linear-gradient(135deg, #1e1e3a 0%, #16213e 100%);
    border: 1px solid #e2b714;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    transition: transform 0.2s;
}
.poke-card:hover { transform: translateY(-3px); }
.poke-card h4 { color: #e2b714; margin: 0 0 8px 0; font-size: 1rem; }
.poke-card p  { color: #ccc; margin: 2px 0; font-size: 0.85rem; }

.trainer-card {
    background: linear-gradient(135deg, #1a2a1a 0%, #0f1f0f 100%);
    border: 1px solid #4caf50;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
}
.trainer-card h4 { color: #4caf50; margin: 0 0 8px 0; font-size: 1rem; }
.trainer-card p  { color: #ccc; margin: 2px 0; font-size: 0.85rem; }

.gym-card {
    background: linear-gradient(135deg, #2a1a2a 0%, #1f0f1f 100%);
    border: 1px solid #ab47bc;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
}
.gym-card h4 { color: #ab47bc; margin: 0 0 8px 0; font-size: 1rem; }
.gym-card p  { color: #ccc; margin: 2px 0; font-size: 0.85rem; }

/* Badge */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-left: 6px;
}
.badge-legendary { background: #e2b714; color: #000; }
.badge-master    { background: #4caf50; color: #000; }
.badge-dispute   { background: #ab47bc; color: #fff; }

/* Barra progreso de medallas */
.medal-bar {
    height: 8px;
    border-radius: 4px;
    background: #333;
    margin: 6px 0;
    overflow: hidden;
}
.medal-fill {
    height: 100%;
    background: linear-gradient(90deg, #e2b714, #ff9800);
    border-radius: 4px;
}

/* Título principal */
.main-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.4rem;
    color: #e2b714;
    text-align: center;
    padding: 1rem 0;
    text-shadow: 0 0 20px rgba(226,183,20,0.5);
}

/* Sidebar nav */
.nav-item {
    font-family: 'Nunito', sans-serif;
    font-size: 0.95rem;
    color: #aaa;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR – NAVEGACIÓN
# ──────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<p class="main-title">🎮 Johto<br>Admin</p>', unsafe_allow_html=True)
    st.divider()
    seccion = st.radio(
        "Navegación",
        ["🏥 Centro Pokémon", "👤 Registro de Entrenadores", "🏟️ Red de Gimnasios"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("Profesor Elm's Lab © 2025")


# ──────────────────────────────────────────────────────────────────────────────
# HELPER: mensajes de éxito / error
# ──────────────────────────────────────────────────────────────────────────────

def ok(msg):  st.success(f"✅ {msg}")
def err(msg): st.error(f"❌ {msg}")


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 – CENTRO POKÉMON
# ══════════════════════════════════════════════════════════════════════════════

if seccion == "🏥 Centro Pokémon":
    st.markdown("## 🏥 Centro Pokémon — Gestión de Especímenes")

    tab_lista, tab_alta, tab_editar, tab_borrar = st.tabs(
        ["📋 Listar", "➕ Nuevo Pokémon", "✏️ Editar", "🗑️ Eliminar"]
    )

    # ── LISTAR ────────────────────────────────────────────────────────────────
    with tab_lista:
        col_f1, col_f2 = st.columns(2)
        tipos = ["Todos"] + db.obtener_tipos_pokemon_unicos()
        entrenadores_raw = db.obtener_entrenadores()
        entrenadores_obj = models.dicts_a_entrenadores(entrenadores_raw)

        with col_f1:
            filtro_tipo = st.selectbox("Filtrar por tipo", tipos)
        with col_f2:
            opciones_e = {"Todos": None} | {e.nombre: e.id for e in entrenadores_obj}
            filtro_e_nombre = st.selectbox("Filtrar por entrenador", list(opciones_e.keys()))
            filtro_e_id = opciones_e[filtro_e_nombre]

        tipo_param = None if filtro_tipo == "Todos" else filtro_tipo
        pokemon_raw = db.obtener_pokemon(filtro_tipo=tipo_param, filtro_entrenador_id=filtro_e_id)
        pokemon_objs = models.dicts_a_pokemon(pokemon_raw)

        st.markdown(f"**{len(pokemon_objs)} Pokémon encontrados**")
        cols = st.columns(3)
        for i, p in enumerate(pokemon_objs):
            leyenda = '<span class="badge badge-legendary">⭐ Legendario</span>' if p.es_legendario() else ''
            with cols[i % 3]:
                st.markdown(f"""
                <div class="poke-card">
                    <h4>{p.emoji_tipo()} {p.nombre_especie} {leyenda}</h4>
                    <p>🆔 ID: {p.id}</p>
                    <p>🔖 Tipo: {p.tipo_principal}</p>
                    <p>📊 Nivel: {p.nivel} — {p.categoria_poder()}</p>
                    <p>👤 Entrenador: {p.nombre_entrenador or 'Sin asignar'}</p>
                </div>
                """, unsafe_allow_html=True)

    # ── ALTA ──────────────────────────────────────────────────────────────────
    with tab_alta:
        st.subheader("Registrar nuevo Pokémon")
        entrenadores_raw2 = db.obtener_entrenadores()
        entrenadores_obj2 = models.dicts_a_entrenadores(entrenadores_raw2)
        opciones_alta = {"Sin asignar": None} | {e.nombre: e.id for e in entrenadores_obj2}

        with st.form("form_nuevo_pokemon"):
            nombre_especie = st.text_input("Nombre de la especie *")
            TIPOS_CONOCIDOS = ['Fuego','Agua','Planta','Eléctrico','Psíquico','Normal',
                               'Roca','Tierra','Volador','Bicho','Veneno','Fantasma',
                               'Dragón','Hielo','Lucha','Acero','Otro']
            tipo_p = st.selectbox("Tipo principal *", TIPOS_CONOCIDOS)
            nivel  = st.number_input("Nivel *", min_value=1, max_value=100, value=5)
            entrenador_nombre = st.selectbox("Asignar a entrenador", list(opciones_alta.keys()))
            submitted = st.form_submit_button("📥 Registrar Pokémon")

        if submitted:
            if not nombre_especie.strip():
                err("El nombre de la especie no puede estar vacío.")
            elif nivel < 1:
                err("El nivel no puede ser menor a 1.")
            else:
                id_e = opciones_alta[entrenador_nombre]
                db.crear_pokemon(nombre_especie.strip(), tipo_p, nivel, id_e)
                ok(f"¡{nombre_especie} registrado exitosamente!")
                st.rerun()

    # ── EDITAR ────────────────────────────────────────────────────────────────
    with tab_editar:
        st.subheader("Editar un Pokémon existente")
        pokemon_raw_e = db.obtener_pokemon()
        pokemon_objs_e = models.dicts_a_pokemon(pokemon_raw_e)
        opciones_poke = {f"[{p.id}] {p.nombre_especie}": p.id for p in pokemon_objs_e}

        if not opciones_poke:
            st.info("No hay Pokémon registrados.")
        else:
            seleccion = st.selectbox("Seleccionar Pokémon", list(opciones_poke.keys()))
            pid = opciones_poke[seleccion]
            poke_actual = db.obtener_pokemon_por_id(pid)

            entrenadores_e = db.obtener_entrenadores()
            entrenadores_oe = models.dicts_a_entrenadores(entrenadores_e)
            opciones_e2 = {"Sin asignar": None} | {e.nombre: e.id for e in entrenadores_oe}

            with st.form("form_editar_pokemon"):
                nuevo_nombre = st.text_input("Nombre", value=poke_actual['nombre_especie'])
                TIPOS_CONOCIDOS2 = ['Fuego','Agua','Planta','Eléctrico','Psíquico','Normal',
                                   'Roca','Tierra','Volador','Bicho','Veneno','Fantasma',
                                   'Dragón','Hielo','Lucha','Acero','Otro']
                idx_tipo = TIPOS_CONOCIDOS2.index(poke_actual['tipo_principal']) if poke_actual['tipo_principal'] in TIPOS_CONOCIDOS2 else 0
                nuevo_tipo  = st.selectbox("Tipo", TIPOS_CONOCIDOS2, index=idx_tipo)
                nuevo_nivel = st.number_input("Nivel", min_value=1, max_value=100, value=poke_actual['nivel'])

                nombres_e2 = list(opciones_e2.keys())
                entrenador_actual_nombre = next(
                    (n for n, i in opciones_e2.items() if i == poke_actual['id_entrenador']), "Sin asignar"
                )
                idx_e2 = nombres_e2.index(entrenador_actual_nombre)
                nuevo_entrenador = st.selectbox("Entrenador", nombres_e2, index=idx_e2)
                guardar = st.form_submit_button("💾 Guardar cambios")

            if guardar:
                if not nuevo_nombre.strip():
                    err("El nombre no puede estar vacío.")
                else:
                    db.actualizar_pokemon(pid, nuevo_nombre.strip(), nuevo_tipo, nuevo_nivel, opciones_e2[nuevo_entrenador])
                    ok("Pokémon actualizado correctamente.")
                    st.rerun()

    # ── BORRAR ────────────────────────────────────────────────────────────────
    with tab_borrar:
        st.subheader("Eliminar un Pokémon")
        pokemon_raw_b = db.obtener_pokemon()
        pokemon_objs_b = models.dicts_a_pokemon(pokemon_raw_b)
        opciones_b = {f"[{p.id}] {p.nombre_especie}": p.id for p in pokemon_objs_b}

        if not opciones_b:
            st.info("No hay Pokémon registrados.")
        else:
            sel_b = st.selectbox("Seleccionar Pokémon a eliminar", list(opciones_b.keys()))
            pid_b = opciones_b[sel_b]
            if st.button("🗑️ Confirmar eliminación", type="primary"):
                db.eliminar_pokemon(pid_b)
                ok(f"Pokémon eliminado.")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 – REGISTRO DE ENTRENADORES
# ══════════════════════════════════════════════════════════════════════════════

elif seccion == "👤 Registro de Entrenadores":
    st.markdown("## 👤 Registro de Entrenadores")

    tab_lista, tab_alta, tab_editar, tab_borrar = st.tabs(
        ["📋 Listar", "➕ Nuevo Entrenador", "✏️ Editar", "🗑️ Eliminar"]
    )

    # ── LISTAR ────────────────────────────────────────────────────────────────
    with tab_lista:
        ciudades = ["Todas"] + db.obtener_ciudades_unicas()
        filtro_ciudad = st.selectbox("Filtrar por ciudad de origen", ciudades)
        ciudad_param = None if filtro_ciudad == "Todas" else filtro_ciudad

        entrenadores_raw = db.obtener_entrenadores(filtro_ciudad=ciudad_param)
        entrenadores_objs = models.dicts_a_entrenadores(entrenadores_raw)

        st.markdown(f"**{len(entrenadores_objs)} entrenadores encontrados**")
        cols = st.columns(3)
        for i, e in enumerate(entrenadores_objs):
            maestro_badge = '<span class="badge badge-master">🏆 Maestro</span>' if e.es_maestro() else ''
            pct = int(e.progreso_medallas() * 100)
            with cols[i % 3]:
                st.markdown(f"""
                <div class="trainer-card">
                    <h4>👤 {e.nombre} {maestro_badge}</h4>
                    <p>🆔 ID: {e.id}</p>
                    <p>🏙️ Ciudad: {e.ciudad_origen or '—'}</p>
                    <p>🎂 Edad: {e.edad or '—'}</p>
                    <p>🥇 Medallas: {e.medallas_ganadas}/8 — {e.rango()}</p>
                    <div class="medal-bar"><div class="medal-fill" style="width:{pct}%"></div></div>
                </div>
                """, unsafe_allow_html=True)

    # ── ALTA ──────────────────────────────────────────────────────────────────
    with tab_alta:
        st.subheader("Registrar nuevo Entrenador")
        with st.form("form_nuevo_entrenador"):
            nombre  = st.text_input("Nombre *")
            ciudad  = st.text_input("Ciudad de origen")
            edad    = st.number_input("Edad *", min_value=1, max_value=120, value=12)
            medallas = st.number_input("Medallas ganadas", min_value=0, max_value=8, value=0)
            submitted = st.form_submit_button("📥 Registrar Entrenador")

        if submitted:
            if not nombre.strip():
                err("El nombre no puede estar vacío.")
            elif edad < 10:
                err("El entrenador debe tener al menos 10 años.")
            else:
                db.crear_entrenador(nombre.strip(), ciudad.strip() or None, edad, medallas)
                ok(f"¡{nombre} registrado exitosamente!")
                st.rerun()

    # ── EDITAR ────────────────────────────────────────────────────────────────
    with tab_editar:
        st.subheader("Editar un Entrenador existente")
        ent_raw_e = db.obtener_entrenadores()
        ent_objs_e = models.dicts_a_entrenadores(ent_raw_e)
        opciones_ent = {f"[{e.id}] {e.nombre}": e.id for e in ent_objs_e}

        if not opciones_ent:
            st.info("No hay entrenadores registrados.")
        else:
            sel_ent = st.selectbox("Seleccionar Entrenador", list(opciones_ent.keys()))
            eid = opciones_ent[sel_ent]
            ent_actual = db.obtener_entrenador_por_id(eid)

            with st.form("form_editar_entrenador"):
                nuevo_nombre  = st.text_input("Nombre",  value=ent_actual['nombre'])
                nueva_ciudad  = st.text_input("Ciudad",  value=ent_actual['ciudad_origen'] or '')
                nueva_edad    = st.number_input("Edad",  min_value=1, max_value=120, value=ent_actual['edad'] or 12)
                nuevas_med    = st.number_input("Medallas", min_value=0, max_value=8, value=ent_actual['medallas_ganadas'])
                guardar = st.form_submit_button("💾 Guardar cambios")

            if guardar:
                if not nuevo_nombre.strip():
                    err("El nombre no puede estar vacío.")
                elif nueva_edad < 10:
                    err("La edad mínima es 10 años.")
                else:
                    db.actualizar_entrenador(eid, nuevo_nombre.strip(), nueva_ciudad or None, nueva_edad, nuevas_med)
                    ok("Entrenador actualizado correctamente.")
                    st.rerun()

    # ── BORRAR ────────────────────────────────────────────────────────────────
    with tab_borrar:
        st.subheader("Eliminar un Entrenador")
        ent_raw_b = db.obtener_entrenadores()
        ent_objs_b = models.dicts_a_entrenadores(ent_raw_b)
        opciones_eb = {f"[{e.id}] {e.nombre}": e.id for e in ent_objs_b}

        if not opciones_eb:
            st.info("No hay entrenadores registrados.")
        else:
            st.warning("⚠️ Eliminar un entrenador también eliminará todos sus Pokémon.")
            sel_eb = st.selectbox("Seleccionar Entrenador a eliminar", list(opciones_eb.keys()))
            eid_b = opciones_eb[sel_eb]
            if st.button("🗑️ Confirmar eliminación", type="primary"):
                db.eliminar_entrenador(eid_b)
                ok("Entrenador eliminado.")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 – RED DE GIMNASIOS
# ══════════════════════════════════════════════════════════════════════════════

elif seccion == "🏟️ Red de Gimnasios":
    st.markdown("## 🏟️ Red de Gimnasios de Johto")

    tab_lista, tab_alta, tab_editar, tab_borrar = st.tabs(
        ["📋 Listar", "➕ Nuevo Gimnasio", "✏️ Editar", "🗑️ Eliminar"]
    )

    # ── LISTAR ────────────────────────────────────────────────────────────────
    with tab_lista:
        tipos_gym = ["Todos"] + db.obtener_tipos_gimnasio_unicos()
        filtro_tg = st.selectbox("Filtrar por tipo de especialidad", tipos_gym)
        tg_param = None if filtro_tg == "Todos" else filtro_tg

        gimnasios_raw = db.obtener_gimnasios(filtro_tipo=tg_param)
        gimnasios_objs = models.dicts_a_gimnasios(gimnasios_raw)

        st.markdown(f"**{len(gimnasios_objs)} gimnasios encontrados**")
        cols = st.columns(3)
        for i, g in enumerate(gimnasios_objs):
            retador_txt = g.nombre_retador if g.tiene_retador() else 'Nadie aún'
            with cols[i % 3]:
                st.markdown(f"""
                <div class="gym-card">
                    <h4>🏟️ {g.nombre_ciudad}</h4>
                    <p>🆔 ID: {g.id}</p>
                    <p>👑 Líder: {g.lider_nombre or '—'}</p>
                    <p>🎯 Tipo: {g.tipo_especialidad or '—'}</p>
                    <p>⚔️ Retador: {retador_txt}</p>
                    <p>{g.estado()}</p>
                </div>
                """, unsafe_allow_html=True)

    # ── ALTA ──────────────────────────────────────────────────────────────────
    with tab_alta:
        st.subheader("Registrar nuevo Gimnasio")
        ent_raw_g = db.obtener_entrenadores()
        ent_objs_g = models.dicts_a_entrenadores(ent_raw_g)
        opciones_g = {"Sin retador": None} | {e.nombre: e.id for e in ent_objs_g}

        with st.form("form_nuevo_gimnasio"):
            nombre_ciudad  = st.text_input("Ciudad *")
            lider_nombre   = st.text_input("Nombre del Líder *")
            tipo_esp       = st.text_input("Tipo de especialidad *")
            retador_nombre = st.selectbox("Retador actual", list(opciones_g.keys()))
            submitted = st.form_submit_button("📥 Registrar Gimnasio")

        if submitted:
            if not nombre_ciudad.strip():
                err("El nombre de la ciudad no puede estar vacío.")
            elif not lider_nombre.strip():
                err("El nombre del líder no puede estar vacío.")
            elif not tipo_esp.strip():
                err("Debes indicar el tipo de especialidad.")
            else:
                db.crear_gimnasio(nombre_ciudad.strip(), lider_nombre.strip(), tipo_esp.strip(), opciones_g[retador_nombre])
                ok(f"¡Gimnasio de {nombre_ciudad} registrado!")
                st.rerun()

    # ── EDITAR ────────────────────────────────────────────────────────────────
    with tab_editar:
        st.subheader("Editar un Gimnasio existente")
        gym_raw_e = db.obtener_gimnasios()
        gym_objs_e = models.dicts_a_gimnasios(gym_raw_e)
        opciones_gym = {f"[{g.id}] {g.nombre_ciudad}": g.id for g in gym_objs_e}

        if not opciones_gym:
            st.info("No hay gimnasios registrados.")
        else:
            sel_gym = st.selectbox("Seleccionar Gimnasio", list(opciones_gym.keys()))
            gid = opciones_gym[sel_gym]
            gym_actual = db.obtener_gimnasio_por_id(gid)

            ent_raw_ge = db.obtener_entrenadores()
            ent_objs_ge = models.dicts_a_entrenadores(ent_raw_ge)
            opciones_ge = {"Sin retador": None} | {e.nombre: e.id for e in ent_objs_ge}

            with st.form("form_editar_gimnasio"):
                nueva_ciudad  = st.text_input("Ciudad", value=gym_actual['nombre_ciudad'])
                nuevo_lider   = st.text_input("Líder",  value=gym_actual['lider_nombre'] or '')
                nuevo_tipo    = st.text_input("Tipo",   value=gym_actual['tipo_especialidad'] or '')
                nombres_ge = list(opciones_ge.keys())
                retador_actual_nombre = next(
                    (n for n, i in opciones_ge.items() if i == gym_actual['id_entrenador_retador']), "Sin retador"
                )
                idx_ge = nombres_ge.index(retador_actual_nombre)
                nuevo_retador = st.selectbox("Retador actual", nombres_ge, index=idx_ge)
                guardar = st.form_submit_button("💾 Guardar cambios")

            if guardar:
                if not nueva_ciudad.strip() or not nuevo_lider.strip():
                    err("Ciudad y Líder no pueden estar vacíos.")
                else:
                    db.actualizar_gimnasio(gid, nueva_ciudad.strip(), nuevo_lider.strip(), nuevo_tipo.strip(), opciones_ge[nuevo_retador])
                    ok("Gimnasio actualizado.")
                    st.rerun()

    # ── BORRAR ────────────────────────────────────────────────────────────────
    with tab_borrar:
        st.subheader("Eliminar un Gimnasio")
        gym_raw_b = db.obtener_gimnasios()
        gym_objs_b = models.dicts_a_gimnasios(gym_raw_b)
        opciones_gb = {f"[{g.id}] {g.nombre_ciudad}": g.id for g in gym_objs_b}

        if not opciones_gb:
            st.info("No hay gimnasios registrados.")
        else:
            sel_gb = st.selectbox("Seleccionar Gimnasio a eliminar", list(opciones_gb.keys()))
            gid_b = opciones_gb[sel_gb]
            if st.button("🗑️ Confirmar eliminación", type="primary"):
                db.eliminar_gimnasio(gid_b)
                ok("Gimnasio eliminado.")
                st.rerun()
