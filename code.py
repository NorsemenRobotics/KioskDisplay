# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2025 Jonathan Reid
# on behalf of FRC Team 3688 - Norsemen Robotics
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>. 


import board
import gc #garbage collector
import traceback
import time
import busio
import sys
import neopixel

import adafruit_vl6180x

# TODO remove DocStrings to save memory (""" comments at firstline of def)
# CONSTANTS
# ==========================================================================================================
PIXEL_PIN = board.A1
PIXEL_COUNT = 24
PIXEL_BRIGHTNESS = 1.0
PIXEL_BYTES = 3
PIXEL_AUTO_WRITE = False
PIXEL_ORDER = neopixel.GRB

SENSOR_MAX_VAL = 180 # sensor appears only to start returning data at ~180 mm or less
SENSOR_MIN_VAL = 1
SENSOR_EXPONENT = 2 # how much to raise sensor value to enhance low-end resolution

INTERACTION_TIMEOUT = 600.0
REQUIRED_STABLE_READINGS = 25

SENSOR_POLL_INTERVAL = 0.1 # how often to read ToF sensors (max 20 Hz)

MAX_RED = (255, 0, 0)
MAX_BLUE = (0, 0, 255)
MAX_GREEN = (0, 255, 0)
MAX_WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CRASH_RED = (106, 0, 0)
CRASH_YELLOW = (68, 68, 0)

# Color Schemes
BALLET = (0xF3EEDD, 0x02576B, 0xFFD9D1, 0x80506F)
BLUES = (0x113C78, 0xFFF6E6, 0xACA6BB, 0x95B4D3)
FIRESIDE = (0x83471D, 0xFFE2A5, 0xFF6714, 0xDA2734)
FRENCH = (0x4185BD, 0xFFC303, 0xFFF5D6, 0x13233E)
PINK = (0xFFF0D1, 0xFFD2D0, 0xFF4D88, 0xA61C62)
FLORIDA = (0xFFD704, 0xFF980B, 0xFFF0D9, 0x65B027)
HARBOR = (0x15518A, 0xFF1A2C, 0xD0BFC9, 0x0977B5)
BIRTHDAY = (0xFF5384, 0xFFE304, 0xFF9627, 0x16AEE0)
OLDSCHOOL = (0xA4A3A9, 0x602630, 0x72ACD9, 0x1A2C43)
DAFFODIL = (0xFFBEB, 0xFFE781, 0xD8D400, 0xFFD304)
BEACH = (0xFF6C80, 0x009EE7, 0xFF3E17, 0xA81D71)
CRUISE = (0x2AB2D1, 0x4B81CE, 0xFFEFC9, 0xC3C20B)
DAHLIA = (0x911234, 0xFF475B, 0xFF3F21, 0xFF5242)
WEEKEND = (0x025363, 0x636041, 0xFFB003, 0xF3E2AC)
FIRECRACKER = (0x007EDB, 0xFFF5E3, 0xD8C1A4, 0xFF2E16)
CORAL = (0xFFF6D8, 0xFF5E3F, 0x82E09F, 0xE5DF00)
COTTAGE = (0xFFF48F, 0x4E6729, 0xFFF1EA, 0xCACFE5)

PANTONE_485 = 0xDA291C
TEST_COLOR = 0xFF0000



# INSTANTIATION
# =========================================================================================================
i2c = busio.I2C(board.SCL, board.SDA)
sensorX = adafruit_vl6180x.VL6180X(i2c)
sensorY = adafruit_vl6180x.VL6180X(i2c,0x69)
pixels = neopixel.NeoPixel(PIXEL_PIN, PIXEL_COUNT, bpp=PIXEL_BYTES, brightness=PIXEL_BRIGHTNESS, auto_write=PIXEL_AUTO_WRITE, pixel_order=PIXEL_ORDER)
gamma_table = [int((i / 255) ** 2.2 * 255 + 0.5) for i in range(256)] # poplulate a pre-calculated table for gamma correction to avoid run-time floating-point math




# FUNCTIONS
# =========================================================================================================

def handle_crash(e):
    crash_time = time.monotonic()
    print(f"\n\n\n---- FATAL ERROR AT TIME {crash_time} ----------------")
    print("Unhandled exception occurred.")

    # Try printing and logging the traceback
    try:
        # Print to console
        traceback.print_exception(e)

        # TODO Also write to file to SD using storage.mount() once SD reader is received.
        #with open("/crash_log.txt", "a") as log:
        #    log.write(f"\n\n---- FATAL ERROR AT {crash_time} ----\n")
        #    log.write(f"Exception: {repr(e)}\n")
        #    traceback.print_exception(e, file=log)
    except Exception as te:
        print("Traceback/logging unavailable:", te)

    # Set crash colors
    for i in range(PIXEL_COUNT):
        if i % 2 == 0:
            pixels[i] = CRASH_RED
        else:
            pixels[i] = CRASH_YELLOW
    pixels.show()

    while True:
        pass  # Halt execution - Do nothing forever.

def print_boot_stats():
    free = gc.mem_free()
    used = gc.mem_alloc()
    name = sys.implementation.name
    version = sys.implementation.version   # returns tuple: major, minor, micro
    major = version[0]
    minor = version[1]
    micro = version[2]
    print(f"\n\n\n\n\n\n\n\n\n\n---- BOOT START AT {boot_time} ----------------------")
    print(f"     - {name} version ", end="")
    print(f"{major}.{minor}.{micro}")

    print(f"     - Heap RAM Available: ", free + used," bytes")
    print(f"     - Heap RAM Used:      ", used, " bytes")
    print(f"     - Heap RAM Remaining: ", free," bytes")
    print()
    return()

def get_raw_sensor_x():
    return int(sensorX.range)

def get_raw_sensor_y():
    return int(sensorY.range)

def hex_to_rgb(hex_color):
    if not (0x000000 <= hex_color <= 0xFFFFFF):
        raise ValueError("ERROR: Hex color must be a 24-bit integer between 0x000000 and 0xFFFFFF.")
    r = (hex_color >> 16) & 0xFF
    g = (hex_color >> 8) & 0xFF
    b = hex_color & 0xFF
    return (r, g, b)

def rgb_to_hex(rgb_tuple):
    r, g, b = rgb_tuple
    if any(not (0x00 <= val <= 0xFF) for val in (r, g, b)):
        raise ValueError("ERROR: Each RGB component must be between 0x00 and 0xFF.")
    return (r << 16) | (g << 8) | b

def hsv_to_rgb(h, s, v):
    """
    Convert HSV color to RGB.

    Parameters:
    h (float or int): Hue angle in degrees [0-360)
    s (float): Saturation [0-1]
    v (float): Value/Brightness [0-1]

    Returns:
    tuple: RGB color as (r, g, b), each 0-255
    """
    try:
        # Validate input ranges
        if not (0 <= s <= 1 and 0 <= v <= 1):
            raise ValueError("ERROR: Saturation and value must be between 0 and 1.")

        # Normalize hue to the range [0–360)
        h = h % 360

        # If saturation is zero, the color is grayscale
        if s == 0.0:
            val = int(v * 255)
            return (val, val, val)

        # Determine the hue sector (0–5)
        h_sector = int(h // 60)

        # Calculate fractional position within the sector
        f = (h / 60) - h_sector

        # Intermediate calculations for RGB conversion
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))

        # Map sector to RGB triplet
        rgb = {
            0: (v, t, p),
            1: (q, v, p),
            2: (p, v, t),
            3: (p, q, v),
            4: (t, p, v),
            5: (v, p, q),
        }[h_sector]

        # Scale RGB components to [0–255] and return as integers
        return tuple(int(c * 255) for c in rgb)

    except (TypeError, ValueError) as e:
        print("ERROR in hsv_to_rgb:", e)
        return (0, 0, 0)  # fallback to black if input is invalid
    
def rgb_to_hsv(r, g, b):
    """
    Convert RGB color to HSV.

    Parameters:
    r, g, b (int): Red, Green, Blue values [0-255]

    Returns:
    tuple: (h, s, v)
        h (float): Hue in degrees [0-360)
        s (float): Saturation [0-1]
        v (float): Value/Brightness [0-1]
    """
    try:
        # Validate RGB input range
        if any(not (0 <= val <= 255) for val in (r, g, b)):
            raise ValueError("ERROR: RGB values must be between 0 and 255.")

        # Normalize RGB values to the [0–1] range
        r /= 255
        g /= 255
        b /= 255

        # Determine max and min RGB values
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        delta = max_val - min_val

        # Value (V) is the maximum RGB component
        v = max_val

        # If delta is 0, the color is grayscale
        if delta == 0:
            h = 0
            s = 0
        else:
            # Saturation is the color intensity
            s = delta / max_val

            # Calculate hue based on which color is max
            if max_val == r:
                h = (g - b) / delta
            elif max_val == g:
                h = 2 + (b - r) / delta
            else:  # max_val == b
                h = 4 + (r - g) / delta

            # Convert hue to degrees
            h *= 60

            # Ensure hue is non-negative
            if h < 0:
                h += 360

        return (h, s, v)

    except (TypeError, ValueError) as e:
        print("ERROR in rgb_to_hsv:", e)
        return (0, 0, 0)  # fallback HSV if input is invalid

def rgb_fade(rgb_tuple, fade_factor):
    if not (0 <= fade_factor <= 1):
        raise ValueError("ERROR: fade_factor out of bounds.")
    r, g, b = rgb_tuple
    r = r * fade_factor
    g = g * fade_factor
    b = b * fade_factor
    return (int(r), int(g), int(b)) # return integers, not floats

def gamma_correct(rgb_tuple):
    r, g, b = rgb_tuple
    return (gamma_table[r], gamma_table[g], gamma_table[b])

def scale_sensor_value(raw_value, input_min, input_max):
    if input_max == input_min:
        return 0
    if raw_value < input_min:
        return 0
    if raw_value > input_max:
        return 255
    scaled = (raw_value - input_min) / (input_max - input_min)
    return int(scaled * 255)

def no_interaction(elapsed_seconds):
    global last_x, last_y, stable_count
    interaction_timeout_reached = (time.monotonic() - boot_time) > elapsed_seconds

    if x == last_x and y == last_y:
        stable_count += 1
    else:
        stable_count = 0

    last_x = x
    last_y = y
    inputs_stable = stable_count >= REQUIRED_STABLE_READINGS

    # TODO move print
    print(f" | Timeout: {interaction_timeout_reached} | Stable: {inputs_stable} ({stable_count})", end="")
    return interaction_timeout_reached and inputs_stable

def grab_attention():
    for i in range(3):
        pixels.fill(MAX_WHITE)
        pixels.show()
        time.sleep(0.1)
        pixels.fill(BLACK)
        pixels.show()
        time.sleep(0.1)

def test_leds():
    for color in [MAX_RED, MAX_GREEN, MAX_BLUE, MAX_WHITE]:
        pixels.fill(color)
        pixels.show()
        time.sleep(0.75)
    pixels.fill(BLACK)
    pixels.show()
    time.sleep(0.25)

def flash_ok():
    for _ in range(2):
        pixels.fill(MAX_GREEN)
        pixels.show()
        time.sleep(0.15)
        pixels.fill(BLACK)
        pixels.show()
        time.sleep(0.15)
    time.sleep(0.25)

def flash_not_ok():
    for _ in range(3):
        pixels.fill(MAX_RED)
        pixels.show()
        time.sleep(0.33)
        pixels.fill(BLACK)
        pixels.show()
        time.sleep(0.33)
    time.sleep(0.67)

# INITIALIZATION
# =========================================================================================================
boot_time = time.monotonic()
x = 0
y = 0
last_x = 0
last_y = 0
stable_count = 0 
last_sensor_poll_time = 0.0

# Perform garbage collection to free up any unreferenced objects
gc.collect()
print_boot_stats()
gc.collect()

test_leds()
time.sleep(0.8)
flash_ok()
time.sleep(0.4)

print(f"---- INITIALIZATION COMPLETE --------------------")
print()

# MAIN LOOP
# =========================================================================================================
try:                                                            # prepare to catch execution exception
    while True:
        # get current time
        current_time = time.monotonic()

        # get sensor data if enough time has passed
        if current_time - last_sensor_poll_time >= SENSOR_POLL_INTERVAL:
            x = get_raw_sensor_x()
            y = get_raw_sensor_y()
            last_sensor_poll_time = current_time

        # print sensor data to console. 
        # TODO remove this
        print(f"\rX:{x:3}mm | Y:{y:3}mm", end="")

        # do something to catch attention if there has been no interaction for a while
        if no_interaction(INTERACTION_TIMEOUT):
            grab_attention()
            boot_time = current_time

        #scale and clamp sensor readings
        x_scaled = scale_sensor_value(x, SENSOR_MIN_VAL, SENSOR_MAX_VAL)

        # invert sensor reading so closer = brighter
        x_inverted = 255 - x_scaled

        # scale x_inverted to float with range of 0.0-1.0
        x_final = x_inverted / 255
   
        color = rgb_fade(MAX_RED, x_final)                      # fade based on proximity
        pixels.fill(gamma_correct(color))                       # apply gamma correction to better present human-perceivable differences
        pixels.show()

except Exception as e:                                          # catch thrown exception
    handle_crash(e)                                             # handle and halt program
