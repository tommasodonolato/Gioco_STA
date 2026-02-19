import arcade

class GameView(arcade.Window):
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    WINDOW_TITLE = "Platformer"
    TILE_SCALING = 1
    PLAYER_MOVEMENT_SPEED = 5
    GRAVITY = 0.8
    PLAYER_JUMP_SPEED = 15
    BARREL_SCALING = 0.4

    def __init__(self):
        super().__init__(GameView.WINDOW_WIDTH, GameView.WINDOW_HEIGHT, GameView.WINDOW_TITLE)
        
        self.player_sprite = None
        self.player_list = None
        self.wall_list = None
        self.physics_engine = None
        self.background = None
        self.camera = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.background = arcade.load_texture("./game_assets/sfondo_gioco.png")
        self.camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()

        # Giocatore
        self.player_sprite = arcade.Sprite("./game_assets/montanaro.png")
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        # Terreno
        for x in range(-350, 10000, 64):
            wall = arcade.Sprite("./game_assets/terreno.png", scale=GameView.TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Barili
        coordinate_list = [[512, 96], [256, 96], [768, 96], [64, 96], [1024, 96]]
        for coordinate in coordinate_list:
            barrel = arcade.Sprite("./game_assets/muro_barile.png", scale=GameView.BARREL_SCALING)
            barrel.position = coordinate
            self.wall_list.append(barrel)

        # Motore fisico
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.wall_list,
            gravity_constant=GameView.GRAVITY
        )

        # Camera
        self.camera = arcade.Camera2D()

    def on_draw(self):
        self.clear()

        # Sfondo fisso
        self.ui_camera.use()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, GameView.WINDOW_WIDTH, GameView.WINDOW_HEIGHT)
        )

        # Resto con camera che segue il player
        self.camera.use()
        self.wall_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()

         # Blocco bordo sinistro per il player
        if self.player_sprite.center_x < 0:
            self.player_sprite.center_x = 0

        camera_x = max(self.player_sprite.center_x, GameView.WINDOW_WIDTH / 2)
        camera_x = min(camera_x, 10000 - GameView.WINDOW_WIDTH / 2)  # blocco a destra
        camera_x = max(camera_x, GameView.WINDOW_WIDTH / 2)          # blocco a sinistra
        self.camera.position = (camera_x, GameView.WINDOW_HEIGHT / 2)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.SPACE):
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = GameView.PLAYER_JUMP_SPEED

        if key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -GameView.PLAYER_MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = GameView.PLAYER_MOVEMENT_SPEED

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