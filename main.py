import pgzrun
from pgzero.actor import Actor
from pygame import mixer
import csv
import os

# ---------------- CONFIGURAÇÕES ----------------------------
WIDTH = 800
HEIGHT = 600
TITLE = "Super Vaca 🐮"

ROWS = 13
COLS = 17
TILE_SIZE_X = WIDTH // COLS
TILE_SIZE_Y = HEIGHT // ROWS

GRAVITY = 0.5
JUMP_FORCE = -12
X_SPEED = 5
ENEMY_SPEED = 2

# ---------------- ESTADO DO JOGO ----------------------------
game_state = "jogando"  # pode ser: "jogando", "vitoria", "morte"

# ---------------- CONFIGURAR SOM ----------------------------
mixer.init()

def carregar_som(caminho):
    """Tenta carregar o som de forma segura."""
    if os.path.exists(caminho):
        return caminho
    else:
        print(f"[AVISO] Som não encontrado: {caminho}")
        return None

# Agora com .wav
musica_fundo = carregar_som(os.path.join("music", "som_fundo.wav"))
som_vitoria = carregar_som(os.path.join("music", "vitoria.wav"))
som_derrota = carregar_som(os.path.join("music", "derrota.wav"))

def tocar_musica_fundo():
    if musica_fundo:
        try:
            mixer.music.load(musica_fundo)
            mixer.music.set_volume(0.5)
            mixer.music.play(-1)
        except Exception as e:
            print(f"Erro ao tocar música de fundo: {e}")

tocar_musica_fundo()

# ---------------- FUNÇÃO PARA LER CSV -------------------
def read_csv(path):
    grid = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            cleaned = []
            for val in row:
                try:
                    cleaned.append(int(val))
                except:
                    cleaned.append(-1)
            grid.append(cleaned)
    return grid

# ---------------- MAPA GERAL --------------------------
mapa = read_csv(os.path.join("mapas", "mapa_geral.csv"))

# ---------------- CRIAÇÃO DOS OBJETOS -------------------
platforms = []
lava_tiles = []
enemies_list = []
hero = None
goal = None
start_pos = (0, 0)

for row_idx, row in enumerate(mapa):
    for col_idx, val in enumerate(row):
        x = col_idx * TILE_SIZE_X
        y = row_idx * TILE_SIZE_Y
        if val == 0:
            tile = Actor("bloco0")
            tile.topleft = (x, y)
            platforms.append(tile)
        elif val == 1:
            tile = Actor("lava1")
            tile.topleft = (x, y + TILE_SIZE_Y * 0.3)
            lava_tiles.append(tile)
        elif val == 2:
            goal = Actor("mato2")
            goal.topleft = (x, y)
        elif val == 3:
            enemy = Actor("rosquinha3")
            enemy.left = x
            enemy.bottom = y + TILE_SIZE_Y
            enemy.vx = ENEMY_SPEED
            enemies_list.append(enemy)
        elif val == 4:
            hero = Actor("vaca_direta")
            hero.x = x
            hero.y = y
            hero.vx = 0
            hero.vy = 0
            start_pos = (x, y)

hero_walk_images = ["vaca_direta", "vaca_direta1"]
hero_walk_left_images = ["vaca_esquerda", "vaca_esquerda1"]
hero_frame = 0
hero_direction = "right"  # direita por padrão

# ---------------- COLISÕES -----------------------------
def check_ground_collision():
    on_ground = False
    for tile in platforms:
        if hero.vy >= 0 and hero.colliderect(tile):
            hero.bottom = tile.top + 1
            hero.vy = 0
            on_ground = True
    if hero.bottom >= HEIGHT:
        hero.bottom = HEIGHT
        hero.vy = 0
        on_ground = True
    return on_ground

def check_collisions():
    global game_state
    # Lava mata
    for lava in lava_tiles:
        if hero.colliderect(lava):
            if som_derrota: mixer.Sound(som_derrota).play()
            mixer.music.stop()
            game_state = "morte"
            return
    # Rosquinha mata
    for enemy in enemies_list:
        if hero.colliderect(enemy):
            if som_derrota: mixer.Sound(som_derrota).play()
            mixer.music.stop()
            game_state = "morte"
            return
    # Mato vence
    if goal and hero.colliderect(goal):
        if som_vitoria: mixer.Sound(som_vitoria).play()
        mixer.music.stop()
        game_state = "vitoria"

def reset_hero():
    global game_state, hero_direction
    hero.x, hero.y = start_pos
    hero.vx = 0
    hero.vy = 0
    hero_direction = "right"
    game_state = "jogando"
    tocar_musica_fundo()

# ---------------- INIMIGOS -------------------
def move_enemies():
    for enemy in enemies_list:
        enemy.x += enemy.vx
        if enemy.left < 0 or enemy.right > WIDTH:
            enemy.vx = -enemy.vx

# ---------------- UPDATE -------------------------------
def update():
    global hero_frame, game_state, hero_direction

    if game_state != "jogando":
        if keyboard.r:
            reset_hero()
        return

    hero.vy += GRAVITY
    hero.y += hero.vy

    on_ground = check_ground_collision()

    hero.vx = 0
    if keyboard.left:
        hero.vx = -X_SPEED
        hero.image = hero_walk_left_images[int(hero_frame)]
        hero_frame = (hero_frame + 0.1) % 2
        hero_direction = "left"
    elif keyboard.right:
        hero.vx = X_SPEED
        hero.image = hero_walk_images[int(hero_frame)]
        hero_frame = (hero_frame + 0.1) % 2
        hero_direction = "right"
    else:
        # Fica parado olhando na última direção
        if hero_direction == "right":
            hero.image = "vaca_direta"
        else:
            hero.image = "vaca_esquerda"

    hero.x += hero.vx

    if keyboard.space and on_ground:
        hero.vy = JUMP_FORCE

    move_enemies()
    check_collisions()

# ---------------- DRAW ------------------------------
def draw():
    screen.clear()
    screen.blit("fundo-1.png", (0, 0))
    for lava in lava_tiles:
        lava.draw()
    for tile in platforms:
        tile.draw()
    for enemy in enemies_list:
        enemy.draw()
    if goal:
        goal.draw()
    hero.draw()

    if game_state == "vitoria":
        screen.draw.text(" VOCÊ VENCEU! ", center=(WIDTH/2, HEIGHT/2 - 30),
                         fontsize=64, color="white", owidth=1, ocolor="green")
        screen.draw.text("Aperte R para reiniciar", center=(WIDTH/2, HEIGHT/2 + 40),
                         fontsize=36, color="yellow")
    elif game_state == "morte":
        screen.draw.text(" VOCÊ MORREU ", center=(WIDTH/2, HEIGHT/2 - 30),
                         fontsize=64, color="white", owidth=1, ocolor="red")
        screen.draw.text("Aperte R para reiniciar", center=(WIDTH/2, HEIGHT/2 + 40),
                         fontsize=36, color="yellow")

pgzrun.go()
