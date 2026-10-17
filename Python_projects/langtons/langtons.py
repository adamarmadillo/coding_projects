import pygame as pg
import math as mat
import random as rand
Vec2 = pg.Vector2


pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

class Cell:
    def __init__(self, world_size, screen, pos=Vec2):
        self.pos = pos
        self.screen = screen
        side_length = screen.get_height() / world_size
        self.rect = ((pos.x * side_length, (world_size - pos.y - 1) * side_length), (side_length, side_length))
        self.state = 0
        self.cols = [
            "#000000",  # 0 black (background)
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

    def draw(self):
        if self.state != 0:
            pg.draw.rect(screen, self.cols[self.state], self.rect)

class Cell_Grid:
    def __init__(self, world_size, screen):
        self.cells = []
        self.world_size = world_size
        for i in range(world_size):
            temp_cells = []
            for j in range(world_size):
                temp_cells.append(Cell(world_size, screen, Vec2(i, j)))
            self.cells.append(temp_cells)

    def draw_grid(self):
        for i in self.cells:
            for j in i:
                j.draw()

# rules set out like (dir, dir, dir)
# 1 = clockwise, 2 = u-turn, 3 = counter, 0 = still
# length of the rules dictates how many colours
# index of direction dictates which state it activates on
# 
# rulesets set out like (if_state, turn_dir)

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

ruleset = (1,1,3,3,3,1,3,3,3,1,1,1)

grid = Cell_Grid(400, screen)
ant = Ant(grid, ruleset, Vec2(200, 200))

turn_count = 1000

font = pg.font.SysFont("Consolas", 15)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                turn_count += 1
            if event.key == pg.K_f and turn_count > 1:
                turn_count -= 1

    keys = pg.key.get_pressed()

    screen.fill("black")

    for i in range(turn_count):
        ant.step()
    grid.draw_grid()

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()

print(ant.pos)