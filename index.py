import sqlite3

def crear_base_johto():
    # Conexión (si no existe, se crea el archivo)
    conexion = sqlite3.connect('region_johto.db')
    cursor = conexion.cursor()

    # 1. Tabla de ENTRENADORES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entrenadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ciudad_origen TEXT,
            medallas_ganadas INTEGER
        )
    ''')

    # 2. Tabla de POKEMON (Relacionada con Entrenadores)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_especie TEXT NOT NULL,
            tipo_principal TEXT, -- Fuego, Agua, Planta, etc.
            nivel INTEGER,
            id_entrenador INTEGER,
            FOREIGN KEY (id_entrenador) REFERENCES entrenadores (id)
        )
    ''')

    # 3. Tabla de GIMNASIOS
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

    # Datos de ejemplo iniciales (Johto Journey)
    entrenadores_iniciales = [
        ('Ash Ketchum', 'Pueblo Paleta', 0),
        ('Misty', 'Ciudad Celeste', 8),
        ('Brock', 'Ciudad Plateada', 8)
    ]
    
    cursor.executemany('INSERT INTO entrenadores (nombre, ciudad_origen, medallas_ganadas) VALUES (?, ?, ?)', entrenadores_iniciales)

    # Pokemon de ejemplo vinculado a Ash (id 1)
    cursor.execute('INSERT INTO pokemon (nombre_especie, tipo_principal, nivel, id_entrenador) VALUES (?, ?, ?, ?)', 
                   ('Pikachu', 'Eléctrico', 25, 1))
    
    cursor.execute('INSERT INTO pokemon (nombre_especie, tipo_principal, nivel, id_entrenador) VALUES (?, ?, ?, ?)', 
                   ('Cyndaquil', 'Fuego', 15, 1))

    conexion.commit()
    conexion.close()
    print("Base de datos 'region_johto.db' creada exitosamente.")

if __name__ == "__main__":
    crear_base_johto()


