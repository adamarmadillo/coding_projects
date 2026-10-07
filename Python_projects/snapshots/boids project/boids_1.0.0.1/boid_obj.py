import pygame as pg
import random as rand
import math as mat

class Boid:
    def __init__(self, id, screen):
        self.id = id
        self.pos = pg.Vector2(rand.randint(0, screen.get_width()), rand.randint(0, screen.get_height()))
        self.speed = 1
        self.dir = rand.uniform(-1 * mat.pi, mat.pi)
        self.dir_delta = 0
    
    def move(self, dt):
        self.pos.x += 100 * mat.cos(self.dir) * dt
        self.pos.y += 100 * mat.sin(self.dir) * dt