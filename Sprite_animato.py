# ===================== SPRITE ANIMATO =====================

import arcade
from Costanti import *


class SpriteAnimato(arcade.Sprite):
    """Sprite base con supporto per animazioni da spritesheet."""

    def __init__(self, scala: float = 1.0):
        super().__init__(scale=scala)
        self.animazioni = {}           # dizionario con tutte le animazioni registrate
        self.animazione_corrente = None
        self.animazione_default = None
        self.tempo_frame = 0.0         # tempo accumulato per il cambio frame
        self.indice_frame = 0          # frame corrente dell'animazione

    def aggiungi_animazione(
        self,
        nome: str,
        percorso: str,
        frame_width: int,
        frame_height: int,
        num_frame: int,
        colonne: int,
        durata: float,
        loop: bool = True,
        default: bool = False,
        riga: int = 0,
    ):
        # Carica lo spritesheet e ritaglia i frame della riga indicata
        sheet = arcade.load_spritesheet(percorso)
        offset = riga * colonne
        tutti = sheet.get_texture_grid(
            size=(frame_width, frame_height),
            columns=colonne,
            count=offset + num_frame,
        )
        self._registra(nome, tutti[offset:], durata, loop, default)

    def _registra(self, nome, textures, durata, loop, default=False):
        # Salva l'animazione nel dizionario calcolando la durata per singolo frame
        self.animazioni[nome] = {
            "textures": textures,
            "durata_frame": durata / len(textures),
            "loop": loop,
        }
        # La prima animazione registrata diventa quella di default
        if default or self.animazione_default is None:
            self.animazione_default = nome
        if self.animazione_corrente is None:
            self._vai(nome)

    def imposta_animazione(self, nome: str):
        # Cambia animazione solo se è diversa da quella corrente
        if nome != self.animazione_corrente:
            self._vai(nome)

    def _vai(self, nome: str):
        # Resetta l'animazione e imposta il primo frame
        self.animazione_corrente = nome
        self.indice_frame = 0
        self.tempo_frame = 0.0
        self.texture = self.animazioni[nome]["textures"][0]

    def update_animation(self, delta_time: float = 1 / 60):
        anim = self.animazioni[self.animazione_corrente]
        self.tempo_frame += delta_time

        # Aspetta finché non è trascorso il tempo di un frame
        if self.tempo_frame < anim["durata_frame"]:
            return
        self.tempo_frame -= anim["durata_frame"]

        prossimo = self.indice_frame + 1
        if prossimo < len(anim["textures"]):
            self.indice_frame = prossimo
        elif anim["loop"]:
            self.indice_frame = 0      # ricomincia da capo se è in loop
        else:
            self.indice_frame = len(anim["textures"]) - 1  # si ferma all'ultimo frame
            return
        self.texture = anim["textures"][self.indice_frame]