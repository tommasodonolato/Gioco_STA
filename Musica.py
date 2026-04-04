# Musica: funzioni per gestire la musica di sottofondo e gli effetti sonori

import arcade


def stoppa_musica(window):
    # Stoppa la musica corrente senza avviarne una nuova.
    if window.music_player and window.music_sound:
        window.music_sound.stop(window.music_player)
    window.music_player = None
    window.music_sound = None


def cambia_musica(window, percorso: str, volume: float = 0.5):
    # Stoppa la musica corrente e avvia quella nuova in loop.
    if window.music_player and window.music_sound:
        window.music_sound.stop(window.music_player)
    window.music_sound = arcade.Sound(percorso)
    window.music_player = window.music_sound.play(loop=True, volume=volume)