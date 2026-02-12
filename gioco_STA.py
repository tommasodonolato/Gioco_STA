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
        self.player_texture = None
        self.player_sprite = None
        self.player_list = None
        self.wall_list = None
        self.background = None
        self.camer = None

    def setup(self):

        self.player_texture = arcade.load_texture(
            "./game_assets/montanaro.png"
        )
        
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.wall_list = arcade.SpriteList(use_spatial_hash = True)

        tile_size = 64 * GameView.TILE_SCALING

        for x in range(-350, 10000, 64):
            wall = arcade.Sprite(
                "./game_assets/terreno.png",
                scale=GameView.TILE_SCALING
            )
            wall.center_x = x
            wall.center_y = tile_size // 2
            self.wall_list.append(wall)


            

        coordinate_list = [[512, 96], [256, 96], [768, 96],[64,96],[1024, 96]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite("./game_assets/muro_barile.png", scale = GameView.BARREL_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

       

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            self.wall_list,
            gravity_constant=GameView.GRAVITY
        )

        
        self.background = arcade.load_texture(
            "./game_assets/sfondo_gioco.png"
        )

        self.camera_sprites = arcade.Camera2D()
        self.camera_background = arcade.Camera2D()

    def on_draw(self):
        self.clear()

        self.camera_background.use()
        arcade.draw_texture_rect(
                self.background,
                arcade.XYWH(
                    self.camera_background.position.x,
                    GameView.WINDOW_HEIGHT / 2,
                    GameView.WINDOW_WIDTH,
                    GameView.WINDOW_HEIGHT
                )
            )
        
 
        self.camera_sprites.use()
        self.wall_list.draw()
        self.player_list.draw()
            

    def on_update(self, delta_time):
        
        self.physics_engine.update()

        x, y = self.player_sprite.position
        
        self.camera_sprites.position = arcade.Vec2(x, y)

        self.camera_background.position = arcade.Vec2(x, y)



    def on_key_press(self, key ,modifiers):
        
        if key == arcade.key.UP or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = GameView.PLAYER_JUMP_SPEED

       
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -GameView.PLAYER_MOVEMENT_SPEED

        if key == arcade.key.RIGHT or key == arcade.key.D:
           self.player_sprite.change_x = GameView.PLAYER_MOVEMENT_SPEED

    def on_key_release (self, key, modifiers):

        if key == arcade.key.P:
            self.setup()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

def main():
    giochino = GameView()
    giochino.setup()
    arcade.run()


if __name__ == "__main__":
    main()