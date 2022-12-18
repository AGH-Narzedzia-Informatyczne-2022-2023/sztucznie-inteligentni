import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 920

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')
 
#define game variables
ground_scroll = 0
scroll_speed = 4
animation_cooldown = 5

#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

# create bird
class Player(pygame.sprite.Sprite):
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
        self.counter += 1
        if self.counter > animation_cooldown:
            self.counter = 0
            self.index += 1
            if self.index > 2:
                self.index = 0
            self.image = self.frames[self.index]



player_group = pygame.sprite.Group()
player = Player(100, screen_width // 2)
player_group.add(player)

run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0, 0))

    player_group.draw(screen)
    player_group.update()

    #draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, 768))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

