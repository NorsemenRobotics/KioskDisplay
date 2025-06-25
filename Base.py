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

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

PINK = (255, 0, 222)
RED = (255, 0, 0)
ORANGE = (255, 50, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BROWN = (41.5, 22.5, 2.5)
OFF = (0, 0, 0)



while True:
    pixels.fill(RED)
    pixels.show()
    # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.show()
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.show()
    time.sleep(1)
    pixels.fill(OFF)
    pixels.show()
    time.sleep(1)

    color_chase(RED, 0.01)  # Increase the number to slow down the color chase
    color_chase(ORANGE, 0.01)
    color_chase(YELLOW, 0.01)
    color_chase(GREEN, 0.01)
    color_chase(CYAN, 0.01)
    color_chase(BLUE, 0.01)
    color_chase(PURPLE, 0.01)
    color_chase(WHITE, 0.01)
    color_chase(BROWN, 0.01)

    rainbow_cycle(0)  # Increase the number to slow down the rainbow
    while True:
        color_chase(RED, 0.005)  # Increase the number to slow down the color chase
        color_chase(ORANGE, 0.005)
        color_chase(YELLOW, 0.005)
        color_chase(GREEN, 0.005)
        color_chase(CYAN, 0.005)
        color_chase(BLUE, 0.005)
        color_chase(PURPLE, 0.005)
        color_chase(PINK, 0.005)
