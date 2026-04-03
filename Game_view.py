# Game View: gestisce il gioco vero e proprio, livelli, fisica, collisioni e fase finale.

import arcade
from Costanti import *
from Player import Player
from Parallax import ParallaxLayer
from Views import MenuView, PauseView, DialogoView, VittoriaView, GameOverView


class GameView(arcade.View):
    #View principale: gestisce livelli, fisica, collisioni e fase finale.

    def __init__(self):
        super().__init__()

        # Sprite e liste
        self.player_sprite: Player | None = None
        self.player_list = None
        self.wall_list = None
        self.coin_list = None
        self.strega_list = arcade.SpriteList()
        self.strega_sprite = None

        # Fisica e camera
        self.physics_engine = None
        self.camera = None
        self.ui_camera = None

        # Sfondo parallasse
        self.parallax_layers = []

        # Stato di gioco
        self.score = 0
        self.current_level = 1
        self.level_width = WINDOW_WIDTH
        self.spawn_destra = True       # da dove spawna il giocatore nel livello

        # Stato fase finale
        self.is_final_level = False
        self.timer_strega = 0          # secondi trascorsi dall'inizio della fase finale
        self.strega_apparsa = False
        self.fase_finale = 0           # 0=inizio, 1=dialogo, 2=strega scende, 3=vittoria


    def setup(self):

        self.score = 0
        self.current_level = 1
        self.is_final_level = False
        self.spawn_destra = True

        self.player_list = arcade.SpriteList()
        self.camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()

        # Sfondo parallasse della foresta per i livelli normali
        self.parallax_layers = [
            ParallaxLayer("./Sfondi_parallasse/forest/forest_sky.png",      speed_factor=0.10),
            ParallaxLayer("./Sfondi_parallasse/forest/forest_mountain.png", speed_factor=0.20),
            ParallaxLayer("./Sfondi_parallasse/forest/forest_back.png",     speed_factor=0.35),
            ParallaxLayer("./Sfondi_parallasse/forest/forest_mid.png",      speed_factor=0.50),
            ParallaxLayer("./Sfondi_parallasse/forest/forest_short.png",    speed_factor=0.70),
        ]

        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        self.carica_livello(self.current_level)


    def carica_livello(self, numero: int):
        # Carica la tilemap del livello indicato e posiziona il giocatore.
        tile_map = arcade.load_tilemap(LEVELS[numero], scaling=TILE_SCALING)
        self.wall_list = tile_map.sprite_lists["Livello tile 1"]
        self.coin_list = tile_map.sprite_lists.get("Monete", arcade.SpriteList())
        self.level_width = tile_map.width * tile_map.tile_width * TILE_SCALING

        # Spawn da sinistra o da destra in base alla direzione di provenienza
        if self.spawn_destra:
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 400
        else:
            self.player_sprite.center_x = self.level_width - 100
            self.player_sprite.center_y = 400

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.wall_list,
            gravity_constant=GRAVITY
        )
        self.camera.position = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)


    def livello_successivo(self):
        # Passa al livello successivo o avvia la fase finale.
        if self.current_level < len(LEVELS):
            self.current_level += 1
            self.carica_livello(self.current_level)
        else:
            self.carica_livello_finale()


    def carica_livello_finale(self):
        # Configura la fase finale sulla luna con gravità ridotta.
        self.is_final_level = True

        # Sostituisce lo sfondo foresta con quello della luna
        self.parallax_layers = [
            ParallaxLayer(path, speed)
            for path, speed in FINAL_BG_LAYERS
        ]

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.level_width = 99999       # livello infinito verso destra

        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 200

        # Reset stato strega
        self.timer_strega = 0
        self.strega_apparsa = False
        self.strega_sprite = None
        self.fase_finale = 0

        # Pavimento invisibile 
        floor = arcade.SpriteSolidColor(99999, 64, color=(0, 0, 0, 0))
        floor.center_x = self.level_width / 2
        floor.center_y = 32
        self.wall_list.append(floor)

        # Gravità ridotta per simulare la luna
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.wall_list,
            gravity_constant=0.2
        )



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
                self.current_level = 1
                self.score = 0
                self.spawn_destra = True
                self.carica_livello(self.current_level)

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
                self.strega_sprite.center_x = 1100
                self.strega_sprite.center_y = 600
                self.strega_list = arcade.SpriteList()
                self.strega_list.append(self.strega_sprite)

        # Collisione con la strega: avvia il dialogo
        if self.strega_apparsa and self.strega_sprite:
            if arcade.check_for_collision(self.player_sprite, self.strega_sprite):
                if self.fase_finale == 0:
                    self.fase_finale = 1
                    self.window.show_view(DialogoView(self))

        # Fase finale 2: la strega scende fino a y=200, poi mostra la vittoria
        if self.fase_finale == 2 and self.strega_sprite:
            if self.strega_sprite.center_y > 200:
                self.strega_sprite.center_y -= 2
            else:
                self.fase_finale = 3
                self.window.show_view(VittoriaView())

        self.pan_camera_to_player()




    def on_key_press(self, key, modifiers):
        # Salto (supporta freccia su, spazio e W)
        if key in (arcade.key.UP, arcade.key.SPACE, arcade.key.W):
            if self.physics_engine.can_jump():
                jump_speed = PLAYER_JUMP_SPEED_LUNA if self.is_final_level else PLAYER_JUMP_SPEED
                self.player_sprite.change_y = jump_speed

        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Pausa
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))

        # COMANDI AMMINISTRATORE 
        if key == arcade.key.Z:
            self.score = 30                                    # imposta monete a 30
        if key == arcade.key.X:
            self.player_sprite.center_x = self.level_width - 60  # teletrasporto alla fine


    def on_key_release(self, key, modifiers):
        # Ferma il movimento orizzontale al rilascio del tasto
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0

        if key == arcade.key.P:
            self.setup()  # reset rapido del gioco (tasto nascosto)