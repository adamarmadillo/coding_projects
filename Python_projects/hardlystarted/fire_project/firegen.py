import pygame as pg
import math as mat
import random as rand
Vec2 = pg.Vector2

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

font = pg.font.SysFont("Consolas", 15)

class Particle:
    def __init__(self, screen, colour):
        self.screen = screen
        self.colour = colour
        self.pos = Vec2(rand.randint(1,800), rand.randint(1,800))

    def draw(self):
        pg.draw.circle(self.screen, self.colour, self.pos, 10)

particles = []
for i in range(10):
    particles.append(Particle(screen, (200, 150, 100)))

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    screen.fill("black")

    for particle in particles:
        particle.draw()

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()