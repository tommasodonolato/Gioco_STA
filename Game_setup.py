# Game Setup: inizializzazione, caricamento livelli e fase finale.

import arcade
from Costanti import *
from Player import Player
from Parallax import ParallaxLayer
from Musica import cambia_musica


class GameSetup(arcade.View):

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
        self.sfx_magic_sound = None    # suono comparsa strega
        self.sfx_magic_player = None   # player del suono comparsa strega
        self.sfx_magic_started = False # True dopo il primo frame che lo suona


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

        # Passa alla musica della luna
        cambia_musica(self.window, MUSIC_LUNA)

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