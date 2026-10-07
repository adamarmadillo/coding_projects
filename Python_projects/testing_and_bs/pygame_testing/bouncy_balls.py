import pygame as pg
import math
import random
Vec2 = pg.Vector2

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0
dt_his = []

font = pg.font.SysFont("Consolas", 15)

# just border x and y RADIUS from center
border = Vec2(350, 350)

def random_pos(border=Vec2(400,400), radius=0):
    return Vec2(
        (random.random() * border.x - radius) * random.choice((1, -1)),
        (random.random() * border.y - radius) * random.choice((1, -1))
    )

def random_vel(max_vel):
    return Vec2(
        random.random() * max_vel * random.choice((1, -1)),
        random.random() * max_vel * random.choice((1, -1))
    )

class Ball():
    def __init__(self, pos=(0,0), vel=(0,0), radius=5, colour = "white"):
        # world pos is 0,0 at center screen
        self.pos = Vec2(pos)
        self.vel = Vec2(vel)
        self.radius = radius
        self.colour = colour

    def move(self, dt, border=Vec2(400,400)):
        # if touching x border reverse x velocity
        x_overlap = abs(self.pos.x) + self.radius - border.x
        if x_overlap >= 0:
            self.vel.x *= -1
            self.pos.x -= math.copysign(x_overlap, self.pos.x)
        # if touching y border reverse y velocity
        y_overlap = abs(self.pos.y) + self.radius - border.y
        if y_overlap >= 0:
            self.vel.y *= -1
            self.pos.y -= math.copysign(y_overlap, self.pos.y)
        self.pos += self.vel * dt

    def collide(self, ball_list):
        for i in ball_list[ball_list.index(self) + 1:]:
            # diff in position and distance between them
            diff = i.pos - self.pos
            distance = diff.magnitude()
            if distance == 0:
                continue
            # check if colliding
            if  distance <= self.radius + i.radius:

                # normal vector is the opposite to the tangent, and is perpendicular
                # normal vector = (-vy, vx) OR (vy, -vx)
                # normalISED vector is just a vector scaled to a [signed] magnitude of 1
                # also called a unit vector or direction

                # normalised normal vector
                # normalised diff, which points in the normal
                n = diff / distance

                # dot product of a vector with a unit vector gives a scalar representing the
                # amount that v goes in the direction of u
                # this is called the scalar projection of v onto u
                # multiplying it by u (or u by it) gives the actual vector along u
                # this is called the vector projection of v onto u
                # adding the vector projection of v onto u, and v onto the normal of u, will give the original vector

                # here we are using it to extract and flip the normal (perpendicular) velocity
                # elastic collisions of equal mass result in swapping their normal velocities

                # calculating dot then projection of v onto n for both balls
                self_n_dot = self.vel.x * n.x + self.vel.y * n.y
                self_n_vel = self_n_dot * n
                i_n_dot = i.vel.x * n.x + i.vel.y * n.y
                i_n_vel = i_n_dot * n

                self_t_vel = self.vel - self_n_vel
                i_t_vel = i.vel - i_n_vel

                # swapping their normal velocities
                self.vel = (((self.radius * self.radius - i.radius * i.radius ) * self_n_vel + 2 * i.radius * i.radius * i_n_vel) / (i.radius * i.radius + self.radius * self.radius)) + self_t_vel
                i.vel = (((i.radius * i.radius - self.radius * self.radius) * i_n_vel + 2 * self.radius * self.radius * self_n_vel) / (i.radius * i.radius + self.radius * self.radius)) + i_t_vel

    def draw(self, screen):
        screen_pos = self.pos + Vec2(screen.get_size()) / 2
        screen_pos = (int(screen_pos.x), int(screen_pos.y))
        pg.draw.circle(screen, self.colour, screen_pos, self.radius)

    def clipping(self, i):
        if i == self:
            return False
        diff = i.pos - self.pos
        distance = diff.magnitude()
        if distance <= i.radius + self.radius:
            return True
        else:
            return False

    def unclip(self, ball_list, border=(0,0), find_spawn=False):
        check_for_clip = True
        while check_for_clip:
            check_for_clip = False
            for i in ball_list:
                if not self.clipping(i):
                    continue
                if find_spawn:
                    self.pos = random_pos(border, self.radius)
                    check_for_clip = True
                else:
                    diff = i.pos - self.pos
                    unclip_adjust = (i.radius + self.radius - diff.magnitude()) * diff.normalize() * 0.5
                    self.pos -= unclip_adjust
                    i.pos += unclip_adjust

radius = 3
ball_list = []
for i in range(200):
    ball_list.append(Ball(
        pos=random_pos(border, radius),
        vel=random_vel(300),
        radius=radius
    ))
    ball_list[i].unclip(ball_list, border, True)

avg_pos_history = []
avg_vel_history = []

counter = 0
skip = 2

pop_counter = 0

def cycle(list, item, length=50):
    list.insert(0, item)
    if len(list) > length:
        list.pop()

def trace(list, colour):
    if len(list) >= 2:
        pg.draw.lines(screen, colour, False, list)
    
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_f]:
        pop_counter += dt * len(ball_list) / 4
        if pop_counter >= 1:
            ball_list.append(Ball(
                pos=random_pos(border, radius),
                vel=random_vel(300),
                radius=radius
            ))
            pop_counter = 0
    if keys[pg.K_r]:
        pop_counter += dt * len(ball_list) / 2
        if pop_counter >= 1 and len(ball_list) > 1:
            ball_list.pop()
            pop_counter = 0
    if keys[pg.K_e]:
        for i in ball_list:
            i.radius *= 1 + dt
    if keys[pg.K_d]:
        for i in ball_list:
            i.radius /= 1 + dt
    if keys[pg.K_t]:
        for i in ball_list:
            i.vel *= 1 + dt
    if keys[pg.K_g]:
        for i in ball_list:
            i.vel /= 1 + dt


    screen.fill("black")
    pg.draw.rect(screen, "red", (Vec2(400,400) - border, border * 2), width = 1)

    for i in ball_list:
        i.move(dt, border)
        i.collide(ball_list)
        i.unclip(ball_list, border)
        i.draw(screen)

    total_pos = Vec2()
    total_vel = Vec2()
    avg_pos = Vec2()
    avg_vel = Vec2()
    for i in ball_list:
        total_pos += i.pos
        total_vel += i.vel
    avg_pos = total_pos / len(ball_list) + (400, 400)
    avg_vel = total_vel / len(ball_list) + (400, 400)

    counter += 1
    if counter == skip:
        cycle(avg_pos_history, avg_pos, 2000)
        cycle(avg_vel_history, avg_vel, 2000)
        counter = 0
    trace(avg_pos_history, "red")
    trace(avg_vel_history, "green")

    text = font.render(f"balls: {len(ball_list)}   dt:{dt}", True, "red")
    screen.blit(text, (20, 20))

    dt_his.insert(1, dt)
    if len(dt_his) > 50:
        dt_his.pop()
        temp_list = []
        for i in range(2, 49):
            temp_list.append((i * 3 + 200, 40 - dt_his[i] * 1000))
        pg.draw.lines(screen, "red", False, temp_list)

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()