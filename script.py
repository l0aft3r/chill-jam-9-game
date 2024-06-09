import sys
import pygame
import math


pygame.init()

size = width, height = 1280, 720
black = 0, 0, 0

objects = []
screen = pygame.display.set_mode(size)
px = 100
py = 200
ball = pygame.image.load("png-transparent-football-ball-game-soccer-ball-soccer-ball-artwork-miscellaneous-sport-sports-equipment-thumbnail.png").convert_alpha()
clock = pygame.time.Clock()
dt = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    mous_pos = pygame.mouse.get_pos()
    screen.fill(black)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        py -= 300 * dt
    elif keys[pygame.K_s]:
        py += 300 * dt
    if keys[pygame.K_a]:
        px -= 300 * dt
    elif keys[pygame.K_d]:
        px += 300 * dt


    anglemous = math.degrees(math.atan2(mous_pos[0] - px, mous_pos[1] - py)) 

    rotatedball = pygame.transform.rotozoom(ball, anglemous, 1)

    rectball = rotatedball.get_rect(center = (px, py))
    
    screen.blit(rotatedball, rectball)
    
    pygame.display.flip()


    dt = clock.tick(60) / 1000