import sys
import pygame
import math
import time
from pathfinding.core.grid import Grid
import csv
import random






pygame.init()

size = width, height = 540, 300
black = 0, 0, 0

screen = pygame.display.set_mode(size, flags=pygame.SCALED)



clock = pygame.time.Clock()
dt = 0
tl = 16

#save the map array inside a variable
def load_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [list(map(int, row)) for row in reader]

collision_map = load_csv('map_Tile Layer 1.csv')
unwalkeble = load_csv('map_obj.csv')

def add_collision(collision_map):
    nonowalk = []
    for row_index, row in enumerate(collision_map):
        for col_index, tile in enumerate(row):
            nonowalk.append(pygame.Rect(col_index * tl, row_index * tl, tl, tl))
    return nonowalk

cant = add_collision(collision_map)
#rotates the gun acording to the mouse position and distanced from the player
def rotate_on_pivot(image, angle, pivot, origin):
    
    surf = pygame.transform.rotate(image, angle)
    ov= pygame.math.Vector2(origin)
    pv = pygame.math.Vector2(pivot)
    offset = pivot + (ov - pv).rotate(-angle)
    rect = surf.get_rect(center = offset)
    
    return surf, rect

class Coconut(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.current_image = 0
        self.images = [
            pygame.image.load('items\coconut\Sprite-0001.png'),
            pygame.image.load('items\coconut\Sprite-0002.png'),
            pygame.image.load('items\coconut\Sprite-0003.png'),
            pygame.image.load('items\coconut\Sprite-0004.png'),
            pygame.image.load('items\coconut\Sprite-0005.png'),
            pygame.image.load('items\coconut\Sprite-0006.png'),
            pygame.image.load('items\coconut\Sprite-0007.png'),
            pygame.image.load('items\coconut\Sprite-0008.png'),
            pygame.image.load('items\coconut\Sprite-0009.png'),
            pygame.image.load('items\coconut\Sprite-0010.png')

        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
    def update(self, player):
        self.current_image +=0.1
        if self.current_image >= len(self.images) - 1:
            self.current_image = 0
        self.image = self.images[int(self.current_image)]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        if self.rect.colliderect(player.rect):
            if player.health < player.max_health:
                player.health = player.health + ((player.max_health/ 100) * 26)
                self.kill()
            
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
"""
class Sunscreen(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.current_image = 0
        self.images = [
            pygame.image.load('items/sunscreen/Sprite-0003.png'),
            pygame.image.load('items/sunscreen/Sprite-0004.png'),
            pygame.image.load('items/sunscreen/Sprite-0005.png'),
            pygame.image.load('items/sunscreen/Sprite-0006.png'),
            pygame.image.load('items/sunscreen/Sprite-0007.png'),
            pygame.image.load('items/sunscreen/Sprite-0008.png'),
            pygame.image.load('items/sunscreen/Sprite-0009.png'),
            pygame.image.load('items/sunscreen/Sprite-0010.png')

        ]
        self.image = self.images[0]
    def update(self, player):
        self.current_image +=0.1
        if self.current_image >= len(self.images) - 1:
            self.current_image = 0
        self.image = self.images[int(self.current_image)]
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
"""
class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.current_image = 0
        self.images = [
            pygame.image.load('items\water\Sprite-0001.png'),
            pygame.image.load('items\water\Sprite-0002.png'),
            pygame.image.load('items\water\Sprite-0003.png'),
            pygame.image.load('items\water\Sprite-0004.png'),
            pygame.image.load('items\water\Sprite-0005.png'),
            pygame.image.load('items\water\Sprite-0006.png'),
            pygame.image.load('items\water\Sprite-0007.png'),
            pygame.image.load('items\water\Sprite-0008.png'),

        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def update(self, player):
        self.current_image +=0.1
        if self.current_image >= len(self.images) - 1:
            self.current_image = 0
        self.image = self.images[int(self.current_image)]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        if self.rect.colliderect(player.rect):
            if player.sun_bar < player.max_sun_bar:
                player.sun_bar = player.max_sun_bar
                self.kill()
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Enemy(pygame.sprite.Sprite):
    def  __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 90
        self.damage = 10
        self.health = 15
        self.og = [
            pygame.image.load("enemies\crab\Sprite-0001.png"),
            pygame.image.load("enemies\crab\Sprite-0002.png"),
            pygame.image.load("enemies\crab\Sprite-0003.png"),
            pygame.image.load("enemies\crab\Sprite-001.png"),
            pygame.image.load("enemies\crab\Sprite-002.png"),
            pygame.image.load("enemies\crab\Sprite-003.png"),
            pygame.image.load("enemies\crab\Sprite-004.png"),
            pygame.image.load("enemies\crab\Sprite-005.png"),
            pygame.image.load("enemies\crab\Sprite-006.png"),
            pygame.image.load("enemies\crab\Sprite-007.png")
        ]
        self.current_lick = 3
        self.image = self.og[0]
        self.move = True
        self.current_image = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.flip = False
    def update(self, dt):
        self.player_pos = pygame.math.Vector2(player.x, player.y)
        self.enemy_pos = pygame.math.Vector2(self.x, self.y)
        self.distance = self.get_distance(self.player_pos, self.enemy_pos)
        if self.distance > 15:
            self.move = True
            self.direction = (self.player_pos - self.enemy_pos).normalize()
        else:
            self.move = False
            if not self.move:
                self.current_lick +=0.34
                if int(self.current_lick) >= 9:
                    self.current_lick = 3
                    player.TakeDamage(10)
            self.image = pygame.transform.flip(self.og[int(self.current_lick)], self.flip, False)
            self.direction = pygame.math.Vector2()
        self.velocity = self.speed * self.direction * dt
        self.x += self.velocity.x
        self.y += self.velocity.y
        if self.direction[0] > 0:
            if self.move:
                self.current_image +=0.1
                if int(self.current_image) >= 3:
                    self.current_image = 0
            self.flip = True
            self.image = pygame.transform.flip(self.og[int(self.current_image)], self.flip, False)

        elif self.direction[0] < 0:
            if self.move:
                self.current_image +=0.1
                if int(self.current_image) >= 3:
                    self.current_image = 0
            self.flip = False
            self.image = pygame.transform.flip(self.og[int(self.current_image)], self.flip, False)

        self.rect = self.image.get_rect(center=(self.x, self.y))
        if self.health <= 0:
            self.YoungManKillYourself()
    def get_distance(self, player_pos, enemy_pos):
        return (player_pos - enemy_pos).magnitude()  
    def YoungManKillYourself(self):
        player.xp += 15
        DropItem(self.x, self.y, random.randint(0, 60))
        self.kill()
    def TakeDamage(self, attack_damage):
        self.health -= attack_damage
    def draw(self, screen):
        if self.health < 16:
            pygame.draw.line(screen, 'red', self.enemy_pos, ((self.enemy_pos[0] + self.health), self.enemy_pos[1]))
        screen.blit(self.image, self.rect.center)

    


class Maps(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.bg = pygame.image.load("map.png")

    def draw(self, screen):
        screen.blit(self.bg, (self.x, self.y))


class Button(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height, text=''):
        super().__init__()
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


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
            self.YoungManKillYourself()
    def YoungManKillYourself(self):
        self.kill()
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
        self.level = 0
        self.xp = 1
        self.next_level_xp = 100
        self.speed = 100
        self.health = 100
        self.max_health = 100
        self.sun_bar = 100
        self.max_sun_bar = 100
        self.pressed = False
        self.time = 5
        self.images = [
            pygame.image.load("running\Sprite-0002.1.png").convert_alpha(),
            pygame.image.load("running\Sprite-0002.2.png").convert_alpha(),
            pygame.image.load("running\Sprite-0002.3.png").convert_alpha(),
            pygame.image.load("running\Sprite-0002.4.png").convert_alpha(),
            pygame.image.load("running\Sprite-0002.5.png").convert_alpha(),
            pygame.image.load("running\Sprite-0002.6.png").convert_alpha(),
            pygame.image.load("running\Sprite-0002.7.png").convert_alpha(),
            pygame.image.load("running\Sprite-0002.8.png").convert_alpha(),
            pygame.image.load("running\Sprite-0002.9.png").convert_alpha(),
            pygame.image.load("running\Sprite-0002.10.png").convert_alpha(),
            pygame.image.load("idle\Sprite-0002.1.png").convert_alpha(),
            pygame.image.load("idle\Sprite-0002.2.png").convert_alpha()
        ]
        self.current_image = 1
        self.image = self.images[self.current_image]
        self.gun = pygame.image.load("guns\Sprite-0001.png").convert_alpha()
        self.gun_rect = self.image.get_rect(center = (self.x, self.y))
        self.last_fired = time.time()
        self.fire_cooldown = 0.4
        self.yy = 0
        self.xx = 0
        self.flip = False
        self.limitx = 200
        self.limiy = 100
        self.flipping_gun = False
        self.run = False
        self.stop = False
        self.attack_damage = 5
    def update(self, dt):
        self.time -= dt
        if self.run:
            self.current_image +=0.2
            if self.current_image >= len(self.images) -2:
                self.current_image = 0
                self.run = False
        else:
            self.current_image +=0.1
            if self.current_image >= len(self.images):
                self.current_image = len(self.images)- 2

        
        self.image = self.images[int(self.current_image)]
        if pygame.mouse.get_pressed()[0] and time.time() - self.last_fired > self.fire_cooldown:
            bullet = Bullet(self.gun_rect.x ,self.gun_rect.y, mouse_angle)
            bullets.add(bullet)
            self.last_fired = time.time()
            #self.pressed = True
        keys = pygame.key.get_pressed()

        self.rect = self.image.get_rect(center=(self.x, self.y))   
        if keys[pygame.K_w] and self.y <= self.limiy:
            self.yy -= self.speed * dt
            self.run = True
            if self.stop:
                self.yy += self.speed * dt
            
        elif keys[pygame.K_s]and self.y >= screen.get_height() - self.limiy:
            self.yy += self.speed * dt
            self.run = True
            if self.stop:
                self.yy -= self.speed * dt
        if keys[pygame.K_a] and self.x <= self.limitx:
            self.xx -= self.speed * dt
            self.flip = False
            self.run = True
            if self.stop:
                self.xx += self.speed * dt
        elif keys[pygame.K_d] and self.x >= screen.get_width()- self.limitx:
            self.xx += self.speed * dt
            self.flip = True
            self.run = True
            if self.stop:
                self.xx -= self.speed * dt

        if keys[pygame.K_w]and self.y >= self.limiy:
            self.y -= self.speed * dt
            self.run = True
            if self.stop:
                self.y += self.speed * dt
        elif keys[pygame.K_s]and self.y <= screen.get_height() - self.limiy:
            self.y += self.speed * dt
            self.run = True
            if self.stop:
                self.y -= self.speed * dt
        if keys[pygame.K_a]and self.x >= self.limitx:
            self.x -= self.speed * dt
            self.flip = False
            self.run = True
            if self.stop:
                self.x += self.speed * dt
        elif keys[pygame.K_d]and self.x <= screen.get_width()- self.limitx:
            self.x += self.speed * dt
            self.flip = True
            self.run = True
            if self.stop:
                self.x -= self.speed * dt
  
        
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
        if self.xp >= self.next_level_xp:
            self.xp = 1 + (self.xp - self.next_level_xp)
            self.next_level_xp = self.next_level_xp + (self.next_level_xp * 2.1)
            self.level +=1
        if self.health > self.max_health:
            self.health = self.max_health
        if self.sun_bar > self.max_sun_bar:
            self.health = self.max_sun_bar
        return (self.x_offset, self.y_offset)
    



            
    def draw(self):
        self.gun_rotate, self.gun_rect = rotate_on_pivot(pygame.transform.flip(self.gun, self.flipping_gun, False), mouse_angle, (self.x, self.y), (self.x, self.y + 14))
        
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        screen.blit(self.gun_rotate, self.gun_rect)

    def TakeDamage(self, amount):
        self.health -= amount
        
player = Player(100, 111)
objects = pygame.sprite.Group()
#objects.add(player)
bullets = pygame.sprite.Group()
ui = pygame.sprite.Group()
maps = pygame.sprite.Group()
bottown = Button('red', 100, 100, 100, 50, 'hello')
ui.add(bottown)
bg = Maps()
maps.add(bg)
en = Enemy(200, 200)
en2 = Enemy(30, 10 )
en1 = Enemy(500, 300)
objects.add(en)
objects.add(en2)
objects.add(en1)
items = pygame.sprite.Group()
def DropItem(x,y, num):
    itms = {
        43: Water(x, y),
        6: Coconut(x, y)
    }
    if num == 43 or num == 6:
        items.add(itms[num])
    else:
        print('nuh uh')

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
    for i in maps:
        i.x = i.x - player.x_offset
        i.y = i.y - player.y_offset
        i.draw(screen)
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
    
    for bullet in bullets:
        for object in objects:
           if bullet.rect.colliderect(object.rect):
               bullet.YoungManKillYourself()
               object.TakeDamage(player.attack_damage)
    
    items.update(player)
    for i in items:
        i.x = i.x - player.x_offset
        i.y = i.y - player.y_offset
        i.draw()
              
    print(f'{player.x} : {player.y}')
     #draw the health bar

    pygame.draw.line(screen, 'blue', (10, screen.get_height() - 10), (10 +round(((player.xp / player.next_level_xp) * 100), 1), screen.get_height() - 10), width=6)
    screen.blit(pygame.image.load('xp_bar.png'), pygame.image.load('xp_bar.png').get_rect(topleft=(7,  screen.get_height() - 20)))
    pygame.draw.line(screen, 'red', (10, 10), (10 + player.health, 10), width=4)
    pygame.draw.line(screen, 'yellow', (10, 20), (10 + player.sun_bar, 20), width=4)
    
    pygame.display.flip()


    dt = clock.tick(60) / 1000