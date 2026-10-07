import math as mat
import pygame as pg

class Body:
    def __init__(self, name, screen, mass, radius, colour, spawn_pos=(0,0), spawn_vel=(0,0), locked=False):
        self.name = name
        self.screen = screen
        self.mass = mass
        self.radius = radius
        self.colour = colour
        self.pos = pg.Vector2(spawn_pos)
        self.vel = pg.Vector2(spawn_vel)
        self.locked = locked        
        self.screensize = pg.Vector2(screen.get_size())
        self.trail = []
        self.trail_frames = 0

    def calc_acc(self, bodylist, G_const, dt):
        acceleration = pg.Vector2(0,0)
        for body in bodylist:
            if body.name != self.name:
                displacement = body.pos - self.pos
                acceleration += G_const * body.mass / displacement.length_squared() * displacement.normalize()
        self.vel += acceleration * dt
    
    def move(self, dt):
        self.pos += self.vel * dt
    
    def adjusted_pos(self, pos, scale, offset):
        pos_holder = (pos - offset) * scale + self.screensize / 2
        return pg.Vector2(int(pos_holder.x), int(pos_holder.y))

    def draw_body(self, scale, offset):
        pg.draw.circle(
            self.screen, 
            self.colour, 
            self.adjusted_pos(self.pos, scale, offset), 
            int(self.radius * scale)
        )
    
    def update_trail(self, time, resolution):
        if self.trail_frames == resolution:
            self.trail.append(self.pos.copy())
            if len(self.trail) >= 144 * time / resolution:
                self.trail.pop(0)
            self.trail_frames = 1
        else:
            self.trail_frames += 1
        
    def draw_trail(self, scale, offset, colour="white", width=1):
        if len(self.trail) > 1:
            pg.draw.lines(
                self.screen, 
                colour, 
                False, 
                [self.adjusted_pos(i, scale, offset) for i in self.trail], 
                width
            )

    def render_tag(self, gamesize):
        font = pg.font.SysFont("Consolas", 12 * gamesize, bold=True)
        colour_scale_factor = 255 / max(self.colour)
        text_colour = [int(colour_scale_factor * self.colour[i]) for i in range(3)]
        self.tag = font.render((" " + self.name + " "), True, text_colour, "black").convert_alpha()
    
    def print_tag(self, screen, scale, offset, game_size=1):
        text_pos = self.adjusted_pos(self.pos, scale, offset) + (int(1.5 * self.radius * scale) + game_size, int(-6 * game_size))
        text_pos = (int(text_pos.x), int(text_pos.y))
        screen.blit(self.tag, text_pos)

    def all_info(self, bodylist):
        if self.name == "Moon":
            orbit_vel = f"{'{:.3f}'.format((self.vel - bodylist[0].vel).length(), 3)} Km/s (to Earth)"
            orbit_len = f"{'{:.3f}'.format((self.pos - bodylist[0].pos).length() * 1000, 3)} thousand Km"
            disp_mass = f"{'{:.2f}'.format(self.mass * 1e3)} billion billion tonnes"
        elif self.name == "Sun":
            orbit_vel = "n/a"
            orbit_len = "n/a"
            disp_mass = f"{int(self.mass) / 1000} trillion trillion tonnes"
        else:
            orbit_vel = f"{'{:.3f}'.format(self.vel.length(), 3)} Km/s"
            orbit_len = f"{'{:.3f}'.format(self.pos.length(), 3)} million Km"
            disp_mass = f"{'{:.2f}'.format(self.mass * 1e3)} billion billion tonnes"
        return(
            f"""You are currently following: {self.name}
Orbit distance: {orbit_len}
Orbit velocity: {orbit_vel}
Mass: {disp_mass}
Diameter: {int(self.radius * 2e6)} Km

"""
        )
