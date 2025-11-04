import pgzrun
from pgzero.actor import Actor
from pygame import mixer
import csv
import os

# --- CONFIGURAÇÕES GERAIS ---
# aqui eu deixei o tamanho da tela e algumas infos do jogo
WIDTH = 800
HEIGHT = 600
TITLE = "Super Vaca 🐮"

# aqui é tipo o tamanho do mapa e das “casinhas” (tiles)
ROWS = 13
COLS = 17
TILE_SIZE_X = WIDTH // COLS
TILE_SIZE_Y = HEIGHT // ROWS

# testei esses valores até achar um pulo legal
GRAVITY = 0.5
JUMP_FORCE = -12
X_SPEED = 5
ENEMY_SPEED = 2

# pra saber em que parte o jogo tá (jogando, morreu ou venceu)
game_state = "jogando"

# --- CONFIGURAÇÃO DO SOM ---
mixer.init()

def carregar_som(caminho):
    # só pra não dar erro se faltar o som
    if os.path.exists(caminho):
        return caminho
    else:
        print(f"[aviso] som não encontrado: {caminho}")
        return None

# aqui eu carreguei os sons (usei .wav porque deu menos bug)
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
            print("deu erro pra tocar o som de fundo:", e)

tocar_musica_fundo()

# --- FUNÇÃO PRA LER O MAPA (CSV) ---
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

# aqui eu leio o arquivo do mapa (ficou em mapas/mapa_geral.csv)
mapa = read_csv(os.path.join("mapas", "mapa_geral.csv"))

# --- CRIAÇÃO DOS OBJETOS ---
platforms = []
lava_tiles = []
enemies_list = []
hero = None
goal = None
start_pos = (0, 0)

# aqui é tipo o que o número do mapa significa
# 0 = chão, 1 = lava, 2 = mato (meta), 3 = rosquinha, 4 = vaca
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

# imagens da vaquinha andando (pra direita e pra esquerda)
hero_walk_images = ["vaca_direta", "vaca_direta1"]
hero_walk_left_images = ["vaca_esquerda", "vaca_esquerda1"]
hero_frame = 0
hero_direction = "right"

# --- COLISÕES ---
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
    # se encostar na lava ou rosquinha, morre
    for lava in lava_tiles:
        if hero.colliderect(lava):
            if som_derrota: mixer.Sound(som_derrota).play()
            mixer.music.stop()
            game_state = "morte"
            return
    for enemy in enemies_list:
        if hero.colliderect(enemy):
            if som_derrota: mixer.Sound(som_derrota).play()
            mixer.music.stop()
            game_state = "morte"
            return
    # se encostar no mato, ganha :)
    if goal and hero.colliderect(goal):
        if som_vitoria: mixer.Sound(som_vitoria).play()
        mixer.music.stop()
        game_state = "vitoria"

def reset_hero():
    # aqui é só pra reiniciar o jogo
    global game_state, hero_direction
    hero.x, hero.y = start_pos
    hero.vx = 0
    hero.vy = 0
    hero_direction = "right"
    game_state = "jogando"
    tocar_musica_fundo()

# --- INIMIGOS (ROSQUINHAS) ---
def move_enemies():
    for enemy in enemies_list:
        enemy.x += enemy.vx
        # eles viram quando batem na parede
        if enemy.left < 0 or enemy.right > WIDTH:
            enemy.vx = -enemy.vx

# --- UPDATE (RODA O TEMPO TODO) ---
def update():
    global hero_frame, game_state, hero_direction

    if game_state != "jogando":
        if keyboard.r:
            reset_hero()
        return

    # gravidade e movimento
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
        # se não tiver andando, fica parada olhando pra última direção
        if hero_direction == "right":
            hero.image = "vaca_direta"
        else:
            hero.image = "vaca_esquerda"

    hero.x += hero.vx

    # pulo
    if keyboard.space and on_ground:
        hero.vy = JUMP_FORCE

    move_enemies()
    check_collisions()

# --- DESENHAR NA TELA ---
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

    # telas de vitória e derrota
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
