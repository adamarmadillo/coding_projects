import pygame as pg
import math as mat
import random as rand
Vec = pg.Vector2


pg.init()
screen = pg.display.set_mode((1200, 900))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0
v_screen = pg.Surface((300,225))

class Head:
    def __init__(self, screen, move_speed, rot_speed):
        self.screen = screen
        self.pos = 0.5 * Vec(v_screen.get_size())
        self.vel = Vec(1,0)
        self.move_speed = move_speed
        self.rot_speed = rot_speed

    def draw(self):
        pg.draw.line(self.screen, "red", self.pos, self.pos + self.vel * 15, 1)
        pg.draw.circle(self.screen, "green", self.pos, 6)
        
    def move(self):
        self.pos += self.vel * self.move_speed

    def turn(self, dir):
        new_vel = Vec(self.vel.as_polar())
        if dir == "left":
            new_vel.y -= self.rot_speed
        else:
            new_vel.y += self.rot_speed
        self.vel.from_polar(new_vel)


class Body:
    def __init__(self, screen, size, leader, avoid_radius):
        self.screen = screen
        self.pos = Vec()
        self.size = size
        self.leader = leader
        self.avoid_radius = avoid_radius

    def move(self):
        dis = self.leader.pos - self.pos
        if dis.length() > self.avoid_radius:
            self.pos += dis - (dis.normalize() * self.avoid_radius)
    
    def draw(self):
        pg.draw.circle(self.screen, "green4", self.pos, self.size, 1)
    

head = Head(v_screen, 0.5, 1)

tail = []
for i in range(10):
    if i == 0:
        leader = head
    else:
        leader = tail[i - 1]
    tail.append(Body(v_screen, 6 - 0.5 * i, leader, 7 - 0.25 * i))


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_d]:
        head.turn("right")
    if keys[pg.K_a]:
        head.turn("left")

    head.move()
    for body in tail:
        body.move()

    v_screen.fill("black")


    for body in tail:
        body.draw()
    
    head.draw()

    scaled_screen = pg.transform.scale_by(v_screen, 4)

    screen.blit(scaled_screen, (0,0))

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()