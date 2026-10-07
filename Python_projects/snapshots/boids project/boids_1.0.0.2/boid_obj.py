import pygame as pg
import random as rand
import math as mat


def pol2car(pol):
    return((pol[0] * mat.cos(pol[1]), pol[0] * mat.sin(pol[1])))


class Boid:
    def __init__(self, id, screen):
        self.id = id
        self.pos = pg.Vector2(rand.randint(0, screen.get_width()), rand.randint(0, screen.get_height()))
        self.dir = rand.uniform(-mat.pi, mat.pi)
    
    def move(self, dt, speed, screen):
        self.pos.x += speed * mat.cos(self.dir) * dt
        self.pos.y += speed * mat.sin(self.dir) * dt
        self.dir = (self.dir + mat.pi) % (2*mat.pi) - mat.pi

    def draw(self, screen, colour, size):
        offset = [(size * 10, self.dir), 
                  (size * 10, 0.9 + (0.5*mat.pi) + self.dir), 
                  (size * 5, mat.pi + self.dir),
                  (size * 10, -0.9 - (0.5*mat.pi) + self.dir)]
        points = [self.pos + (pol2car(offset[i])) for i in range(4)]
        pg.draw.polygon(screen, colour, points)
    
    def draw_rad(self, screen, colour, radius, avoid, blindspot):
        pg.draw.circle(screen, colour, self.pos, radius, 1)
        if avoid:
            offset = [(radius, blindspot*mat.pi + self.dir), 
                      (0, 0),
                      (radius, -blindspot*mat.pi + self.dir)]
            points = [self.pos + (pol2car(offset[i])) for i in range(3)]
            pg.draw.lines(screen, colour, False, points, 1)

    def get_closeboids(self, boidlist, radius):
        self.near_boids = []
        for boid in boidlist:
            if not boid.id == self.id:    
                if mat.hypot((boid.pos.x - self.pos.x),(boid.pos.y - self.pos.y)) <= radius:
                    self.near_boids.append(boid)

    def boid_avoid(self, dt, speed, blindspot):
        turn_dir = 0
        for boid in self.near_boids:
            boid_angle = mat.atan2(boid.pos.y - self.pos.y, boid.pos.x - self.pos.x)
            angle_diff = (boid_angle - self.dir + mat.pi) % (2*mat.pi) - mat.pi
            if 0 < angle_diff < blindspot*mat.pi:
                turn_dir -= 1
            elif -blindspot*mat.pi < angle_diff < 0:
                turn_dir += 1
        self.dir += turn_dir * speed * mat.pi * dt

    def wall_avoid(self, screen, dt, speed, radius):
        if not radius < self.pos.x < screen.get_width() - radius or not radius < self.pos.y < screen.get_height() - radius:
            if self.pos.x >= screen.get_width() - radius:
                if self.dir > 0:
                    self.dir += speed * mat.pi * dt
                else:
                    self.dir -= speed * mat.pi * dt
            elif self.pos.x <= radius:
                if self.dir > 0:
                    self.dir -= speed * mat.pi * dt
                else:
                    self.dir += speed * mat.pi * dt
            elif self.pos.y >= screen.get_height() - radius:
                if abs(self.dir) <= 0.5*mat.pi:
                    self.dir -= speed * mat.pi * dt
                else:
                    self.dir += speed * mat.pi * dt
            elif self.pos.y <= radius:
                if abs(self.dir) <= 0.5*mat.pi:
                    self.dir += speed * mat.pi * dt
                else:
                    self.dir -= speed * mat.pi * dt
