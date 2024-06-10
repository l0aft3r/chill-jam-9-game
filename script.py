import sys
import pygame
import math

pygame.init()

BLACK = 0, 0, 0

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #You can comment this line out and set your own screen dimensions if you find it annoying
clock = pygame.time.Clock()
dt = 0

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.temp = 0
        self.x = x
        self.y = y
        self.speed = 300
        self.image = pygame.image.load("png-transparent-football-ball-game-soccer-ball-soccer-ball-artwork-miscellaneous-sport-sports-equipment-thumbnail.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def update(self, dt, keys):
         if keys[pygame.K_w]:
             self.y -= self.speed * dt
         elif keys[pygame.K_s]:
             self.y += self.speed * dt
         if keys[pygame.K_a]:
             self.x -= self.speed * dt
         elif keys[pygame.K_d]:
             self.x += self.speed * dt

    def draw(self, mouse_pos):
        mouse_angle = math.degrees(math.atan2(mouse_pos[0] - player.x, mouse_pos[1] - player.y)) 
        self.rotate = pygame.transform.rotozoom(self.image, mouse_angle, 1)
        self.orthogonally_tilted_quadrilateral_plane = self.rotate.get_rect(center = (self.x, self.y))
        screen.blit(self.rotate, self.orthogonally_tilted_quadrilateral_plane)
       
player = Player(600, 400)

objects = pygame.sprite.Group()
objects.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: #Added closing the game using ESC
        pygame.quit()
        sys.exit()
    
    mouse_pos = pygame.mouse.get_pos()

    screen.fill(BLACK)
    objects.update(dt, keys)
    for i in objects:
            i.draw(mouse_pos)

    pygame.display.flip()


    dt = clock.tick(60) / 1000