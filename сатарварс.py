#Создай собственный Шутер!
from random import randint
from pygame import *
score = 0
win_height = 500
win_width = 700
lost = 0
max_lost = 3 
goal = 10
img_bullet = "пуля.png"
img_enemy = "ситх.png"
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE:(', True, (180, 0, 0))
font2 = font.Font(None, 36)  


class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d]  and self.rect.x  < win_width - 80:
            self.rect.x += self.speed   
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20,20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.x += self.speed
        global lost
        if self.rect.x > win_width:
            self.rect.y = randint(win_height-100, win_height-50)
            self.rect.x = 0 
            lost = lost + 1 


class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x <0:
            self.kill


window = display.set_mode((700,500))
display.set_caption('STAR_WARS')


background = transform.scale(image.load('а.jpg'),(700, 500))
'''
mixer.init()
mixer.music.load("atmosfera-kosmicheskogo-prostrnstra.ogg")
fire_sound = mixer.Sound("vzryiv-s-ognennyim-plamenem.ogg")
mixer.music.load("atmosfera-kosmicheskogo-prostrnstra.ogg")
mixer.music.play()
'''
player = Player('щит.png', 450,400 , 100,75, 4)
monsters = sprite.Group()
for i in range (1, 6):
    monster = Enemy("ситх.png", randint(80, win_width - 80), -40, 75,75,randint(1, 5))
    monsters.add(monster)




game = True
finish = False
clock = time.Clock()
FPS = 60


bullets = sprite.Group()
while game: 
    
    for e in event.get():
        if e.type == QUIT:

            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                player.fire()
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        player.reset()
        monsters.update()
        bullets.draw(window)
        bullets.update()
        monsters.draw(window)
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
        score = score + 1
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40 , 65,65,   randint(1, 5))
        monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200, 200))
    if score >= goal:
        finish = True
        window.blit(win, (200, 200))
        text = font2.render("Счёт: " + str(score), 1 , (255, 255, 255))
        window.blit(text, (10,20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose,(10, 50))
    display.update()
    clock.tick(FPS)
