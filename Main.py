'''
COMANDI AMMINISTRATORE: (non sono indicati nei comandi del gioco, ma possono essere usati per il testing e per passare più velocemnte alla fase finale)
- Premi "Z" per impostare il punteggio a 30 
- Premi "X" per teletrasportarti direttamente alla fine del livello 

Gioco ideato e sviluppato da Tommaso Donolato

Il gioco è un platform 2D in cui il giocatore controlla un personaggio che deve attraversare vari livelli, raccogliendo monete e evitando ostacoli. 
Il gioco include una storia narrata attraverso schermate di dialogo e una fase finale con una strega. 
Il giocatore vince se riesce a completare tutti i livelli e raccogliere tutte le monete.

Software utilizzato per lo sviluppo:
- Python 3.10 su vs code
- Arcade 2.6.17

Software - siti web utilizzati per la creazione del gioco:
- Tiled per la creazione dei livelli
- Itch.io per la ricerca di assets grafici
- AI per la creazione e l'editing di sprite personalizzati (Grok e Gemini) e per la scrittura dei dialoghi (ChatGPT e Gemini)
- Presentazioni Google per la creazione di sfondi personalizzati e per la scrittura della storia del gioco
- Paint e Remove BG per la rimozione di backgrounds e l'editing di sprite e sfondi
- W3 Schools, Claude AI e i blog su Classroom per aiuto con la programmazione in Python e l'utilizzo di Arcade

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