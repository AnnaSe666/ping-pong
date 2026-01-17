import pygame
from pygame import *
from random import randint

pygame.init()

# ================= НАСТРОЙКИ ОКНА =================

win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Pong with Levels")
back = (200, 255, 255)

clock = time.Clock()
FPS = 60

# ================= ШРИФТЫ =================

font.init()
main_font = font.Font(None, 35)
small_font = font.Font(None, 28)

lose1 = main_font.render('PLAYER LOSE!', True, (180, 0, 0))
lose2 = main_font.render('COMPUTER LOSE!', True, (0, 150, 0))

# ================= КЛАССЫ =================

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x, y))

    def reset(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

    def update_ai(self, ball, speed_x):
        if speed_x < 0:
            return  # мяч летит от компьютера

        error = randint(-30, 30) #погрешность
        target_y = ball.rect.centery + error #Вместо точного центра мяча компьютер едет к примерной позиции

        if self.rect.centery < target_y:
            self.rect.y += self.speed #Если центр ракетки выше цели → едем вниз
        elif self.rect.centery > target_y:
            self.rect.y -= self.speed

# ================= ОБЪЕКТЫ =================

racket1 = Player('racket.png', 30, 200, 4, 50, 150)
racket2 = Player('racket.png', 520, 200, 3, 50, 150)
ball = GameSprite('ball.png', 275, 225, 4, 50, 50)

# ================= СКОРОСТЬ МЯЧА =================

speed_x = 3
speed_y = 3

# ================= УРОВНИ =================

start_time = time.get_ticks()
level = 1

game = True
finish = False

# ================= ЦИКЛ =================

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)

        # уровни
        current_time = time.get_ticks()
        if current_time - start_time >= 30000 and level == 1:
            racket2.speed += 1
            level = 2

        # управление
        racket1.update_l()
        racket2.update_ai(ball, speed_x)

        # движение мяча
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # столкновения
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1

        if ball.rect.top <= 0 or ball.rect.bottom >= win_height:
            speed_y *= -1

        # проигрыш
        if ball.rect.left < 0:
            finish = True
            window.blit(lose1, (200, 200))

        if ball.rect.right > win_width:
            finish = True
            window.blit(lose2, (180, 200))

        # отрисовка
        racket1.reset()
        racket2.reset()
        ball.reset()

        lvl_text = small_font.render("LEVEL " + str(level), True, (0, 0, 0))
        window.blit(lvl_text, (260, 20))

    display.update()
    clock.tick(FPS)

pygame.quit()
