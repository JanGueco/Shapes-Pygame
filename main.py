import pygame, time, sys, random
from pygame.locals import *


# initialize it
pygame.init()

vec = pygame.math.Vector2

# configurations
frames_per_second = 60
window_height = 600
window_width = 800
game_speed = 3

#Physics
ACC = 0.7
FRIC = -0.12

#Clock
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

#Assets
pygame.mixer.init()
score_sound = pygame.mixer.Sound("Assets/coin.wav")



# creating window
display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Shapes')

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Shape game batak', True, GREEN, BLUE)
textRect = text.get_rect()
textRect.center = (window_width * .95 , window_height * .10)

#Global Vars


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 50))
        self.surf.fill(BLUE)
        self.rect = self.surf.get_rect()
   
        self.pos = vec((window_width*0.10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.IsJump = False
        self.IsDuck = False
        self.score = 0
 
    def move(self):


        self.acc = vec(0,1)
    
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.jump()
        # if pressed_keys[K_LEFT]:
        #     self.acc.x = -ACC
        # if pressed_keys[K_RIGHT]:
        #     self.acc.x = ACC
        if pressed_keys[K_DOWN]:
            self.duck()
        if self.IsDuck and not pressed_keys[K_DOWN]:
            self.IsDuck = False
            self.surf = pygame.transform.smoothscale(self.surf,(30,60))
            self.rect = self.surf.get_rect()
             
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > window_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = window_width
            
        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.IsJump = False

        hits2 = pygame.sprite.spritecollide(P1, enemies, False)
        if hits2:
            self.score -= 1
            game_over()
            
    def jump(self):
        if not self.IsJump:
            self.vel.y = -15
            self.IsJump=True

    def duck(self):
        if not self.IsDuck:
            self.surf = pygame.transform.smoothscale(self.surf,(30,30))
            self.rect = self.surf.get_rect()
            if self.IsJump:
                self.vel.y = 20
            self.IsDuck = True

    def reset(self):
        self.pos = vec((window_width*0.10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.IsJump = False
        if self.IsDuck:
            self.surf = pygame.transform.smoothscale(self.surf,(30,60))
            self.rect = self.surf.get_rect()
            self.IsDuck = False
        self.score = 0


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x = window_width-35, y = window_height-49):
        super().__init__()
        self.surf = pygame.Surface((25,60))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center = (x, y))
        self.pos = vec((x, y+30))
        self.vel = vec(0,0)
        self.is_scored = False
        
    def move(self):
        self.vel.x = -1 * game_speed
        self.pos += self.vel
        self.rect.midbottom = self.pos

    
        
        
class Bird(pygame.sprite.Sprite):
    def __init__(self, x = window_width-35, y = window_height-49):
        super().__init__()
        self.surf = pygame.Surface((60,25))
        self.surf.fill(BLACK)
        self.rect = self.surf.get_rect(center = (x, y))
        self.pos = vec((x, y))
        self.vel = vec(0,0)
        self.is_scored = False
        
    def move(self):
        self.vel.x = -1 * game_speed
        self.pos += self.vel
        self.rect.midbottom = self.pos   



class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((window_width, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (window_width/2, window_height - 10))
    
    def reset(self):
        self.rect = self.surf.get_rect(center = (window_width/2, window_height - 10))




PT1 = platform()
P1 = Player()

platforms = pygame.sprite.Group()
platforms.add(PT1)

enemies = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)



def game_over():
    global enemy_list

    for entities in all_sprites:
        if entities in enemies:
            entities.kill()
    
    enemies.empty()
    enemy_list = list()


    display.fill((BLACK))
    gameover_font = pygame.font.Font('freesansbold.ttf', 16)
    gameover_text = gameover_font.render("Game over, press r to respawn or q to quit", True, WHITE)
    gameover_rect = gameover_text.get_rect()
    gameover_rect.center = (window_width/2, window_height/2)
    display.blit(gameover_text, gameover_rect)
    pygame.display.update()
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit
        sys.exit()
    elif event.type == KEYDOWN:
        if event.key == K_q:
            pygame.quit
            sys.exit()
        elif event.key == K_r:
            P1.reset()
            pass
        


    # gameover_text = pygame.font.Font('freesansbold.ttf', 72)
    # gameover_surf = gameover_text.render('Game over', True, GREEN)
    # gameover_rect = gameover_surf.get_rect()
    # gameover_rect.midtop = (window_width / 2, window_height / 2)
    # display.blit(gameover_surf,gameover_rect)
    


# forever loop
enemy_list = list()


def main():
    enemy_time = time.time() + 5
    global enemy_list

    while True:
        global game_speed
        # frame clock ticking
        clock.tick(frames_per_second)

        # frame Drawing
        display.fill(WHITE)
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        P1.move()
        P1.update()
        
        for e in enemy_list:
            e.move()

            if P1.rect.x > e.rect.x and not e.is_scored:
                score_sound.play()
                P1.score += 1
                e.is_scored = True



            if e.rect.x < -60:
                enemy_list.remove(e)

        if time.time() > enemy_time:
            
            enemy_type = random.randint(1,100)
            if enemy_type <=50:
                a = Cactus(window_width-30)
                all_sprites.add(a)
                enemies.add(a)
                enemy_list.append(a)
            else:
                a = Bird(window_width-30)
                all_sprites.add(a)
                enemies.add(a)
                enemy_list.append(a)
            
            enemy_time = time.time() + random.randint(1,3)
            game_speed += 0.5
        
        

        for entity in all_sprites:
            display.blit(entity.surf, entity.rect)
        
        text = font.render('Score: ' + str(P1.score), True, GREEN, BLUE)
        display.blit(text, textRect)

        


        pygame.display.update()
        clock.tick(frames_per_second)


main()