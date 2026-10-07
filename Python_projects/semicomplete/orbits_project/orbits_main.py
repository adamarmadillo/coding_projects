import pygame as pg
import random as rand
import math as mat

from coding_projects.Python_projects.semicomplete.orbits_project.orbits_body import Body

pg.init()
true_screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Orbits")
clock = pg.time.Clock()
running = True

font = pg.font.SysFont("Consolas", 12)
game_size = 4
sim_screen = pg.Surface(pg.Vector2(true_screen.get_size()) * game_size)
true_dt = 0
sim_dt = 0
timespeed = 1e-3

scale = 1000
offset = pg.Vector2(0,0)
move_offset = pg.Vector2(0,0)
follow_offset = pg.Vector2(0,0)
mouse_offset = pg.Vector2(0,0)
mouse_temp_offset = pg.Vector2(0,0)
mouse_down = False
body_follow = 0

G_const = 667.430

earth = Body("Earth", sim_screen, 5.97219, 6.371e-3, (10, 115, 174), (-149.6,0), (0,2978))
moon = Body("Moon", sim_screen, 0.07347, 1.7374e-3, (88, 89, 98), (-149.984,0), (0, 3080))
sun = Body("Sun", sim_screen, 1.98848e6, 0.6957, (239, 216, 76), (0,0), (0,0), True)
mercury = Body("Mercury", sim_screen, 0.33011, 2.439e-3, (84, 80, 78), (32.5269,-32.6269), (-4171.9,-4171.9))
venus = Body ("Venus", sim_screen, 4.86732, 6.052e-3, (160, 128, 38), (-18.664, -105.8471), (-3472.43, 612.28))

bodylist = [earth, moon, sun, mercury, venus]

linelist = []

for body in bodylist:
    body.render_tag(game_size)

def swap_follow():
    global body_follow, move_offset, mouse_offset
    if body_follow == len(bodylist) - 1:
        body_follow = 0
    else:
        body_follow += 1
        move_offset = pg.Vector2(0,0)
        mouse_offset = pg.Vector2(0,0)

while running:    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_down = True
            mouse_pos_init = pg.Vector2(pg.mouse.get_pos())
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mouse_down = False
            mouse_offset += mouse_temp_offset
            mouse_temp_offset = pg.Vector2(0,0)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            swap_follow()
    
    for body in bodylist:
        if not body.locked:
            body.calc_acc(bodylist, G_const, sim_dt)
    
    for body in bodylist:
        if not body.locked:                     
            body.move(sim_dt)
            body.update_trail(1,1)
    
    follow_offset = bodylist[body_follow].pos.copy()

    keys = pg.key.get_pressed()
    if keys[pg.K_r]:
        scale *= 3 ** true_dt
    if keys[pg.K_f]:
        scale /= 3 ** true_dt
    
    if keys[pg.K_x]:
        timespeed /= 2 ** true_dt
    if keys[pg.K_c]:
        timespeed *= 2 ** true_dt
    
    if keys[pg.K_a]:
        move_offset.x -= 500 * true_dt * game_size / scale
    if keys[pg.K_d]:
        move_offset.x += 500 * true_dt * game_size / scale
    if keys[pg.K_s]:
        move_offset.y += 500 * true_dt * game_size / scale
    if keys[pg.K_w]:
        move_offset.y -= 500 * true_dt * game_size / scale

    if mouse_down:
        mouse_temp_offset = (mouse_pos_init - pg.mouse.get_pos()) * game_size / scale

    offset = move_offset + follow_offset + mouse_offset + mouse_temp_offset
    
    sim_screen.fill("black")

    for body in bodylist:
        body.draw_trail(scale, offset)

    for body in bodylist:
        body.draw_body(scale, offset)

    i = len(bodylist)
    while i >= 0:
        i -= 1
        bodylist[i].print_tag(sim_screen, scale, offset, game_size)

    scaled_screen = pg.transform.smoothscale(sim_screen, (800,800))
    true_screen.blit(scaled_screen, (0,0))

    line_y = 0
    corner_text = f"""Solar system V1.0.0.3

Time: {round(100000000 * timespeed)}x speed
1px = {round(1e6 / scale * game_size)} Km

{bodylist[body_follow].all_info(bodylist)}"""
    
    lines = corner_text.splitlines()
    for line in lines:
        text_screen = font.render(line, True, "white")
        true_screen.blit(text_screen, (25,line_y + 25))
        line_y += 15

    linelist.append(true_dt)
    if len(linelist) > 300:
           linelist.pop(0)
    if len(linelist) > 5:
        avg = int(sum(linelist) * 10000 / len(linelist))
        pg.draw.line(true_screen, (140,140,140), (40, 700), (640, 700))
        pg.draw.line(true_screen, (140, 140, 140), (40, 700 - avg), (640, 700 - avg))
        pg.draw.lines(true_screen, "red", False, [(40 + 2 * i, 700 - int(10000 * linelist[i])) for i in range(len(linelist))])


    pg.display.flip()

    true_dt = clock.tick(144) / 1000
    sim_dt = true_dt * timespeed

pg.quit()