import arcade

#valori assoluti
LARGHEZZA_FINESTRA = 1280
ALTEZZA_FINESTRA = 720
TITOLO_FINESTRA = "Platformer"

class GameView(arcade.Window):
    
    def __init__(self):
        super().__init__(LARGHEZZA_FINESTRA, ALTEZZA_FINESTRA, TITOLO_FINESTRA)

        self.background_color = arcade.csscolor.ANTIQUE_WHITE

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()