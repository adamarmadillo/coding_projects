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

def rotate(coord=pg.Vector2(), angle=0):
    x = (coord.x * mat.cos(angle)) - (coord.y * mat.sin(angle))
    y = (coord.x * mat.sin(angle)) + (coord.y * mat.cos(angle))
    return pg.Vector2(x, y)

class glitter:
    def __init__(self, preset, radius):
        self.shape = preset[0]
        self.behaviour = preset[1]
        if self.behaviour == 0:
            self.radius = preset[2]
        if self.behaviour == 1:
            self.radius = radius
        self.angle = preset[3]
        if self.behaviour == 1:
            self.colour = [240, 240, 0]
        else:
            self.colour = preset[4] 
        if self.behaviour == 1:
            col_dif = int((12 - self.radius) * 20)
            self.colour = [int(self.colour[i] - col_dif) for i in range(3)]
            for i in range(3):
                self.colour[i] = max(self.colour[i], 0)
        self.fill_colour = [int(self.colour[i] * 0.8) for i in (0, 1, 2)]
        self.pos = pg.Vector2(preset[5]) - (self.radius, self.radius)
        self.speedmult = preset[6]
        self.rotatemult = preset[7]
        self.vx = rand.uniform(8, 20)
        self.vx_target = rand.uniform(20,30)
        self.vy = 15
        self.vx_peaked = True
        self.vx_dir = rand.choice((-1, 1))
        self.vy = 0
        self.timer_target = rand.uniform(0.8, 1.4)
        self.droptimer = 0
        if rand.random() < 0.04:
            self.dropstate = True
        else:
            self.dropstate = False


    def move(self, dt):
        if self.behaviour == 0:
            self.pos.y += dt * self.speedmult * 50
            self.angle += self.rotatemult * dt
            #self.speedmult += (rand.random() - 0.5) * 0.5
            #self.speedmult = max(self.speedmult, 0)
            if self.angle > 2 * mat.pi:
                self.angle -= 2 * mat.pi
            if self.angle < 0:
                self.angle += 2 * mat.pi
        if self.behaviour == 1:
            if self.dropstate:
                if self.droptimer < 0.5 * self.timer_target:
                    self.vx += 50 * dt * self.vx_dir
                    self.vy += 250 * dt
                    self.droptimer += dt
                elif 0.5 * self.timer_target < self.droptimer < self.timer_target:
                    self.vx += 50 * dt * self.vx_dir
                    self.vy -= 250 * dt
                    self.droptimer += dt
                else:
                    self.dropstate = False
                    self.droptimer = 0
                    self.timer_target = rand.uniform(0.8, 1.4)

            else:
                if self.vx_peaked == False:
                    self.vx += self.vx_dir * 50 * dt
                    self.vy = 20 + self.vx_target * 0.5 - 10 * (self.vx_target - self.vx * self.vx_dir) / self.vx_target
                else:
                    self.vx -= self.vx_dir * 50 * dt
                    self.vy = 10 + self.vx_target * 0.5 - 15 * (self.vx_target - self.vx * self.vx_dir) / self.vx_target
                if abs(self.vx) >= self.vx_target:
                    self.vx_peaked = True
                if self.vx * self.vx_dir <= 0:
                        self.vx_dir = rand.choice((-1, 1))
                        self.vx_target = rand.uniform(20, 70)
                        self.vx = 0
                        self.vx_peaked = False
                        if rand.random() < 0.1:
                            self.dropstate = True
            self.pos += (self.vx * dt * self.radius * 0.1, self.vy * dt * self.radius * 0.1)
            angle_target = mat.atan2(self.vx, self.vy)
            if (self.angle - angle_target) % (mat.pi * 2) - mat.pi <= 0:
                self.angle -= 10 * dt / (self.radius / 8)
            else:
                self.angle += 10 * dt / (self.radius / 8)


    def draw(self, screen):
        if self.shape == 0:
            shape_coords = [
                pg.Vector2(1, 1),
                pg.Vector2(1, -1),
                pg.Vector2(-1, -1),
                pg.Vector2(-1, 1)
            ]
        if self.shape == 1:
            shape_coords = [
                pg.Vector2(0, 1),
                pg.Vector2(-0.86, -0.5),
                pg.Vector2(0.86, -0.5)
            ]
        for i in range(len(shape_coords)):
            p = shape_coords[i] * self.radius
            x = (p.x * mat.cos(self.angle)) - (p.y * mat.sin(self.angle))
            y = (p.x * mat.sin(self.angle)) + (p.y * mat.cos(self.angle))
            p = (x, y)
            p += self.pos
            shape_coords[i] = p
        if self.dropstate:
            colour = "red"
        else:
            colour = self.colour
        pg.draw.polygon(screen, self.colour, shape_coords, 0)
        pg.draw.polygon(screen, self.fill_colour, shape_coords, 2)

def g_preset(i, x):
    return (
    1, 
    0,
    rand.randint(5, 12),
    rand.uniform(0, mat.pi * 2),
    rand.choice((
        (255, 0, 0), 
        (0, 255, 0), 
        (255, 255, 0), 
        (192, 60, 255),
        (0, 255, 255),
        #(255, 255, 255),
        (64, 64, 255),
        (255, 128, 0)
        )), 
    [rand.randint(50, 750), x], 
    rand.uniform(1.5, 2.5),
    rand.uniform(0.5, 2) * rand.choice((1, -1))
)

rects = []
for i in range(100):
    rects.append(glitter(g_preset(i, rand.randint(0, 800)), 4 + (8 * i / 100)))

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
    keys = pg.key.get_pressed()

    screen.fill((255, 254, 245))

    for i in rects:
        if i.pos.y - i.radius > 800:
            radius = i.radius
            p = rects.index(i)
            rects[p] = glitter(g_preset(i, 0), radius)
        i.move(dt)
        i.draw(screen)

    text = font.render(f"{dt}", True, "red2")
    screen.blit(text, (20, 20))

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()

for i in rects:
    print(int(i.pos.y / 10))