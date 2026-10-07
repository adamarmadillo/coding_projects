import pygame as pg
import math as mat
import random as rand

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

font = pg.font.SysFont("Consolas", 15)


def newpos(pos, scale, offset, screen):
    midscreen = (screen.get_width() / 2, screen.get_height() / 2)
    return(scale * (pos - offset - midscreen) + midscreen)

class Body:
    def __init__(self, id, screen, mass, colour, radius, spawn_location, spawn_velocity=(0,0), locked=False):
        self.id = id
        self.screen = screen
        self.mass = mass
        self.colour = colour
        self.radius = radius
        self.pos = pg.Vector2(spawn_location)
        self.vel = pg.Vector2(spawn_velocity)
        self.locked = locked
        self.trail = []
        self.trail_count = 1

    def gravity(self, body_list, gravity_const, dt):
        acceleration = pg.Vector2(0,0)
        for body in body_list:
            if self.id != body.id:
                if self.pos != body.pos:
                    displacement = body.pos - self.pos
                    acceleration += (gravity_const * body.mass / displacement.length_squared()) * displacement.normalize()
        self.vel += acceleration * dt

    def move(self, dt):
        self.pos += self.vel * dt
    
    def draw_circle(self, scale=1, offset=(0,0)):
        pg.draw.circle(self.screen, self.colour, newpos(self.pos, scale, offset, self.screen), mat.ceil(scale * self.radius))

    def draw_trail(self, colour, time, scale=1, offset=(0,0), trail_res=1, width=1):
        if self.trail_count == trail_res:
            self.trail.append(self.pos.copy())
            if len(self.trail) >= 144 * time / trail_res:
                self.trail.pop(0)
            self.trail_count = 1
        else:
            self.trail_count += 1
        if len(self.trail) > 1:
            newtrail = [newpos(i, scale, offset, self.screen) for i in self.trail]
            pg.draw.lines(self.screen, colour, False, newtrail, mat.ceil(scale * width))


body1 = Body(0, screen, 5.972, "green", 0.00637, (400,549.6), (29.78, 0))
body2 = Body(1, screen, 1.9885e6, "red", 0.696, (400,400), locked=True)
body3 = Body(2, screen, 0.07347, "blue", 0.00174, (400,549.984), (30.80, 0))

bodies = [body1, body2, body3]

g_const = 6.67430e-2

offset = pg.Vector2(0,0)
scale = 1

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                scale *= 4 ** 0.1
            if event.button == 5:
                scale /= 4 ** 0.1

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        offset.y -= 200 / scale * dt
    if keys[pg.K_s]:
        offset.y += 200 / scale * dt    
    if keys[pg.K_a]:
        offset.x -= 200 / scale * dt
    if keys[pg.K_d]:
        offset.x += 200 / scale * dt
    
    if keys[pg.K_r]:
        scale *= 4 ** dt
    if keys[pg.K_f]:
        scale /= 4 ** dt


    screen.fill("black")

    # calculate force, then move
    for body in bodies:
        if not body.locked:
            body.gravity(bodies, g_const, dt)
    for body in bodies:
        if not body.locked:
            body.move(dt)

    if keys[pg.K_SPACE]:
        offset = body1.pos.xy - (400,400)

    # render trails, then circles
    for body in bodies:
        if not body.locked:
            body.draw_trail("white", 5, scale, offset, trail_res=1, width=0.0001)
    for body in bodies:
        body.draw_circle(scale, offset)

    info_text = font.render(f"{round(scale, 1)}, {[round(body.pos.x, 1) for body in bodies]}", True, "white")
    screen.blit(info_text, (20,20))

    pg.display.flip()
    dt = clock.tick(144) / 1000

pg.quit()