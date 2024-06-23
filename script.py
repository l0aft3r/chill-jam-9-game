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

main_font = pygame.font.SysFont("cambria", 50)
clock = pygame.time.Clock()
dt = 0
tl = 16

from ui import Button

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

#i asked chat gpt to do this cuz we dont have much time YOLO
#btw i can do it myself but u know i dont need to rn
class FloatingText(pygame.sprite.Sprite):
    def __init__(self, text, pos, color):
        super().__init__()
        self.text = text
        self.pos = list(pos)  # Position as [x, y]
        self.font = pygame.font.Font(None, 14)  # Font and size
        self.color = color
        self.speed = -1  # Speed of floating text movement
        self.fade_speed = 4  # Speed of fading out
        self.alpha = 255  # Initial alpha value (fully opaque)


    def draw(self, screen):
        # Render the text
        self.pos[1] += self.speed
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.alpha = 0
            self.kill()
        text_surface = self.font.render(self.text, False, self.color)
        text_surface.set_alpha(self.alpha)
        
        # Blit the text surface onto the screen
        screen.blit(text_surface, self.pos)


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
    def  __init__(self, x, y, level):
        super().__init__()
        self.x = x
        self.y = y
        self.level = level
        self.speed = random.randint(80, 150) 
        self.takingDamage = False

        self.damage = 10 * (1 + (self.level / 5))
        self.health = 15 * (1 + (self.level / 2))
        self.max_health = 15 * (1 + (self.level / 2))
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
                self.current_lick +=0.5
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
        brighten = 255
        if self.takingDamage:
            self.image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
            self.takingDamage = False
        self.rect = self.image.get_rect(center=(self.x, self.y))
        if self.health <= 0:
            self.YoungManKillYourself()
    def get_distance(self, player_pos, enemy_pos):
        return (player_pos - enemy_pos).magnitude()  
    def YoungManKillYourself(self):
        player.xp += 15 * (self.level * 1.6)
        DropItem(self.x, self.y, random.randint(0, 60))
        player.startfish += random.randint(player.level * 2, player.level * 6)
        self.kill()
    def TakeDamage(self, attack_damage):
        self.takingDamage = True
        self.health -= attack_damage
    def draw(self, screen):
        if self.health < self.max_health:
            pygame.draw.line(screen, 'red', self.enemy_pos, ((self.enemy_pos[0] + (self.health / self.max_health) * 15), self.enemy_pos[1]))
        screen.blit(self.image, self.rect.center)

    


class Maps(pygame.sprite.Sprite):
    def __init__(self, map):
        super().__init__()
        self.x = 0
        self.y = 0
        self.bg = pygame.image.load(f'maps\{map}.png')
        self.base = pygame.Rect(620 + self.x - player.x_offset, 100 + self.y - player.y_offset, 30, 100)
        self.map = map
        self.next_level = pygame.Rect(350 + self.x - player.x_offset, 460 + self.y - player.y_offset, 100, 50)
        self.arrow2 = 0
        self.arrow3 = 0
        self.arrow_up = pygame.transform.rotate(pygame.image.load('arrow.png'), -270)
        if self.map == 1:
            self.top = 80
            self.bottom = 430
            self.left = 0
            self.right = 470
        elif self.map == 2:
            self.top = 0
            self.bottom = 470
            self.left = 150
            self.right = 640
        elif self.map == 3:
            self.top = 100
            self.bottom = 470
            self.left = 120
            self.right = 640
        elif self.map == 4:
            self.top = 0
            self.bottom = 470
            self.left = 0
            self.right = 640
        elif self.map == 5:
            self.top = 0
            self.bottom = 410
            self.left = 110
            self.right = 640

    def draw(self, screen):
        self.base = pygame.Rect(620 + self.x - player.x_offset, 100 + self.y - player.y_offset, 30, 100)
        if self.map == 1:
            self.next_level = pygame.Rect(0 + self.x - player.x_offset, 0 + self.y - player.y_offset, 30, 400)
        elif self.map == 2 or self.map == 3 or self.map == 4:
            self.next_level = pygame.Rect(350 + self.x - player.x_offset, 460 + self.y - player.y_offset, 100, 20)
        else:
            self.next_level = pygame.Rect(100 + self.x - player.x_offset, 0 + self.y - player.y_offset, 200, 20)
        
        
        screen.blit(self.bg, (self.x, self.y))
        if can_leave and not map == 1 and not map == 5:
            self.arrow2 += 0.04
            if self.arrow2 >= 2:
                self.arrow2 = 0
            if int(self.arrow2) == 1:
                screen.blit(pygame.transform.rotate(pygame.image.load('arrow.png').convert_alpha(), -90), (self.next_level[0], self.next_level[1] -50))
            else:
                screen.blit(pygame.transform.rotate(pygame.image.load('arrow2.png').convert_alpha(), -90), (self.next_level[0], self.next_level[1] -50))
        elif can_leave and not map == 1 and map == 5:
            self.arrow2 += 0.04
            if self.arrow2 >= 2:
                self.arrow2 = 0
            if int(self.arrow2) == 1:
                screen.blit(self.arrow_up, (self.next_level[0], self.next_level[1]))
            else:
                screen.blit(self.arrow_up, self.next_level)
        if can_leave:
            self.arrow3 += 0.04
            if self.arrow3 >= 2:
                self.arrow3 = 0
            if int(self.arrow3) == 1:
                screen.blit(pygame.image.load('arrow.png').convert_alpha(), (self.base[0] - 64, self.base[1]))
            else:
                screen.blit(pygame.image.load('arrow2.png').convert_alpha(), (self.base[0] - 64, self.base[1]))

        
            

        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_angle, speed):
        super().__init__()
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.x = x
        self.y = y
        self.mouse_angle = mouse_angle
        self.speed = speed
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
        self.level = 1
        self.xp = 1
        self.next_level_xp = 200
        self.speed = 100
        self.health = 100
        self.max_health = 100 * (1 + (self.level / 10))
        self.sun_bar = 100
        self.max_sun_bar = 100
        self.pressed = False
        self.time = 5
        self.startfish_image = pygame.image.load('starfish.png')
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
        self.fire_cooldown = 0.1
        self.yy = 0
        self.xx = 0
        self.flip = False
        self.limitx = 200
        self.limiy = 100
        self.flipping_gun = False
        self.run = False
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.attack_damage = int(5 * (1 + (self.level / 11)))
        self.n_bullet = 1
        self.startfish = 0
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

        if self.x - bg.x <= bg.left:
            self.left = True
        else:
            self.left = False
        if self.x - bg.x >= bg.right:
            self.right = True
        else:
            self.right = False
        if self.y - bg.y <= bg.top:
            self.up = True
        else:
            self.up = False
        if self.y - bg.y >= bg.bottom:
            self.down = True
        else:
            self.down = False
        self.image = self.images[int(self.current_image)]
        if pygame.mouse.get_pressed()[0] and time.time() - self.last_fired > self.fire_cooldown:
            for i in range(self.n_bullet):
                bullet = Bullet(self.gun_rect.x ,self.gun_rect.y, mouse_angle * (1 + (i /10)), 300)
                bullets.add(bullet)
            self.last_fired = time.time()
            #self.pressed = True
        keys = pygame.key.get_pressed()

        self.rect = self.image.get_rect(center=(self.x, self.y))   
        if keys[pygame.K_w] and self.y <= self.limiy:
            self.yy -= self.speed * dt
            self.run = True
            if self.up:
                self.yy += self.speed * dt
            
        elif keys[pygame.K_s]and self.y >= screen.get_height() - self.limiy:
            self.yy += self.speed * dt
            self.run = True
            if self.down:
                self.yy -= self.speed * dt
        if keys[pygame.K_a] and self.x <= self.limitx:
            self.xx -= self.speed * dt
            self.flip = False
            self.run = True
            if self.left:
                self.xx += self.speed * dt
        elif keys[pygame.K_d] and self.x >= screen.get_width()- self.limitx:
            self.xx += self.speed * dt
            self.flip = True
            self.run = True
            if self.right:
                self.xx -= self.speed * dt

        if keys[pygame.K_w]and self.y >= self.limiy:
            self.y -= self.speed * dt
            self.run = True
            if self.up:
                self.y += self.speed * dt
        elif keys[pygame.K_s]and self.y <= screen.get_height() - self.limiy:
            self.y += self.speed * dt
            self.run = True
            if self.down:
                self.y -= self.speed * dt
        if keys[pygame.K_a]and self.x >= self.limitx:
            self.x -= self.speed * dt
            self.flip = False
            self.run = True
            if self.left:
                self.x += self.speed * dt
        elif keys[pygame.K_d]and self.x <= screen.get_width()- self.limitx:
            self.x += self.speed * dt
            self.flip = True
            self.run = True
            if self.right:
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
            self.max_health = int(100 * (1 + (self.level / 10)))
            self.attack_damage = int(self.attack_damage * (1 + (self.level / 8)))
            self.health = self.max_health
            LevelUP(self)
        if self.health > self.max_health:
            self.health = self.max_health
        if self.sun_bar > self.max_sun_bar:
            self.health = self.max_sun_bar
        return (self.x_offset, self.y_offset)
    



            
    def draw(self):
        screen.blit(self.startfish_image, (screen.get_width() - 64, 10))
        self.gun_rotate, self.gun_rect = rotate_on_pivot(pygame.transform.flip(self.gun, self.flipping_gun, False), mouse_angle, (self.x, self.y), (self.x, self.y + 14))
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        screen.blit(self.gun_rotate, self.gun_rect)

    def TakeDamage(self, amount):
        self.health -= amount
def LevelUP(player):
    damage_counter.add(FloatingText('Level up', [player.x, player.y], 'blue'))
player = Player(100, 111)
objects = pygame.sprite.Group()
#objects.add(player)
bullets = pygame.sprite.Group()
ui = pygame.sprite.Group()
maps = pygame.sprite.Group()
#bottown = Button('red', 100, 100, 100, 50, 'hello')
#ui.add(bottown)
global bg
bg = Maps(2)

maps.add(bg)
en = Enemy(200, 200, 1)
en2 = Enemy(30, 10, 2)
en1 = Enemy(500, 300, 3)
objects.add(en)
objects.add(en2)
objects.add(en1)
items = pygame.sprite.Group()
damage_counter = pygame.sprite.Group()
can_leave = False
wave = random.randint(0, 2)
og_wave = wave
n_enemies = random.randint(int(player.level), int(player.level * 2.5))
spawn_time = random.randint(40, 100)
current_spawn_time = 0
enemies_spawned = 0
spwn_speed =  0.05 + abs(wave - og_wave)/ 20

def DropItem(x,y, num):
    itms = {
        43: Water(x, y),
        6: Coconut(x, y)
    }
    if num == 43 or num == 6:
        items.add(itms[num])
    else:
        print('nuh uh')

def mainGame():
    pygame.display.set_caption("Game")
    global dt
    global mouse_angle
    global bg
    global wave
    global og_wave
    global can_leave
    global n_enemies
    global current_spawn_time
    global enemies_spawned
    global spawn_time
    global spwn_speed
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
        if len(objects) == 0 and wave <= 0:
            can_leave = True
        elif bg.map == 1:
            can_leave = False
        else:
            can_leave = False
        if len(objects) == 0 and wave > 0 and not bg.map == 1:
            wave -= 1
            n_enemies = random.randint(int(player.level), int(player.level * 2.5))
            enemies_spawned = 0
            spwn_speed =  0.05 + abs(wave - og_wave)/ 20

        current_spawn_time += spwn_speed
        if not bg.map == 1:
                if n_enemies >= enemies_spawned:
                    if current_spawn_time >= spawn_time:
                        objects.add(Enemy(random.randint(bg.left, bg.right), random.randint(bg.top, bg.bottom), abs(wave - og_wave) + player.level + random.randint(0, 1)))
                        enemies_spawned += 1
                        spawn_time = random.randint(0, 2)
                        current_spawn_time = 0

        print(wave)
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
                   damage_counter.add(FloatingText(f'{player.attack_damage}', [object.x, object.y], 'red'))

        items.update(player)
        for i in items:
            i.x = i.x - player.x_offset
            i.y = i.y - player.y_offset
            i.draw()
        for i in damage_counter:
            i.x = i.pos[0] - player.x_offset
            i.y = i.pos[1] - player.y_offset
            i.draw(screen)
        pygame.draw.rect(screen, (200,0,0), bg.base)
        if can_leave:
            if bg.next_level.colliderect(player.rect):
                    print('wi')
                    maps.remove(bg)
                    bg = Maps(random.randint(2, 5))
                    maps.add(bg)
                    player.x = 300
                    player.y = 100
                    og_wave = random.randint(player.level, player.level + 4)
                    wave = og_wave
            if bg.base.colliderect(player.rect):
                    maps.remove(bg)
                    for i in objects:
                        objects.remove(i)
                    bg = Maps(1)
                    maps.add(bg)
                    player.x = 300
                    player.y = 100
                  
        #print(f'{int(player.x - bg.x)} : {int(player.y - bg.y)}')
         #draw the health bar
        
        pygame.draw.line(screen, 'blue', (10, screen.get_height() - 10), (10 +round(((player.xp / player.next_level_xp) * 100), 1), screen.get_height() - 10), width=6)
        screen.blit(pygame.image.load('xp_bar.png'), pygame.image.load('xp_bar.png').get_rect(topleft=(7,  screen.get_height() - 20)))
        pygame.draw.line(screen, 'red', (10, 10), (10 + (player.health / player.max_health) * 100, 10), width=4)
        pygame.draw.line(screen, 'yellow', (10, 20), (10 + player.sun_bar, 20), width=4)

        pygame.display.flip()


        dt = clock.tick(60) / 1000

def mainMenu():
    pygame.display.set_caption("Menu")
    global dt
    global mouse_angle
    BG = pygame.image.load("Ocean.png")
    BG = pygame.transform.scale(BG, (width*2, height*1.1))
    BG2 = pygame.transform.scale(BG, (width*2, height*1.1))
    x = 0
    x2 = width*2
    while True:
        screen.blit(BG, (x, 0))
        screen.blit(BG, (x2, 0)) #Moves 2 background Images in a way that it looks seamless
        if x < 3*width*-1:
            x = width
        if x2 < 3*width*-1:
            x2 = width
        x -= 30 * dt
        x2 -= 30 * dt
        mouse_pos = pygame.mouse.get_pos()

        menu_text = main_font.render("Freaky Summer", True, "Black")
        menu_rect = menu_text.get_rect(center=(width/2, height/5))
        screen.blit(menu_text, menu_rect)

        play__btn = Button(image=None, pos=(width/2, height/2), 
                            text_input="PLAY", font=main_font, base_color="Black", hovering_color="#5b5b5b")
        quit_btn = Button(image=None, pos=(width/2, height/1.4), 
                            text_input="QUIT", font=main_font, base_color="Black", hovering_color="#5b5b5b")
        
        for button in [play__btn, quit_btn]:
            button.changeColor(mouse_pos)
            button.update(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play__btn.checkForInput(mouse_pos):
                    mainGame()
                if quit_btn.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

#mainGame()
mainMenu()