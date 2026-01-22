import arcade

#valori assoluti
WINDOW_WIDHT = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"
TILE_SCALING = 0,5

class GameView(arcade.Window):


    
    
    def __init__(self):
        super().__init__(WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDHT)

        self.background_color = arcade.csscolor.ANTIQUE_WHITE

        #self.player_texture = arcade.load_texture(
         #   "./game_assets./montanaro.jpg"
        #)

        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.wall_list = arcade.SpriteList(use_spatial_hash = True)

        for x in range(0, 1250, 64):
           # wall = arcade.Sprite (sprite muro, scale = TILE_SCALING) 
           #wall.center_x = x
          # wall.center_y = 32
           #self.wall_list.append(wall)
            pass
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite("sprite muro", scale = TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)



    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        self.player_list.draw()
        self.wall_list.draw()

def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()