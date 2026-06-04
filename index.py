"""
index.py — Punto de entrada unificado para los modelos.
Importa y re-exporta todo desde los archivos individuales,
así app.py puede seguir usando: import index as m
"""

from modeloEntrenador import Entrenador, filas_a_entrenadores, MEDALLAS_MAESTRO
from modeloPkmn import Pokemon, filas_a_pokemon, TIPOS_POKEMON, NIVEL_LEGENDARIO
from modeloGimnasio import Gimnasio, filas_a_gimnasios

__all__ = [
    "Entrenador", "filas_a_entrenadores", "MEDALLAS_MAESTRO",
    "Pokemon",    "filas_a_pokemon",      "TIPOS_POKEMON", "NIVEL_LEGENDARIO",
    "Gimnasio",   "filas_a_gimnasios",
]