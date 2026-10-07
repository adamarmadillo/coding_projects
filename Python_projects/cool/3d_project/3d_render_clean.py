import pygame as pg
import math as mat
import random as rand
Vec3 = pg.Vector3
Vec2 = pg.Vector2

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

font = pg.font.SysFont("Consolas", 15)


# world pos -> relative pos -> cam yaw pos -> cam pitch pos

# cam yaw = +- pi (looped)
# cam pitch = +- pi/2 (cramped)
# yaw first to avoid causing overall roll

class Point:
    def __init__(self, screen, world_pos=(0,0,0), colour="red"):
        self.world_pos = Vec3(world_pos)
        self.screen = screen
        self.colour = colour

    # move the world around the view
    # [world to relative positon]
    def world_to_rel(self, offset):
        return (self.world_pos - offset)

    # rotate the world around the view
    # [relative to view-relative position]
    def view_pos(self, offset, cam_yaw, cam_pitch):
        # relative position
        rel_pos = self.world_to_rel(offset)
        # adjust to yaw first (pitch is complicated)
        # [rotates x by yaw, rotates z by yaw]
        x1 = rel_pos.x * mat.cos(cam_yaw) - rel_pos.z * mat.sin(cam_yaw)
        z1 = rel_pos.x * mat.sin(cam_yaw) + rel_pos.z * mat.cos(cam_yaw)
        y1 = rel_pos.y

        # adjust to pitch on the new yaw-relative x axis (rotates on an aparallel line)
        ry = y1 * mat.cos(cam_pitch) - z1 * mat.sin(cam_pitch)
        rz = y1 * mat.sin(cam_pitch) + z1 * mat.cos(cam_pitch)

        # x does not have to be changed because it is not affect
        return Vec3(x1, ry, rz)

    def screen_pos(self, offset=Vec3(), cam_yaw=0, cam_pitch=0):
        rpos = self.view_pos(offset, cam_yaw, cam_pitch)
        if rpos.z > 0:
            screen_pos = (Vec2(rpos.x / rpos.z, -1 * rpos.y / rpos.z) + (1, 1)) * self.screen.get_height() / 2
        #if self.world_pos.z - offset.z != 0:
        #    screen_pos = Vec2(self.world_pos.xy) + offset.xy
        #    screen_pos /= self.world_pos.z + offset.z
        #    screen_pos += (1, 1)
        #    screen_pos /= 2
        #    screen_pos *= self.screen.get_height()
            return screen_pos
        else:
            return "na"

    def draw(self, screen, offset, cam_yaw, cam_pitch):
        if self.screen_pos(offset, cam_yaw, cam_pitch) != "na":
            pg.draw.circle(screen, self.colour, self.screen_pos(offset, cam_yaw, cam_pitch), 1)

point_list = (
    ((-0.5, 0.5, 1.5), "white"),
    ((0.5, 0.5, 1.5), "white"),
    ((0.5, -0.5, 1.5), "white"),
    ((-0.5, -0.5, 1.5), "white"),

    ((-0.5, 0.5, 0.5), "white"),
    ((0.5, 0.5, 0.5), "white"),
    ((0.5, -0.5, 0.5), "white"),
    ((-0.5, -0.5, 0.5), "white")
)

def connect(screen, point_set, offset, yaw, pitch):
    for i in range(len(point_set)):
        pa = point_set[i]
        pa_pos = pa.screen_pos(offset, yaw, pitch)
        if pa_pos == "na":
            continue
        if i == len(point_set) - 1:
            pb = point_set[0]
        else:
            pb = point_set[i + 1]
        pb_pos = pb.screen_pos(offset, yaw, pitch)
        if pb_pos == "na":
            continue
        pg.draw.line(screen, "red", pa_pos, pb_pos)


        #if p.screen_pos(offset, yaw, pitch) != "na":
        #    pg.draw.lines(screen, "red", True, [i.screen_pos(offset, yaw, pitch) for i in point_set], 1)

offset = Vec3(0,0,0)
cam_yaw = 0
cam_pitch = 0

points = [Point(screen, i[0], i[1]) for i in point_list]

point_sets = (
    (
        points[0],
        points[1],
        points[2],
        points[3]
    ),
    (
        points[4],
        points[5],
        points[6],
        points[7]
    ),
    (
        points[0],
        points[4]
    ),
    (
        points[1],
        points[5]
    ),
    (
        points[2],
        points[6]
    ),
    (
        points[3],
        points[7]
    )
)

def rand_pos_in_bounds(bounds):
    pos = [rand.random() * (bounds[1][i] - bounds[0][i]) + bounds[0][i] for i in range(3)]
    return pos

def star_gen(num, bounds=((-1,-1,-1),(1,1,1)), colour=False):
    stars = []
    colours = ["white", "lightpink", "lightsalmon", "lightyellow", "lightsteelblue", 
               "thistle", "bisque", "lavender", "mintcream", "azure", "linen", "oldlace"]
    for i in range(num):
        if colour == False:
            col = rand.choice(colours)
        else:
            col = colour
        pos = Vec3(rand_pos_in_bounds(bounds))
        stars.append(Point(screen, pos, col))
    return stars

stars = []

green_point = Point(screen, Vec3(0, 0, 1), "green")

velocity = Vec3(0,0,0)
use_velocity = True

bound_on = True
middle_point_on = True
debug_on = True

def increment(offset, velocity, use_velocity, input):
    if use_velocity == True:
        velocity += input
    else:
        offset += input
    return offset, velocity

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_v:
                use_velocity = not use_velocity
            elif event.key == pg.K_c:
                if len(stars) == 0:
                    stars = star_gen(2000, ((-0.5, -0.5, 0.5), (0.5, 0.5, 1.5)))
                else:
                    stars = []
            elif event.key == pg.K_x:
                bound_on = not bound_on
            elif event.key == pg.K_z:
                middle_point_on = not middle_point_on
            elif event.key == pg.K_b:
                debug_on = not debug_on
            
            
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        offset.xz, velocity.xz = increment(
            offset.xz, 
            velocity.xz, 
            use_velocity, 
            Vec2(mat.sin(cam_yaw), mat.cos(cam_yaw)) * dt * slow_input
        )
    if keys[pg.K_s]:
        offset.xz, velocity.xz = increment(
            offset.xz, 
            velocity.xz, 
            use_velocity, 
            -1 * Vec2(mat.sin(cam_yaw), mat.cos(cam_yaw)) * dt * slow_input
        )

    if keys[pg.K_d]:
        offset.xz, velocity.xz = increment(
            offset.xz, 
            velocity.xz, 
            use_velocity, 
            Vec2(mat.cos(cam_yaw), mat.sin(cam_yaw) * -1) * dt * slow_input
        )
    if keys[pg.K_a]:
        offset.xz, velocity.xz = increment(
            offset.xz, 
            velocity.xz, 
            use_velocity, 
            -1 * Vec2(mat.cos(cam_yaw), mat.sin(cam_yaw) * -1) * dt * slow_input
        )

    if keys[pg.K_r]:
        offset.y, velocity.y = increment(
            offset.y, 
            velocity.y, 
            use_velocity, 
            dt * slow_input
        )
    if keys[pg.K_f]:
        offset.y, velocity.y = increment(
            offset.y,
            velocity.y,
            use_velocity,
            -1 * dt * slow_input
        )

    if use_velocity:
        offset += velocity * 10 * dt
        velocity *= 1 - 4 * dt

    if keys[pg.K_DOWN]:
        if cam_pitch <= -1 * mat.pi / 2:
            cam_pitch = -1 * mat.pi / 2
        else:
            cam_pitch -= dt * mat.sqrt(slow_input)
    if keys[pg.K_UP]:
        if cam_pitch >= mat.pi / 2:
            cam_pitch = mat.pi / 2
        else:
            cam_pitch += dt * mat.sqrt(slow_input)

    if keys[pg.K_RIGHT]:
        cam_yaw += dt * mat.sqrt(slow_input)
        if cam_yaw > mat.pi:
            cam_yaw -= 2 * mat.pi
    if keys[pg.K_LEFT]:
        cam_yaw -= dt * mat.sqrt(slow_input)
        if cam_yaw < -1 * mat.pi:
            cam_yaw += 2 * mat.pi

    if keys[pg.K_SPACE]:
        slow_input = 0.1
    else:
        slow_input = 1

    screen.fill("black")

    if bound_on:
        for s in point_sets:
            connect(screen, s, offset, cam_yaw, cam_pitch)

    for p in points:
        p.draw(screen, offset, cam_yaw, cam_pitch)

    for s in stars:
        s.draw(screen, offset, cam_yaw, cam_pitch)

    if middle_point_on:
        green_point.draw(screen, offset, cam_yaw, cam_pitch)

    if debug_on:
        pg.draw.circle(screen, "red", (750, 50), 20, 1)
        pg.draw.line(screen, "red", (750, 50), (750 + 20 * mat.sin(cam_yaw), 50 - 20 * mat.cos(cam_yaw)))

        pg.draw.arc(screen, "red", ((730, 100), (40, 40)), mat.pi / 2, mat.pi / -2, 1)
        pg.draw.line(screen, "red", (750, 100), (750, 140))
        pg.draw.line(screen, "red", (750, 120), (750 - 20 * mat.cos(cam_pitch), 120 - 20 * mat.sin(cam_pitch)))

        line = 0
        debug_info = [
            f"X: {round(offset.x, 3)}",
            f"Y: {round(offset.y, 3)}",
            f"Z: {round(offset.z, 3)}",
            f"",
            f"Yaw: {round(cam_yaw * 180 / mat.pi, 1)}",
            f"Pitch: {round(cam_pitch * 180 / mat.pi, 1)}"
            ]

        for i in range(6):
            text = font.render(debug_info[i], True, "red")
            screen.blit(text, (10, 15 * (i + 1)))

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()