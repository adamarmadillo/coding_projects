import pygame as pg
import math as mat
import random as rand
Vec2 = pg.Vector2
from slider import Slider

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0



class Cell:
    def __init__(self, world_size, screen, colour_limit, pos=Vec2):
        self.pos = pos
        self.screen = screen
        side_length = screen.get_height() / world_size
        if side_length == 1:
            self.q_rect = False
        else:
            self.q_rect = True
        self.rect = ((int(pos.x * side_length), int((world_size - pos.y - 1) * side_length)), (side_length, side_length))
        self.state = 0
        self.cols = [
            "#FFFFFF",  # 1 white
            "#E6194B",  # 2 red
            "#4363D8",  # 3 blue
            "#FFE119",  # 4 yellow
            "#3CB44B",  # 5 green
            "#F58231",  # 6 orange
            "#911EB4",  # 7 purple
            "#46F0F0",  # 8 cyan
            "#F032E6",  # 9 magenta
            "#BCF60C",  # 10 lime
            "#9A6324",  # 11 brown
            "#008080",  # 12 teal
            "#800000",  # 13 maroon
            "#000075",  # 14 navy
            "#AAFFC3",  # 15 mint
            "#808000",  # 16 olive
            "#FFD8B1",  # 17 apricot
            "#FABEBE",  # 18 pink
            "#808080",  # 19 grey
        ]
        self.colour_limit = colour_limit

    def draw(self):
        if self.state != 0:
            if self.q_rect == True:
                pg.draw.rect(self.screen, self.cols[self.state % self.colour_limit], self.rect)
            else:
                self.screen.set_at(self.rect[0], self.cols[self.state % self.colour_limit])


class Cell_Grid:
    def __init__(self, world_size, colour_limit, screen):
        self.cells = []
        self.world_size = world_size
        for i in range(world_size):
            temp_cells = []
            for j in range(world_size):
                temp_cells.append(Cell(world_size, screen, colour_limit, Vec2(i, j)))
            self.cells.append(temp_cells)

    def draw_grid(self):
        for i in self.cells:
            for j in i:
                j.draw()

class Ant:
    def __init__(self, grid, rules, pos = Vec2()):
        self.pos = pos
        self.dir = 1
        self.dirs = ((0,1), (-1,0), (0,-1), (1,0))
        self.grid = grid
        self.world_size = grid.world_size
        self.rules = rules
        self.step_num = 0
        self.cycle_len = len(rules)

    def flip_cell(self):
        self.grid.cells[int(self.pos.x)][int(self.pos.y)].state += 1
        self.grid.cells[int(self.pos.x)][int(self.pos.y)].state %= self.cycle_len

    def step(self):
        state = self.grid.cells[int(self.pos.x)][int(self.pos.y)].state
        self.dir = (self.dir + self.rules[state]) % 4
        self.flip_cell()
        next_pos = self.pos + self.dirs[self.dir]
        if next_pos.x >= 0 and next_pos.x < self.world_size and next_pos.y >= 0 and next_pos.y < self.world_size:
            self.pos += self.dirs[self.dir]

def new_ruleset(mode=0, rulesets=[], set=0):
    ruleset = []
    if mode == 0:
        r = 6
    elif mode == 1:
        r = rand.randint(50, 100)
    if mode == 0 or mode == 1:
        for i in range(r):
            ruleset.append(rand.choice((0,1,2,3)))
    if mode == 2:
        ruleset = cool_rulesets[ruleset_n]
    return ruleset

def new_grid_ants(grid_size, colour_limit):
    grid = Cell_Grid(grid_size, colour_limit, screen)
    ants = [Ant(grid, ruleset, Vec2(grid_size // 2, grid_size // 2))]
    return grid, ants

def check_ant_collision(ants):
    for ant1 in ants:
        for ant2 in ants:
            if ant1.pos == ant2.pos:
                ants.pop(ant1)

def run_turn():
    for ant in ants:
        ant.step()

cool_rulesets = [
    [1, 3],             #MS classic
    [2, 1, 3, 2, 0, 2], #S  windows
    [0, 0, 2, 1, 3, 2], #M  japandi
    [1, 1, 1, 1, 3, 3], #M  city roads
    [2, 0, 1, 2, 2, 3], #M  trignerd        4
    [2, 3, 3, 2, 0],    #MS factory fill
    [3, 2, 3],          #M? ants?
    [3,2,3,3,2,3,3,2,3,3,2,1], # pretty cool
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,2,2,3], #S painter
    [0, 0, 0, 0, 2, 3, 3, 2, 3, 3, 1, 3, 3, 1, 2, 1, 1, 0, 1, 3, 1, 2, 1, 1, 0, 1, 2, 3, 2, 0, 0, 0, 3, 3, 2, 0, 2, 3, 1, 1, 2, 2, 1, 1, 2, 2, 0, 3, 1, 3, 1, 3, 0, 2, 3, 3, 3, 0, 1, 2, 2, 1, 3, 2, 2, 0, 1, 1, 2, 3, 2, 3],
    #MS maximal
    [2, 2, 3, 3, 2, 3, 0, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 0, 0, 2, 1, 0, 3, 1, 2, 0, 3, 2, 1, 2, 0, 3, 2, 1, 1, 0, 1, 0, 1, 2, 2, 2, 1, 2, 2, 0, 3, 1, 2, 0, 3, 0, 1, 3, 3, 1, 0, 2, 3, 0],
    #MS wallpaper
    [1, 0, 3, 2, 3, 2, 3, 2, 0, 1, 2, 1, 0, 0, 0, 1, 2, 1, 2, 0, 2, 1, 3, 0, 0, 0, 3, 3, 1, 2, 2, 2, 1, 1, 0, 2, 2, 0, 2, 0, 0, 1, 0, 3, 3, 1, 2, 0, 3, 1, 3, 1, 2, 1, 0, 1, 1, 1, 0, 2, 0, 2, 1, 1, 2, 1, 2, 3, 1, 3, 1, 1, 1, 3, 1, 1, 2, 2, 1, 3, 3, 1, 0, 2, 2, 1, 0, 1],
    #M triangles
]
ruleset_n = 9
reset_mode = 2

grid_size = 400
colour_limit = 8

ruleset = new_ruleset(reset_mode, cool_rulesets, ruleset_n)
grid, ants = new_grid_ants(grid_size, colour_limit)

slider = Slider((20, 20), 10, 65, "grey", 20, "white", 15)

turn_count = 1
generation = 0
timer = 0

font = pg.font.SysFont("Consolas", 15)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                ruleset = new_ruleset(reset_mode, cool_rulesets, ruleset_n)
                grid, ants = new_grid_ants(grid_size, colour_limit)
                generation = 0
            elif event.key == pg.K_e:
                grid, ants = new_grid_ants(grid_size, colour_limit)
                generation = 0
            elif event.key == pg.K_f:
                print(f"\n\n\nEPIC RULES: {ruleset}\n\n\n")
            elif event.key == pg.K_t:
                ants.append(Ant(grid, ruleset, Vec2(grid_size/2, grid_size/2)))
        if event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
            mousePos = pg.mouse.get_pos()
            slider.MouseClick(event, mousePos)

    keys = pg.key.get_pressed()

    screen.fill("black")

    if turn_count >= 1:
        for i in range(int(turn_count)):
            run_turn()
        generation += turn_count
    else:
        timer += turn_count
        if timer >= 1:
            timer -= 1
            run_turn()
            generation += 1

    turn_count = mat.pow(10, ((slider.Value() / 10) - 1.5))
    
    grid.draw_grid()

    slider.draw(screen)
    slider.operate(pg.mouse)

    text = font.render(f"Turns/frame: {round(turn_count, 3)}", True, "white", "black")
    screen.blit(text, (20, 40))
    text = font.render(f"Turn: {int(generation)}", True, "white", "black")
    screen.blit(text, (20, 58))
    text = font.render(f"T/s: {int(turn_count / dt) if dt != 0 else turn_count}", True, "white", "black")
    screen.blit(text, (20, 76))

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()

print(ruleset)