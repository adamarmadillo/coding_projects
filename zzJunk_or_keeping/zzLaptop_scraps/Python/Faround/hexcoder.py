import pygame as pg
import random as rand

pg.init()
screen = pg.display.set_mode((400, 400))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True

dt = 0
mouseButtonDown = False
shiftHeld = False
mousePos = (0,0)
font = pg.font.SysFont("Consolas", 12)
font2 = pg.font.SysFont("Consolas", 18)

def InRect(pos, v1, v2):
    if v1[0] <= pos[0] <= v2[0] and v1[1] <= pos[1] <= v2[1]:
        return True
    else:
        return False
    
def HexColour(colour):
    return f"#{colour[0]:02X}{colour[1]:02X}{colour[2]:02X}"

# hover highlight: if mouse pos is within knob range, knobColour + (50,50,50), sliderColour + (50,50,50)
class Slider:
    def __init__(self, sliderPos, sliderLen, sliderHeight, knobLen, knobColour, sliderColour):
        self.knobPos = pg.Vector2(sliderPos)
        self.sliderPos = pg.Vector2(sliderPos)
        self.sliderLen = sliderLen
        self.sliderHeight = sliderHeight
        self.knobLen = knobLen
        self.knobColour = knobColour
        self.sliderColour = sliderColour
        self.mouseBound = False
        self.mouseXOffset = 0

        self.sliderRect = (self.sliderPos, pg.Vector2(sliderLen + knobLen, sliderHeight))

    def KnobRect(self):
        return (self.knobPos, pg.Vector2(self.knobLen, self.sliderHeight))
    
    def slideToMouse(self, mousePos, sliders, shiftHeld):
        mouseX = (mousePos[0] + self.mouseXOffset)
        if self.mouseBound:
            if mouseX > self.sliderPos.x + self.sliderLen:
                self.knobPos.x = self.sliderPos.x + self.sliderLen        
            elif mouseX < self.sliderPos.x:
                self.knobPos.x = self.sliderPos.x
            else:
                self.knobPos.x = mouseX
        if self.mouseBound == False and shiftHeld:
            boundX = 0
            for slider in sliders:
                if slider.mouseBound:
                    boundX = slider.knobPos.x
            if boundX != 0:
                self.knobPos.x = boundX

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
    
    def clickCheck(self, mousePos):
        if self.mouseBound == False and \
           InRect(mousePos, self.knobPos.xy, (self.knobPos + self.KnobRect()[1]).xy):
            self.mouseBound = True
            self.mouseXOffset = self.knobPos.x - mousePos[0]
        

    def randomiseX(self):
        self.knobPos.x = rand.randint(int(self.sliderPos.x), int(self.sliderPos.x + self.sliderLen))

    def Colour(self):
        return int(self.knobPos.x - self.sliderPos.x)

sliders = [Slider((55,50 + 50 * i), 255, 17, 30, (220,220,220), (140,140,140)) for i in range(3)]

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key != pg.K_LSHIFT and event.key != pg.K_RSHIFT:
                for slider in sliders:
                    slider.randomiseX()
            if event.key == pg.K_RSHIFT or event.key == pg.K_LSHIFT:
                shiftHeld = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_RSHIFT or event.key == pg.K_LSHIFT:
                shiftHeld = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mousePos = pg.mouse.get_pos()
            if InRect(mousePos, (55, 255), (135, 285)):
                running = False                                
            for slider in sliders:
                slider.clickCheck(mousePos)                
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            for slider in sliders:    
                slider.mouseBound = False
        
    mousePos = pg.mouse.get_pos()
    for slider in sliders:    
        slider.slideToMouse(mousePos, sliders, shiftHeld)

    screen.fill([int(sliders[i].knobPos.x - sliders[i].sliderPos.x) for i in range(0,3)])

    for slider in sliders:    
        slider.draw(screen)
    
    pg.draw.rect(screen, (190,190,190), ((55,255), (80,30)))

    brightness = 0
    for j in range(0,3):
        brightness += [255 - int(sliders[i].knobPos.x - sliders[i].sliderPos.x) for i in range(0,3)][j]
    brightness = int(brightness / 3)

    if brightness > 128:
        textColour = "white"
    else:
        textColour = "black"

    colourResult = [int(sliders[i].knobPos.x - sliders[i].sliderPos.x) for i in range(3)]

    text1 = font.render(f"{colourResult}", True, (textColour))
    screen.blit(text1, (55,200))
    text2 = font.render(HexColour(colourResult), True, textColour)
    screen.blit(text2, (55,225))


    text3 = font.render("I like it", True, "black")
    screen.blit(text3, (62, 265))

    pg.display.flip()

    clock.tick(144)

colourFinal = f'{colourResult}'.strip("[]")
hexFinal = HexColour(colourResult)
print(f"""
-----------------------

Your colour: ({colourFinal})

In Hexcode: {hexFinal}

It's beautiful!

-----------------------
""")

pg.quit()