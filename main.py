import pygame
from pygame.locals import *
import random

# --- 1. Initializing
pygame.init()

# 1.1. Setting up display
clock = pygame.time.Clock()
fps = 60
screen_width = 800
screen_height = 920
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird Clones')

# 1.2. Loading background
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
 
# 1.3. Setting game variables
ground_scroll = 0
scroll_speed = 4
animation_cooldown = 5
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #miliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

# --- 2. Player class
class Player(pygame.sprite.Sprite):
    # 2.1. Initializing the player
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.index = 0
        self.counter = 0
        self.frames = [
            pygame.image.load('img/sprite1.png'),
            pygame.image.load('img/sprite2.png'),
            pygame.image.load('img/sprite3.png')
        ]
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
     
        if flying == True:
            # 2.2. Gravity 
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        
        if game_over == False:
            # 2.3. Jump 
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
     
            # 2.4. Flapping animation
            self.counter += 1
            if self.counter > animation_cooldown:
                self.counter = 0
                self.index += 1
                if self.index > 2:
                    self.index = 0
            self.image = self.frames[self.index]
            
            # 2.5. Rotate the player
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


# 4.1 Pipe class
class Pipe(pygame, sprite, Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png') #zrobić obrazek pipe
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
          
          
# 2.6. Creating the player
player_group = pygame.sprite.Group()
player = Player(100, screen_width // 2)
player_group.add(player)

# 4.2 Creating pipes
pipe_group = pygame.sprite.Sprite

# --- 3. Game loop
run = True
while run:

    clock.tick(fps)

    # 3.1. Drawing background
    screen.blit(bg, (0, 0))
    screen.blit(ground_img, (ground_scroll, 768))
    
    # 4.3 Collision
    if pygame.sprite.groupcollide(player_group, pipe_group, False, False) or player.rect.bottom < 0:
        game_over = True

    # 3.2. Check if player has hit the ground 
    if player.rect.bottom >= 768:
        game_over = True
        flying = False
    
    if game_over == False and flying == True:
        # 4.4 Generating new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(100, 100)
            btm_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now


        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()
         
    # 3.3. Drawing and animating the player
    player_group.draw(screen)
    player_group.update()

    # 4.5 Drawing pipes
    pipe_group.draw(screen)

    # 3.4. Listening for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()

