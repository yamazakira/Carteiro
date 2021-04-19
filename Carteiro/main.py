import pygame
import pygame.locals
import random


TELA_LADOS = 500
pygame.init()
pygame.mixer.init()
pygame.font.init()
tela = pygame.display.set_mode((TELA_LADOS, TELA_LADOS))
pygame.display.set_caption('Carteiro')
icon = pygame.image.load('data/enemies/slime.png')
pygame.display.set_icon(icon)

relogio = pygame.time.Clock()

# VARIÁVEIS IMUTÁVEIS 
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

SPEED = 13
GRAVIDADE = 1
GAME_SPEED = 10

ENEMY_LADOS = 64
FLENEMY_HEIGHT = 64
FLENEMY_WIDHT = 100

DODGEMODE = False
dodgemodeoff = 0
dodgemodecooldown = 0

flenemygen = 0
flenemygentime = random.randint(30, 70)

chao = pygame.Rect(0, 410, TELA_LADOS, 90)
vivo = True
# Pontuação
score = 0
pontos = pygame.font.SysFont('Comic Sans MS', 30)
titulo = pygame.font.SysFont(None, 60)
subtitulo = pygame.font.SysFont(None, 45)
comandos = pygame.font.SysFont(None, 32)
aumentoscore = 0
aumentospeed = 10

finalscore = 0
bestscore = 0
# PLAYER
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('data/player/sprite_0.png').convert_alpha(),
                       pygame.image.load('data/player/sprite_1.png').convert_alpha(),
                       pygame.image.load('data/player/sprite_2.png').convert_alpha(),
                       pygame.image.load('data/player/sprite_3.png').convert_alpha(),
                       pygame.image.load('data/player/sprite_4.png').convert_alpha(),
                       pygame.image.load('data/player/sprite_5.png').convert_alpha(),
                       pygame.image.load('data/player/sprite_6.png').convert_alpha(),
                       pygame.image.load('data/player/sprite_7.png').convert_alpha(),
                       pygame.image.load('data/player/dodge.png').convert_alpha()]

        self.imagem_agora = 0

        self.speed = SPEED

        self.count = 0

        self.image = pygame.image.load('data/player/sprite_0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect[0] = TELA_LADOS / 10
        self.rect[1] = 311

    def PULO(self):
        self.speed = -SPEED    
        self.rect[1] += self.speed
    def update(self):
        self.count+=1
        if DODGEMODE == True:
            self.image = pygame.image.load('data/player/dodge.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 100))
  
        if DODGEMODE == False:
            if self.count > 2:
                self.imagem_agora = (self.imagem_agora + 1) %8
                self.image = self.images[self.imagem_agora]
                self.image = pygame.transform.scale(self.image, (100, 100))
                self.count=0
        yant = self.rect[1]
        if pygame.Rect.colliderect(self.rect, chao) == True:
            self.rect[1] = yant
            if self.rect[1] > 311:
                self.rect[1] = 311
        else:
            self.rect[1] += self.speed
            self.speed+= GRAVIDADE

# INIMIGOS
class Enemy(pygame.sprite.Sprite):

    def __init__(self, posx):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('data/enemies/slime.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ENEMY_LADOS, ENEMY_LADOS))

        self.rect = self.image.get_rect()

        self.rect[0] = posx
        self.rect[1] = 346

    def update(self):
        self.rect[0] -= GAME_SPEED

# INIMIGO VOADOR
class FLenemy(pygame.sprite.Sprite):

    def __init__(self, posx):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('data/enemies/whale.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (FLENEMY_WIDHT, FLENEMY_HEIGHT))

        self.rect = self.image.get_rect()

        self.rect[0] = posx
        self.rect[1] = 240

    def update(self):
        self.rect[0] -= GAME_SPEED + 20
      
# Testar se algo está fora da tela
def off_screen(sprite):
    return sprite.rect[2] < -(sprite.rect[0]+10)

# Jogador
player_grupo = pygame.sprite.Group()
player = Player()
player_grupo.add(player)

# Inimigos
enemy_grupo = pygame.sprite.Group()
for i in range(1):
    enemy = Enemy(TELA_LADOS)
    enemy_grupo.add(enemy)

# Inimigo voador
flenemy_grupo = pygame.sprite.Group()
for i in range(1):
    flenemy = FLenemy(TELA_LADOS)
    flenemy_grupo.add(flenemy)

# Atribui uma imagem ao fundo; Reescala a imagem
FUNDO = pygame.image.load('fundo.png')
FUNDO = pygame.transform.scale(FUNDO, (TELA_LADOS, TELA_LADOS))

menuplayer = pygame.image.load('data/player/sprite_0.png')
pygame.Surface.convert_alpha(menuplayer)
pygame.transform.scale(menuplayer, (100, 100))

chao12 = pygame.image.load('chao.png')
chao12 = pygame.transform.scale(chao12, (TELA_LADOS, 90))

saida = False

menu = True
derrota = False
while saida == False:

    while menu:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                saida = True
            if event.type == pygame.KEYDOWN:            
                if event.key == pygame.K_SPACE:
                    menu = False
        
        relogio.tick(30)
        tela.blit(FUNDO, (0, 0))

        if derrota == False:
            titulo2 = titulo.render('Carteiro', True, VERMELHO)
            subtitulo2 = subtitulo.render('Aperte espaço para começar', True, VERMELHO)
            comandos1 = comandos.render('CIMA para pular', True, VERMELHO)
            comandos3 = comandos.render('DIREITA para desvir no ar', True, VERMELHO)
        if derrota == True:
            titulo2 = titulo.render('Perdeste!', True, VERMELHO)
            subtitulo2 = subtitulo.render('Aperte espaço para recomeçar', True, VERMELHO)
            comandos1 = comandos.render('Seus pontos: {}'.format(finalscore), True, VERMELHO)
            comandos3 = comandos.render('Melhor pontuação: {}'.format(bestscore), True, VERMELHO)

        comandos2 = comandos.render('BAIXO para cair rápido', True, VERMELHO)

        player_grupo.update()
        if vivo == True and derrota == False:
            player_grupo.draw(tela)
        tela.blit(chao12, (0, 410))

        tela.blit(titulo2, (175, 50))
        tela.blit(subtitulo2, (45, 420))
        tela.blit(comandos1, (215, 200))
        tela.blit(comandos3, (215, 260))
        if derrota == False:
            tela.blit(comandos2, (215, 230))
        score = 0
        pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            saida = True
        if event.type == pygame.KEYDOWN:            
            if event.key == pygame.K_UP and pygame.Rect.colliderect(player.rect, chao) == True:
                player.PULO()
            if event.key == pygame.K_RIGHT and dodgemodecooldown == 0:
                DODGEMODE = True
                dodgemodecooldown = 30
                dodgemodeoff = 17
            if event.key == pygame.K_DOWN:
                player.rect[1] = 311
            
    tela.fill(BRANCO)
    relogio.tick(30)

    tela.blit(FUNDO, (0, 0))

    if DODGEMODE == True:
        if dodgemodeoff > 0:
            dodgemodeoff -=1
        elif dodgemodeoff == 0:
            DODGEMODE = False

    if DODGEMODE == False:
        if (dodgemodecooldown == 0) == False:
            dodgemodecooldown -= 1
    
    # Trazer o inimigo para o outro lado da tela quando ele estiver fora da tela
    if off_screen(enemy_grupo.sprites()[0]):
        enemy_grupo.remove(enemy_grupo.sprites()[0])

        new_enemy = Enemy(TELA_LADOS)
        enemy_grupo.add(new_enemy)
    
    # Aumentar Pontuação
    aumentoscore+=1
    if aumentoscore > 15:
        score+=1
        aumentoscore = 0
    textopontos = pontos.render('Pontos: {}'.format(score), False,BRANCO)
    tela.blit(textopontos, (0, 0))

    if score == aumentospeed:
        GAME_SPEED = GAME_SPEED + 1
        aumentospeed = aumentospeed+10
    
    if off_screen(flenemy_grupo.sprites()[0]):
        if len(flenemy_grupo.sprites()) >= 2:
            flenemy_grupo.remove(flenemy_grupo.sprites()[0])
    flenemygen +=1
    if flenemygen == flenemygentime:
        new_flenemy = FLenemy(TELA_LADOS)
        flenemy_grupo.add(new_flenemy)
        flenemygen = 0
        flenemygentime = random.randint(30, 60)

    finalscore = score
    if finalscore > bestscore:
        bestscore = finalscore

    enemy_grupo.update()
    player_grupo.update()
    flenemy_grupo.update()

    player_grupo.draw(tela)
    enemy_grupo.draw(tela)
    flenemy_grupo.draw(tela)

    pygame.draw.rect(tela, VERMELHO, chao)
    tela.blit(chao12, (0, 410))
    pygame.display.flip()
    
    # Testa se há colisão entre os píxeis do player e inimigos.
    if (pygame.sprite.groupcollide(player_grupo, enemy_grupo, False, False, pygame.sprite.collide_mask)) or ((pygame.sprite.groupcollide(player_grupo, flenemy_grupo, False, False, pygame.sprite.collide_mask)) and DODGEMODE == False):
        #Game Over
        flenemy_grupo.remove(flenemy_grupo.sprites()[0])
        enemy_grupo.remove(enemy_grupo.sprites()[0])
        new_enemy = Enemy(TELA_LADOS)
        enemy_grupo.add(new_enemy)
        new_flenemy = FLenemy(TELA_LADOS)
        flenemy_grupo.add(new_flenemy)
        flenemygen = 0
        flenemygentime = random.randint(30, 60)
        derrota = True
        menu = True
        vivo = False

pygame.quit()