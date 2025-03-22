from pygame import *
from random import randint

window = display.set_mode((700, 500))
display.set_caption("Shooter_game")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
game = True
mixer.init()
space = mixer.Sound('space.ogg')
fire = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height)) 
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()        
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x  < 635:
            self.rect.x += self.speed 
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

player = Player('rocket.png', 100, 400, 50, 101, 10)

lost = 0 
count = 0 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 635)
            self.rect.y = 0
            lost = lost + 1 

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, 635), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()


finish = False

font.init()
font2 = font.SysFont('Arial', 36)
lose = font2.render("YOU LOSE", 1, (255, 255, 255))
win = font2.render("YOU WIN", 1, (255, 255, 255))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -10:
            self.kill()
bullet = Bullet('bullet.png', 250, 500, 10, 30, -10)
score = 0

while game:
    if finish != True:

        window.blit(background, (0, 0))
        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        text_win = font2.render('Счёт:' + str(score), 1, (255, 255,255))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        window.blit(text_lose, (10, 60))
        window.blit(text_win, (10, 30))
        

        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(lose, (300, 250))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for monster in sprites_list:
            score += 1
            monster = Enemy("ufo.png", randint(80, 635), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if score >= 3:  
            finish = True 
            window.blit(win, (300, 250))

        if lost > 10:
            finish = True 
            window.blit(lose, (300, 250))
            
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire.play()

            




    
    display.update()
    clock.tick(FPS)

            
             
             
              