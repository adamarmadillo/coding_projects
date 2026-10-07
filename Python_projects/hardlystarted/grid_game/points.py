import pygame as pg
import math as mat
Vec = pg.Vector2

class Point:
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = Vec(pos)
        self.screen_dim = Vec(screen.get_size())

    def adjusted_pos(self, scale, offset):
        pos = self.pos - offset
        pos = Vec(pos.x % 1600, pos.y % 1600)
        return scale * (pos - self.screen_dim / 2) + self.screen_dim / 2

    def draw(self, scale, offset):
        pg.draw.circle(self.screen, (150,150,150), self.adjusted_pos(scale, offset), 4 * scale)