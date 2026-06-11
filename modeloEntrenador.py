"""
modeloEntrenador.py — Clase Entrenador y su función de conversión desde BD.
"""

MEDALLAS_MAESTRO = 8


class Entrenador:
    """Representa a un entrenador de la región Johto."""

    def __init__(self, id, nombre, ciudad_origen, edad, medallas_ganadas):
        self.id = id
        self.nombre = nombre
        self.ciudad_origen = ciudad_origen or "Desconocida"
        self.edad = edad or 0
        self.medallas_ganadas = medallas_ganadas or 0

    def es_maestro(self) -> bool:
        """Un entrenador es Maestro Pokémon si tiene las 8 medallas de Johto."""
        return self.medallas_ganadas >= MEDALLAS_MAESTRO

    def rango(self) -> str:
        """Devuelve el rango del entrenador según sus medallas."""
        if self.medallas_ganadas == 0:
            return "Novato"
        elif self.medallas_ganadas <= 2:
            return "Aprendiz"
        elif self.medallas_ganadas <= 5:
            return "Veterano"
        elif self.medallas_ganadas <= 7:
            return "Experto"
        else:
            return "🏆 Maestro Pokémon"

    def __repr__(self):
        return f"Entrenador({self.nombre}, medallas={self.medallas_ganadas})"


def filas_a_entrenadores(filas: list) -> list:
    """Convierte una lista de tuplas de BD en objetos Entrenador."""
    return [
        Entrenador(id=f[0], nombre=f[1], ciudad_origen=f[2], edad=f[3], medallas_ganadas=f[4])
        for f in filas
    ]