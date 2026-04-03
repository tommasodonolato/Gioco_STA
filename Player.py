# Player 

from Costanti import *
from sprite_animato import SpriteAnimato


class Player(SpriteAnimato):
    # Gestisce il personaggio giocabile con le sue animazioni e il flip orizzontale.

    def __init__(self):
        super().__init__(scala=2.0)
        self._in_aria = False
        self._guarda_destra = True     # direzione in cui guarda il personaggio

        # Animazione idle 
        self.aggiungi_animazione(
            nome="idle",
            percorso=PLAYER_IDLE_SOURCE,
            frame_width=PLAYER_FRAME_WIDTH,
            frame_height=PLAYER_FRAME_HEIGHT,
            num_frame=PLAYER_NUM_FRAME,
            colonne=PLAYER_NUM_FRAME,
            durata=0.8,
            loop=True,
            default=True,
        )

        # Animazione walk 
        self.aggiungi_animazione(
            nome="walk",
            percorso=PLAYER_WALK_SOURCE,
            frame_width=PLAYER_FRAME_WIDTH,
            frame_height=PLAYER_FRAME_HEIGHT,
            num_frame=PLAYER_NUM_FRAME,
            colonne=PLAYER_NUM_FRAME,
            durata=0.6,
            loop=True,
        )

        # Animazione jump (salto, non in loop)
        self.aggiungi_animazione(
            nome="jump",
            percorso=PLAYER_JUMP_SOURCE,
            frame_width=PLAYER_FRAME_WIDTH,
            frame_height=PLAYER_FRAME_HEIGHT,
            num_frame=PLAYER_NUM_FRAME,
            colonne=PLAYER_NUM_FRAME,
            durata=0.4,
            loop=False,
        )

        # Posizione iniziale
        self.center_x = 100
        self.center_y = 150

    def update_animation(self, delta_time: float = 1 / 60):
        # Aggiorna la direzione in base al movimento orizzontale
        if self.change_x > 0:
            self._guarda_destra = True
        elif self.change_x < 0:
            self._guarda_destra = False

        # Flip orizzontale dello sprite tramite scala negativa
        self.scale = (abs(self.scale[0]) if self._guarda_destra
                      else -abs(self.scale[0]), abs(self.scale[1]))

        # Sceglie l'animazione in base allo stato del giocatore
        if abs(self.change_y) > 1.5:
            self._in_aria = True
            if self.animazione_corrente != "jump":
                self.imposta_animazione("jump")
        else:
            self._in_aria = False
            if self.change_x != 0:
                self.imposta_animazione("walk")
            else:
                self.imposta_animazione("idle")

        super().update_animation(delta_time)