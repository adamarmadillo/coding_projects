import pygame as pg
import random as rand

def InRect(pos, v1, v2):
    return v1[0] <= pos[0] <= v2[0] and v1[1] <= pos[1] <= v2[1]

class Slider:
    def __init__(
            self, 
            sliderPos, sliderHeight,
            sliderLen, sliderColour, 
            knobLen, knobColour,
            knobVal=0
        ):
        
        self.knobPos = pg.Vector2(sliderPos) + (knobVal, 0)
        self.sliderPos = pg.Vector2(sliderPos)
        self.sliderHeight = sliderHeight
        self.sliderLen = sliderLen
        self.sliderColour = sliderColour
        self.knobLen = knobLen
        self.knobColour = knobColour
        self.mouseBound = False
        self.mouseXOffset = 0
        self.sliderRect = (self.sliderPos, pg.Vector2(sliderLen + knobLen, sliderHeight))

    def KnobRect(self):
        return (self.knobPos, pg.Vector2(self.knobLen, self.sliderHeight))
    
    def slideToMouse(self, mousePos):
        mouseX = (mousePos[0] + self.mouseXOffset)
        self.knobPos.x = max(self.sliderPos.x, min(mouseX, self.sliderPos.x + self.sliderLen))

    def draw(self, screen):
        pg.draw.rect(
            screen,
            self.sliderColour,
            self.sliderRect
            )
        pg.draw.rect(
            screen,
            self.knobColour,
            self.KnobRect()
            )
    
    def MouseClick(self, event, mousePos):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:                             
            if self.mouseBound == False and \
               InRect(
                   mousePos, 
                   self.knobPos.xy, 
                   (self.knobPos + self.KnobRect()[1]).xy
                ):
                self.mouseBound = True
                self.mouseXOffset = self.knobPos.x - mousePos[0]                
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.mouseBound = False

    def randomiseX(self):
        self.knobPos.x = rand.randint(self.sliderPos.x, self.sliderPos.x + self.sliderLen)

    def Value(self):
        return int(self.knobPos.x - self.sliderPos.x)