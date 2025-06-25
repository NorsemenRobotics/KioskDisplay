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


def shooting_star(color, tail_length, speed_delay):
    for i in range(NUM_PIXELS + tail_length):
        leds.fill((0, 0, 0)) # Clear the strip

        # Draw the star
        if i < NUM_PIXELS:
            leds[i] = color

        # Draw the fading tail
        for j in range(1, tail_length + 1):
            if i - j >= 0:
                # Calculate faded color (example: linear fade)
                fade_factor = (tail_length - j) / tail_length
                faded_color = (int(color[0] * fade_factor),
                               int(color[1] * fade_factor),
                               int(color[2] * fade_factor))
                pixels[i - j] = faded_color

        leds.show()
        time.sleep(speed_delay)

# Example usage:
while True:
    shooting_star((255, 255, 0), 10, 0.05) # Yellow star, 10-pixel tail, 0.05s delay
    # Add other shooting star variations or animations here