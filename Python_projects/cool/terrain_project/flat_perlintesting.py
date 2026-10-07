import math as mat
import random as rand

def gen_perm(seed=None, size=255):
    rng = rand.Random(seed)
    perm = [[(rng.random() * 2 * mat.pi) for i in range(size)] for j in range(size)]
    xg = [[mat.cos(j) for j in i] for i in perm]
    yg = [[mat.sin(j) for j in i] for i in perm]
    return [xg, yg]

def fade(x):
    return 6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3

def lerp(x, a, b):
    return a + x * (b - a)

def perlin(x, y, perm):
    size = len(perm[0])
    
    xi0 = mat.floor(x)
    xf0 = x - xi0
    xi1 = (xi0 + 1)
    xf1 = x - xi1
    if xi1 == size:
        xi1 = 0

    yi0 = mat.floor(y)
    yf0 = y - yi0
    yi1 = (yi0 + 1)
    yf1 = y - yi1
    if yi1 == size:
        yi1 = 0

    dp00 = perm[0][yi0][xi0] * xf0 + perm[1][yi0][xi0] * yf0
    dp01 = perm[0][yi0][xi1] * xf1 + perm[1][yi0][xi1] * yf0
    dp10 = perm[0][yi1][xi0] * xf0 + perm[1][yi1][xi0] * yf1
    dp11 = perm[0][yi1][xi1] * xf1 + perm[1][yi1][xi1] * yf1

    tx = fade(xf0)
    ty = fade(yf0)

    v_bottom = lerp(tx, dp00, dp01)
    v_top = lerp(tx, dp10, dp11)
    return (lerp(ty, v_bottom, v_top)) * mat.sqrt(2) / 2 + 0.5

def gen_perlin_array(seed, scale, amp, size=80):
    perm = gen_perm(seed, mat.ceil(size / scale))
    array = []
    for i in range(size):
        temp = []
        for j in range(size):
            temp.append(perlin(i / scale, j / scale, perm) * amp)
        array.append(temp)
    return array


# ideally the end goal is an infinitely scalable, walkable perlin generator
# some useful things to put out there:
# detail becomes irrelevant after 1 pixel randomness
# offset is a requirement
# minimising work per sample makes it runnable