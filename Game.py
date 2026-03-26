import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Giochino"

TILE_SCALING = 1
BARREL_SCALING = 0.4
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 15
GRAVITY = 0.8
CAMERA_SPEED = 0.1

LEVEL_WIDTH = 10000


class ParallaxLayer:
    def __init__(self, texture_path: str, speed_factor: float):
        self.texture = arcade.load_texture(texture_path)
        self.speed_factor = speed_factor
        self.width = self.texture.width
        self.height = self.texture.height

    def draw(self, cam_x: float):

        # Scala proporzionalmente: altezza fissa = WINDOW_HEIGHT
        scale = WINDOW_HEIGHT / self.height
        draw_width = self.width * scale
        draw_height = WINDOW_HEIGHT  # altezza sempre uguale alla finestra

        # Quanti pixel si è spostato il layer rispetto all'origine
        layer_offset = cam_x * self.speed_factor

        # Calcola quale "tile" è visibile
        start_tile = int(layer_offset // draw_width)
        draw_x_start = start_tile * draw_width - layer_offset

        # Disegna abbastanza ripetizioni per coprire lo schermo
        x = draw_x_start
        while x < WINDOW_WIDTH:
            arcade.draw_texture_rect(
                self.texture,
                arcade.XYWH(x + draw_width / 2, WINDOW_HEIGHT / 2,
                             draw_width, draw_height)
            )
            x += draw_width


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("./game_assets/montanaro.png")
        self.center_x = 100
        self.center_y = 150


class GameView(arcade.Window):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_sprite = None
        self.player_list = None
        self.wall_list = None
        self.coin_list = None
        self.physics_engine = None

        self.camera = None
        self.ui_camera = None
        self.parallax_layers = []

        self.score = 0

    def setup(self):
        self.score = 0

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self.camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()


        self.parallax_layers = [
            ParallaxLayer("./forest/forest_sky.png",      speed_factor=0.10),
            ParallaxLayer("./forest/forest_mountain.png", speed_factor=0.20),
            ParallaxLayer("./forest/forest_back.png",     speed_factor=0.35),
            ParallaxLayer("./forest/forest_mid.png",      speed_factor=0.50),
            ParallaxLayer("./forest/forest_short.png",    speed_factor=0.70),
        ]

        # ─── PLAYER ───
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        # ─── TERRENO ───
        for x in range(-350, LEVEL_WIDTH, 64):
            wall = arcade.Sprite("./game_assets/terreno.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # ─── BARILI ───
        barrel_coords = [[512, 96], [256, 96], [768, 96], [1024, 96]]
        for coord in barrel_coords:
            barrel = arcade.Sprite("./game_assets/muro_barile.png", scale=BARREL_SCALING)
            barrel.position = coord
            self.wall_list.append(barrel)

        # ─── MONETE ───
        coin_coords = [[128, 96], [384, 96], [640, 96], [1152, 96]]
        for coord in coin_coords:
            coin = arcade.Sprite("./game_assets/moneta.png", scale=COIN_SCALING)
            coin.position = coord
            self.coin_list.append(coin)

        # ─── MOTORE FISICO ───
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.wall_list,
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()

        # 1) Sfondo parallax: disegnato in coordinate SCHERMO (ui_camera)
        #    così non viene spostato dalla camera del mondo.
        self.ui_camera.use()
        cam_x = self.camera.position[0] - WINDOW_WIDTH / 2  # bordo sinistro camera
        for layer in self.parallax_layers:
            layer.draw(cam_x)

        # 2) Mondo (terreno, barili, monete, player) in coordinate MONDO
        self.camera.use()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        # 3) UI
        self.ui_camera.use()
        arcade.draw_text(
            f"Monete: {self.score}",
            20, WINDOW_HEIGHT - 40,
            arcade.color.WHITE, 20, bold=True
        )

    def pan_camera_to_player(self):
        target_x = max(self.player_sprite.center_x, WINDOW_WIDTH / 2)
        target_x = min(target_x, LEVEL_WIDTH - WINDOW_WIDTH / 2)
        target_pos = (target_x, WINDOW_HEIGHT / 2)

        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            target_pos,
            CAMERA_SPEED
        )

    def on_update(self, delta_time):
        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x, self.player_sprite.center_y = 100, 150

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