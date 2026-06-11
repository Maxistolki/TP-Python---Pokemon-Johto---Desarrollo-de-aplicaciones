import sqlite3

DB_PATH = 'region_johto.db'


# ─────────────────────────────────────────────
# CONEXIÓN
# ─────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_base():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entrenadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ciudad_origen TEXT,
            edad INTEGER,
            medallas_ganadas INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_especie TEXT NOT NULL,
            tipo_principal TEXT,
            nivel INTEGER,
            id_entrenador INTEGER,
            FOREIGN KEY (id_entrenador) REFERENCES entrenadores (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gimnasios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_ciudad TEXT NOT NULL,
            lider_nombre TEXT,
            tipo_especialidad TEXT,
            id_entrenador_retador INTEGER,
            FOREIGN KEY (id_entrenador_retador) REFERENCES entrenadores (id)
        )
    ''')

    # Verificar si ya hay datos
    cursor.execute("SELECT COUNT(*) FROM entrenadores")
    count = cursor.fetchone()[0]

    if count == 0:
        entrenadores_iniciales = [
            ('Ash Ketchum', 'Pueblo Paleta', 14, 0),
            ('Misty', 'Ciudad Celeste', 14, 8),
            ('Brock', 'Ciudad Plateada', 15, 8),
            ('Gold', 'Ciudad Trigal', 13, 5),
        ]
        cursor.executemany(
            'INSERT INTO entrenadores (nombre, ciudad_origen, edad, medallas_ganadas) VALUES (?, ?, ?, ?)',
            entrenadores_iniciales
        )

        pokemon_iniciales = [
            ('Pikachu',   'Eléctrico', 25, 1),
            ('Cyndaquil', 'Fuego',     15, 1),
            ('Bulbasaur', 'Planta',    18, 1),
            ('Staryu',    'Agua',      30, 2),
            ('Steelix',   'Acero',     40, 3),
            ('Chikorita', 'Planta',    12, 4),
            ('Totodile',  'Agua',      14, 4),
        ]
        cursor.executemany(
            'INSERT INTO pokemon (nombre_especie, tipo_principal, nivel, id_entrenador) VALUES (?, ?, ?, ?)',
            pokemon_iniciales
        )

        gimnasios_iniciales = [
            ('Ciudad Trigal',   'Falkner',   'Volador',   None),
            ('Ciudad Azalea',   'Bugsy',     'Bicho',     None),
            ('Ciudad Malva',    'Whitney',   'Normal',    None),
            ('Ciudad Ecruteak', 'Morty',     'Fantasma',  2),
            ('Ciudad Olivina',  'Jasmine',   'Acero',     3),
            ('Ciudad Mahoghany','Pryce',     'Hielo',     None),
            ('Ciudad Caoba',    'Clair',     'Dragón',    None),
            ('Ciudad Plateada', 'Chuck',     'Lucha',     3),
        ]
        cursor.executemany(
            'INSERT INTO gimnasios (nombre_ciudad, lider_nombre, tipo_especialidad, id_entrenador_retador) VALUES (?, ?, ?, ?)',
            gimnasios_iniciales
        )

        conn.commit()

    conn.close()


# ─────────────────────────────────────────────
# CRUD ENTRENADORES
# ─────────────────────────────────────────────

def obtener_entrenadores(filtro_ciudad=None):
    conn = get_connection()
    cursor = conn.cursor()
    if filtro_ciudad:
        cursor.execute(
            "SELECT * FROM entrenadores WHERE ciudad_origen = ?", (filtro_ciudad,)
        )
    else:
        cursor.execute("SELECT * FROM entrenadores")
    rows = cursor.fetchall()
    conn.close()
    return [tuple(r) for r in rows]


def obtener_entrenador_por_id(eid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entrenadores WHERE id = ?", (eid,))
    row = cursor.fetchone()
    conn.close()
    return tuple(row) if row else None


def crear_entrenador(nombre, ciudad_origen, edad, medallas_ganadas):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entrenadores (nombre, ciudad_origen, edad, medallas_ganadas) VALUES (?, ?, ?, ?)",
        (nombre, ciudad_origen, edad, medallas_ganadas)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def actualizar_entrenador(eid, nombre, ciudad_origen, edad, medallas_ganadas):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE entrenadores SET nombre=?, ciudad_origen=?, edad=?, medallas_ganadas=? WHERE id=?",
        (nombre, ciudad_origen, edad, medallas_ganadas, eid)
    )
    conn.commit()
    conn.close()


def eliminar_entrenador(eid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pokemon WHERE id_entrenador = ?", (eid,))
    cursor.execute("UPDATE gimnasios SET id_entrenador_retador = NULL WHERE id_entrenador_retador = ?", (eid,))
    cursor.execute("DELETE FROM entrenadores WHERE id = ?", (eid,))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
# CRUD POKEMON
# ─────────────────────────────────────────────

def obtener_pokemon(filtro_tipo=None, filtro_entrenador_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT p.*, e.nombre as nombre_entrenador
        FROM pokemon p
        LEFT JOIN entrenadores e ON p.id_entrenador = e.id
        WHERE 1=1
    """
    params = []
    if filtro_tipo:
        query += " AND p.tipo_principal = ?"
        params.append(filtro_tipo)
    if filtro_entrenador_id:
        query += " AND p.id_entrenador = ?"
        params.append(filtro_entrenador_id)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [tuple(r) for r in rows]


def obtener_pokemon_por_id(pid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemon WHERE id = ?", (pid,))
    row = cursor.fetchone()
    conn.close()
    return tuple(row) if row else None


def crear_pokemon(nombre_especie, tipo_principal, nivel, id_entrenador):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pokemon (nombre_especie, tipo_principal, nivel, id_entrenador) VALUES (?, ?, ?, ?)",
        (nombre_especie, tipo_principal, nivel, id_entrenador)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def actualizar_pokemon(pid, nombre_especie, tipo_principal, nivel, id_entrenador):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pokemon SET nombre_especie=?, tipo_principal=?, nivel=?, id_entrenador=? WHERE id=?",
        (nombre_especie, tipo_principal, nivel, id_entrenador, pid)
    )
    conn.commit()
    conn.close()


def eliminar_pokemon(pid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pokemon WHERE id = ?", (pid,))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
# CRUD GIMNASIOS
# ─────────────────────────────────────────────

def obtener_gimnasios(filtro_tipo=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT g.*, e.nombre as nombre_retador
        FROM gimnasios g
        LEFT JOIN entrenadores e ON g.id_entrenador_retador = e.id
        WHERE 1=1
    """
    params = []
    if filtro_tipo:
        query += " AND g.tipo_especialidad = ?"
        params.append(filtro_tipo)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [tuple(r) for r in rows]


def obtener_gimnasio_por_id(gid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gimnasios WHERE id = ?", (gid,))
    row = cursor.fetchone()
    conn.close()
    return tuple(row) if row else None


def crear_gimnasio(nombre_ciudad, lider_nombre, tipo_especialidad, id_entrenador_retador=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO gimnasios (nombre_ciudad, lider_nombre, tipo_especialidad, id_entrenador_retador) VALUES (?, ?, ?, ?)",
        (nombre_ciudad, lider_nombre, tipo_especialidad, id_entrenador_retador)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def actualizar_gimnasio(gid, nombre_ciudad, lider_nombre, tipo_especialidad, id_entrenador_retador=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE gimnasios SET nombre_ciudad=?, lider_nombre=?, tipo_especialidad=?, id_entrenador_retador=? WHERE id=?",
        (nombre_ciudad, lider_nombre, tipo_especialidad, id_entrenador_retador, gid)
    )
    conn.commit()
    conn.close()


def eliminar_gimnasio(gid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gimnasios WHERE id = ?", (gid,))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def obtener_ciudades_unicas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ciudad_origen FROM entrenadores WHERE ciudad_origen IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]


def obtener_tipos_pokemon_unicos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT tipo_principal FROM pokemon WHERE tipo_principal IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]


def obtener_tipos_gimnasio_unicos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT tipo_especialidad FROM gimnasios WHERE tipo_especialidad IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]
