import pygame
from pygame.locals import *

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
    
    def update(self):
        # 2.2. Flapping animation
        self.counter += 1
        if self.counter > animation_cooldown:
            self.counter = 0
            self.index += 1
            if self.index > 2:
                self.index = 0
            self.image = self.frames[self.index]


# 2.3. Creating the player
player_group = pygame.sprite.Group()
player = Player(100, screen_width // 2)
player_group.add(player)

# --- 3. Game loop
run = True
while run:

    clock.tick(fps)

    # 3.1. Drawing and scrolling background
    screen.blit(bg, (0, 0))
    screen.blit(ground_img, (ground_scroll, 768))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    # 3.2. Drawing and animating the player
    player_group.draw(screen)
    player_group.update()

    # 3.3. Listening for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

