#!/usr/bin/env python3
#loading_bar.py
import time
from random import randint

def loading_bar_random(speed=3):
    speed *= 10000
    dash =''
    try:
        for i in range(101):
            if i%2 == 0:
                dash  += '-'
            arrow = dash + '>'
            space = (52 - len(arrow)) * ' '
            bar = "[" + arrow + space + "]"
            message = "%LOADING% " + bar + str(i).rjust(4) + "%"
            print(message, end='')
            print('\b' * len(str(message)), end='', flush=True)
            delay = randint(1, speed) / 100000
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return False
    print("\nDone.")

def main():
    loading_bar_random()

if __name__ == "__main__":
    main()
