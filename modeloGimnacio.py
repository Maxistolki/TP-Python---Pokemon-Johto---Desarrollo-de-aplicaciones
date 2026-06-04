"""
modeloGimnasio.py — Clase Gimnasio y su función de conversión desde BD.
"""


class Gimnasio:
    """Representa un Gimnasio Pokémon de la región Johto."""

    TIPOS_DEBILIDADES = {
        "Fuego":     ["Agua", "Roca", "Tierra"],
        "Agua":      ["Planta", "Eléctrico"],
        "Planta":    ["Fuego", "Hielo", "Veneno", "Volador", "Bicho"],
        "Eléctrico": ["Tierra"],
        "Roca":      ["Agua", "Planta", "Lucha", "Tierra"],
        "Volador":   ["Eléctrico", "Hielo", "Roca"],
        "Fantasma":  ["Fantasma", "Oscuro"],
        "Normal":    ["Lucha"],
        "Bicho":     ["Fuego", "Volador", "Roca"],
        "Psíquico":  ["Bicho", "Fantasma", "Oscuro"],
    }

    def __init__(self, id, nombre_ciudad, lider_nombre, tipo_especialidad, retador=None):
        self.id = id
        self.nombre_ciudad = nombre_ciudad
        self.lider_nombre = lider_nombre or "Sin líder"
        self.tipo_especialidad = tipo_especialidad or "Desconocido"
        self.retador = retador  # nombre del entrenador retador o None

    def tiene_retador(self) -> bool:
        """Devuelve True si hay un entrenador desafiando al gimnasio actualmente."""
        return self.retador is not None

    def debilidades(self) -> list:
        """Devuelve los tipos que son efectivos contra la especialidad del gimnasio."""
        return self.TIPOS_DEBILIDADES.get(self.tipo_especialidad, ["Desconocido"])

    def __repr__(self):
        return f"Gimnasio({self.nombre_ciudad}, líder={self.lider_nombre}, tipo={self.tipo_especialidad})"


def filas_a_gimnasios(filas: list) -> list:
    """Convierte una lista de tuplas de BD en objetos Gimnasio.
    Espera columnas: id, nombre_ciudad, lider_nombre, tipo_especialidad, retador_nombre
    """
    return [
        Gimnasio(id=f[0], nombre_ciudad=f[1], lider_nombre=f[2], tipo_especialidad=f[3], retador=f[4])
        for f in filas
    ]