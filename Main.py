import arcade
from Game_view import GameView


def main():

    window = GameView()
    window.setup()

    arcade.run()


if __name__ == "__main__":
    main()