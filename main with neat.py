import pygame, time, sys, random, math, os, neat
from pygame.locals import *


# initialize it
pygame.init()

vec = pygame.math.Vector2

# configurations
frames_per_second = 60
window_height = 600
window_width = 800
game_speed = 5
number_of_generations = 200

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

font = pygame.font.Font('freesansbold.ttf', 24)
text = font.render('Shape game batak', True, GREEN, BLUE)
text2 = font.render('',True,GREEN, BLUE)
text3 = font.render('',True,GREEN, BLUE)
text4 = font.render('',True,GREEN, BLUE)
textRect = text.get_rect()
textRect2 = text2.get_rect()
textRect3 = text3.get_rect()
textRect4 = text4.get_rect()
textRect.center = (window_width * .70 , window_height * .10)
textRect2.center = (window_width * .70 , window_height * .15)
textRect3.center = (window_width * .70 , window_height * .20)
textRect4.center = (window_width * .05 , window_height * .10)

#Global Vars


class Player(pygame.sprite.Sprite):
    def __init__(self, x = window_width*0.10, y = 540):
        super().__init__() 
        self.x = x
        self.y = y
        self.surf = pygame.Surface((30, 60))
        self.surf.fill(BLUE)
        self.rect = self.surf.get_rect()
        self.pos = vec((x, y))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.IsJump = False
        self.IsDuck = False
        self.score = 0
        self.nearest_distance = 0
        self.nearest_type = 0
        self.nearest_x_distance = 0
 
    def move(self):
        global player_list

        self.acc = vec(0,3)

        if self.IsJump and self.pos.y <= window_height * 0.80:
            self.acc = vec(0,3)
            self.vel.y = 0


        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.jump()
        # if pressed_keys[K_LEFT]:
        #     self.acc.x = -ACC
        # if pressed_keys[K_RIGHT]:
        #     self.acc.x = ACC
        if pressed_keys[K_DOWN]:
            self.duck(not self.IsDuck)
        # if self.IsDuck and not pressed_keys[K_DOWN]:
        #     self.IsDuck = False
        #     self.surf = pygame.transform.smoothscale(self.surf,(30,60))
        #     self.rect = self.surf.get_rect()
             
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > window_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = window_width
        
        if self.pos.y > window_height-20:
            self.pos.y = window_height-20
            self.IsJump = False
            
        self.rect.midbottom = self.pos

    def update(self):
        global ge, player_list
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.IsJump = False

        hits2 = pygame.sprite.spritecollide(self, enemies, False)
        if hits2:
            index = player_list.index(self)
            ge[index].fitness -=2
            remove(index)
            self.die()
          
        
    def jump(self):
        # This current jump mechanism is too slow for fast game modes
        if not self.IsJump:
            self.vel.y = -30
            self.IsJump=True

        # if not self.IsJump:
        #     self.acc.y = -15
        #     self.vel.y += self.acc.y
        #     self.IsJump=True


    def duck(self,duck):
        # if not self.IsDuck:
        #     self.surf = pygame.transform.smoothscale(self.surf,(30,30))
        #     self.rect = self.surf.get_rect()
        #     if self.IsJump:
        #         self.vel.y = 20
        #     self.IsDuck = True
        if duck and self.IsDuck:
            pass
        
        elif duck and not self.IsDuck:
            self.surf = pygame.transform.smoothscale(self.surf,(30,30))
            self.rect = self.surf.get_rect()
            self.vel.y = 20
            self.IsDuck = True

        elif not duck and self.IsDuck:
            self.surf = pygame.transform.smoothscale(self.surf,(30,60))
            self.rect = self.surf.get_rect()
            self.IsDuck = False
            
        else:
            self.surf = pygame.transform.smoothscale(self.surf,(30,60))
            self.rect = self.surf.get_rect()
            self.IsDuck = False

    def reset(self):
        self.pos = vec((self.x, self.y))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.IsJump = False
        if self.IsDuck:
            self.surf = pygame.transform.smoothscale(self.surf,(30,60))
            self.rect = self.surf.get_rect()
            self.IsDuck = False
        self.score = 0
    
    def die(self):
        self.kill()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x = window_width-35, y = window_height-49):
        super().__init__()
        self.surf = pygame.Surface((25,60))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center = (x, y))
        self.pos = vec((x, y+30))
        self.vel = vec(0,0)
        self.is_scored = False
        self.enemy_type = 1
        
    def move(self):
        self.vel.x = -1 * game_speed
        self.pos += self.vel
        self.rect.midbottom = self.pos
    

    
        
        
class Bird(pygame.sprite.Sprite):
    def __init__(self, x = window_width-35, y = window_height-70):
        super().__init__()
        self.surf = pygame.Surface((40,65))
        self.surf.fill(BLACK)
        self.rect = self.surf.get_rect(center = (x, y))
        self.pos = vec((x, y))
        self.vel = vec(0,0)
        self.is_scored = False
        self.enemy_type = 2
        
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



player_list = list()
PT1 = platform()



platforms = pygame.sprite.Group()
platforms.add(PT1)

enemies = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
for p in player_list:
    all_sprites.add(p)



def distance(pos_a, pos_b):
    x1 = pos_a[0]
    y1 = pos_a[1]
    x2 = pos_b[0]
    y2 = pos_b[1]
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def game_over():
    global enemy_list, nearest_distance, nearest, player_list, highest_score

    for entities in all_sprites:
        if entities in enemies:
            entities.kill()
    
    enemies.empty()
    enemy_list = list()
    nearest = 0
    nearest_distance = 0
    highest_score = 0

    display.fill((BLACK))
    pygame.display.update()

    

    for p in player_list:
        p.reset()
        all_sprites.add(p)
    
    time.sleep(2)


# forever loop
enemy_list = list()
nearest = 0
nearest_distance = 0
highest_score = 0

def eval_genomes(genomes, config):
    enemy_time = time.time() + 5
    global enemy_list, nearest, nearest_distance, player_list, highest_score, ge, nets, game_speed

    player_list=[]
    ge = []
    nets = []
    
    #set all default
    for entities in all_sprites:
        if entities in enemies:
            entities.kill()
    
    enemies.empty()
    enemy_list = list()

    game_speed = 10 if game_speed - 2 < 10 else game_speed - 1

    


    for genome_id, genome in genomes:
        player_list.append(Player())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    for p in player_list:
        all_sprites.add(p)

    while True:
        
        # frame clock ticking
        clock.tick(frames_per_second)

        # frame Drawing
        display.fill(WHITE)
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    game_speed += 0.5

        if len(player_list) == 0:
            break
        
        
        
        
        for e in enemy_list:
            e.move()

            if e.rect.x < -60:
                    enemy_list.remove(e)

            for i,p in enumerate(player_list):
                if p.rect.midleft[0] > e.rect.midright[0] and not e.is_scored:
                    #score_sound.play()
                    p.score += 1
                    if e.enemy_type == 1:
                        ge[i].fitness += 2
                    else:
                        ge[i].fitness += 1
                    e.is_scored = True
                
                p.update()

        
        # for p in player_list:
        #     for e in enemy_list:
        #         if distance((p.rect.x, p.rect.y), (e.rect.midtop))>0:
        #             p.nearest_distance=distance((p.rect.x, p.rect.y), (e.rect.midtop))
        #             p.nearest_type = e.enemy_type
        #             p.nearest_height = e.rect.midbottom[1]
        #             break


        #if time.time() > enemy_time:
        if len(enemy_list) == 0:    
            enemy_type = random.randint(1,100)
            if enemy_type >= 50:
                a = Cactus(window_width-30)
                all_sprites.add(a)
                enemies.add(a)
                enemy_list.append(a)
            else:
                a = Bird(window_width-30)
                all_sprites.add(a)
                enemies.add(a)
                enemy_list.append(a)

            #enemy_time = time.time() + random.randint(2,3)
            game_speed += 0.10

        #set limit on speed
        game_speed = 50 if game_speed > 50 else game_speed
        # for p in player_list:
        #     p.move()
        #     p.update()
        #     if p.score > highest_score:
        #         highest_score = p.score
        
        for i, p in enumerate(player_list):

            for e in enemy_list:
                if distance((p.rect.topright), (e.rect.topleft))>0:
                    p.nearest_distance=distance((p.rect.topright), (e.rect.topleft))
                    p.nearest_type = e.enemy_type
                    p.nearest_x_distance = e.rect.midbottom[0] - p.rect.midbottom[0]  if e.rect.midbottom[0]  - p.rect.midbottom[0]  > 0 else 0
                    #p.nearest_height = e.rect.midbottom[1]
                    break
                elif distance((p.rect.topright), (e.rect.topleft))<0:
                    p.nearest_distance = 0
                    p.nearest_type = 0
                    p.nearest_height = 0
                    p.nearest_x_distance = 0

            output = nets[i].activate((p.rect.y, p.nearest_distance,p.nearest_type,p.nearest_x_distance, game_speed))
            if output[0] > 0.5 and not p.IsJump:
                p.jump()
            if output[1] > 0.5:
                p.duck(True)
            elif output[1] <= 0.5 and p.IsDuck:
                p.duck(False)
        
            p.move()
            p.update()
            if p.score > highest_score:
                highest_score = p.score
        
        
        # for p in player_list:
            


        for entity in all_sprites:
            display.blit(entity.surf, entity.rect)
        
        #input
        


        # text = font.render('Score: ' + str(highest_score) + " Nearest Distance: " + str(player_list[0].nearest_distance), True, GREEN, BLUE)
        text = font.render("Player count: " + str(len(player_list)), True, GREEN, BLUE)
        display.blit(text, textRect)
        text2 = font.render("Highest Score: " + str(highest_score), True, GREEN,BLUE)
        display.blit(text2, textRect2)
        text3 = font.render("Game speed: " + str(game_speed), True, GREEN,BLUE)
        display.blit(text3, textRect3)
        text4 = font.render("Generation: " + str(pop.generation + 1) + "/" + str(number_of_generations), True, GREEN,BLUE)
        display.blit(text4, textRect4)
        pygame.display.update()
        clock.tick(frames_per_second)



def remove(index):
    global player_list, ge, nets
    player_list.pop(index)
    ge.pop(index)
    nets.pop(index)

#Neat Implementation
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, number_of_generations)
    print("Generations: " + str(pop.generation + 1), " Highest score: " + str(highest_score))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)