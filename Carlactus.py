import pygame, random
##Declaro las respectivas variables necesarias para el funcionamiento del juego. 
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
BLUE = (0, 0, 254)
TURQUOISE =(64,224,208)
RED=(255,0,0)

##Datos de pygame para en el codigo.
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carlacticos")
clock = pygame.time.Clock()
    

##Funcion principal para mostrar por patalla los textos.
def mostrar_text(surface, text, size, x, y):
    font = pygame.font.SysFont("Impact", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def mostrar_text1(surface, text, size, x, y):
    font = pygame.font.SysFont("Chiller", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
    
def mostrar_text2(surface, text, size, x, y):
    font = pygame.font.SysFont("Playbill", size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
    
##La barra de vida la cual dependiendo el daño que reciba baja la cantidad de la linea verde. 
def barra_vida(surface, x, y, percentage):
    BAR_LENGHT = 150
    BAR_HEIGHT = 20
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, TURQUOISE, fill)
    pygame.draw.rect(surface, BLUE, border, 2)
    
def intro_juego():
    intro=True
    while intro:
        screen.blit(background, [0,0])
        mostrar_text1(screen, "Game Over", 85, WIDTH // 2, HEIGHT // 4)
        mostrar_text1(screen, "Precione Enter Para Jugar", 50, WIDTH // 2, HEIGHT // 1.7)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
    
        
    
##Creo una clase Jugador para llamarla mas adelante.
##Tambien llamo una funcion para acortar el codigo y sea mas facil de que visualizar.
##Escribo la relacion correspondiente para la creacion de una imagen y se pueda ver en el juego.
##Dentro de la funcion __init__ hago todo para el jugador se pueda mover y estar dentro del resolucion propuesta en el un principio.
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("archivos/naveplayer.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

##Esta parte conforma las teclas,las cuales al declararlas antes el juego puede saber que hacer o iniciar. 
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
##LLamo la funcion disparo.
##Tambien para hacer mas ilustrativo el juego, puese sonido de derrivo. La cual se crea con el nombre del objeto llamado que
##desee .play()
    def disparo(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()
        
        
##Creo una clase Arcade. Y una funcion. Todo esto para el funcionamiento del los "meteoritos" que caen. 
class Arcade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(arcade_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
        

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, - 100)
            self.speedy = random.randrange(1, 10)
##Creo una clase Bullet la cual hace referencia a las balas de ña funcion de arriba. 
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("archivos/balin.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
##Esta parte corresponde a las Esplosiones con su respectiva animacion.
##Tambien dentro de la funcion __inti__ creo la animacion y la velocidad de la misma
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

##Esta parte es la mas importate ya que de aqui depende el inicio y el final, del juego al reiniciar o perder toda la vida.
##Tambien creo los diferentes datos para que el usuario pueda visualizar dicha informaicion. 
def pantalla_inicial():
    screen.blit(background, [0,0])
    mostrar_text1(screen, "CARLACTICOS", 85, WIDTH // 2, HEIGHT // 4)
    mostrar_text1(screen, "Precione Enter Para Jugar", 50, WIDTH // 2, HEIGHT // 1.7)
    mostrar_text1(screen,"Proyecto BYCarlosV",30, 100, 580-25)


    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
##La parte mas atractiva de todo el juego ya que todos los arcade caen con diferentes colores, y conforman a los enemigos que tiene luchar el jugador.
##La cual agrupe en una lista para llamar cada imagen y luego dependiendo de cada imagen hacer tal cosa: "Aunque podria hacerlo", pero me parecio mas facil de esta manera
arcade_images = []
arcade_list = ["archivos/emo0.png","archivos/emo1.png","archivos/emo2.png","archivos/emo3.png","archivos/emo4.png","archivos/emo5.png","archivos/emo6.png","archivos/emo7.png", "archivos/emo8.png"]
for img in arcade_list:
    arcade_images.append(pygame.image.load(img).convert())


##  EXPOLOSION DE LAS IMAGENES.
explosion_anim = []
for i in range(9):
    file = "archivos/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)

##Esta parte corresponde a la carga de la imagen que va a tener el juego de fondo. 
background = pygame.image.load("archivos/background.png").convert()

##La aparte creativa del juego. Cargo los sonidos de cada objeto tanto las balas como las explosiones, como tambien el sonido de fondo. 
laser_sound = pygame.mixer.Sound("archivos/sound_bala.wav")
explosion_sound = pygame.mixer.Sound("archivos/explosion.wav")
pygame.mixer.music.load("archivos/soundintro.mp3")
pygame.mixer.music.set_volume(0.1)




##...........GAME OVER.........
def pantalla_game_over(score):
    screen.blit(background, [0,0])
    mostrar_text1(screen, "Game Over", 90, WIDTH // 2, HEIGHT // 4)
    mostrar_text1(screen,f"Puntuacion Total {score}", 50, WIDTH // 2,HEIGHT // 1.7)
    mostrar_text1(screen, "Precione Escape Para Salir", 50, WIDTH // 2, HEIGHT * 3/4)
    
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

                
game_over = False
running = True
pantalla_inicial()
all_sprites = pygame.sprite.Group()
arcade_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()

jugador = Jugador()
all_sprites.add(jugador)
for i in range(8):
    arcade = Arcade()
    all_sprites.add(arcade)
    arcade_list.add(arcade)
            
score=0
pygame.mixer.music.play(loops=-1)

while running:
    if game_over:
        pantalla_game_over(score)
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.K_ESCAPE:
            print("Prueba")
            running=False
            break
                          
   
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.disparo()

    all_sprites.update()
    

    ##colisiones - arcade - disparo
    hits = pygame.sprite.groupcollide(arcade_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion_sound.play()
        pygame.mixer.music.set_volume(0.1)
        #explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        arcade = Arcade()
        all_sprites.add(arcade)
        arcade_list.add(arcade)

    ##colisiones - jugador - arcade
    hits = pygame.sprite.spritecollide(jugador, arcade_list, True)
    for hit in hits:
        jugador.shield -= 10
        arcade = Arcade()
        all_sprites.add(arcade)
        arcade_list.add(arcade)
        if jugador.shield <= 0:
            pygame.mixer.music.stop()
            game_over = True
            pantalla_game_over(score)
            running=False
        

    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    ##Marcador
    mostrar_text2(screen, str(score).zfill(5),40, WIDTH // 10,25)

    ##Unico NIVEL
    level="NIVEL 1"
    

    mostrar_text2(screen, str(level), 30, WIDTH // 2,10,)


    ##Escudo.
    barra_vida(screen, 5, 5, jugador.shield)

    pygame.display.flip()
pygame.quit()

