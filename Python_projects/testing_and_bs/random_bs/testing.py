import pygame as pg

vec = pg.Vector2(5,5)
vec = pg.Vector2(vec.as_polar())
vec += (0,45)
vec.from_polar(vec)

print(vec)