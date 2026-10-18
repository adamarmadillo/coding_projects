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

pallet_num = 0
from colours import pallets
colours = pallets[pallet_num]

dirs = ((0,1), (-1,0), (0,-1), (1,0))

rulesets = [
    [[1, 3], "classic"],             #MS classic
    [[2, 1, 3, 2, 0, 2], "windows"], #S  windows
    [[0, 0, 2, 1, 3, 2], "japandi"], #M  japandi
    [[1, 1, 1, 1, 3, 3], "city roads"], #M  city roads
    [[2, 0, 1, 2, 2, 3], "trignerd"],    #M  trignerd        4
    [[2, 3, 3, 2, 0], "factory fill"],   #MS factory fill
    [[3, 2, 3], "ants?"],          #M? ants?
    [[3,2,3,3,2,3,3,2,3,3,2,1], "pretty cool"], # pretty cool
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,2,2,3], "painter"], #S painter
    [[0, 0, 0, 0, 2, 3, 3, 2, 3, 3, 1, 3, 3, 1, 2, 1, 1, 0, 1, 3, 1, 2, 1, 1, 0, 1, 2, 3, 2, 0, 0, 0, 3, 3, 2, 0, 2, 3, 1, 1, 2, 2, 1, 1, 2, 2, 0, 3, 1, 3, 1, 3, 0, 2, 3, 3, 3, 0, 1, 2, 2, 1, 3, 2, 2, 0, 1, 1, 2, 3, 2, 3],
    "maximal"],#MS maximal
    [[2, 2, 3, 3, 2, 3, 0, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 0, 0, 2, 1, 0, 3, 1, 2, 0, 3, 2, 1, 2, 0, 3, 2, 1, 1, 0, 1, 0, 1, 2, 2, 2, 1, 2, 2, 0, 3, 1, 2, 0, 3, 0, 1, 3, 3, 1, 0, 2, 3, 0],
    "wallpaper"],#MS wallpaper
    [[1, 0, 3, 2, 3, 2, 3, 2, 0, 1, 2, 1, 0, 0, 0, 1, 2, 1, 2, 0, 2, 1, 3, 0, 0, 0, 3, 3, 1, 2, 2, 2, 1, 1, 0, 2, 2, 0, 2, 0, 0, 1, 0, 3, 3, 1, 2, 0, 3, 1, 3, 1, 2, 1, 0, 1, 1, 1, 0, 2, 0, 2, 1, 1, 2, 1, 2, 3, 1, 3, 1, 1, 1, 3, 1, 1, 2, 2, 1, 3, 3, 1, 0, 2, 2, 1, 0, 1],
    "triangles"],#M triangles
    [[2, 3, 2, 3, 0, 1], "rails"],
   [[0, 0, 2, 0, 1, 3, 0, 0, 2, 0, 0, 1, 2, 1, 2, 1, 0, 1, 1, 0, 0, 2, 0, 0, 0, 3, 2, 3], "mechanic"],
]

class Cell:
    def __init__(self, grid_size, colour_limit, pos):
        self.pos = pos
        self.state = 0
        self.colour_limit = colour_limit

        side_length = screen.get_height() / grid_size
        if side_length == 1:
            self.q_rect = False
        else:
            self.q_rect = True
            self.rect = ((int(pos.x * side_length), int((grid_size - pos.y - 1) * side_length)), (side_length, side_length))

    def draw(self):
        if self.state == 0:
            return
        col = (self.state % self.colour_limit - 1)
        col %= len(colours)
        if self.q_rect == True:
            pg.draw.rect(screen, colours[col], self.rect)
        else:
            screen.set_at(self.rect[0], colours[col])


class Cell_Grid:
    def __init__(self, grid_size, colour_limit):
        self.cells = []
        self.grid_size = grid_size
        for i in range(grid_size):
            temp_cells = []
            for j in range(grid_size):
                temp_cells.append(Cell(grid_size, colour_limit, Vec2(i, j)))
            self.cells.append(temp_cells)

    def draw_grid(self):
        for i in self.cells:
            for j in i:
                j.draw()

    def reset_grid(self):
        for i in grid.cells:
            for j in i:
                j.state = 0

class Ant:
    def __init__(self, grid, ruleset, pos=Vec2()):
        self.grid = grid
        self.grid_size = self.grid.grid_size
        self.ruleset = ruleset
        self.cycle_len = len(ruleset)
        if pos == Vec2():
            self.pos = Vec2(self.grid.grid_size // 2)
            self.dir = 1
        else:
            self.pos = pos
            self.dir = rand.choice((1,2,3,0))

    def flip_cell(self):
        self.grid.cells[int(self.pos.x)][int(self.pos.y)].state += 1
        self.grid.cells[int(self.pos.x)][int(self.pos.y)].state %= self.cycle_len

    def step(self):
        # get cell state
        state = self.grid.cells[int(self.pos.x)][int(self.pos.y)].state
        state %= self.cycle_len

        # turn according to state
        self.dir = (self.dir + self.ruleset[state]) % 4

        # cycle cell colour
        self.flip_cell()

        # move unless projecting out of bounds
        next_pos = self.pos + dirs[self.dir]
        if next_pos.x >= 0 and next_pos.x < self.grid_size and next_pos.y >= 0 and next_pos.y < self.grid_size:
            self.pos += dirs[self.dir]

class Ants:
    def __init__(self, grid, ruleset=rulesets[0][0]):
        self.grid = grid
        self.ants = [Ant(grid, ruleset)]
        self.rand_pos = False

    def gen_ant(self, ruleset):
        if self.rand_pos:
            pos = Vec2(rand.randint(0, grid.grid_size - 1), rand.randint(0, grid.grid_size - 1))
        else:
            pos = Vec2()
        self.ants.append(Ant(self.grid, ruleset, pos))

    def reset_ants(self, ruleset):
        self.ants = []
        self.gen_ant(ruleset)

    def run_turn(self):
        for i in ants.ants:
            i.step()

    def update_ants_ruleset(self, ruleset):
        for i in self.ants:
            i.ruleset = ruleset
            i.cycle_len = len(i.ruleset)

class Ruleset:
    def __init__(self, rule_n=0):
        self.rule_n = rule_n
        self.ruleset = rulesets[rule_n][0]
        self.ruleset_name = rulesets[rule_n][1]

    def gen_new(self, max_size, min_size=1):
        self.ruleset = []
        n_rules = rand.randint(min_size, max_size)
        for i in range(n_rules):
            self.ruleset.append(rand.choice((0,1,2,3)))
        self.ruleset_name = "random"

    def cycle_defaults(self):
        self.rule_n += 1
        self.rule_n %= len(rulesets)
        self.ruleset = rulesets[self.rule_n][0]
        self.ruleset_name = rulesets[self.rule_n][1]

grid_size = 400
colour_limit = 19

ruleset = Ruleset(4)
grid = Cell_Grid(grid_size, colour_limit)
ants = Ants(grid, ruleset.ruleset)

slider = Slider((20, 20), 10, 65, "grey", 20, "white", 15)

pause = False
top_info_shown = True
bottom_info_shown = True
turn_count = 1
generation = 0
timer = 0

font = pg.font.SysFont("Consolas", 15)
font2 = pg.font.SysFont("Consolas", 10)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:

            # space = print ruleset
            if event.key == pg.K_SPACE:
                print(ruleset.ruleset)

            # x = toggle pause
            elif event.key == pg.K_x:
                pause = not pause
            
            # r = reset all
            elif event.key == pg.K_r:
                grid.reset_grid()
                ants.reset_ants(ruleset.ruleset)
                generation = 0
            
            # f = reset grid, ant remains    
            elif event.key == pg.K_f:
                grid.reset_grid()
            
            # v = reset ants    
            elif event.key == pg.K_v:
                ants.reset_ants(ruleset.ruleset)
            
            # w = reset all and generate random ruleset
            elif event.key == pg.K_w:
                ruleset.gen_new(100,6)
                grid.reset_grid()
                ants.reset_ants(ruleset.ruleset)

            elif event.key == pg.K_t:
                ants.gen_ant(ruleset.ruleset)
            elif event.key == pg.K_g:
                ants.rand_pos = not ants.rand_pos
            elif event.key == pg.K_e:
                ruleset.gen_new(100,6)
            elif event.key == pg.K_c:
                ants.update_ants_ruleset(ruleset.ruleset)
            elif event.key == pg.K_d:
                ruleset.cycle_defaults()

            elif event.key == pg.K_q:
                top_info_shown = not top_info_shown
            elif event.key == pg.K_a:
                bottom_info_shown = not bottom_info_shown
            elif event.key == pg.K_z:
                pallet_num += 1
                pallet_num %= len(pallets)
                colours = pallets[pallet_num]

        if event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
            mousePos = pg.mouse.get_pos()
            slider.MouseClick(event, mousePos)

    keys = pg.key.get_pressed()

    screen.fill("black")

    if turn_count >= 1 and not pause:
        for i in range(int(turn_count)):
            ants.run_turn()
        generation += turn_count
    elif pause:
        continue
    else:
        timer += turn_count
        if timer >= 1:
            timer -= 1
            ants.run_turn()
            generation += 1

    turn_count = mat.pow(10, ((slider.Value() / 10) - 1.5))

    grid.draw_grid()

    if top_info_shown:
        slider.draw(screen)
        slider.operate(pg.mouse)
        text = font.render(f"Turns/frame: {round(turn_count, 3)}", True, "white", "black")
        screen.blit(text, (20, 40))
        text = font.render(f"Turn: {int(generation)}", True, "white", "black")
        screen.blit(text, (20, 58))
        text = font.render(f"T/s: {int(turn_count / dt) if dt != 0 else turn_count}", True, "white", "black")
        screen.blit(text, (20, 76))
        text = font.render(f'"{ruleset.ruleset_name}"', True, "white", "black")
        screen.blit(text, (20, 94))
    if bottom_info_shown:
        text = font2.render(f'space: print ruleset, x: pause, r: reset all, f: reset world, v: reset ants, w: reset random', True, "white", "black")
        screen.blit(text, (10, 742))
        text = font2.render(f't: add ant, e: new random ruleset, d: cycle default rulesets, c: update ants to ruleset, g: toggle random ant spawn', True, "white", "black")
        screen.blit(text, (10, 762))
        text = font2.render(f'q: hide top info, a: hide bottom info, z: change colour pallet', True, "white", "black")
        screen.blit(text, (10, 780))
    
    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()

print(ruleset.ruleset)