"""
models.py – Clases Python que representan las entidades de la región Johto.
Cada clase se construye a partir de un diccionario proveniente de la base de datos.
"""


# ──────────────────────────────────────────────────────────────────────────────
# Pokémon
# ──────────────────────────────────────────────────────────────────────────────

class Pokemon:
    TIPOS_EMBLEMA = {
        'Fuego':     '🔥',
        'Agua':      '💧',
        'Planta':    '🌿',
        'Eléctrico': '⚡',
        'Psíquico':  '🔮',
        'Normal':    '⭐',
        'Roca':      '🪨',
        'Tierra':    '🌍',
        'Volador':   '🌬️',
        'Bicho':     '🐛',
        'Veneno':    '☠️',
        'Fantasma':  '👻',
        'Dragón':    '🐉',
        'Hielo':     '❄️',
        'Lucha':     '🥊',
        'Acero':     '⚙️',
    }

    def __init__(self, datos: dict):
        self.id               = datos.get('id')
        self.nombre_especie   = datos.get('nombre_especie', '')
        self.tipo_principal   = datos.get('tipo_principal', '')
        self.nivel            = datos.get('nivel', 1)
        self.id_entrenador    = datos.get('id_entrenador')
        self.nombre_entrenador = datos.get('nombre_entrenador', 'Sin entrenador')

    # ── Método 1: determina si el Pokémon es Legendario por su nivel ──────────
    def es_legendario(self) -> bool:
        """Un Pokémon se considera 'Legendario' si su nivel supera 60."""
        return self.nivel > 60

    # ── Método 2: calcula la categoría de poder ───────────────────────────────
    def categoria_poder(self) -> str:
        """Devuelve una etiqueta de potencia según el nivel."""
        if self.nivel <= 10:
            return 'Novato'
        elif self.nivel <= 30:
            return 'En entrenamiento'
        elif self.nivel <= 60:
            return 'Veterano'
        else:
            return '⭐ Estrella'

    # ── Método 3: devuelve el emoji del tipo ─────────────────────────────────
    def emoji_tipo(self) -> str:
        return self.TIPOS_EMBLEMA.get(self.tipo_principal, '❓')

    def __repr__(self):
        return f"<Pokemon {self.nombre_especie} Nv.{self.nivel} ({self.tipo_principal})>"


