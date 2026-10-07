import pygame as pg
import math as mat
import random as rand

from slider import Slider
from flat_perlintesting import gen_perm, perlin, gen_perlin_array, fade

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

font = pg.font.SysFont("Consolas", 15)

class Box:
    def __init__(self, pos, colour):
        self.pos = pos
        self.colour = colour

    def draw(self, screen):
        pg.draw.rect(screen, self.colour, (self.pos, (1, 1)))

def gen_boxlist(array):
    boxlist = []
    l = len(array)
    for i in range(l):
        for j in range(l):
            col = array[i][j] * 255
            boxlist.append(Box((i, j), (col, col, col)))
    return boxlist

def permerge(arr1, arr2, dampen):
    l = len(arr1)
    arr = []
    for i in range(l):
        temp = []
        for j in range(l):
            temp.append((arr1[i][j] + arr2[i][j]) / dampen)
        arr.append(temp)
    return arr

def contrast(array):
    temp1 = []
    for i in array:
        temp2 = []
        for j in i:
            temp2.append(fade(j))
        temp1.append(temp2)
    return temp1

seed = 1

perlina = gen_perlin_array(1, 150, 1, 800)

#perlinb = contrast(gen_perlin_array(2, 80, 1, 800))
#perlinf = permerge(perlina, perlinb, 2)

#perlina = contrast(gen_perlin_array(3, 200, 1, 800))
#perlinf = permerge(perlinf, perlina, 2)

boxlista = gen_boxlist(perlina)
#boxlistb = gen_boxlist(perlinb)
#boxlistf = gen_boxlist(perlinf)

# fallthrough is that amp and octave cannot easily be modified and is innacurate through contrast()
# ideally it should be possible to layer the arrays without dampening too much
# if you add an array based on a flat gray array and divide, you will get a les detailed array, as limits becoem more rare?


#boxlistlist = [boxlista, boxlistb, boxlistf]
boxpick = 2

boxlistnames = ("boxlist a", "boxlist b", "boxlist f")

while running:

    mousePos = pg.mouse.get_pos()
    
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            running = False
            continue
        
        if event.type not in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
            continue

        if event.type == pg.MOUSEBUTTONDOWN:
            boxpick += 1
            boxpick = boxpick % 3

#        freq_slider.MouseClick(event, mousePos)

    keys = pg.key.get_pressed()
    
#    if keys[pg.K_SPACE]:
#        seed += 1
#        perlin1 = gen_perlin_array(seed, 80, 100, 1)
#        boxlist = gen_boxlist(gen_perlin_array(None, 10, 1))

#    if freq_slider.mouseBound:
#        freq_slider.slideToMouse(mousePos)

    screen.fill("black")

    #for i in boxlistlist[boxpick]:
    #    i.draw(screen)

    for i in boxlista:
        i.draw(screen)

    text = font.render(f"{boxlistnames[boxpick]}", True, "blue", None)
    screen.blit(text, (20, 20))

#    freq_slider.draw(screen)

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()