import pygame as pg
import math as mat
import random as rand
from coding_projects.Python_projects.hardlystarted.grid_game.points import Point
Vec = pg.Vector2

pg.init()
screen_real = pg.display.set_mode((800, 800))
screen_sim = pg.Surface((800 * 2,800 * 2))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0
scale = 1
scale_vel = 0
offset = Vec(0,0)
offset_vel = Vec (0,0)

linelist = []

points = []
for i in range(18):
    for j in range(18):
        points.append(Point(screen_sim, (i * 100, j * 100)))

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                if scale_vel < 0:
                    scale_vel = 0
                scale_vel += 0.4
            if event.button == 5 and scale > 1:
                if scale_vel > 0:
                    scale_vel = 0
                scale_vel -= 0.4

    if 5 >= scale >= 1:    
        scale += scale_vel * dt
        scale_vel /= 5 ** dt
    elif scale > 5:
        scale = 5
        scale_vel = 0
    else:
        scale = 1
        scale_vel = 0

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        offset_vel.y -= 6400 * dt
    if keys[pg.K_s]:
        offset_vel.y += 6400 * dt
    if keys[pg.K_a]:
        offset_vel.x -= 6400 * dt
    if keys[pg.K_d]:
        offset_vel.x += 6400 * dt

    if offset_vel.length() > 12800:
        offset_vel.scale_to_length(12800)
    offset_vel /= 20 ** dt
    offset += offset_vel * dt / scale

    screen_sim.fill((230,230,230))

    for point in points:
        point.draw(scale, offset)

    linelist.append(dt)
    if len(linelist) > 300:
        linelist.pop(0)
    
    

    screen_scaled = pg.transform.smoothscale(screen_sim, (800,800))
    screen_real.blit(screen_scaled, (0,0))
    if len(linelist) > 5:
        avg = int(sum(linelist) * 10000 / len(linelist))
        pg.draw.line(screen_real, (140,140,140), (40, 700), (640, 700))
        pg.draw.line(screen_real, (140, 140, 140), (40, 700 - avg), (640, 700 - avg))
        pg.draw.lines(screen_real, "red", False, [(40 + 2 * i, 700 - int(10000 * linelist[i])) for i in range(len(linelist))])
        

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()
print(scale)