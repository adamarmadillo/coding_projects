import pygame as pg
import math as mat
import random as rand
Vec3 = pg.Vector3
Vec2 = pg.Vector2

arg = 1

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

    # returns a polar coordinate relative to viewer (yaw, pitch, magnitude)
    # 0 yaw = facing +z
    # 0 pitch = flat on xy axis
    def polar_pos(self, offset):
        relative_pos = self.world_pos - offset
        yaw = mat.atan2(relative_pos.x, relative_pos.z)
        xz_mag = relative_pos.xz.magnitude()
        pitch = mat.atan2(relative_pos.y, xz_mag)
        xyz_mag = mat.sqrt(xz_mag ** 2 + relative_pos.y ** 2)
        return (yaw, pitch, xyz_mag)

    # returns rectangular coords of point relative to cameras yaw/pitch (rotates the world around camera)
    def cam_relative_pos(self, offset, cam_yaw, cam_pitch):
        polar_pos = self.polar_pos(offset)
        ryaw = polar_pos[0] - cam_yaw

        opitch = polar_pos[1]
        xyz_mag = polar_pos[2]
        xz_mag = mat.cos(opitch) * xyz_mag
        ny = mat.sin(opitch) * xyz_mag
        nz = mat.cos(ryaw) * xz_mag
        rx = mat.sin(ryaw) * xz_mag

        ry = ny * mat.cos(cam_pitch) - nz * mat.sin(cam_pitch)
        rz = ny * mat.sin(cam_pitch) + nz * mat.cos(cam_pitch)



        #rpitch = polar_pos[1] - cam_pitch
        #xyz_mag = polar_pos[2]
        #xz_mag = mat.cos(rpitch) * xyz_mag
        #ry = mat.sin(rpitch) * xyz_mag
        #rz = mat.cos(ryaw) * xz_mag
        #rx = mat.sin(ryaw) * xz_mag
        return Vec3(rx, ry, rz)

    def screen_pos(self, offset=Vec3(), cam_yaw=0, cam_pitch=0):
        rpos = self.cam_relative_pos(offset, cam_yaw, cam_pitch)
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

bounding = True
middle_point = True

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
                bounding = not bounding
            elif event.key == pg.K_z:
                middle_point = not middle_point
            
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

    if bounding:
        for s in point_sets:
            connect(screen, s, offset, cam_yaw, cam_pitch)

    for p in points:
        p.draw(screen, offset, cam_yaw, cam_pitch)

    for s in stars:
        s.draw(screen, offset, cam_yaw, cam_pitch)

    if middle_point:
        green_point.draw(screen, offset, cam_yaw, cam_pitch)

    pg.draw.circle(screen, "red", (750, 50), 20, 1)
    pg.draw.line(screen, "red", (750, 50), (750 + 20 * mat.sin(cam_yaw), 50 - 20 * mat.cos(cam_yaw)))

    pg.draw.arc(screen, "red", ((730, 100), (40, 40)), mat.pi / 2, mat.pi / -2, 1)
    pg.draw.line(screen, "red", (750, 100), (750, 140))
    pg.draw.line(screen, "red", (750, 120), (750 - 20 * mat.cos(cam_pitch), 120 - 20 * mat.sin(cam_pitch)))

    line = 0
    coords = [
        f"X: {round(offset.x, 3)}",
        f"Y: {round(offset.y, 3)}",
        f"Z: {round(offset.z, 3)}",
        f"",
        f"Yaw: {round(cam_yaw * 180 / mat.pi, 1)}",
        f"Pitch: {round(cam_pitch * 180 / mat.pi, 1)}"
        ]
    for i in range(6):
        text = font.render(coords[i], True, "red")
        screen.blit(text, (10, 15 * (i + 1)))

    pg.display.flip()

    dt = clock.tick(144) / 1000

    #db_world_pos = points[9].world_pos
    #db_polar_pos = points[9].polar_pos(Vec3(offset))
    #db_cam_rel_pos = points[9].cam_relative_pos(Vec3(offset), cam_yaw, cam_pitch)
    #db_screen_pos = points[9].screen_pos(Vec3(offset), cam_yaw, cam_pitch)
    #db_rel_pos = points[9].world_pos - Vec3(offset)

pg.quit()

#def simple(x, n):
#    return [round(x[i], n) for i in range(len(x))]
#
#print(f"""
#
#World Pos: {db_world_pos}
#Offset: {simple(offset, 1)}
#
#Relative pos: {simple(db_rel_pos, 3)}
#Polar pos: {simple(db_polar_pos, 3)}
#
#Yaw: {round(cam_yaw, 3)}
#Pitch: {round(cam_pitch, 3)}
#
#Cam relative pos: {simple(db_cam_rel_pos, 3)}
#
#Screen pos: {simple(db_screen_pos, 1)}""")