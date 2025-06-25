# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials NeoPixel example"""
import time
import board
from rainbowio import colorwheel
import neopixel

pixel_pin = board.A1
num_pixels = 250

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False) # was 0.3


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


RED = (255, 0, 0)
ORANGE = (255, 50, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 100, 255)
PURPLE = (50, 0, 255)
BURGUNDY = (102, 0, 51)
PINK = (255, 0, 240)
WHITE = (255, 255, 255)
BROWN = (41.5, 22.5, 2.5)
OFF = (0, 0, 0)

CHANGE_SPEED = 0.005
#spiral speed. 0.005 is a good speed for change

while True:
    pixels.fill(RED)
    pixels.show()   # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(ORANGE)
    pixels.show()
    time.sleep(1)
    pixels.fill(YELLOW)
    pixels.show()
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.show()
    time.sleep(1)
    pixels.fill(CYAN)
    pixels.show()   # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.show()
    time.sleep(1)
    pixels.fill(PURPLE)
    pixels.show()
    time.sleep(1)
    pixels.fill(BURGUNDY)
    pixels.show()
    time.sleep(1)
    pixels.fill(PINK)
    pixels.show()   # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(WHITE)
    pixels.show()
    time.sleep(1)
    pixels.fill(BROWN)
    pixels.show()
    time.sleep(1)
    pixels.fill(OFF)
    pixels.show()
    time.sleep(1.5)

    color_chase(RED, CHANGE_SPEED)  # Increase the number to slow down the color chase
    color_chase(ORANGE, CHANGE_SPEED)
    color_chase(YELLOW, CHANGE_SPEED)
    color_chase(GREEN, CHANGE_SPEED)
    color_chase(CYAN, CHANGE_SPEED)
    color_chase(BLUE, CHANGE_SPEED)
    color_chase(PURPLE, CHANGE_SPEED)
    color_chase(BURGUNDY, CHANGE_SPEED)
    color_chase(PINK, CHANGE_SPEED)   
    color_chase(WHITE, CHANGE_SPEED)
    color_chase(BROWN, CHANGE_SPEED)

    rainbow_cycle(0.03)  # Increase the number to slow down the rainbow

    
    while True:
        color_chase(RED, CHANGE_SPEED)  # Increase the number to slow down the color chase
        color_chase(ORANGE, CHANGE_SPEED)
        color_chase(YELLOW, CHANGE_SPEED)
        color_chase(GREEN, CHANGE_SPEED)
        color_chase(CYAN, CHANGE_SPEED)
        color_chase(BLUE, CHANGE_SPEED)
        color_chase(PURPLE, CHANGE_SPEED)
        color_chase(BURGUNDY, CHANGE_SPEED)
        color_chase(PINK, CHANGE_SPEED)   
