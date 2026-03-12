import arcade

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("./game_assets/montanaro.png")

        self.center_x = 100
        self.center_y = 150