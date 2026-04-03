# Parallasse 

import arcade
from Costanti import *


class ParallaxLayer:
# Singolo layer dello sfondo con effetto parallasse

    def __init__(self, texture_path: str, speed_factor: float):
        self.texture = arcade.load_texture(texture_path)
        self.speed_factor = speed_factor   # più è basso, più il layer sembra lontano
        self.width = self.texture.width
        self.height = self.texture.height

    def draw(self, cam_x: float):
        # Scala il layer per coprire tutta l'altezza della finestra
        scale = WINDOW_HEIGHT / self.height
        draw_width = self.width * scale
        draw_height = WINDOW_HEIGHT

        # Calcola l'offset in base alla posizione della camera e al fattore di velocità
        layer_offset = cam_x * self.speed_factor
        start_tile = int(layer_offset // draw_width)
        draw_x_start = start_tile * draw_width - layer_offset

        # Disegna il layer finché riempie tutta la finestra
        x = draw_x_start
        while x < WINDOW_WIDTH:
            arcade.draw_texture_rect(
                self.texture,
                arcade.XYWH(x + draw_width / 2, WINDOW_HEIGHT / 2,
                             draw_width, draw_height)
            )
            x += draw_width