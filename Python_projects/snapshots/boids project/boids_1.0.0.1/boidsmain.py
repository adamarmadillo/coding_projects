import pygame as pg
import random as rand
import math as mat

from boid_obj import Boid

pg.init()
screen = pg.display.set_mode((800,800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True

dt = 0
swapwait = 1
boidlist = []

for boid in range(2000):
    boid = Boid(1, screen)
    boid.pos.xy = (400,400)
    boidlist.append(boid)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    # logic

    # every second change swapdir to 1, 0, -1
    if swapwait >= 1:
        swapwait = 0
        for boid in boidlist:
            boid.dir_delta = (10 * rand.randint(-1, 1)) % mat.pi
    else:
        swapwait += dt

    # change direction by 1 - -1 per sec
    for boid in boidlist:
        boid.dir += boid.dir_delta * dt
        boid.move(dt)

    screen.fill("black")

    for boid in boidlist:
        pg.draw.circle(screen, "blue", boid.pos, 2)

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()
