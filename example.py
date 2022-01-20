import random


def do_something(x, y):
    if x > y and x < 0:
        return y
    elif x > y and x < 10:
        return 10 - x
    elif x < y and x > 0:
        return y - x
    elif x < 0:
        return x


def guess():
    number = random.randint(0, 200)
    count = 0
    while count < 5:
        guess_number = int(input("guess num:"))
        if guess_number == number:
            print("bro, you are right.")
            return
        elif guess_number < number:
            print("too small")
        else:
            print("bigger")
        count += 1
    print("You failed! The number is:", number)
