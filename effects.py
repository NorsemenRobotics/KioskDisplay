# fire.py

import time
import math
import random
from ulab import numpy as np
from colors import FIRE
from utils import hex_to_rgb, rgb_fade

def fire(pixels_np, fade_by, pixel_count, spiral_drift, spark_count):
    base_color = hex_to_rgb(FIRE)

    # Create new sparks at the bottom (highest index)
    for _ in range(spark_count):
        r = random.random()
        index = pixel_count - 1 - int((1.0 - r**2) * (pixel_count // 8))
        flicker = tuple(max(0, min(255, val + random.randint(-40, 40))) for val in base_color)
        pixels_np[index] = flicker

    # Fade all pixels
    pixels_np += fade_by

    # Cooling gradient + spiral twist
    for i in range(pixel_count):
        inv_i = pixel_count - 1 - i
        vertical_cool = 1.0 - (inv_i / pixel_count) * 0.5
        angle = inv_i * spiral_drift
        twinkle = 0.9 + 0.1 * math.sin(angle + time.monotonic() * 2)
        cooling_factor = max(0.0, min(1.0, vertical_cool * twinkle))
        pixels_np[i] = np.array(rgb_fade(pixels_np[i], cooling_factor), dtype=np.int16)

    return np.clip(pixels_np, 0, 255)

def random_stroke_count():
    """
    Return a stroke count (3–12), biased toward lower numbers.
    Compatible with CircuitPython (no random.choices()).
    """
    choices = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    weights = [10, 9, 8, 6, 5, 4, 3, 2, 1, 1]

    # Create a cumulative list of choices repeated by weight
    weighted_list = []
    for value, weight in zip(choices, weights):
        weighted_list.extend([value] * weight)

    return random.choice(weighted_list)

def random_lightning_color(brightness=255):
    """
    Return a bluish-white color with random variation.
    Blue: high, Red/Green: moderately high.
    """
    r = random.randint(int(0.7 * brightness), brightness)
    g = random.randint(int(0.7 * brightness), brightness)
    b = random.randint(int(0.9 * brightness), brightness)
    return (r, g, b)

def random_delay_leader():
    """
    Return a short delay (in seconds) for leader steps,
    simulating a fast stepped leader descent.
    """
    return random.uniform(0.001, 0.004)  # 1 to 4 milliseconds

def random_delay_flash():
    """
    Return a pseudo-Gaussian flash duration (seconds),
    simulated using the average of 3 uniform samples.
    Typical result: 0.02 to 0.10 seconds, biased toward 0.05.
    """
    # Average of 3 samples gives a pseudo-bell-curve
    delay = sum(random.uniform(0.02, 0.08) for _ in range(3)) / 3
    return delay

def lightning(pixels):
    """
    Simulate a lightning flash sequence.
    
    Parameters:
    - pixels: NeoPixel object (1-based index, top to bottom)
    - stroke_count: number of main flashes
    - delay_leader: delay between pixels during leader sweep
    - delay_flash: duration of main flashes
    """
    num_pixels = len(pixels)
    stroke_count = random_stroke_count()
    delay_leader = random_delay_leader()
    delay_flash = random_delay_flash()

    # 1. Leader phase: sweep top to bottom
    for i in range(num_pixels):
        pixels[i] = random_lightning_color(brightness=80)  # Dim leader
        pixels.show()
        #time.sleep(delay_leader)
        # TODO make stroke go faster; use 5 pixels at once

    time.sleep(0.02)

    # 2. Main stroke flashes
    for _ in range(stroke_count):
        # Flash all pixels with full-bright bluish-white
        color = random_lightning_color(brightness=255)
        for i in range(num_pixels):
            pixels[i] = color
        pixels.show()
        time.sleep(delay_flash)

        # Go dark briefly
        for i in range(num_pixels):
            pixels[i] = (0, 0, 0)
        pixels.show()
        time.sleep(random.uniform(0.02, 0.07))  # Random flicker delay
