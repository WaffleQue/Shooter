#Создай собственный Шутер!

import pygame
from random import *
from time import *


def set_vol():
    global vol
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        vol += 0.01
    if keys[pygame.K_DOWN]:
        vol -= 0.01
    pygame.mixer.music.set_volume(vol)
    fire.set_volume(vol)
    alien1.set_volume(vol)
    alien2.set_volume(vol)
    hit.set_volume(vol)
    snap.set_volume(vol)
    clang.set_volume(vol)
    crunch.set_volume(vol)
    boing.set_volume(vol)
    


vol = 0.05
pygame.init()
pygame.mixer.music.load('Sounds/space.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(vol)
fire = pygame.mixer.Sound('Sounds/fire.ogg')
snap = pygame.mixer.Sound('Sounds/Snap.wav')
hit = pygame.mixer.Sound('Sounds/TennisHit.wav')
alien1 = pygame.mixer.Sound('Sounds/AlienCreak1.wav')
alien2 = pygame.mixer.Sound('Sounds/AlienCreak2.wav')
clang = pygame.mixer.Sound('Sounds/Clang.wav')
crunch = pygame.mixer.Sound('Sounds/Crunch.wav')
boing = pygame.mixer.Sound('Sounds/LowBoing.wav')
aliens = [alien1, alien2]
hits = [clang, crunch]



win_size = (700, 500)
window = pygame.display.set_mode(win_size)
pygame.display.set_caption("Shooter")

pygame.font.init()
Font1 = pygame.font.SysFont('Arial', 35)
Font2 = pygame.font.SysFont('Arial', 50)
score_var = 0
missed_var = 0
health_var = 10
score = Font1.render('Score: '+str(score_var), True, (255, 255, 255))
missed = Font1.render('Missed: '+str(missed_var), True, (255, 255, 255))
health1 = Font1.render('Health: '+str(health_var), True, (255, 255, 255))
Lose = Font2.render('You Lost!', True, (255, 0, 0))
Win = Font2.render('You Won!', True, (0, 255, 0))
reloading = Font2.render('Reloading', True, (255, 255, 255))
ammo = 20
r_time = 150
is_reaload = False


class GameSprite(pygame.sprite.Sprite):
   #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed, w , h):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = pygame.transform.scale(pygame.image.load(player_image), (w, h))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = w
        self.height = h

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            bullets.remove(self)



class Hero(GameSprite):
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if self.rect.x <= 0:
            self.rect.x = 640
        if self.rect.x >= 650:
            self.rect.x = 0
    def fire(self):
        fire.play()
        bullet = Bullet('bullet.png', self.rect.x + self.width/2 - 10, self.rect.y, 5, 20, 40)
        bullets.append(bullet)
        
        
class Enemy(GameSprite):
    def move(self):
        global missed_var
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(0, win_size[0]-80)
            self.rect.y = -70
            self.speed = randint(1, 4)
            boing.play()
            missed_var += 1

class Asteroid(GameSprite):
    health = 3
    xspeed = randint(-1, 1)
    def move(self):
        self.rect.x += self.xspeed
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(0, win_size[0]-80)
            self.rect.y = -70
            self.speed = randint(1, 4)
            self.xspeed = randint(-1, 1)
            self.health = 3

class Animate_Object(GameSprite):
    images = ['Animations/1.png', 'Animations/2.png', 'Animations/3.png',
    'Animations/4.png', 'Animations/5.png', 'Animations/6.png',
    'Animations/7.png', 'Animations/8.png']
    images2 = ['Animations2/1.png', 'Animations2/2.png',
     'Animations2/3.png', 'Animations2/4.png', 'Animations2/5.png', 'Animations2/6.png',
     'Animations2/7.png', 'Animations2/8.png', 'Animations2/9.png', 'Animations2/10.png',
     'Animations2/11.png', 'Animations2/12.png', 'Animations2/13.png', 'Animations2/14.png',
     'Animations2/15.png', 'Animations2/16.png']
    current_image = 0
    def animate(self):
        self.current_image += 1
        self.image = pygame.transform.scale(pygame.image.load(self.images[self.current_image // 5]), (self.width, self.height))
        if self.current_image >= 5*len(self.images)-1:
           animate_objects.remove(self)

class Animate_Object2(GameSprite):
    images = [f"Animations2/{i}.png" for i in range(1,17)]
    current_image = 0
    def animate(self):
        self.current_image += 1
        self.image = pygame.transform.scale(pygame.image.load(self.images[self.current_image // 5]), (self.width, self.height))
        if self.current_image >= 5*len(self.images)-1:
           animate_objects.remove(self)








background = GameSprite('galaxy.jpg', 0, 0, 0, 700, 500)
hero = Hero('rocket.png', 350-35, 420, 5, 70, 80)
enemies = []
bullets = []
animate_objects = []
asteroids = []
for i in range(5):
    enemy1 = Enemy('ufo.png', randint(0, win_size[0]-80), -70, randint(1, 4), 80, 70)
    enemies.append(enemy1)

for i in range(3):
    asteroid1 = Asteroid('asteroid.png', randint(0, win_size[0]-80), -70, randint(1, 4), 50, 50)
    asteroids.append(asteroid1)
game = True
finish = False
clock = pygame.time.Clock()
vol = 0


set_vol()



while game:
    
    


    #KEYS
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if ammo > 0:
                    hero.fire()
                    ammo -= 1
                else:
                    is_reaload = True
            if e.key == pygame.K_r:
                health_var = 10
                missed_var = 0
                score_var = 0
                ammo = 20
                r_time = 150
                bullets = []
                enemies = []
                asteroids = []
                for i in range(5):
                    enemy1 = Enemy('ufo.png', randint(0, win_size[0]-80), -70, randint(1, 4), 80, 70)
                    enemies.append(enemy1)
                for i in range(3):
                    asteroid1 = Asteroid('asteroid.png', randint(0, win_size[0]-80), -70, randint(1, 4), 50, 50)
                    asteroids.append(asteroid1)
                hero = Hero('rocket.png', 350-35, 420, 5, 70, 80)
                animate_objects = []
                finish = False




    if not finish:
        if is_reaload == True:
            r_time-= 1
            hit.play()
            if r_time == 0:
                r_time = 150
                ammo = 20
                is_reaload = False

        background.reset(window)
        hero.reset(window)
        hero.move()
        

    
        #ENEMIES
        for enemy in enemies:
            enemy.reset(window)
            enemy.move()
            missed = Font1.render('Missed: ' +str(missed_var), True, (255, 255, 255))
            if enemy.rect.colliderect(hero.rect):
                clang.play()
                health_var -= 1
                health1 = Font1.render('Health: ' +str(health_var), True, (255, 255, 255))
                enemy.rect.x = randint(0, win_size[0]-80)
                enemy.rect.y = -70
                enemy.speed = randint(1, 5)
                if health_var <= 0:
                    bullets = []
                    enemies = []
                    asteroids = []
                    finish = True
                    window.blit(Lose, (200, 200))
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    r2 = randint(0, 1)
                    aliens[r2].play()
                    a = Animate_Object('Animations/1.png', enemy.rect.x, enemy.rect.y, 0, 80, 80) if randint(1, 2) == 1 else Animate_Object2('Animations2/1.png', enemy.rect.x, enemy.rect.y, 0, 80, 80)
                    animate_objects.append(a)
                    enemy.rect.y = -70
                    enemy.rect.x = randint(0, win_size[0]-80)
                    enemy.speed = randint(1, 5)
                    bullets.remove(bullet)
                    score_var += 1
                    score = Font1.render('Score: ' +str(score_var), True, (255, 255, 255))



        for obj in animate_objects:
            obj.animate()
            obj.reset(window)

        #ASTEROIDS
        for asteroid in asteroids:
            asteroid.reset(window)
            asteroid.move()
            if asteroid.rect.colliderect(hero.rect):
                clang.play()
                health_var -= 1
                health1 = Font1.render('Health: ' +str(health_var), True, (255, 255, 255))
                asteroid.rect.x = randint(0, win_size[0]-80)
                asteroid.rect.y = -70
                asteroid.speed = randint(1, 4)
                asteroid.xspeed = randint(-1, 1)
                asteroid.health = 3
                if health_var <= 0:
                    bullets = []
                    enemies = []
                    asteroids = []
                    finish = True
                    window.blit(Lose, (200, 200))
            for bullet in bullets:
                if asteroid.rect.colliderect(bullet.rect):
                    asteroid.health -= 1
                    if asteroid.health <= 0:
                        a = Animate_Object('Animations/1.png', asteroid.rect.x, asteroid.rect.y, 0, 80, 80) if randint(1,2) == 1 else Animate_Object2('Animations2/1.png', asteroid.rect.x, asteroid.rect.y, 0, 80, 80)
                        asteroid.rect.y = -70
                        asteroid.rect.x = randint(0, win_size[0]-80)
                        asteroid.speed = randint(1, 4)
                        asteroid.xspeed = randint(-1 ,1)
                        asteroid.health = 3
                        crunch.play()
                        animate_objects.append(a)
                    else:
                        crunch.play()
                        try:
                            bullets.remove(bullet)
                        except:
                            pass
        #BULLETS    
        for bullet in bullets:
            bullet.move()
            bullet.reset(window)
            bullet.move()
        #EVERYTHING ELSE
        
        
        
        set_vol()
        if is_reaload:
            reloading = Font2.render('Reloading ' +str(r_time), True, (255, 255, 255))
            window.blit(reloading, (200, 200))
        window.blit(score, (0, 0))
        window.blit(missed, (0, 40))
        window.blit(health1, (0, 80))
        if score_var >= 50:
            bullets = []
            enemies = []
            asteroids = []
            window.blit(Win, (200, 200))
            finish = True
        if missed_var >= 50:
            bullets = []
            enemies = []
            asteroids = []
            window.blit(Lose, (200, 200))
            finish = True

    pygame.display.update()
    clock.tick(60)






