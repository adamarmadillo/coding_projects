import pygame as pg

# pg setup
pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True

# other setup
dt = 0

# running loop
while running:
    # check events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # get inputs
    keys = pg.key.get_pressed()

    # run logic HERE


    # draw everything
    # screen colour
    screen.fill("black")

    # flip display
    pg.display.flip()
    # calc dt + wait
    dt = clock.tick(144) / 1000

# exit the game
pg.quit()