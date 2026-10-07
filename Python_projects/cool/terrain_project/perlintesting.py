import math as mat
import random as rand

def form_perm(seed=None):
    rng = rand.Random(seed)
    p = list(range(2048))
    rng.shuffle(p)
    return p * 2

def fade(x):
    return 6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3

def lerp(x, a, b):
    return a + x * (b - a)

def perlin(x, perm):
    x_int = mat.floor(x) & 2047
    x_fract = x - mat.floor(x)

    fade_x = fade(x_fract)

    return lerp(fade_x, perm[x_int], perm[x_int + 1])

perm = form_perm(10)

zerototwo = [perlin((x * 0.1), perm) for x in range(20)]

print(f"{zerototwo} wait wait {perm}")
