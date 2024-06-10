import sys
import pygame
import math
import time


pygame.init()

size = width, height = 1280, 600
black = 0, 0, 0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
dt = 0
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_angle):
        super().__init__()
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.x = x
        self.y = y
        self.mouse_angle = mouse_angle
        self.speed = 400
        self.lifetime = 3
        self.rotate = pygame.transform.rotozoom(self.image, mouse_angle, 1)
        self.rect = self.rotate.get_rect(center =(self.x, self.y))
        self.dx = self.speed * math.cos(math.radians(self.mouse_angle - 90))
        self.dy = -self.speed * math.sin(math.radians(self.mouse_angle - 90))
    
    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        #life time of the bullet
        self.lifetime -= dt
        if self.lifetime <= 0:
            print('deleting')
            pygame.sprite.Sprite.kill(self)



        

    def draw(self):
        print('e')
        self.rotate = pygame.transform.rotozoom(self.image, self.mouse_angle, 1)
        self.rect = self.rotate.get_rect(center=(self.x, self.y))
        screen.blit(self.rotate, (self.rect.center))


        

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 400
        self.image = pygame.image.load("player.png").convert_alpha()
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
         if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet(self.x, self.y, mouse_angle)
            bullets.add(bullet)
        
            
    def draw(self, mouse_angle):
        self.rotate = pygame.transform.rotozoom(self.image, mouse_angle, 1)
        self.orthogonally_tilted_quadrilateral_plane = self.rotate.get_rect(center = (self.x, self.y))
        screen.blit(self.rotate, self.orthogonally_tilted_quadrilateral_plane)
       
player = Player(600, 400)
objects = pygame.sprite.Group()
objects.add(player)
bullets = pygame.sprite.Group()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(black)

    mouse_angle = math.degrees(math.atan2(mouse_pos[0] - player.x, mouse_pos[1] - player.y)) 
    objects.update(dt)
    bullets.update(dt)
    for i in objects:
        i.draw(mouse_angle)

    for i in bullets:
        i.draw()

   
    
    pygame.display.flip()


    dt = clock.tick(60) / 1000