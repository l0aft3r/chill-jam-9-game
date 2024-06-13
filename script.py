import sys
import pygame
import math
import time
from pathfinding.core.grid import Grid



pygame.init()

size = width, height = 540, 300
black = 0, 0, 0

screen = pygame.display.set_mode(size, flags=pygame.SCALED)



clock = pygame.time.Clock()
dt = 0

def rotate_on_pivot(image, angle, pivot, origin):
    
    surf = pygame.transform.rotate(image, angle)
    ov= pygame.math.Vector2(origin)
    pv = pygame.math.Vector2(pivot)
    offset = pivot + (ov - pv).rotate(-angle)
    rect = surf.get_rect(center = offset)
    
    return surf, rect
"""class Enemy(pygame.sprite.Sprite):
    def  __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'{image}.png')
    def update(self):

    def draw(self):"""


class Objects(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.bgt = pygame.image.load("bg.png")
        self.bg = pygame.transform.scale(self.bgt, (1000, 1000))

    def draw(self, screen):
        screen.blit(self.bg, (self.x, self.y))


class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, height, width, color, image_path):
        super().__init__()
        self.rect = pygame.Rect(x,y, width, height)
        self.surface = pygame.surface.Surface((width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    def draw(self):
         self.surface.fill(self.color)
         screen.blit(self.surface, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_angle):
        super().__init__()
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.x = x
        self.y = y
        self.mouse_angle = mouse_angle
        self.speed = 900
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
        self.rotate = pygame.transform.rotozoom(self.image, self.mouse_angle, 1)
        self.rect = self.rotate.get_rect(center=(self.x, self.y))
        screen.blit(self.rotate, (self.rect.center))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.x_offset = 0
        self.y_offset = 0
        self.speed = 200
        self.health = 100
        self.sun_bar = 100
        self.pressed = False
        self.time = 5
        self.image = pygame.image.load("player.png").convert_alpha()
        self.gun = pygame.transform.scale(pygame.image.load("gun.png").convert_alpha(), (16,16))
        self.gun_rect = self.image.get_rect(center = (self.x, self.y))
        self.last_fired = time.time()
        self.fire_cooldown = 0.4
        self.yy = 0
        self.xx = 0
        self.flip = False
        self.limitx = 200
        self.limiy = 100
        self.flipping_gun = False

    def update(self, dt):
        self.time -= dt
        if pygame.mouse.get_pressed()[0] and time.time() - self.last_fired > self.fire_cooldown:
            bullet = Bullet(self.gun_rect.x ,self.gun_rect.y, mouse_angle)
            bullets.add(bullet)
            self.last_fired = time.time()
            #self.pressed = True
        keys = pygame.key.get_pressed()


        if keys[pygame.K_w] and self.y <= self.limiy:
            self.yy -= self.speed * dt
        elif keys[pygame.K_s]and self.y >= screen.get_height() - self.limiy:
            self.yy += self.speed * dt
        if keys[pygame.K_a] and self.x <= self.limitx:
            self.xx -= self.speed * dt
            self.flip = False
        elif keys[pygame.K_d] and self.x >= screen.get_width()- self.limitx:
            self.xx += self.speed * dt
            self.flip = True

        if keys[pygame.K_w]and self.y >= self.limiy:
            self.y -= self.speed * dt
        elif keys[pygame.K_s]and self.y <= screen.get_height() - self.limiy:
            self.y += self.speed * dt
        if keys[pygame.K_a]and self.x >= self.limitx:
            self.x -= self.speed * dt
            self.flip = False
        elif keys[pygame.K_d]and self.x <= screen.get_width()- self.limitx:
            self.x += self.speed * dt
            self.flip = True
       
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.x_offset = self.xx
        self.y_offset = self.yy
        self.gun_rect.x = self.x
        self.gun_rect.y= self.y 
        self.xx = 0
        self.yy = 0
        self.flipping_gun = True if(mouse_angle < 0) else False
        
        
        #drains the sun bar every 5 seconds
        if self.time <= 0:
           print('sun damage')
           self.sun_bar -=1
           self.time = 5
           
        #kill the player when health reaches 0
        if self.health <= 0 or self.sun_bar <= 0:
            pygame.sprite.Sprite.kill(self)

        return (self.x_offset, self.y_offset)
            
    def draw(self):
        self.rotate = pygame.transform.scale(self.image, (32,32))
        self.gun_rotate, self.gun_rect = rotate_on_pivot(pygame.transform.flip(self.gun, self.flipping_gun, False), mouse_angle, (self.x, self.y), (self.x, self.y + 30))
        
        screen.blit(pygame.transform.flip(self.rotate, self.flip, False), self.rect)
        screen.blit(self.gun_rotate, self.gun_rect)

    def TakeDamage(self, amount):
        self.health -= amount
        
player = Player(600, 400)
objects = pygame.sprite.Group()
#objects.add(player)
bullets = pygame.sprite.Group()
ui = pygame.sprite.Group()
bottown = Button('fuck', 60, 60, 30, 100, 'red', 'wa')
ui.add(bottown)
bg = Objects()
objects.add(bg)
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
    
    

    player.update(dt)
    for i in objects:
        i.x = i.x - player.x_offset
        i.y = i.y - player.y_offset
        i.draw(screen)

    player.draw()
    for i in bullets:
        i.x = i.x - player.x_offset
        i.y = i.y - player.y_offset
        i.draw()
    
    for i in ui:
        i.draw()
    
     #draw the health bar
    pygame.draw.line(screen, 'red', (10, 10), (10 + player.health, 10), width=4)
    pygame.draw.line(screen, 'yellow', (10, 20), (10 + player.sun_bar, 20), width=4)
    
    pygame.display.flip()


    dt = clock.tick(60) / 1000