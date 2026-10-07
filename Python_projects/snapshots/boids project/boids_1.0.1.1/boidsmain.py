import pygame as pg
import math as mat
import random as rand
Vec = pg.Vector2
from boid_obj import Boid
from slider import Slider
from button import Button

pg.init()
screen = pg.display.set_mode((1800, 1000))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0
screenDimensions = Vec(screen.get_size())

font = pg.font.SysFont("Consolas", 12)

boidCount = 100
avoidRadius = 12
viewRadius = 40
alignRadius = 48
maxVel = 200
conformStrength = 10
alignStrength = 20

# def text 

def trueFalse(bool):
    return "On" if bool else "Off"

# init sliders

sliders = []
defaultValues = [viewRadius / 2, avoidRadius, alignRadius / 2, maxVel/10, conformStrength * 2, alignStrength * 2]
for i in range(6):
    sliders.append(
        Slider(
            sliderPos=(20, 40 + 45 * i), 
            sliderHeight=12, 
            sliderLen=100, 
            sliderColour=(100,100,100), 
            knobLen=16, 
            knobColour=(150,150,150),
            knobVal=(defaultValues[i])
        )
    )

# init buttons

buttons = []
for i in range(9):
    if i in (0,1):
        defaultOnOff = True
    else:
        defaultOnOff = False
    buttons.append(
        Button(
            screen=screen, 
            position=(20, 35 + 45 * len(sliders) + 40 * i), 
            width=24, height=21, 
            onColour=(150,150,150), 
            offColour=(80,80,80), 
            onOff=defaultOnOff
        )
    )

# init boids

colourList = [(227, 230, 214), (78, 60, 43), (36, 31, 25)]
boidList = []
for i in range(boidCount):
    boidList.append(
        Boid(
            id=i,
            surface=screen,
            gamePos=(
                rand.randint(0,screenDimensions.x), 
                rand.randint(0,screenDimensions.y)
            ),
            velocity=(0,0), 
            dirCol=colourList[i % 3]
        )
    )

# init pause screen

pauseScreen = pg.Surface((1800, 1000))
pauseScreen.fill("black")
pauseScreen.set_alpha(128)

pauseButton = Button(screen, (840, 15), 120, 24, (150,150,150), (130,130,130))
buttons.append(pauseButton)
pauseOn = False

def DrawPauseScreen():
    screen.blit(pauseScreen, (0,0))
    pauseButton.Draw()
    text = font.render("Resume", True, "white")
    screen.blit(text, (878, 22))

# game loop

while running:
    
    mousePos = pg.mouse.get_pos()
    
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            running = False
            continue
        
        if event.type not in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
            continue

        if pauseOn:
            if event.type == pg.MOUSEBUTTONDOWN:
                pauseButton.ButtonPress(mousePos)
            continue

        for slider in sliders:
            slider.MouseClick(event, mousePos)
        
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in buttons:
                button.ButtonPress(mousePos)

    pauseOn = pauseButton.value
    
    if pauseOn:
        if not pauseDrawn:
            DrawPauseScreen()
            pauseDrawn = True

    else:
        pauseDrawn = False

        for slider in sliders:
            if slider.mouseBound:
                slider.slideToMouse(mousePos)

        viewRadius = 2 * sliders[0].Value()
        avoidRadius = sliders[1].Value()
        alignRadius = 2 * sliders[2].Value()
        maxVel = 10 * sliders[3].Value()
        conformStrength = int((sliders[4].Value() / 2))
        alignStrength = int((sliders[5].Value() / 2))

        screen.fill((76, 125, 87))
        pg.draw.rect(screen, (78, 60, 43), ((40,40), (1720, 920)), 2)

        for boid in boidList:
            boid.Accelerate(
                boidList,
                avoidRadius, 
                viewRadius, 
                maxVel, 
                mousePos, 
                buttons[0].value,
                buttons[8].value,
                conformStrength)

        for boid in boidList:
            boid.Move(dt, boidList, alignRadius, maxVel, alignStrength)

        for boid in boidList:
            boid.DrawLines(
                boidList, mousePos,
                avoidRadius, viewRadius, alignRadius,
                conformStrength,
                conformCircle = buttons[2].value,
                avoidCircle = buttons[3].value, 
                conformLine = buttons[5].value,            
                avoidLine = buttons[6].value,
                alignLine = buttons[7].value,
                alignCircle = buttons[4].value,
                mouseAvoidLine = buttons[0].value
            )

        if buttons[3].value and buttons[0].value:
            pg.draw.circle(screen, (128,0,0), mousePos, avoidRadius * 3.5, 1)

        for boid in boidList:
            boid.DrawSelf(directionLine = buttons[1].value)

        for slider in sliders:
            slider.draw(screen)

        sliderText = f"""
Conform Radius:{viewRadius}
Avoid Radius:{avoidRadius}
Align Radius:{alignRadius}
Max Velocity:{maxVel}
Conform Strength:{conformStrength}
Align Strength:{alignStrength}"""
        sliderText = sliderText.splitlines()
        lineNo = 0
        for line in sliderText:
            text = font.render(line, True, "white")
            screen.blit(text, (20, -20 + 45 * lineNo))
            lineNo += 1

        for button in buttons:
            button.Draw()

        buttonText = f"""
Avoid Mouse:{trueFalse(buttons[0].value)}
Direction:{trueFalse(buttons[1].value)}
Conform Radius:{trueFalse(buttons[2].value)}
Avoid Radius:{trueFalse(buttons[3].value)}
Align Radius:{trueFalse(buttons[4].value)}
Conform direction:{trueFalse(buttons[5].value)}
Avoid line:{trueFalse(buttons[6].value)}
Align line:{trueFalse(buttons[7].value)}
Flat Avoid:{trueFalse(buttons[8].value)}"""
        buttonText = buttonText.splitlines()
        lineNo = 0
        for line in buttonText:
            text = font.render(line, True, "white")
            screen.blit(text, (50, (45 * len(sliders)) + 40 * lineNo))
            lineNo += 1
        
        text = font.render("Pause", True, "white")
        screen.blit(text, (881, 22))

    pg.display.flip()

    dt = clock.tick(144) / 1000

pg.quit()