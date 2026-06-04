"""
modeloPkmn.py — Clase Pokemon y su función de conversión desde BD.
"""

NIVEL_ESTRELLA = 80

TIPOS_POKEMON = [
    "Agua", "Bicho", "Dragon", "Eléctrico", "Fantasma",
    "Fuego", "Hielo", "Lucha", "Normal", "Planta",
    "Psíquico", "Roca", "Tierra", "Veneno", "Volador",
]


class Pokemon:
    """Representa un espécimen Pokémon registrado en la Pokédex."""

    def __init__(self, id, nombre_especie, tipo_principal, nivel, entrenador=None):
        self.id = id
        self.nombre_especie = nombre_especie
        self.tipo_principal = tipo_principal or "Desconocido"
        self.nivel = nivel or 1
        self.entrenador = entrenador  # nombre del entrenador (string) o None

    def es_estrella(self) -> bool:
        """Un Pokémon se considera estrella si supera el nivel umbral."""
        return self.nivel >= NIVEL_ESTRELLA

    def categoria(self) -> str:
        """Clasifica al Pokémon según su nivel de poder."""
        if self.nivel < 10:
            return "Cría"
        elif self.nivel < 25:
            return "En entrenamiento"
        elif self.nivel < 50:
            return "Experimentado"
        elif self.nivel < 80:
            return "⚡ Élite"
        else:
            return "🌟 estrella"

    def esta_libre(self) -> bool:
        """Devuelve True si el Pokémon no pertenece a ningún entrenador."""
        return self.entrenador is None

    def __repr__(self):
        return f"Pokemon({self.nombre_especie}, nivel={self.nivel}, tipo={self.tipo_principal})"


def filas_a_pokemon(filas: list) -> list:
    """Convierte una lista de tuplas de BD en objetos Pokemon.
    Espera columnas: id, nombre_especie, tipo_principal, nivel, entrenador_nombre
    """
    return [
        Pokemon(id=f[0], nombre_especie=f[1], tipo_principal=f[2], nivel=f[3], entrenador=f[4])
        for f in filas
    ]