# Game View: input del giocatore (tastiera).

import arcade
from Costanti import *
from Views import PauseView
from Musica import cambia_musica
from Game_logic import GameLogic


class GameView(GameLogic):

    def on_key_press(self, key, modifiers):
        # Salto (supporta freccia su, spazio e W)
        if key in (arcade.key.UP, arcade.key.SPACE, arcade.key.W):
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.Sound(SFX_JUMP).play(volume=25)  # suona l'effetto di salto

        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Pausa
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))

        # COMANDI AMMINISTRATORE
        if key == arcade.key.Z:
            self.score = 30                                       # imposta monete a 30
        if key == arcade.key.X:
            self.player_sprite.center_x = self.level_width - 60  # teletrasporto alla fine


    def on_key_release(self, key, modifiers):
        # Ferma il movimento orizzontale al rilascio del tasto
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0

        if key == arcade.key.P:
            self.setup()  # reset rapido del gioco
            cambia_musica(self.window, MUSIC_PLATFORMER)