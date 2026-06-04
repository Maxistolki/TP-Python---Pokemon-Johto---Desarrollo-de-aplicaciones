# ──────────────────────────────────────────────────────────────────────────────
# Gimnasio
# ──────────────────────────────────────────────────────────────────────────────

class Gimnasio:
    def __init__(self, datos: dict):
        self.id                  = datos.get('id')
        self.nombre_ciudad       = datos.get('nombre_ciudad', '')
        self.lider_nombre        = datos.get('lider_nombre', '')
        self.tipo_especialidad   = datos.get('tipo_especialidad', '')
        self.id_entrenador_retador = datos.get('id_entrenador_retador')
        self.nombre_retador      = datos.get('nombre_retador', 'Nadie aún')

    # ── Método 1: verifica si el gimnasio tiene un retador activo ─────────────
    def tiene_retador(self) -> bool:
        return self.id_entrenador_retador is not None

    # ── Método 2: estado del gimnasio ─────────────────────────────────────────
    def estado(self) -> str:
        return '⚔️  En disputa' if self.tiene_retador() else '🟢 Disponible'

    def __repr__(self):
        return f"<Gimnasio {self.nombre_ciudad} – Líder: {self.lider_nombre}>"


# ──────────────────────────────────────────────────────────────────────────────
# Función de conversión: lista de dicts → lista de objetos
# ──────────────────────────────────────────────────────────────────────────────

def dicts_a_pokemon(lista_dicts: list) -> list:
    return [Pokemon(d) for d in lista_dicts]


def dicts_a_entrenadores(lista_dicts: list) -> list:
    return [Entrenador(d) for d in lista_dicts]


def dicts_a_gimnasios(lista_dicts: list) -> list:
    return [Gimnasio(d) for d in lista_dicts]
