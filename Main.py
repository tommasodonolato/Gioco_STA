# ===================== MAIN =====================

'''
COMANDI AMMINISTRATORE (non mostrati al giocatore, solo per testing):
- Z  →  imposta il punteggio a 30
- X  →  teletrasporto alla fine del livello corrente

Gioco ideato e sviluppato da Tommaso Donolato

Software utilizzato:
- Python 3.10 su VS Code
- Arcade 2.6.17
- Tiled (creazione livelli)
- Itch.io (asset grafici)
- Grok / Gemini (sprite personalizzati)
- ChatGPT / Gemini (dialoghi)
- Google Presentazioni (sfondi e storia)
- Paint / Remove BG (editing sprite)
- W3Schools, Claude AI, blog Classroom (supporto programmazione)
'''

import arcade
from Costanti import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from Views import MenuView


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()