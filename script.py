import sys
import pygame
import math


pygame.init()

size = width, height = 1280, 720
black = 0, 0, 0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
dt = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 400
        self.image = pygame.image.load("png-transparent-football-ball-game-soccer-ball-soccer-ball-artwork-miscellaneous-sport-sports-equipment-thumbnail.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def update(self, dt):
         keys = pygame.key.get_pressed()
         if keys[pygame.K_w]:
             self.y -= 300 * dt
         elif keys[pygame.K_s]:
             self.y += 300 * dt
         if keys[pygame.K_a]:
             self.x -= 300 * dt
         elif keys[pygame.K_d]:
             self.x += 300 * dt
    def draw(self, mouse_angle):
        print('he')
        self.rotate = pygame.transform.rotozoom(self.image, mouse_angle, 1)
        self.retartded_rect = self.rotate.get_rect(center = (self.x, self.y))
        screen.blit(self.rotate, self.retartded_rect)
       
player = Player(600, 400)
objects = pygame.sprite.Group()
objects.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(black)

    mouse_angle = math.degrees(math.atan2(mouse_pos[0] - player.x, mouse_pos[1] - player.y)) 
    objects.update(dt)
    for i in objects:
        i.draw(mouse_angle)

   
    
    pygame.display.flip()


    dt = clock.tick(60) / 1000