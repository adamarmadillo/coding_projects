import pygame as pg
import math as mat
import random as rand

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

font = pg.font.SysFont("Consolas", 15)

workleft = (2, 4, 0)

newWorkByWeek = [
    # week 3
    [(1, 1, 5), (0, 0, 0), (1, 1, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0)],

    # week 4
    [(1, 1, 5), (0, 0, 0), (1, 1, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0)],

    # week 5
    [(1, 1, 5), (0, 0, 0), (1, 1, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0)],

    # week 6
    [(1, 1, 4), (0, 0, 0), (1, 1, 0), (0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0)],

    # week 7
    [(0, 0, 4), (0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],

    # week 8
    [(0, 0, 3), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
]

workDoneByWeek = [
    # week 3
    [(0, 0, 0), (2, 0, 0), (0, 0, 1), (0, 0, 0), (0, 0, 0), (0, 0, 2), (1, 0, 2)],

    # week 4
    [(2, 0, 0), (0, 0, 0), (1, 0, 1), (1, 0, 1), (1, 0, 1), (0, 0, 2), (0, 0, 0)],

    # week 5
    [(1, 1, 0), (0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 0, 2), (0, 0, 0)],

    # week 6
    [(1, 1, 0), (0, 0, 0), (1, 0, 1), (0, 0, 2), (1, 0, 1), (0, 2, 0), (0, 0, 0)],

    # week 7
    [(0, 2, 0), (0, 0, 0), (1, 0, 1), (0, 0, 2), (0, 1, 1), (0, 2, 0), (0, 0, 0)],
    
    # week 8
    [(0, 0, 2), (0, 0, 0), (0, 1, 1), (0, 2, 0), (0, 2, 0), (0, 0, 0), (0, 0, 0)]
]

line201 = []
b201sLeft = 2
for i in range(6):
    for j in range(7):
        b201sLeft += newWorkByWeek[i][j][0]
        line201.append(b201sLeft)
        b201sLeft -= workDoneByWeek[i][j][0]
        line201.append(b201sLeft)

line204 = []
b204sLeft = 4
for i in range(6):
    for j in range(7):
        b204sLeft += newWorkByWeek[i][j][1]
        line204.append(b204sLeft)
        b204sLeft -= workDoneByWeek[i][j][1]
        line204.append(b204sLeft)

line203 = []
m203sLeft = 0
for i in range(6):
    for j in range(7):
        m203sLeft += newWorkByWeek[i][j][2]
        line203.append(m203sLeft)
        m203sLeft -= workDoneByWeek[i][j][2]
        line203.append(m203sLeft)


lineTotal = []
totalLeft = 6
for i in range(6):
    for j in range(7):
        totalLeft += sum(newWorkByWeek[i][j])
        lineTotal.append(totalLeft)
        totalLeft -= sum(workDoneByWeek[i][j])
        lineTotal.append(totalLeft)

class WeekBox:
    def __init__(self, screen, id, font):
        self.screen = screen
        self.id = id
        self.font = font
        self.colour = "black"
        self.yPosition = 50 + id * 120

    def graphPoints(self, list, id):
        line = list[id * 14 : id * 14 + 14]
        graphPoints = []
        for i in range(14):
            xPos = 114 + 44 * i -1
            if i == 0:
                xPos += 2
            yOff = (50 + 90 + id * 120) - 5 * line[i] - 2
            graphPoints.append((xPos, yOff))
        return graphPoints

    def renderBox(self):
        pg.draw.rect(
            self.screen,
            self.colour,
            ((100, self.yPosition), 
            (600, 100)), 
            2
        )
        pg.draw.rect(
            self.screen, 
            self.colour, 
            ((114, self.yPosition + 10), 
            (572, 80)), 
            1
        )

    def renderLine(self, list, colour):
        pg.draw.lines(
            self.screen,
            colour,
            False,
            self.graphPoints(list, (self.id)),
            2
        )

    def renderFig(self):
        for i in range(15):
            yPos = self.yPosition + 89 - 5 * (i + 1)
            pg.draw.line(screen, (160, 160, 160), (115, yPos), (684 , yPos))


weekBoxList = []
for i in range(6):
    weekBoxList.append(
        WeekBox(screen, i, font)
        )

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    screen.fill((230, 227, 217))

    for i in weekBoxList:
        i.renderBox()
        i.renderFig()
        if keys[pg.K_1]:
            i.renderLine(line201, (20, 200, 20))
        if keys[pg.K_2]:
            i.renderLine(line204, "blue")
        if keys[pg.K_3]:
            i.renderLine(line203, "red")
        if not keys[pg.K_SPACE]:
            i.renderLine(lineTotal, "black")

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()