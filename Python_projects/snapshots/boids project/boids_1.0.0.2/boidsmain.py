import pygame as pg
import random as rand
import math as mat

from boid_obj import Boid

# pygame setup
pg.init()
screen = pg.display.set_mode((800,800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True

# game setup
dt = 0

boid_count = 200
move_speed = 150

avoid_radius = 80
avoid_turnspeed = 0.5
blindspot_size = 0.35

wall_avoid_radius = 20
wall_avoid_turnspeed = 5

assimilate_radius = 100
assimilate_turnspeed = 2

avoid_circle = 0
assimilate_circle = 0
avoid_wall = 0

def truefalse(cond):    
    if cond == 1:
        cond = True
    else:
        cond = False

truefalse(avoid_circle)
truefalse(assimilate_circle)
truefalse(avoid_wall)


# generate boids
boidlist = []
id = 0
for boid in range(boid_count):
    boid = Boid(id, screen)
    boid.pos.xy = (rand.randint(20, screen.get_width() - 20), rand.randint(20, screen.get_height() - 20))
    boidlist.append(boid)
    id += 1

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    # logic

    for boid in boidlist:
        boid.get_closeboids(boidlist, avoid_radius)
        boid.boid_avoid(dt, avoid_turnspeed, blindspot_size)
        boid.wall_avoid(screen, dt, wall_avoid_turnspeed, wall_avoid_radius)
        boid.move(dt, move_speed, screen)
        

    # render

    screen.fill("black")

    for boid in boidlist:
        if avoid_circle:
            boid.draw_rad(screen, "red4", avoid_radius * 0.5, True, blindspot_size)
        if assimilate_circle:
            boid.draw_rad(screen, "blue", assimilate_radius, False)
        boid.draw(screen, "orange", 1)
    
    if avoid_wall:
        pg.draw.rect(screen, "gold", (wall_avoid_radius, wall_avoid_radius, screen.get_width() - 2 * wall_avoid_radius, screen.get_height() - 2 * wall_avoid_radius), 1)
    

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()
