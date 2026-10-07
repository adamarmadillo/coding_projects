def onepooptwopoop(silly_number):
    if silly_number % 2 == 0:
        return "2 poop!"
    else:
        return "1 poop!"

print(onepooptwopoop(int(input("How much poop? Dawg... \n"))))
import math
def biggassnum(waaat):
    flippin_number_yo = 1
    bungly = 1
    while bungly < waaat:
        flippin_number_yo = flippin_number_yo * flippin_number_yo + 1
        bungly += 1
    return int(flippin_number_yo)
while True:
    flippin_num = int(input("What's the bignum of poop? \n"))
    print(biggassnum(flippin_num))
    print("Digits: ", math.floor(math.log10(biggassnum(flippin_num))))