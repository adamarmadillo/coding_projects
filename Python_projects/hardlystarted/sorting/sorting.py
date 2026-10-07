import pygame as pg
import math as mat
import random as rand

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

font = pg.font.SysFont("Consolas", 15)

array_length = 50
array = list(range(1, array_length + 1))
rand.shuffle(array)

sort_running = False
moves_per_second = 144
time_since_frame = 0

value_a = 0
value_b = 0
pos = 0
next_move = "na"
swaps = 0
compares = 0
finished_line = len(array)

def make_move():
    global value_a, value_b, pos, next_move, swaps, compares, finished_line
    if next_move == "na" or next_move == "value_get_1":
        value_a = array[pos]
        pos += 1
        next_move = "value_get_2"
    
    elif next_move == "value_get_2":
        value_b = array[pos]
        next_move = "compare"
    
    elif next_move == "compare":
        if value_a > value_b:
            next_move = "swap"
            pos -= 1
        else:
            if pos == finished_line:
                finished_line = pos - 1
                pos = 0
                next_move = "value_get_1"

            else:
                value_a = value_b
                pos += 1
                next_move = "value_get_2"
        compares += 1

    elif next_move == "swap":
        array[pos] = value_b
        array[pos + 1] = value_a
        if pos == finished_line - 2:
            finished_line = pos + 1
            pos = 0
            next_move = "value_get_1"
        else:
            pos += 2
            next_move = "value_get_2"
        swaps += 1

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            continue

        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            sort_running = not sort_running
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                moves_per_second += 1
            elif event.button == 5:
                moves_per_second -= 1

    if sort_running:
        if time_since_frame > 1 / moves_per_second or moves_per_second == 144:
            make_move()
            time_since_frame = 0
        else:
            time_since_frame += dt

    screen.fill("black")

    pg.draw.rect(screen, "white", ((90,90), (620, 320)), 1)
    # area is 100,100 to 700,400
    # area is 600 by 300

    bar_width = 600 / len(array)
    for i in array:
        if array.index(i) == pos:
            colour = "red"
        if array.index(i) == finished_line:
            colour = "green"
        else:
            colour = "white"
        bar_height = i * 300 / len(array)
        rect = ((int(array.index(i) * bar_width + 100), 400 - int(i * 300 / len(array))), (int(bar_width), int(i * 300 / len(array))))
        pg.draw.rect(screen, colour, rect)

    line_y = 420
    info = f"position: {pos + 1} \nswaps: {swaps} \ncompares: {compares}"
    lines = info.splitlines()
    for line in lines:
        text = font.render(line, True, "white")
        screen.blit(text, (100, line_y))
        line_y += 15


    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()