from pygame import *

BLUE=(220,220,220)
window = display.set_mode((400,500))
window.fill(BLUE)
display.set_caption('Maze Game')

class GameSprite(sprite.Sprite):
    def __init__ (self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

wall1 = GameSprite('wall.png', 350, 60, -40, 80)
wall2 = GameSprite('wall.png', 350, 60, 150, 220)
wall3 = GameSprite('wall.png', 350, 60, -40, 360)
flag = GameSprite('finish.png', 50, 50, 10, 435)

walls = sprite.Group()
walls.add(wall1)
walls.add(wall2)
walls.add(wall3)

balls = sprite.Group()
ghosts = sprite.Group()

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, speed_x, speed_y):
        super().__init__(picture, w, h, x, y)
        self.x_speed = speed_x
        self.y_speed = speed_y
        self.face_right = self.image
        self.face_left = transform.flip(self.image,True,False)
        self.dir = 1

    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            self.image = self.face_right
            self.dir = 1
            for p in platforms_touched:
                self.rect.right = min(self.rect.right,p.rect.left)
        elif self.x_speed < 0:
            self.dir = -1
            self.image = self.face_left
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,p.rect.right)

        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top,p.rect.bottom)
        elif self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom,p.rect.top)

    def fire(self):
        ball = Bullet('volleyball.png', 30, 30, self.rect.centerx-15, self.rect.centery-15, self.dir*15)
        balls.add(ball)
            
pacman = Player('pacman.png', 65, 70, 5, 5, 0, 0)

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed

    def update(self):
        if self.rect.x <= 5:
            self.direction = 'kanan'
        elif self.rect.x > 340:
            self.direction = 'kiri'

        if self.direction == 'kiri':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

ghost = Enemy('enemy.png', 50, 60, 5, 290, 20)
ghosts.add(ghost)

class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 390:
            self.kill()

end_layer = transform.scale(image.load('endlayer.png'),(400,500))
font.init()
font = font.SysFont('arial',40)
win = font.render('Anda Menang!', True, (0,0,0))
lose = font.render('Anda Kalah!', True, (0,0,0))

run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                pacman.x_speed -= 5
            elif e.key == K_RIGHT:
                pacman.x_speed += 5
            elif e.key == K_DOWN:
                pacman.y_speed += 5
            elif e.key == K_UP:
                pacman.y_speed -= 5
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                pacman.x_speed = 0
            elif e.key == K_RIGHT:
                pacman.x_speed = 0
            elif e.key == K_DOWN:
                pacman.y_speed = 0
            elif e.key == K_UP:
                pacman.y_speed = 0
            elif e.key == K_SPACE:
                pacman.fire()

    if finish != True:
        window.fill(BLUE)
        walls.update()
        walls.draw(window)
        flag.reset()
        pacman.update()
        pacman.reset()
        ghosts.update()
        ghosts.draw(window)
        balls.update()
        balls.draw(window)

        sprite.groupcollide(balls, ghosts, True, True)
        sprite.groupcollide(balls, walls, True, False)

        if sprite.collide_rect(pacman,flag):
            finish = True
            window.blit(end_layer,(0,0))
            window.blit(win,(100,200))

        if sprite.spritecollide(pacman, ghosts, False):
            finish = True
            window.blit(end_layer,(0,0))
            window.blit(lose,(100,200))

    display.update()