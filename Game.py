import arcade

# ────────────────────────────────────────────────
# COSTANTI (ex Costanti.py)
# ────────────────────────────────────────────────
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING     = 1
BARREL_SCALING   = 0.4
COIN_SCALING     = 0.5

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED     = 15
GRAVITY               = 0.8


# ────────────────────────────────────────────────
# CLASSE PLAYER
# ────────────────────────────────────────────────
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("./game_assets/montanaro.png")
        self.center_x = 100
        self.center_y = 150


# ────────────────────────────────────────────────
# CLASSE PRINCIPALE DEL GIOCO
# ────────────────────────────────────────────────
class GameView(arcade.Window):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_sprite = None
        self.player_list = None
        self.wall_list = None
        self.coin_list = None

        self.physics_engine = None

        self.background = None
        self.camera = None
        self.ui_camera = None

        self.score = 0

    def setup(self):

        self.score = 0

        self.player_list = arcade.SpriteList()
        self.wall_list   = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list   = arcade.SpriteList(use_spatial_hash=True)

        self.background = arcade.load_texture("./game_assets/sfondo_gioco.png")

        self.camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()

        # PLAYER
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        # TERRENO
        for x in range(-350, 10000, 64):
            wall = arcade.Sprite("./game_assets/terreno.png",
                                 scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # BARILI (muri)
        barrel_coordinate_list = [
            [512, 96],
            [256, 96],
            [768, 96],
            [64, 96],
            [1024, 96]
        ]

        for coordinate in barrel_coordinate_list:
            barrel = arcade.Sprite(
                "./game_assets/muro_barile.png",
                scale=BARREL_SCALING
            )
            barrel.position = coordinate
            self.wall_list.append(barrel)

        # MONETE
        coin_coordinate_list = [
            [128, 96],
            [384, 96],
            [640, 96],
            [896, 96],
            [1152, 96]
        ]

        for coordinate in coin_coordinate_list:
            coin = arcade.Sprite(
                "./game_assets/moneta.png",
                scale=COIN_SCALING
            )
            coin.position = coordinate
            self.coin_list.append(coin)

        # MOTORE FISICO
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.wall_list,
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()

        # Sfondo (con camera UI)
        self.ui_camera.use()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        # Mondo di gioco
        self.camera.use()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        # Testo punteggio (sopra tutto)
        self.ui_camera.use()
        arcade.draw_text(
            f"Monete: {self.score}",
            10,
            WINDOW_HEIGHT - 40,
            arcade.color.WHITE,
            24
        )

    def on_update(self, delta_time):
        self.physics_engine.update()

        # Raccolta monete
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.coin_list
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Non uscire a sinistra
        if self.player_sprite.center_x < 0:
            self.player_sprite.center_x = 0

        # Caduta → respawn
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 150

        # Camera segue il giocatore (con limiti)
        camera_x = max(self.player_sprite.center_x, WINDOW_WIDTH / 2)
        camera_x = min(camera_x, 10000 - WINDOW_WIDTH / 2)
        camera_x = max(camera_x, WINDOW_WIDTH / 2)

        self.camera.position = (camera_x, WINDOW_HEIGHT / 2)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.SPACE):
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A,
                   arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0

        # Reset partita con P
        if key == arcade.key.P:
            self.setup()


# ────────────────────────────────────────────────
# AVVIO DEL GIOCO
# ────────────────────────────────────────────────
def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()