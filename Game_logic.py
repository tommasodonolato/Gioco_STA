# Game Logic: disegno, aggiornamento fisica, collisioni e fase finale.

import arcade
from Costanti import *
from Views import DialogoView, VittoriaView, GameOverView
from Musica import cambia_musica, stoppa_musica
from Game_setup import GameSetup


class GameLogic(GameSetup):

    def on_draw(self):
        self.clear()

        # Lo sfondo viene disegnato con la ui_camera (coordinate schermo)
        self.ui_camera.use()
        cam_x = self.camera.position[0] - WINDOW_WIDTH / 2
        for layer in self.parallax_layers:
            layer.draw(cam_x)

        # Gli elementi di gioco vengono disegnati con la camera di gioco
        self.camera.use()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        # La strega viene disegnata solo quando è apparsa nella fase finale
        if self.is_final_level and self.strega_apparsa and self.strega_sprite:
            self.strega_list.draw()

        # il punteggio viene disegnato con la ui_camera in posizione fissa
        self.ui_camera.use()
        arcade.draw_text(
            f"MONETE: {self.score}",
            20, WINDOW_HEIGHT - 40,
            arcade.color.GOLD, 20, font_name="Courier New", bold=True
        )


    def pan_camera_to_player(self):
        # Segue il giocatore con la camera usando un lerp per un effetto fluido.
        if self.is_final_level:
            # Nella fase finale la camera segue solo in orizzontale
            self.camera.position = arcade.math.lerp_2d(
                self.camera.position,
                (self.player_sprite.center_x, WINDOW_HEIGHT / 2),
                CAMERA_SPEED
            )
        else:
            # Clamp ai bordi del livello
            target_x = max(self.player_sprite.center_x, WINDOW_WIDTH / 2)
            target_x = min(target_x, self.level_width - WINDOW_WIDTH / 2)
            self.camera.position = arcade.math.lerp_2d(
                self.camera.position,
                (target_x, WINDOW_HEIGHT / 2),
                CAMERA_SPEED
            )


    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update_animation(delta_time)

        # Raccolta monete
        for coin in arcade.check_for_collision_with_list(self.player_sprite, self.coin_list):
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.Sound(SFX_COIN).play()  # suona l'effetto di raccolta moneta

        # Uscita a sinistra: torna al livello precedente (o blocca al bordo)
        if self.player_sprite.left < 0:
            if self.is_final_level:
                self.player_sprite.left = 0
            elif self.current_level > 1:
                self.current_level -= 1
                self.spawn_destra = False
                self.carica_livello(self.current_level)
            else:
                self.player_sprite.left = 0

        # Caduta fuori dalla mappa: respawn
        if self.player_sprite.center_y < -100:
            if self.is_final_level:
                self.player_sprite.center_x = 100
                self.player_sprite.center_y = 400
            else:
                # Nei livelli normali la caduta resetta tutto dal livello 1
                stoppa_musica(self.window)
                arcade.Sound(SFX_LOSE).play()  # suona l'effetto di sconfitta
                self.current_level = 1
                self.score = 0
                self.spawn_destra = True
                self.carica_livello(self.current_level)
                cambia_musica(self.window, MUSIC_PLATFORMER)  # riavvia la musica del platformer

        # Uscita a destra: passa al livello successivo
        if self.player_sprite.center_x > self.level_width - 50:
            if not self.is_final_level:
                self.spawn_destra = True
                self.livello_successivo()

        # Fase finale: fa apparire la strega dopo 5 secondi
        if self.is_final_level:
            self.timer_strega += delta_time
            if self.timer_strega > 5 and not self.strega_apparsa:
                self.strega_apparsa = True
                self.strega_sprite = arcade.Sprite("./game_assets/strega.png", scale=2)
                self.strega_sprite.center_x = self.player_sprite.center_x + 1000
                self.strega_sprite.center_y = 600
                self.strega_list = arcade.SpriteList()
                self.strega_list.append(self.strega_sprite)
                stoppa_musica(self.window)  # stoppa la musica attuale
                self.sfx_magic_sound = arcade.Sound(SFX_MAGIC)
                self.sfx_magic_player = self.sfx_magic_sound.play(volume=20)  # suona il suono di comparsa strega
                self.sfx_magic_started = False

        # Collisione con la strega: avvia il dialogo
        if self.strega_apparsa and self.strega_sprite:
            if arcade.check_for_collision(self.player_sprite, self.strega_sprite):
                if self.fase_finale == 0:
                    self.fase_finale = 1
                    self.window.show_view(DialogoView(self))

        # Quando l'effetto della strega è finito, riavvia la musica della luna
        if self.sfx_magic_player and self.sfx_magic_sound:
            if self.sfx_magic_sound.is_playing(self.sfx_magic_player):
                self.sfx_magic_started = True  # confermato che sta suonando
            elif self.sfx_magic_started:       # era partito ed ora è finito
                cambia_musica(self.window, MUSIC_LUNA)
                self.sfx_magic_player = None
                self.sfx_magic_sound = None
                self.sfx_magic_started = False

        # Fase finale 2: la strega scende fino a y=200, poi mostra la vittoria
        if self.fase_finale == 2 and self.strega_sprite:
            if self.strega_sprite.center_y > 200:
                self.strega_sprite.center_y -= 2
            else:
                self.fase_finale = 3
                self.window.show_view(VittoriaView())

        self.pan_camera_to_player()