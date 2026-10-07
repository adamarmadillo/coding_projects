import pygame as pg
import math as mat
import random as rand
from heatmaps import heatmaps

Vec2 = pg.Vector2

pg.init()
screen = pg.display.set_mode((1600, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

font = pg.font.SysFont("Consolas", 15)

def query(bool, if_true="Yes", if_false="No"):
    if bool:
        return if_true
    else:
        return if_false

def in_rect(pos, rect):
    if rect[0][0] <= pos.x < rect[0][0] + rect[1][0] and rect[0][1] <= pos.y < rect[0][1] + rect[1][1]:
        return True
    else:
        return False

def print_lines(screen, lines, start_coord):
    start_coord = Vec2(start_coord)
    for i in range(len(lines)):
        text = font.render(lines[i], True, "white")
        screen.blit(text, (start_coord.x, start_coord.y + 20 * i))

def mouse_pos_to_id(mouse_pos, screen, square_size):
    pos_inverted_y = Vec2(mouse_pos[0], screen.get_height() - mouse_pos[1])
    world_pos = Vec2(pos_inverted_y) // square_size
    world_width = screen.get_width() / square_size
    id = world_pos.y * world_width + world_pos.x
    return int(id)

class Cell:
    def __init__(self, id, screen, square_size, looping=False, state=0, birth_num=[3], live_num=[2,3]):
        self.screen = screen
        self.id = id
        self.world_size = Vec2(screen.get_size()) / square_size
        self.pos = Vec2(id % self.world_size.x, id // self.world_size.x)
        screen_pos = Vec2(
            self.pos.x * square_size, 
            ((self.world_size.y - self.pos.y - 1) * square_size)
            )
        self.rect = (screen_pos, Vec2(square_size))
        self.looping = looping
        self.state = state
        self.d_state = 0
        self.birth_num = birth_num
        self.live_num = live_num
        self.state_colours = ["#101010", "#f0e0c0"]
        self.cells = []
        self.neighbors = []
        self.needs_update = False

        self.time_since_1 = 0
        self.frames_per_colour = 10

    def offset_to_id(self, offset, looping):
        pos = self.pos + offset
        if looping:
            pos.x %= self.world_size.x
            pos.y %= self.world_size.y
        else:
            if not in_rect(pos, ((0, 0), self.world_size)):
                return "out of bounds"
        id = pos.y * self.world_size.x + pos.x
        return int(id)
    
    def init_neighbors(self):       # get all neighbors
        # list of neighbor offsets
        neighbor_offsets = [
            (-1,-1), (0,-1), (1,-1),
            (-1, 0),         (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ]

        self.neighbors = []
        for n_offset in neighbor_offsets:
            n_id = self.offset_to_id(n_offset, self.looping)
            self.neighbors.append(self.cells[n_id])

    def init_env(self, cells):
        self.cells = cells
        self.init_neighbors()

    def update_neighbors(self):
        for n in self.neighbors:
            n.needs_update = True
        self.needs_update = True

    def get_neighbor_states(self):
        neighbor_states = []
        for cell in self.neighbors:
            neighbor_states.append(cell.state)
        return neighbor_states

    def calc_d_state(self, pending_cells):
        if self.needs_update == False:
            if self.time_since_1 == 0:
                self.update_time_since_1()
            return
        
        living_neighbors = int(0)
        neighbor_states = self.get_neighbor_states()
        for s in neighbor_states:
            living_neighbors += int(s)

        if self.state == 0 and living_neighbors in self.birth_num:
            self.d_state = 1
            self.update_neighbors()
        elif self.state == 1 and living_neighbors in self.live_num:
            self.d_state = 1
        else:
            if self.state == 1:
                self.update_neighbors()
            self.d_state = 0

        self.update_time_since_1()
        pending_cells.append(self.id)

    def update_time_since_1(self):
        if self.d_state == 1: # if 1 next frame, timer is off
            self.time_since_1 = 0
        elif self.state == 1: # if 0 next frame and was 1 last, timer starts
            self.time_since_1 = 1
        elif self.time_since_1 >= 10 * self.frames_per_colour: # if timer reaches the end turn it off
            self.time_since_1 = 0
        elif self.time_since_1 != 0:
            self.time_since_1 += 1

    def colour(self, heatmap):
        if self.time_since_1 == 0 or heatmap == []:
            return self.state_colours[self.state]
        else:
            fade_stage = mat.floor((self.time_since_1 - 1) / self.frames_per_colour)
            return heatmap[fade_stage]

    def idle_check(self):
        if self.state != self.d_state:
            return
        for i in self.neighbors:
            if i.state != i.d_state:
                return
        self.needs_update = False

    def update_state(self):
        self.state = self.d_state

    def run_click(self):
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1
            self.time_since_1 = 0
        self.update_neighbors()

    def draw_self(self, heatmap):
        if self.state == 1 or (self.time_since_1 != 0 and heatmap != []):
            pg.draw.rect(self.screen, self.colour(heatmap), self.rect)

    def run_hold(self, state):
        if self.state != state:
            self.state = state
            self.update_neighbors()
            if self.state == 0:
                self.time_since_1 = 1

square_size = 4
screen_size = screen.get_size()
cell_num = (screen.get_height() * screen.get_width()) / square_size ** 2

looping = True
birth_num = [3]
live_num = [2, 3]

# B345 S234 = blood sigil
# B1 S123 = castle
# B3457 S4578 = "assimilation"
# B34_678 S5678 = amoeba
# B1357 S1357 = fractal VERY COOL
# B378 S235678 = coagulation
# B45678 S12345 = city walls

def bs_string(birth_num, live_num):
    b_string = "B"
    for i in birth_num:
        b_string = b_string + f"{i}"
    s_string = "S"
    for i in live_num:
        s_string = s_string + f"{i}"
    bs_string = b_string + " " + s_string
    return bs_string

bs = bs_string(birth_num, live_num)

def change_rule(num_list, num):
    if num in num_list:
        num_list.pop(num_list.index(num))
    else:
        num_list.append(num)
        num_list.sort()


frames_per_tick = 1
d_frame = 0
paused = True

tps = 0
time_since_tps_update = 0
ticks_since_tps_update = 0
heatmap = 0
show_info = True
rule_select = "B"
debug_updates = False

num_keys = [
    pg.K_0,
    pg.K_1,
    pg.K_2,
    pg.K_3,
    pg.K_4,
    pg.K_5,
    pg.K_6,
    pg.K_7,
    pg.K_8
]

cells = []
for i in range(int(cell_num)):
    cells.append(Cell(i, screen, square_size, looping, 0, birth_num, live_num))
for cell in cells:
    cell.init_env(cells)

for cell in cells:
    if cell.pos in ((79,79), (79,80), (80,80), (80,79)):
        cell.state = 1
        cell.update_neighbors

def run_tick(cells):
    pending_cells = []
    for cell in cells:
        cell.calc_d_state(pending_cells)
    for cell in cells:
        cell.idle_check()
    for id in pending_cells:
        cells[id].update_state()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # functions for individual key presses
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                paused = not paused
            elif event.key == pg.K_g:
                looping = not looping
            elif event.key == pg.K_f:
                if heatmap == len(heatmaps) - 1:
                    heatmap = 0
                else:
                    heatmap += 1
            elif event.key == pg.K_d:
                show_info = not show_info
            elif event.key == pg.K_e:
                for cell in cells:
                    cell.state = 0
                    cell.d_state = 0
            elif event.key == pg.K_s:
                if rule_select == "B":
                    rule_select = "S"
                else:
                    rule_select = "B"
            elif event.key == pg.K_b:
                debug_updates = not debug_updates
            elif event.key in num_keys:
                change_num = num_keys.index(event.key)
                if rule_select == "S":
                    change_rule(live_num, change_num)
                if rule_select == "B":
                    change_rule(birth_num, change_num)
                bs = bs_string(birth_num, live_num)
                for cell in cells:
                    cell.birth_num = birth_num
                    cell.live_num = live_num
                    cell.needs_update = True

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                cell_id = mouse_pos_to_id(mouse_pos, screen, square_size)
                cells[cell_id].run_click()
            elif event.button == 4 and frames_per_tick < 144:
                frames_per_tick += 1
            elif event.button == 5 and frames_per_tick > 0:
                frames_per_tick -= 1


    # init constant key presses
    keys = pg.key.get_pressed()

    if keys[pg.K_r]:
        cell_id = mouse_pos_to_id(pg.mouse.get_pos(), screen, square_size)
        cells[cell_id].run_hold(1)

    if keys[pg.K_t]:
        cell_id = mouse_pos_to_id(pg.mouse.get_pos(), screen, square_size)
        cells[cell_id].run_hold(0)

    screen.fill("#105010") # flush display

    if d_frame >= frames_per_tick:
        run_tick(cells)
        ticks_since_tps_update += 1
        d_frame = 0
    elif paused == False:
        d_frame += 1

    time_since_tps_update += dt
    if time_since_tps_update >= 1:
        time_since_tps_update -= 1
        tps = ticks_since_tps_update
        ticks_since_tps_update = 0

    for cell in cells:
        if debug_updates:
            if cell.needs_update:
                pg.draw.rect(screen, "green", cell.rect)
        else:
            cell.draw_self(heatmaps[heatmap])

    lines = [
        f"{bs}",
        f"{query(paused, 'paused', 'unpaused')}",
        f"game speed: {round(1 / max(1, frames_per_tick), 2)} {query(frames_per_tick == 0, '(CPU limited)', '')}",
        f"tps: {tps}",
        f"heatmap: {heatmap}",
        f"looping: {query(looping)}",
        f"change rule: {rule_select}",
    ]
    if show_info:
        print_lines(screen, lines, (20, 20))

    pg.display.flip() # print display

    dt = clock.tick(144) / 1000 # update tick time

pg.quit()

db_pending = 0
db_update = 0
for cell in cells:
    if cell.needs_update:
        db_update += 1

print(db_update)