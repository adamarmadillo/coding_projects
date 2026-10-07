while True:    
    while True:
        numinput = input("What number would you like to test?\n")
        if numinput.isdigit() and int(numinput) > 1:
            numinput = int(numinput)
            break
        else:
            print("Invalid input, please insert a number larger than 1.")
    numtemp = 1
    while True:
        numtemp += 1
        if numtemp >= numinput:
            print(f"Your number is prime.")
            break
        elif numinput % numtemp == 0:
            print(f"You number can be divided by {numtemp}.")
            while True:
                tempinput = input("Divide? (y/n)\n").lower()
                if tempinput == "y":
                    print(f"{numinput} divided by {numtemp} is {int(numinput / numtemp)}.")
                    break
                elif tempinput == "n":
                    break
                else:
                    print("Invalid input, try again")
            break