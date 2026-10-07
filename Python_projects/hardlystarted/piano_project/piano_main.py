import pygame as pg
import numpy as np
import random

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

pg.mixer.init(frequency=44100, size=-16, channels=1)

def make_tone(freq, duration= )

font = pg.font.SysFont("Consolas", 15)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()




    screen.fill("black")

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()