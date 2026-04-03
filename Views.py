# ===================== VIEWS (schermate) =====================

import arcade
from Costanti import *


class MenuView(arcade.View):
    """Schermata iniziale del gioco con sfondo e pulsante per iniziare."""

    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("./game_assets/sfondo_inizio.jpg")

        # Pre-carica le texture usate nel gioco per evitare lag al primo avvio
        arcade.load_texture(PLAYER_IDLE_SOURCE)
        arcade.load_texture(PLAYER_WALK_SOURCE)
        arcade.load_texture(PLAYER_JUMP_SOURCE)
        for path, _ in FINAL_BG_LAYERS:
            arcade.load_texture(path)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_mouse_press(self, x, y, button, modifiers):
        # Click sul pulsante "Inizia" porta alla schermata della lore
        if 440 < x < 840 and 100 < y < 200:
            self.window.show_view(LoreView())


# ---------------------------------------------------------------

class PauseView(arcade.View):
    """Schermata di pausa. Invio per riprendere."""

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view     # riferimento alla GameView per poterla riprendere
        self.background = arcade.load_texture("./game_assets/pausa.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            self.window.show_view(self.game_view)  # riprende il gioco


# ---------------------------------------------------------------

class CommandsView(arcade.View):
    """Schermata con i comandi del gioco. Invio per iniziare a giocare."""

    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("./game_assets/comandi.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            # Import qui per evitare import circolare con game_view.py
            from Game_view import GameView
            game = GameView()
            game.setup()
            self.window.show_view(game)


# ---------------------------------------------------------------

class LoreView(arcade.View):
    """Schermata della storia iniziale. Premi N per andare avanti."""

    def __init__(self):
        super().__init__()
        self.immagini = [
            arcade.load_texture("./Lore/Lore_1.png"),
            arcade.load_texture("./Lore/Lore_2.png"),
            arcade.load_texture("./Lore/Lore_3.png"),
            arcade.load_texture("./Lore/Lore_4.png"),
            arcade.load_texture("./Lore/Lore_5.png"),
        ]
        self.indice = 0  # indice della slide corrente

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.immagini[self.indice],
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.N:
            self.indice += 1
            if self.indice >= len(self.immagini):
                self.window.show_view(CommandsView())  # finite le slide, mostra i comandi


# ---------------------------------------------------------------

class DialogoView(arcade.View):
    """Schermata di dialogo con la strega. Premi N per avanzare."""

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view     # riferimento alla GameView per aggiornare lo stato
        self.immagini = [
            arcade.load_texture("./game_assets/Dialogo_1.png"),
            arcade.load_texture("./game_assets/Dialogo_2.png"),
            arcade.load_texture("./game_assets/Dialogo_3.png"),
        ]
        self.indice = 0

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.immagini[self.indice],
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.N:
            self.indice += 1
            # Alla seconda slide controlla se il giocatore ha abbastanza monete
            if self.indice == 2:
                if self.game_view.score < 30:
                    self.window.show_view(GameOverView())
                    return
            if self.indice >= len(self.immagini):
                self.game_view.fase_finale = 2   # sblocca la fase finale
                self.window.show_view(self.game_view)


# ---------------------------------------------------------------

class GameOverView(arcade.View):
    """Schermata di game over. Invio per tornare al menu."""

    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("./game_assets/Game_over.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            self.window.show_view(MenuView())  # torna al menu principale


# ---------------------------------------------------------------

class VittoriaView(arcade.View):
    """Schermata di vittoria. Invio per tornare al menu."""

    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("./game_assets/Victory.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            self.window.show_view(MenuView())  # torna al menu principale