import pygame as pg
import math as mat
import random as rand
Vec2 = pg.Vector2

pg.init()
screen = pg.display.set_mode((800, 400))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

font = pg.font.SysFont("Consolas", 15)

amount_done = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        amount_done += dt   
    if keys[pg.K_s]:
        amount_done -= dt
    if keys[pg.K_e]:
        amount_done += 10 * dt   
    if keys[pg.K_d]:
        amount_done -= 10 * dt
    if keys[pg.K_r]:
        amount_done += 100 * dt
    if keys[pg.K_f]:
        amount_done -= 100 * dt

    screen.fill("black")

    fract_done = int(400 * amount_done / 1008)

    pg.draw.rect(screen, (100,100,100), ((200, 175), (400, 50)))
    pg.draw.rect(screen, (100,255,100), ((200, 175), (fract_done, 50)))

    info = f"{int(amount_done)}"
    text = font.render(info, True, "white")
    screen.blit(text, (100,100))

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()