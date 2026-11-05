import random
import pygame as pg

pg.init()
screen = pg.display.set_mode((1000, 500))
pg.display.set_caption("Game")
clock = pg.time.Clock()
running = True
dt = 0

def generate_list(size):
    L = list(range(size))
    random.shuffle(L)
    return L

#length_1 = int(input("Length?"))
#ratio_1 = float(input("Ratio?"))
#ratio_1 = int(length_1 * ratio_1)
#repeat_1 = int(input("# of trials?"))

def run_test(length, ratio, repeat):
    results = []
    for i in range(repeat):
        L = generate_list(length)
        best = L[0]
        for j in range(ratio):
            if L[j] > best:
                best = L[j]
        max = 0
        outcome = "undefined"
        for j in range(ratio, length):
            if L[j] > best:
                max = L[j]
                break
        for j in range(ratio, length):
            if L[j] > max:
                outcome = "beaten"
        if max == 0:
            outcome = "no candidate"
        elif outcome != "beaten":
            outcome = "success"
        results.append(outcome)

    NC = 0
    S = 0
    B = 0
    for i in results:
        if i == "no candidate":
            NC += 1
        elif i == "success":
            S += 1
        elif i == "beaten":
            B += 1
    return [B, S, NC]

trials = 100

test_range = []
for i in range(trials):
    test = run_test(trials, i, 100000)
    test_range.append(test)
    print(test)

lines = [
    ((0, 400), (1000, 400)),
    [(i * 1000 / trials, 400 - (test_range[i][0] / 333.33)) for i in range(trials)],
    [(i * 1000 / trials, 400 - ((test_range[i][0] + test_range[i][1]) / 333.33)) for i in range(trials)],
    ((0, 100), (1000, 100))
]

colours = ["white", "red", "green", "white"]

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")

    for i in range(4):
        pg.draw.lines(screen, colours[i], False, lines[i])

    pg.display.flip()

    clock.tick(144)
pg.quit()

#test = run_test(length_1, ratio_1, repeat_1)
#print(f"Successes: {test[0]}  No candidate: {test[1]}  Beaten: {test[2]}")