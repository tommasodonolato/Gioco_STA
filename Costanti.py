# Costanti di gioco e percorsi dei file usati in tutto il progetto. .

# Dimensioni della finestra
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Giochino"

# Scaling degli oggetti nella tilemap
TILE_SCALING = 2
BARREL_SCALING = 0.4
COIN_SCALING = 0.5

# Velocità e fisica del giocatore
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 13
GRAVITY = 1
CAMERA_SPEED = 0.1


# Percorsi dei file tmx dei livelli
LEVELS = {
    1: "./Tiled/mappa_1.tmx",
    2: "./Tiled/mappa_2.tmx",
    3: "./Tiled/mappa_3.tmx"
}

# Percorsi degli spritesheet del giocatore
PLAYER_IDLE_SOURCE = "./sprite_animato/idle.png"
PLAYER_WALK_SOURCE = "./sprite_animato/run.png"
PLAYER_JUMP_SOURCE = "./sprite_animato/jump.png"

# Dimensioni dei frame dello spritesheet del giocatore
PLAYER_FRAME_WIDTH  = 128
PLAYER_FRAME_HEIGHT = 64
PLAYER_NUM_FRAME    = 8

# Layer del parallasse per la fase finale (luna), con il rispettivo fattore di velocità
FINAL_BG_LAYERS = [
    ("./Sfondi_parallasse/moon/moon_sky.png",   0.05),
    ("./Sfondi_parallasse/moon/moon_earth.png", 0.05),
    ("./Sfondi_parallasse/moon/moon_back.png",  0.20),
    ("./Sfondi_parallasse/moon/moon_mid.png",   0.35),
    ("./Sfondi_parallasse/moon/moon_front.png", 0.55),
    ("./Sfondi_parallasse/moon/moon_floor.png", 0.80),
]

# Percorsi file audio
MUSIC_DIALOGO = "./Sounds/Dialogo_music.wav"
MUSIC_PLATFORMER = "./Sounds/Platformer_music.wav"
MUSIC_LUNA = "./Sounds/Luna_music.wav"