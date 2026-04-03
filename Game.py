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
            self._vai(self.animazione_default)
            return
        self.texture = anim["textures"][self.indice_frame]



class Player(SpriteAnimato):
    def __init__(self):
        super().__init__(scala=2.0)

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
        # Flip sinistra/destra
        if self.change_x > 0:
            self._guarda_destra = True
        elif self.change_x < 0:
            self._guarda_destra = False

        self.scale = (abs(self.scale[0]) if self._guarda_destra
                      else -abs(self.scale[0]), abs(self.scale[1]))

        # Priorità: salto > corsa > idle
        if self.change_y != 0:
            self.imposta_animazione("jump")
        elif self.change_x != 0:
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



class GameView(arcade.Window):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

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

    def setup(self):
        self.score = 0
        
        self.current_level = 1

        self.player_list = arcade.SpriteList()
     

        self.camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()

        self.parallax_layers = [
            ParallaxLayer("./forest/forest_sky.png",      speed_factor=0.10),
            ParallaxLayer("./forest/forest_mountain.png", speed_factor=0.20),
            ParallaxLayer("./forest/forest_back.png",     speed_factor=0.35),
            ParallaxLayer("./forest/forest_mid.png",      speed_factor=0.50),
            ParallaxLayer("./forest/forest_short.png",    speed_factor=0.70),
        ]

        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

       
        self.carica_livello(self.current_level)

    
    def carica_livello(self, numero: int):

        tile_map = arcade.load_tilemap(LEVELS[numero], scaling=TILE_SCALING)

        self.wall_list = tile_map.sprite_lists["Livello tile 1"]

        self.coin_list = tile_map.sprite_lists.get("monete", arcade.SpriteList())

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
        target_x = max(self.player_sprite.center_x, 0)
        target_x = min(target_x, self.level_width - WINDOW_WIDTH / 2)
        self.camera.position = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    def livello_successivo(self):
        if self.current_level < len(LEVELS):
            self.current_level += 1
            self.carica_livello(self.current_level)
        else:
            print("Hai completato tutti i livelli!")

        

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

        self.ui_camera.use()
        arcade.draw_text(
            f"Monete: {self.score}",
            20, WINDOW_HEIGHT - 40,
            arcade.color.WHITE, 20, bold=True
        )

    def pan_camera_to_player(self):
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

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        if self.player_sprite.left < 0:
            if self.current_level > 1:
                self.current_level -= 1
                self.spawn_destra = False
                self.carica_livello(self.current_level)
            else:
                self.player_sprite.left = 0

        if self.player_sprite.center_y < -100:
            self.current_level = 1
            self.spawn_destra = True
            self.carica_livello(self.current_level)

        if self.player_sprite.center_x > self.level_width - 50:
            self.spawn_destra = True
            self.livello_successivo()

        self.pan_camera_to_player()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.SPACE, arcade.key.W):
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0
        if key == arcade.key.P:
            self.setup()



def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
