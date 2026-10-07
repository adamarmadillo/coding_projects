import pygame as pg
import math as mat
import random as rand
#fah
# wait no its not accurate
pi = 3.14159

Vec2 = pg.Vector2

# all init here: pg, disp, clock, font
pg.init()

screen = pg.display.set_mode((900, 600))
pg.display.set_caption("boids no way")

clock = pg.time.Clock()
running = True
dt = 0

font = pg.font.SysFont("Consolas", 14)


class Boid:
    def __init__(self, id, colour="white", pos=Vec2(300,300), dir=0, size=10, width=0):
        self.id = id
        self.colour = colour
        self.pos = Vec2(pos)
        self.dir = dir
        self.size = size
        # shape vector angles
        self.polar_shape = [0, 2.3, 3.14, 3.9]
        self.width = width

    def rot(self, va, dt):
        self.dir += 2 * pi * va * dt
        # snap into 2 pi range
        if self.dir >= 2 * pi:
            self.dir -= 2 * pi
        elif self.dir < 0:
            self.dir += 2 * pi

    # self.dir stores angle, apply to polar coords, translate to vector
    # no questions why I did it this way
    # there has to be an easier way to just store local shape coordinates and rotate them with a single func
    def draw(self, screen):
        # first write direction onto new list
        mod_polar_shape = []
        for i in self.polar_shape:
            r = i + self.dir
            if r >= 2 * pi:
                r -= 2 * pi 
            elif r < 0:
                r += 2 * pi
            mod_polar_shape.append(r)

        # calc coords from modded shape
        shape_coord_matrix = []
        for i in range(4):
            # var to scale dent in back
            d_scale = 1
            if i == 2:
                d_scale = 0.5
            x = mat.cos(mod_polar_shape[i]) * d_scale * self.size
            y = mat.sin(mod_polar_shape[i]) * d_scale * self.size
            shape_coord_matrix.append(Vec2(x, y))

        # translate + draw
        for i in shape_coord_matrix:
            i += self.pos
        pg.draw.polygon(screen, self.colour, shape_coord_matrix, self.width)
        
boid_a = Boid(0, "green", (450, 300), 0)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break

    keys = pg.key.get_pressed()

    screen.fill("black")

    if keys[pg.K_r]:
        boid_a.rot(dt)
        pg.draw.rect(screen, "white", ((200, 200), (50, 50)))

    boid_a.rot(0.5, dt)
    boid_a.draw(screen)

    d_text = font.render(f"Error NA", True, "white")
    screen.blit(d_text, (10, 10))

    pg.display.flip()
    dt = clock.tick(144) / 1000
pg.quit()