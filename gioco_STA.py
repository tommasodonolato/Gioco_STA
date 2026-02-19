import arcade

class GameView(arcade.Window):
    # Costanti della finestra
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    WINDOW_TITLE = "Platformer"

    # Costanti di gioco
    TILE_SCALING = 1
    PLAYER_MOVEMENT_SPEED = 5
    GRAVITY = 0.8
    PLAYER_JUMP_SPEED = 15
    BARREL_SCALING = 0.4
    COIN_SCALING = 0.5

    def __init__(self):
        super().__init__(GameView.WINDOW_WIDTH, GameView.WINDOW_HEIGHT, GameView.WINDOW_TITLE)
        
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
        # Reset punteggio
        self.score = 0

        # Inizializzazione delle liste di sprite
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        # Caricamento dello sfondo
        self.background = arcade.load_texture("./game_assets/sfondo_gioco.png")

        # Inizializzazione delle camere
        self.camera = arcade.Camera2D()     # camera che segue il player
        self.ui_camera = arcade.Camera2D()  # camera fissa per lo sfondo e UI

        # --- GIOCATORE ---
        self.player_sprite = arcade.Sprite("./game_assets/montanaro.png")
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        # --- TERRENO ---
        for x in range(-350, 10000, 64):
            wall = arcade.Sprite("./game_assets/terreno.png", scale=GameView.TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # --- BARILI ---
        barrel_coordinate_list = [[512, 96], [256, 96], [768, 96], [64, 96], [1024, 96]]
        for coordinate in barrel_coordinate_list:
            barrel = arcade.Sprite("./game_assets/muro_barile.png", scale=GameView.BARREL_SCALING)
            barrel.position = coordinate
            self.wall_list.append(barrel)

        # --- MONETE ---
        coin_coordinate_list = [[128, 96], [384, 96], [640, 96], [896, 96], [1152, 96]]
        for coordinate in coin_coordinate_list:
            coin = arcade.Sprite("./game_assets/moneta.png", scale=GameView.COIN_SCALING)
            coin.position = coordinate
            self.coin_list.append(coin)

        # --- MOTORE FISICO ---
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.wall_list,
            gravity_constant=GameView.GRAVITY
        )

    def on_draw(self):
        self.clear()

        # Disegna lo sfondo con la camera fissa
        self.ui_camera.use()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, GameView.WINDOW_WIDTH, GameView.WINDOW_HEIGHT)
        )

        # Disegna il resto con la camera che segue il player
        self.camera.use()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        # Disegna il punteggio con la camera fissa (UI)
        self.ui_camera.use()
        arcade.draw_text(
            f"Monete: {self.score}",
            10,
            GameView.WINDOW_HEIGHT - 40,
            arcade.color.WHITE,
            24
        )

    def on_update(self, delta_time):
        # Aggiorna il motore fisico
        self.physics_engine.update()

        # Controlla collisioni con le monete e aggiorna il punteggio
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Blocca il player al bordo sinistro
        if self.player_sprite.center_x < 0:
            self.player_sprite.center_x = 0

        # Se il player cade nel vuoto, resetta la posizione
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 150

        # Aggiorna la posizione della camera
        camera_x = max(self.player_sprite.center_x, GameView.WINDOW_WIDTH / 2)
        camera_x = min(camera_x, 10000 - GameView.WINDOW_WIDTH / 2)  # blocco a destra
        camera_x = max(camera_x, GameView.WINDOW_WIDTH / 2)          # blocco a sinistra
        self.camera.position = (camera_x, GameView.WINDOW_HEIGHT / 2)

    def on_key_press(self, key, modifiers):
        # Salto
        if key in (arcade.key.UP, arcade.key.SPACE):
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = GameView.PLAYER_JUMP_SPEED

        # Movimento orizzontale
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -GameView.PLAYER_MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = GameView.PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        # Ferma il player quando si lascia il tasto
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0

        # Tasto P per resettare il gioco
        if key == arcade.key.P:
            self.setup()


def main():
    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()