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
