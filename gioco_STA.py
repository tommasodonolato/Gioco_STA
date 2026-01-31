import arcade

#valori assoluti
WINDOW_WIDHT = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 10

class GameView(arcade.Window):    
    
    def __init__(self):
        super().__init__(WINDOW_WIDHT, WINDOW_HEIGHT, WINDOW_TITLE)

        self.background = None

        self.player_texture = arcade.load_texture(
            "./game_assets/montanaro.png"
        )
        self.setup()
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.wall_list = arcade.SpriteList(use_spatial_hash = True)
           
        coordinate_list = [[512, 96], [256, 96], [768, 96],[64,96],[1024, 96]]

        self.wall_list.append(arcade.Sprite("./game_assets/terreno.png",2,WINDOW_WIDHT/2,10))

        for coordinate in coordinate_list:
            wall = arcade.Sprite("./game_assets/muro_barile.png", scale = TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.wall_list
        )


    def setup(self):
        self.background = arcade.load_texture(
            "./game_assets/sfondo_gioco.png"
        )

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,arcade.XYWH(WINDOW_WIDHT/2,WINDOW_HEIGHT/2,WINDOW_WIDHT, WINDOW_HEIGHT))
        arcade.draw_sprite(self.player_sprite)
        self.player_list.draw()
        self.wall_list.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()

    def on_key_press(self, key ,modifiers):
        
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

       
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        if key == arcade.key.RIGHT or key == arcade.key.D:
           self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
   
    def on_key_release (self, key, modifiers):
        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

def main():
    giochino = GameView()
    arcade.run()


if __name__ == "__main__":
    main()