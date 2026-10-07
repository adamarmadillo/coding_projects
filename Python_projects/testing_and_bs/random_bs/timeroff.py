import pygame as pg
import math as mat
import random as rand
import pickle

pg.init()
screen = pg.display.set_mode((400, 200))
pg.display.set_caption("Time Off")
clock = pg.time.Clock()
running = True
dt = 0

font1 = pg.font.SysFont("Consolas", 15, True)
font2 = pg.font.SysFont("Consolas", 18, True)

#with open("data.pkl", "rb") as f:
#    my_list = pickle.load(f)

#gt = my_list[0]
#bt = my_list[1]
g_true = False
unhovered = 1

gt = 0
bt = 9.5 * 60 * 60

t_text = "Start work"

btext_list = [
    "Don't give in!!",
    "Giving up?",
    "Destined for faliure?",
    "Can't do a basic task?",
    "You have no determination"
]

gtext_list = [
    "Good shit",
    "Work time",
    "Destined for success!",
    "You might just make it"
]

mb_d = False

while running:
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if 100 < pos[0] < 300 and 140 < pos[1] < 170 and not mb_d:
                if g_true:
                    g_true = False
                    unhovered = 0
                    t_text = gtext_list[rand.randint(0, 3)]
                    mb_d = True
                else:
                    g_true = True
                    unhovered = 0
                    t_text = btext_list[rand.randint(0, 4)]
                    mb_d = True

            if 310 < pos[0] < 340 and 140 < pos[1] < 170:
                gt = 0.01
                bt = 0.01
        
        if event.type == pg.MOUSEBUTTONUP:
            mb_d = False

    keys = pg.key.get_pressed()

    screen.fill((230, 223, 210))

    pg.draw.rect(screen, (210, 175, 160), ((100, 140), (200, 30)))
    
    if 100 < pos[0] < 300 and 140 < pos[1] < 170 and unhovered == 1:
        text = font2.render(t_text, True, "black")
    elif not 100 < pos[0] < 300 or not 140 < pos[1] < 170:
        unhovered = 1
        text = font2.render("Swap timers", True, "black")
    else:
        text = font2.render("Swap timers", True, "black")
    screen.blit(text, (200 - (text.get_width() / 2), 145))

    if g_true:
        gt += dt
        bt -= dt
    #else:
    #    bt += dt
    
    g_port = gt / (gt + bt)
    b_port = bt / (gt + bt)

    g_rect = ((55, 40), (290 * g_port, 40))
    pg.draw.rect(screen, "green3", g_rect)
    pg.draw.rect(screen, "green", g_rect, 2)
    b_rect = ((55 + g_port * 290, 40), (290 - g_port * 290, 40))
    pg.draw.rect(screen, "red3", b_rect)
    pg.draw.rect(screen, "red", b_rect, 2)

    gs = gt % 60
    gm = int(((gt - gs) / 60) % 60)
    gh = int((((gt - gs) / 60) - gm) / 60)

    bs = bt % 60
    bm = int(((bt - bs) / 60) % 60)
    bh = int((((bt - bs) / 60) - bm) / 60)

    text = font2.render(f"{gh}:{gm:02d}:{gs:05.2f}", True, (50, 150, 60))
    w = text.get_width()
    screen.blit(text, (50, 95))

    text = font2.render(f"{bh}:{bm:02d}:{bs:05.2f}", True, (150, 50, 60))
    w = text.get_width()
    screen.blit(text, (250, 95))

    text = font2.render(f"{g_port * 100:04.1f}:{b_port * 100:04.1f}", True, (50, 50, 60))
    w = text.get_width()
    screen.blit(text, (200 - (w / 2), 115))

    pg.draw.rect(screen, (210, 175, 160), ((310, 140), (30, 30)))
    pg.draw.circle(screen, (50, 50, 60), (325, 156), 10)
    pg.draw.circle(screen, (210, 175, 160), (325, 156), 7)
    pg.draw.polygon(screen, (210, 175, 160), ((310, 153), (325, 156), (322, 141)))
    pg.draw.polygon(screen, (50, 50, 60), ((325, 151), (325, 143), (321, 147)))

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()

my_list = [gt, bt]
with open("data.pkl", "wb") as f:
    pickle.dump(my_list, f)