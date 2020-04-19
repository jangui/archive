#!/usr/bin/env python3
import pyautogui as pygui

print("Press control-C to quit.")

try:
    while True:
        width, height = pygui.position()
        cords = "X: "+ str(width).rjust(4) + ", Y: " + str(height).rjust(4)
        print(cords, end='')
        print('\b' * len(cords), end='', flush=True)

except KeyboardInterrupt:
    print('\nDone.')
