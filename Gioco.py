'''

COMANDI AMMINISTRATORE: (non sono indicati nei comandi del gioco, ma possono essere usati per il testing e per passare più velocemnte alla fase finale)
- Premi "Z" per impostare il punteggio a 30 
- Premi "X" per teletrasportarti direttamente alla fine del livello 

Gioco ideato e sviluppato da Tommaso Donolato

Il gioco è un platform 2D in cui il giocatore controlla un personaggio che deve attraversare vari livelli, raccogliendo monete e evitando ostacoli. 
Il gioco include una storia narrata attraverso schermate di dialogo e una fase finale con una strega. 
Il giocatore vince se riesce a completare tutti i livelli e raccogliere tutte le monete.

Software utilizzato per lo sviluppo:
- Python 3.10 su vs code
- Arcade 2.6.17

Software - siti web utilizzati per la creazione del gioco:
- Tiled per la creazione dei livelli
- Itch.io per la ricerca di assets grafici
- AI per la creazione e l'editing di sprite personalizzati (Grok e Gemini) e per la scrittura dei dialoghi (ChatGPT e Gemini)
- Presentazioni Google per la creazione di sfondi personalizzati e per la scrittura della storia del gioco
- Paint e Remove BG per la rimozione di backgrounds e l'editing di sprite e sfondi
- W3 Schools, Claude AI e i blog su Classroom per aiuto con la programmazione in Python e l'utilizzo di Arcade
- Free Sound per la ricerca di effetti sonori

'''

import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Giochino"

TILE_SCALING = 2
BARREL_SCALING = 0.4
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 13
GRAVITY = 1
CAMERA_SPEED = 0.1

LEVELS = {
    1: "./Tiled/mappa_1.tmx",
    2: "./Tiled/mappa_2.tmx",
    3: "./Tiled/mappa_3.tmx"
}

PLAYER_IDLE_SOURCE = "./sprite_animato/idle.png"
PLAYER_WALK_SOURCE = "./sprite_animato/run.png"
PLAYER_JUMP_SOURCE = "./sprite_animato/jump.png"

PLAYER_FRAME_WIDTH  = 128
PLAYER_FRAME_HEIGHT = 64
PLAYER_NUM_FRAME    = 8

FINAL_BG_LAYERS = [
    ("./Sfondi_parallasse/moon/moon_sky.png",   0.05),
    ("./Sfondi_parallasse/moon/moon_earth.png", 0.05),
    ("./Sfondi_parallasse/moon/moon_back.png",  0.20),
    ("./Sfondi_parallasse/moon/moon_mid.png",   0.35),
    ("./Sfondi_parallasse/moon/moon_front.png", 0.55),
    ("./Sfondi_parallasse/moon/moon_floor.png", 0.80),
]

MUSIC_DIALOGO    = "./Sounds/Dialogo_music.wav"
MUSIC_PLATFORMER = "./Sounds/Platformer_music.wav"
MUSIC_LUNA       = "./Sounds/Luna_music.wav"

SFX_COIN    = "./Sounds/Coin_collect.wav"
SFX_JUMP    = "./Sounds/Jump.wav"
SFX_LOSE    = "./Sounds/Lose.wav"
SFX_MAGIC   = "./Sounds/Magic_appear.wav"
SFX_DIALOGO = "./Sounds/Next_dialogo.wav"


def stoppa_musica(window):
    if window.music_player and window.music_sound:
        window.music_sound.stop(window.music_player)
    window.music_player = None
    window.music_sound = None


def cambia_musica(window, percorso: str, volume: float = 0.5):
    if window.music_player and window.music_sound:
        window.music_sound.stop(window.music_player)
    window.music_sound = arcade.Sound(percorso)
    window.music_player = window.music_sound.play(loop=True, volume=volume)


class SpriteAnimato(arcade.Sprite):
    def __init__(self, scala: float = 1.0):
        super().__init__(scale=scala)
        self.animazioni = {}
        self.animazione_corrente = None
        self.animazione_default = None
        self.tempo_frame = 0.0
        self.indice_frame = 0

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
        sheet = arcade.load_spritesheet(percorso)
        offset = riga * colonne
        tutti = sheet.get_texture_grid(
            size=(frame_width, frame_height),
            columns=colonne,
            count=offset + num_frame,
        )
        self._registra(nome, tutti[offset:], durata, loop, default)

    def _registra(self, nome, textures, durata, loop, default=False):
        self.animazioni[nome] = {
            "textures": textures,
            "durata_frame": durata / len(textures),
            "loop": loop,
        }
        if default or self.animazione_default is None:
            self.animazione_default = nome
        if self.animazione_corrente is None:
            self._vai(nome)

    def imposta_animazione(self, nome: str):
        if nome != self.animazione_corrente:
            self._vai(nome)

    def _vai(self, nome: str):
        self.animazione_corrente = nome
        self.indice_frame = 0
        self.tempo_frame = 0.0
        self.texture = self.animazioni[nome]["textures"][0]

    def update_animation(self, delta_time: float = 1 / 60):
        anim = self.animazioni[self.animazione_corrente]
        self.tempo_frame += delta_time
        if self.tempo_frame < anim["durata_frame"]:
            return
        self.tempo_frame -= anim["durata_frame"]
        prossimo = self.indice_frame + 1
        if prossimo < len(anim["textures"]):
            self.indice_frame = prossimo
        elif anim["loop"]:
            self.indice_frame = 0
        else:
            self.indice_frame = len(anim["textures"]) - 1
            return
        self.texture = anim["textures"][self.indice_frame]


class Player(SpriteAnimato):
    def __init__(self):
        super().__init__(scala=2.0)
        self._in_aria = False

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

        self.center_x = 100
        self.center_y = 150
        self._guarda_destra = True

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x > 0:
            self._guarda_destra = True
        elif self.change_x < 0:
            self._guarda_destra = False

        self.scale = (abs(self.scale[0]) if self._guarda_destra
                    else -abs(self.scale[0]), abs(self.scale[1]))

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


class ParallaxLayer:
    def __init__(self, texture_path: str, speed_factor: float):
        self.texture = arcade.load_texture(texture_path)
        self.speed_factor = speed_factor
        self.width = self.texture.width
        self.height = self.texture.height

    def draw(self, cam_x: float):
        scale = WINDOW_HEIGHT / self.height
        draw_width = self.width * scale
        draw_height = WINDOW_HEIGHT

        layer_offset = cam_x * self.speed_factor
        start_tile = int(layer_offset // draw_width)
        draw_x_start = start_tile * draw_width - layer_offset

        x = draw_x_start
        while x < WINDOW_WIDTH:
            arcade.draw_texture_rect(
                self.texture,
                arcade.XYWH(x + draw_width / 2, WINDOW_HEIGHT / 2,
                             draw_width, draw_height)
            )
            x += draw_width


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("./game_assets/sfondo_inizio.jpg")
        cambia_musica(self.window, MUSIC_DIALOGO)

        arcade.load_texture(PLAYER_IDLE_SOURCE)
        arcade.load_texture(PLAYER_WALK_SOURCE)
        arcade.load_texture(PLAYER_JUMP_SOURCE)
        for path, _ in FINAL_BG_LAYERS:
            arcade.load_texture(path)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if 440 < x < 840 and 100 < y < 200:
            self.window.show_view(LoreView())


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.background = arcade.load_texture("./game_assets/pausa.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            self.window.show_view(self.game_view)


class CommandsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("./game_assets/comandi.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            cambia_musica(self.window, MUSIC_PLATFORMER)
            game = GameView()
            game.setup()
            self.window.show_view(game)


class LoreView(arcade.View):
    def __init__(self):
        super().__init__()
        self.immagini = [
            arcade.load_texture("./Lore/Lore_1.png"),
            arcade.load_texture("./Lore/Lore_2.png"),
            arcade.load_texture("./Lore/Lore_3.png"),
            arcade.load_texture("./Lore/Lore_4.png"),
            arcade.load_texture("./Lore/Lore_5.png"),
        ]
        self.indice = 0

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.immagini[self.indice],
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.N:
            arcade.Sound(SFX_DIALOGO).play()
            self.indice += 1
            if self.indice >= len(self.immagini):
                self.window.show_view(CommandsView())


class DialogoView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.immagini = [
            arcade.load_texture("./game_assets/Dialogo_1.png"),
            arcade.load_texture("./game_assets/Dialogo_2.png"),
            arcade.load_texture("./game_assets/Dialogo_3.png"),
        ]
        self.indice = 0

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.immagini[self.indice],
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.N:
            arcade.Sound(SFX_DIALOGO).play()
            self.indice += 1
            if self.indice == 2:
                if self.game_view.score < 30:
                    self.window.show_view(GameOverView())
                    return
            if self.indice >= len(self.immagini):
                self.game_view.fase_finale = 2
                self.window.show_view(self.game_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("./game_assets/Game_over.png")
        stoppa_musica(self.window)
        arcade.Sound(SFX_LOSE).play()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            self.window.show_view(MenuView())


class VittoriaView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("./game_assets/Victory.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            stoppa_musica(self.window)
            self.window.show_view(MenuView())


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.player_sprite: Player | None = None
        self.player_list = None
        self.wall_list = None
        self.coin_list = None
        self.physics_engine = None
        self.camera = None
        self.ui_camera = None
        self.parallax_layers = []
        self.score = 0
        self.current_level = 1
        self.level_width = WINDOW_WIDTH
        self.spawn_destra = True
        self.is_final_level = False
        self.timer_strega = 0
        self.strega_apparsa = False
        self.strega_sprite = None
        self.fase_finale = 0
        self.strega_list = arcade.SpriteList()
        self.sfx_magic_sound = None
        self.sfx_magic_player = None

    def setup(self):
        self.score = 0
        self.current_level = 1
        self.is_final_level = False
        self.spawn_destra = True

        self.player_list = arcade.SpriteList()
        self.camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()

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
        tile_map = arcade.load_tilemap(LEVELS[numero], scaling=TILE_SCALING)
        self.wall_list = tile_map.sprite_lists["Livello tile 1"]
        self.coin_list = tile_map.sprite_lists.get("Monete", arcade.SpriteList())
        self.level_width = tile_map.width * tile_map.tile_width * TILE_SCALING

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
        if self.current_level < len(LEVELS):
            self.current_level += 1
            self.carica_livello(self.current_level)
        else:
            self.carica_livello_finale()

    def carica_livello_finale(self):
        self.is_final_level = True
        cambia_musica(self.window, MUSIC_LUNA)

        self.parallax_layers = [
            ParallaxLayer(path, speed)
            for path, speed in FINAL_BG_LAYERS
        ]

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.level_width = 99999

        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 200

        self.timer_strega = 0
        self.strega_apparsa = False
        self.strega_sprite = None
        self.fase_finale = 0

        floor = arcade.SpriteSolidColor(99999, 64, color=(0, 0, 0, 0))
        floor.center_x = self.level_width / 2
        floor.center_y = 32
        self.wall_list.append(floor)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.wall_list,
            gravity_constant=0.2
        )

    def on_draw(self):
        self.clear()

        self.ui_camera.use()
        cam_x = self.camera.position[0] - WINDOW_WIDTH / 2
        for layer in self.parallax_layers:
            layer.draw(cam_x)

        self.camera.use()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        if self.is_final_level and self.strega_apparsa and self.strega_sprite:
            self.strega_list.draw()

        self.ui_camera.use()
        arcade.draw_text(
            f"MONETE: {self.score}",
            20, WINDOW_HEIGHT - 40,
            arcade.color.GOLD, 20, font_name="Courier New", bold=True
        )

    def pan_camera_to_player(self):
        if self.is_final_level:
            self.camera.position = arcade.math.lerp_2d(
                self.camera.position,
                (self.player_sprite.center_x, WINDOW_HEIGHT / 2),
                CAMERA_SPEED
            )
        else:
            target_x = max(self.player_sprite.center_x, WINDOW_WIDTH / 2)
            target_x = min(target_x, self.level_width - WINDOW_WIDTH / 2)
            target_pos = (target_x, WINDOW_HEIGHT / 2)
            self.camera.position = arcade.math.lerp_2d(
                self.camera.position,
                target_pos,
                CAMERA_SPEED
            )

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update_animation(delta_time)

        for coin in arcade.check_for_collision_with_list(self.player_sprite, self.coin_list):
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.Sound(SFX_COIN).play()

        if self.player_sprite.left < 0:
            if self.is_final_level:
                self.player_sprite.left = 0
            elif self.current_level > 1:
                self.current_level -= 1
                self.spawn_destra = False
                self.carica_livello(self.current_level)
            else:
                self.player_sprite.left = 0

        if self.player_sprite.center_y < -100:
            if self.is_final_level:
                self.player_sprite.center_x = 100
                self.player_sprite.center_y = 400
            else:
                stoppa_musica(self.window)
                arcade.Sound(SFX_LOSE).play()
                self.current_level = 1
                self.score = 0
                self.spawn_destra = True
                self.carica_livello(self.current_level)
                cambia_musica(self.window, MUSIC_PLATFORMER)

        if self.player_sprite.center_x > self.level_width - 50:
            if not self.is_final_level:
                self.spawn_destra = True
                self.livello_successivo()

        if self.is_final_level:
            self.timer_strega += delta_time
            if self.timer_strega > 5 and not self.strega_apparsa:
                self.strega_apparsa = True
                self.strega_sprite = arcade.Sprite("./game_assets/strega.png", scale=2)
                self.strega_sprite.center_x = self.player_sprite.center_x + 1000
                self.strega_sprite.center_y = 600
                self.strega_list = arcade.SpriteList()
                self.strega_list.append(self.strega_sprite)
                stoppa_musica(self.window)
                self.sfx_magic_sound = arcade.Sound(SFX_MAGIC)
                self.sfx_magic_player = self.sfx_magic_sound.play(volume=20)

        if self.sfx_magic_player and self.sfx_magic_sound:
            if not self.sfx_magic_sound.is_playing(self.sfx_magic_player):
                cambia_musica(self.window, MUSIC_LUNA)
                self.sfx_magic_player = None
                self.sfx_magic_sound = None

        if self.strega_apparsa and self.strega_sprite:
            if arcade.check_for_collision(self.player_sprite, self.strega_sprite):
                if self.fase_finale == 0:
                    self.fase_finale = 1
                    self.window.show_view(DialogoView(self))

        if self.fase_finale == 2 and self.strega_sprite:
            if self.strega_sprite.center_y > 200:
                self.strega_sprite.center_y -= 2
            else:
                self.fase_finale = 3
                self.window.show_view(VittoriaView())

        self.pan_camera_to_player()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.SPACE, arcade.key.W):
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.Sound(SFX_JUMP).play(volume=25)

        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))

        if key == arcade.key.Z:
            self.score = 30

        if key == arcade.key.X:
            self.player_sprite.center_x = self.level_width - 60

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0

        if key == arcade.key.P:
            self.setup()


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.music_player = None
    window.music_sound = None
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()