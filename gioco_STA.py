import arcade

#valori assoluti
LARGHEZZA_FINESTRA = 1280
ALTEZZA_FINESTRA = 720
TITOLO_FINESTRA = "Platformer"

class GameView(arcade.Window):


    
    
    def __init__(self):
        super().__init__(LARGHEZZA_FINESTRA, ALTEZZA_FINESTRA, TITOLO_FINESTRA)

        self.background_color = arcade.csscolor.ANTIQUE_WHITE

        #self.player_texture = arcade.load_texture(
         #   "./game_assets./montanaro.jpg"
        #)

        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        arcade.draw_sprite(self.player_sprite)

def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()