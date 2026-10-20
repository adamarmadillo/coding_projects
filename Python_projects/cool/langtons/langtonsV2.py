import pygame as pg
import math as mat
import random as rand
Vec2 = pg.Vector2
from slider import Slider

pg.init()
screen = pg.display.set_mode((1200, 600))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

pallet_num = 0
from colours import pallets
colours = pallets[pallet_num]

dirs = ((0,1), (-1,0), (0,-1), (1,0))
surrounding = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

background_fill = "#000000"

rulesets = [
    [[1, 3], 
    "classic"],
    [[0, 0, 2, 1, 3, 2], 
    "japandi"],
    [[2, 0, 1, 2, 2, 3], 
    "trignerd"],
    [[2, 3, 3, 2, 0], 
    "factory fill"],
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 2, 2, 3], 
    "paint line"],
    [[0, 0, 0, 0, 2, 3, 3, 2, 3, 3, 1, 3, 3, 1, 2, 1, 1, 0, 1, 3, 1, 2, 1, 1, 0, 1, 2, 3, 2, 0, 0, 0, 3, 3, 2, 0, 2, 3, 1, 1, 2, 2, 1, 1, 2, 2, 0, 3, 1, 3, 1, 3, 0, 2, 3, 3, 3, 0, 1, 2, 2, 1, 3, 2, 2, 0, 1, 1, 2, 3, 2, 3],
    "paint fill"],
    [[0, 0, 2, 0, 1, 3, 0, 0, 2, 0, 0, 1, 2, 1, 2, 1, 0, 1, 1, 0, 0, 2, 0, 0, 0, 3, 2, 3], 
    "paint pattern"],
    [[1, 0, 3, 2, 3, 2, 3, 2, 0, 1, 2, 1, 0, 0, 0, 1, 2, 1, 2, 0, 2, 1, 3, 0, 0, 0, 3, 3, 1, 2, 2, 2, 1, 1, 0, 2, 2, 0, 2, 0, 0, 1, 0, 3, 3, 1, 2, 0, 3, 1, 3, 1, 2, 1, 0, 1, 1, 1, 0, 2, 0, 2, 1, 1, 2, 1, 2, 3, 1, 3, 1, 1, 1, 3, 1, 1, 2, 2, 1, 3, 3, 1, 0, 2, 2, 1, 0, 1], 
    "triangles"],
    [[2, 3, 2, 3, 0, 1], 
    "rails"],
    [[3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 2, 1] , 
    "rails complex"],
    [[1, 1, 3, 3, 3, 1, 3, 3, 3, 1, 1, 1], 
    "3d triangle"],
    [[1, 2, 0, 0, 1, 3, 2, 2, 1, 3, 3, 3, 3, 3, 0, 0, 3, 3, 1, 1, 1, 0, 0, 3, 3, 3, 0, 2, 3, 0, 3, 1, 3, 2, 3, 0], 
    "diagoneal"],
    [[2, 0, 1, 2, 2, 3, 2, 0, 1, 2, 2, 3, 2, 0, 1, 2, 2, 3, 2, 0, 1, 2, 2, 3, 2, 0, 1, 2, 2, 3, 2, 0, 1, 2, 2, 3],
    "trignerd big"],
    [[2, 3, 2, 3, 0, 1, 2, 3, 2, 3, 0, 1, 2, 3, 2, 3, 0, 1, 2, 3, 2, 3, 0, 1, 2, 3, 2, 3, 0, 1, 2, 3, 2, 3, 0, 1],
    "rails big"],
    [[1, 2, 0, 0, 1, 3, 2, 2, 1, 3, 3, 3, 3, 3, 0, 0, 3, 3, 1, 1, 1, 0, 0, 3, 3, 3, 0, 2, 3, 0, 3, 1, 3, 2, 3, 0, 1, 2, 0, 0, 1, 3, 2, 2, 1, 3, 3, 3, 3, 3, 0, 0, 3, 3, 1, 1, 1, 0, 0, 3, 3, 3, 0, 2, 3, 0, 3, 1, 3, 2, 3, 0, 1, 2, 0, 0, 1, 3, 2, 2, 1, 3, 3, 3, 3, 3, 0, 0, 3, 3, 1, 1, 1, 0, 0, 3, 3, 3, 0, 2, 3, 0, 3, 1, 3, 2, 3, 0], 
    "diagoneal big"],
    [[0, 0, 0, 0, 2, 3, 3, 2, 3, 3, 1, 3, 3, 1, 2, 1, 1, 0, 1, 3, 1, 2, 1, 1, 0, 1, 2, 3, 2, 0, 0, 0, 3, 3, 2, 0, 2, 3, 1, 1, 2, 2, 1, 1, 2, 2, 0, 3, 1, 3, 1, 3, 0, 2, 3, 3, 3, 0, 1, 2, 2, 1, 3, 2, 2, 0, 1, 1, 2, 3, 2, 3, 0, 0, 0, 0, 2, 3, 3, 2, 3, 3, 1, 3, 3, 1, 2, 1, 1, 0, 1, 3, 1, 2, 1, 1, 0, 1, 2, 3, 2, 0, 0, 0, 3, 3, 2, 0, 2, 3, 1, 1, 2, 2, 1, 1, 2, 2, 0, 3, 1, 3, 1, 3, 0, 2, 3, 3, 3, 0, 1, 2, 2, 1, 3, 2, 2, 0, 1, 1, 2, 3, 2, 3, 0, 0, 0, 0, 2, 3, 3, 2, 3, 3, 1, 3, 3, 1, 2, 1, 1, 0, 1, 3, 1, 2, 1, 1, 0, 1, 2, 3, 2, 0, 0, 0, 3, 3, 2, 0, 2, 3, 1, 1, 2, 2, 1, 1, 2, 2, 0, 3, 1, 3, 1, 3, 0, 2, 3, 3, 3, 0, 1, 2, 2, 1, 3, 2, 2, 0, 1, 1, 2, 3, 2, 3], 
    "paint line big"],
    [[2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0, 2, 3, 3, 2, 0], 
    "factory fill big"],
]

def in_bounds(pos, grid_size):
    if pos.x < 0 or pos.x >= grid_size.x:
        return False
    elif pos.y < 0 or pos.y >= grid_size.y:
        return False
    else:
        return True

class Cell:
    def __init__(self, grid_size, pos):
        self.pos = pos
        self.state = 0

        side_length = screen.get_height() / grid_size.y
        if int(screen.get_height()) == int(grid_size.y):
            self.q_rect = False
        else:
            self.q_rect = True
            self.rect = ((int(pos.x * side_length), int((grid_size.y - pos.y - 1) * side_length)), (side_length, side_length))

    def draw(self):
        if self.state == 0:
            return
        col = (self.state % len(colours))
        if self.q_rect == True:
            pg.draw.rect(screen, colours[col], self.rect)
        else:
            screen.set_at((int(self.pos.x), int(self.pos.y)), colours[col])

class Cell_Grid:
    def __init__(self, grid_size):
        self.cells = []
        self.grid_size = grid_size
        for i in range(int(grid_size.x)):
            temp_cells = []
            for j in range(int(grid_size.y)):
                temp_cells.append(Cell(grid_size, Vec2(i, j)))
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
    def __init__(self, grid, ruleset, pos=Vec2(), death_ant=False, death_ant_type="random"):
        self.grid = grid
        self.grid_size = self.grid.grid_size
        self.ruleset = ruleset
        self.cycle_len = len(ruleset)
        if pos == Vec2():
            self.pos = Vec2(self.grid.grid_size.x // 2, self.grid.grid_size.y // 2)
            self.dir = 1
        else:
            self.pos = pos
            self.dir = rand.choice((1,2,3,0))
        self.death_ant = death_ant
        self.death_ant_type = death_ant_type
        self.internal_timer = 0
        self.surrounding_dir = [0,1,2,3]
        self.surrounding_cells = list(surrounding)

    def flip_cell(self):
        self.grid.cells[int(self.pos.x)][int(self.pos.y)].state += 1
        self.grid.cells[int(self.pos.x)][int(self.pos.y)].state %= self.cycle_len

    def wipe_cell(self):
        self.grid.cells[int(self.pos.x)][int(self.pos.y)].state = 0

    def move(self, dir=Vec2()):
        # get next positon (default direction if not forced)
        if dir == Vec2():
            next_pos = self.pos + dirs[self.dir]
        else:
            next_pos = self.pos + dir

        # move to the next position (if not out of bounds)
        if in_bounds(next_pos, self.grid_size):
            self.pos += dirs[self.dir]

    def get_state(self, pos=Vec2()):
        if pos == Vec2():
            state = self.grid.cells[int(self.pos.x)][int(self.pos.y)].state
            state %= self.cycle_len
            return state
        else:
            state = self.grid.cells[int(pos.x)][int(pos.y)].state
            state %= self.cycle_len
            return state            

    def normal_step(self):
        # get cell state
        state = self.get_state()

        # turn according to state
        self.dir = (self.dir + self.ruleset[state]) % 4

        # cycle cell colour
        self.flip_cell()

        # move unless projecting out of bounds
        self.move()

    def death_step(self):
        state = self.get_state()

        if self.death_ant_type == "random":
            # just random direction
            self.dir = rand.choice((0,1,2,3))
            self.wipe_cell()
            self.move()

        elif self.death_ant_type == "follow":
            # follows its ruleset movement unless the cell is empty
            if state == 0:
                self.dir = rand.choice((0,1,2,3))
            else:
                self.dir = (self.dir +self.ruleset[state]) % 4
            self.wipe_cell()
            self.move()

        elif self.death_ant_type == "wipe":
            # random direction and kill 8 surrounding cells
            self.dir = rand.choice((0,1,2,3))
            if state == 0:
                pass
            else:
                for i in surrounding:
                    pos = self.pos + i
                    if in_bounds(pos, self.grid_size):
                        self.grid.cells[int(pos.x)][int(pos.y)].state = 0
            self.wipe_cell()
            self.move()

        elif self.death_ant_type == "streak":
            # specifically targets living cells (orthagonal)
            dir_found = False

            for i in self.surrounding_dir:
                pos = self.pos + dirs[i]
                if in_bounds(pos, self.grid_size):
                    if self.get_state(pos) != 0:
                        self.dir = i
                        dir_found = True
                        break

            self.internal_timer += 1
            if self.internal_timer >= 5000:
                self.internal_timer -= 5000
                rand.shuffle(self.surrounding_dir)
                dir_found = False
                for i in range(3):
                    self.move()

            if dir_found == False:
                self.dir = rand.choice((0,1,2,3))
            self.wipe_cell()
            self.move()

        elif self.death_ant_type == "happy kill":
            if self.internal_timer <= 1000:
                self.internal_timer += 1
            else:
                x1 = int(self.pos.x)
                x2 = rand.randint(0, int(self.grid_size.x - 1))
                y1 = int(self.pos.y)
                y2 = rand.randint(0, int(self.grid_size.y - 1))
                if abs(x1 - x2) < self.grid_size.x / 10 and abs(y1 - y2) < self.grid_size.x / 10:
                    for i in range(int(min(x1, x2)), int(max(x1, x2))):
                        for j in range(int(min(y1, y2)), int(max(y1, y2))):
                            self.grid.cells[i][j].state = 0
                    self.internal_timer -= rand.randint(200, 1000)
            self.dir = rand.choice((0,1,2,3))
            self.move()
            
        elif self.death_ant_type == "wiper":
            # specifically targets living cells (orthagonal)
            dir_found = False
            state = self.get_state()

            for i in self.surrounding_dir:
                pos = self.pos + dirs[i]
                if in_bounds(pos, self.grid_size):
                    target_state = self.get_state(pos)
                    if target_state != 0 and target_state == state:
                        self.dir = i
                        dir_found = True
                        break
            
            if not dir_found:
                for i in self.surrounding_dir:
                    pos = self.pos + dirs[i]
                    if in_bounds(pos, self.grid_size):
                        target_state = self.get_state(pos)
                        if target_state != 0:
                            self.dir = i
                            dir_found = True
                            break

            if not dir_found:
                self.dir = rand.choice((0,1,2,3))

            self.internal_timer += 1
            if self.internal_timer >= 10000:
                self.internal_timer -= 10000
                rand.shuffle(self.surrounding_dir)
                self.dir = rand.choice((0,1,2,3))
                for i in range(3):
                    self.move()

            self.wipe_cell()
            self.move()

        if self.death_ant_type == "ant_agonist":
            # just random direction
            self.dir = rand.choice((0,1,2,3))
            if in_bounds(self.pos, self.grid_size) and self.internal_timer >= 100:
                self.grid.cells[int(self.pos.x)][int(self.pos.y)].state += 1
                self.internal_timer = 0
            else:
                self.internal_timer += 1
            self.move()
            

    def step(self):
        if not self.death_ant:
            self.normal_step()
        else:
            self.death_step()

class Ants:
    def __init__(self, grid, ruleset=rulesets[0][0]):
        self.grid = grid
        self.ants = [Ant(grid, ruleset)]
        self.rand_pos = False

    def gen_ant(self, ruleset, death_ant=False, death_ant_type="random"):
        if self.rand_pos:
            pos = Vec2(rand.randint(0, int(grid.grid_size.x - 1)), rand.randint(0, int(grid.grid_size.y - 1)))
        else:
            pos = Vec2()
        self.ants.append(Ant(self.grid, ruleset, pos, death_ant, death_ant_type))

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

grid_size = Vec2(600, 300)

ruleset = Ruleset(5)
grid = Cell_Grid(grid_size)
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
            elif event.key == pg.K_2:
                ruleset.gen_new(250,250)
                grid.reset_grid()
                ants.reset_ants(ruleset.ruleset)
            elif event.key == pg.K_3:
                ruleset.gen_new(250,250)
                grid.reset_grid()
            elif event.key == pg.K_1:
                if background_fill == "#000000":
                    background_fill = "#04101f"
                else:
                    background_fill = "#000000"

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

            elif event.key == pg.K_j:
                ants.gen_ant(ruleset.ruleset, True, "random")
            elif event.key == pg.K_k:
                ants.gen_ant(ruleset.ruleset, True, "follow")
            elif event.key == pg.K_l:
                ants.gen_ant(ruleset.ruleset, True, "wipe")
            elif event.key == pg.K_n:
                ants.gen_ant(ruleset.ruleset, True, "streak")
            elif event.key == pg.K_m:
                ants.gen_ant(ruleset.ruleset, True, "happy kill")
            elif event.key == pg.K_b:
                ants.gen_ant(ruleset.ruleset, True, "wiper")
            elif event.key == pg.K_h:
                ants.gen_ant(ruleset.ruleset, True, "ant_agonist")

        if event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
            mousePos = pg.mouse.get_pos()
            slider.MouseClick(event, mousePos)

    keys = pg.key.get_pressed()

    screen.fill(background_fill)

    if turn_count >= 1 and not pause:
        for i in range(int(turn_count)):
            ants.run_turn()
        generation += turn_count
    elif pause:
        pass
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