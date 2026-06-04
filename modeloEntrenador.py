class Entrenador:
    TOTAL_MEDALLAS_JOHTO = 8

    def __init__(self, datos: dict):
        self.id               = datos.get('id')
        self.nombre           = datos.get('nombre', '')
        self.ciudad_origen    = datos.get('ciudad_origen', '')
        self.edad             = datos.get('edad', 0)
        self.medallas_ganadas = datos.get('medallas_ganadas', 0)

    # ── Método 1: verifica si el entrenador es Maestro Pokémon ───────────────
    def es_maestro(self) -> bool:
        """Un entrenador es Maestro si ganó las 8 medallas de Johto."""
        return self.medallas_ganadas >= self.TOTAL_MEDALLAS_JOHTO

    # ── Método 2: calcula el progreso hacia el título de Maestro ─────────────
    def progreso_medallas(self) -> float:
        """Devuelve el porcentaje de medallas obtenidas (0.0 – 1.0)."""
        return min(self.medallas_ganadas / self.TOTAL_MEDALLAS_JOHTO, 1.0)

    # ── Método 3: devuelve una etiqueta de rango ─────────────────────────────
    def rango(self) -> str:
        m = self.medallas_ganadas
        if m == 0:
            return 'Principiante'
        elif m <= 2:
            return 'Novato'
        elif m <= 5:
            return 'Experimentado'
        elif m < 8:
            return 'Avanzado'
        else:
            return '🏆 Maestro Pokémon'

    def __repr__(self):
        return f"<Entrenador {self.nombre} – {self.medallas_ganadas} medallas>"
