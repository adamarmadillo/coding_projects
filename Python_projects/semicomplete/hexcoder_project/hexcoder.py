import pygame as pg
import random as rand
from coding_projects.Python_projects.semicomplete.hexcoder_project.slider import Slider, InRect

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True

dt = 0
mousePos = (0,0)
font = pg.font.SysFont("Consolas", 12)
font2 = pg.font.SysFont("Consolas", 18)

def HexColour(colour):
    return f"#{colour[0]:02X}{colour[1]:02X}{colour[2]:02X}"

sliders = [
        Slider(
            sliderPos=(55,50 + 50 * i), 
            sliderHeight=17, 
            sliderLen=255, 
            sliderColour=(140,140,140),
            knobLen=30, 
            knobColour=(220,220,220)
        ) 
        for i in range(3)
    ]

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
            mousePos = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN and \
            event.button == 1 and \
            InRect(mousePos, (55, 255), (135, 285)):
                running = False
                break                          
            else:
                for slider in sliders:
                    slider.MouseClick(event, mousePos)

    for slider in sliders:    
        if slider.mouseBound:
            mousePos = pg.mouse.get_pos()
            slider.slideToMouse(mousePos)

    screen.fill([sliders[i].Value() for i in range(0,3)])

    for slider in sliders:    
        slider.draw(screen)
    
    pg.draw.rect(screen, (190,190,190), ((55,255), (80,30)))

    brightness = 0
    for j in range(0,3):
        brightness += [255 - sliders[i].Value() for i in range(0,3)][j]
    brightness = int(brightness / 3)

    if brightness > 128:
        textColour = "white"
    else:
        textColour = "black"

    colourResult = [int(sliders[i].Value()) for i in range(3)]

    text1 = font.render(f"{colourResult}", True, (textColour))
    screen.blit(text1, (55,200))
    text2 = font.render(HexColour(colourResult), True, textColour)
    screen.blit(text2, (55,225))


    text3 = font.render(f"I like it!", True, "black")
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