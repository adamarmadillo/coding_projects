import pygame as pg
import math as mat
import random as rand
Vec = pg.Vector2

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

class Ball:
    def __init__(self, pos, screen):
        self.pos = Vec(pos)
        self.vel = Vec(200,0)
        self.rad = 10
        self.col = "red"
        self.screen = screen
    
    def draw(self):
        pg.draw.circle(self.screen, self.col, self.pos, self.rad)

    def bounce(self):
        if self.pos.x < 100 + self.rad:
            self.pos.x = 100 + self.rad
            self.vel.x *= -0.9
        elif self.pos.x > 700 - self.rad:
            self.pos.x = 700 - self.rad
            self.vel.x *= -0.9
        if self.pos.y < 100 + self.rad:
            self.pos.y = 100 + self.rad
            self.vel.y *= -0.9       
        elif self.pos.y > 700 - self.rad:
            self.pos.y = 700 - self.rad
            self.vel.y *= -0.9

    def move(self, dt):
        self.pos += self.vel * dt / 1000

    def gravitate(self, dt):
        self.vel.y += dt
    
    def free_move(self, dt):
        self.move(dt)
        self.gravitate(dt)
        self.bounce()

ball = Ball((400,400), screen)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    ball.free_move(dt)


    screen.fill("gray50")
    pg.draw.rect(screen, "gray90", ((100,100), (600,600)))

    ball.draw()

    pg.display.flip()

    dt = clock.tick(144)

pg.quit()