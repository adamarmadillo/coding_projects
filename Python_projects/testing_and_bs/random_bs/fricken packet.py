over = ""
while over != "yo":
    over = input("Bro: fricken packet? \nMe: ")

    temp_over = ""
    i = 0
    while i < len(over):
        if over[i].isalpha() == True:
            temp_over = temp_over + over[i]
        i = i + 1
    over = temp_over
print("Teacher: six seven!")