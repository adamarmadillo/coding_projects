import pygame, math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Screen test")
clock = pygame.time.Clock()
running = True

# setup
dt = 0
c_pos = pygame.Vector2(200, 400)
c_vel = pygame.Vector2(0, 0)
h_pos = pygame.Vector2(600, 400)
h_vel = pygame.Vector2(0, 0)
h_dir = 0

image = pygame.image.load("housemd.png")
scale = 0.25
image = pygame.transform.scale_by(image, scale)
image_offset = pygame.Vector2(-96 * scale, -128 * scale)

def wrap(vector):
    vector.x = vector.x % screen.get_width()
    vector.y = vector.y % screen.get_height()

# run the game loop
while running:
    for event in pygame.event.get():
        # end running loop if X is clicket
        if event.type == pygame.QUIT:
            running = False
    
    # fill screen colour
    screen.fill("black")

    # render game
    pygame.draw.circle(screen, "blue", c_pos, 40)
    screen.blit(image, (h_pos + image_offset))

    # move circle

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        c_vel.y -= 10 * dt
    if keys[pygame.K_s]:
        c_vel.y += 10 * dt
    
    if keys[pygame.K_a]:
        c_vel.x -= 10 * dt
    if keys[pygame.K_d]:
        c_vel.x += 10 * dt
    
    if keys[pygame.K_SPACE]:
        c_vel *= 0.1 ** dt

    c_pos += c_vel
    wrap(c_pos)

    # move house

    h_dir = math.atan2((c_pos.y - h_pos.y), (c_pos.x - h_pos.x))
    
    h_vel.x += 2 * math.cos(h_dir) * dt
    h_vel.y += 2 * math.sin(h_dir) * dt

    h_vel *= 0.9 ** dt
    
    h_pos += h_vel


    # flip display
    pygame.display.flip()
    # 
    dt = clock.tick(144) / 1000






# close the program
pygame.quit()