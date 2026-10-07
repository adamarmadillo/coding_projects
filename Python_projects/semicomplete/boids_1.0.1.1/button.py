import pygame as pg
Vec = pg.Vector2

def InRect(pos, v1, v2):
    return v1[0] <= pos[0] <= v2[0] and v1[1] <= pos[1] <= v2[1]

class Button:
    def __init__(self, screen, position, width, height, onColour, offColour, onOff=False):
        self.screen = screen
        self.pos = Vec(position)
        self.bound = (width, height)
        self.onColour = onColour
        self.offColour = offColour
        self.value = onOff

    def ButtonPress(self, mousePos):
        if InRect(mousePos, self.pos, self.pos + self.bound):
            self.value = not self.value
    
    def Draw(self):
        if self.value:
            colour = self.onColour
        else:
            colour = self.offColour
        pg.draw.rect(self.screen, colour, (self.pos, self.bound))