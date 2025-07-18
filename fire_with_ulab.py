import board
import neopixel
import time
import rainbowio
#import fire_leds


# Set up NeoPixels
NUM_PIXELS = 256
PIXEL_PIN = board.A1
BRIGHTNESS = 0.05

import time, random
import board, neopixel
from ulab import numpy as np

num_leds = 256  # 256 even though we're only showing 64

leds = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.4, auto_write=False)

leds_np = np.array(leds, dtype=np.int16)  # numpy working copy of LED data

fade_by = np.array( (-3,-3,-3), dtype=np.int16 )  # amount to fade by

fire_color = 0xff6600

while True:
    # pick a new random set of LEDs to light up with fire
    c = fire_color
    c = (c>>16 & 0xff, c>>8 & 0xff, c & 0xff)  # turn into tuple
    for i in range(3):
        leds_np[ random.randint(0,num_leds-1) ] = c

    start_time = time.monotonic()

    # fade down all LEDs, using numpy,  takes 4 msec for 256 LEDs on RP2040
    leds_np += fade_by         # fade down the working numpy array
    leds_np = np.clip(leds_np, 0,255)  # constrain everyting to 0-255
    leds[:] = leds_np.tolist()  # copy working array to leds

    elapsed_time = time.monotonic() - start_time
    print(int(elapsed_time*1000))  # print out how long calculation took

    # update the strip
    leds.show()