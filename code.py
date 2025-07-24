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

try:
    import board
    import gc
    import traceback
    import time
    from ulab import numpy as np
    import busio
    import sys
    import neopixel
    import digitalio

    import adafruit_vl6180x
    from colors import *
    from effects import *
    from utils import *

except Exception as e:
    print(f"\n\n---- FATAL ERROR LOADING IMPORTS ---------------------")
    print("Exception occurred.", e)
    while True:
        pass # Halt program. Do nothing forever.


# CONSTANTS
PIXEL_PIN = board.A1
PIXEL_BRIGHTNESS = 1.0
PIXEL_BYTES = 3
PIXEL_AUTO_WRITE = False
PIXEL_ORDER = neopixel.GRB
PIXEL_COUNT = 250
HELIX_TURNS = 7.8
HELIX_HEIGHT = PIXEL_COUNT
SPARK_COUNT = 8
SPIRAL_DRIFT = 0.196

SENSOR_MAX_VAL = 180
SENSOR_MIN_VAL = 1
SENSOR_EXPONENT = 2

INTERACTION_TIMEOUT = 15
REQUIRED_STABLE_READINGS = 25
SENSOR_POLL_INTERVAL = 0.1

# INSTANTIATION
i2c = busio.I2C(board.SCL, board.SDA)
sensorX = adafruit_vl6180x.VL6180X(i2c)
sensorY = adafruit_vl6180x.VL6180X(i2c, 0x69)
pixels = neopixel.NeoPixel(PIXEL_PIN, PIXEL_COUNT, bpp=PIXEL_BYTES,
                           brightness=PIXEL_BRIGHTNESS, auto_write=PIXEL_AUTO_WRITE,
                           pixel_order=PIXEL_ORDER)

button1 = digitalio.DigitalInOut(board.D0)                      # define our pin
button1.direction = digitalio.Direction.INPUT                   # define that we're using it as an INPUT, not an OUTPUT
button1.pull = digitalio.Pull.DOWN                              # defalt the input to LOW (false)

gamma_table = [int((i / 255) ** 2.2 * 255 + 0.5) for i in range(256)]
pixels_np = np.array(pixels, dtype=np.int16)
fire_fade_by = np.array((-3, -3, -3), dtype=np.int16)

# FUNCTIONS

# TODO add SD card write to this routine
def handle_crash(e):
    crash_time = time.monotonic()
    print(f"\n\n---- FATAL ERROR AT TIME {crash_time} ----------------")
    print("Exception occurred.")
    try:
        traceback.print_exception(e)
    except Exception as te:
        print("Traceback/logging unavailable:", te)

    for i in range(PIXEL_COUNT):
        pixels[i] = CRASH_RED if i % 2 == 0 else CRASH_YELLOW
    pixels.show()
    while True:
        pass # Halt program. Do nothing forever.

def print_boot_stats():
    free = gc.mem_free()
    used = gc.mem_alloc()
    name = sys.implementation.name
    version = sys.implementation.version
    print(f"\n\n---- BOOT: START AT {boot_time} ---------------------")
    print(f"     - {name} version {version[0]}.{version[1]}.{version[2]}")
    print(f"     - Heap RAM Available: {free + used} bytes")
    print(f"     - Heap RAM Used:      {used} bytes")
    print(f"     - Heap RAM Remaining: {free} bytes\n")

def get_raw_sensor_x():
    return int(sensorX.range)

def get_raw_sensor_y():
    return int(sensorY.range)

def scale_sensor_value(raw_value, input_min, input_max):
    """(raw value, min input, max input) return int (0-255)"""
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
    return interaction_timeout_reached and inputs_stable

def grab_attention():
    lightning(pixels)
   
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

def go_blue():
    pixels.fill(MAX_BLUE)


# INITIALIZATION
boot_time = time.monotonic()
x = 0
y = 0
last_x = 0
last_y = 0
stable_count = 0
last_sensor_poll_time = 0.0

execution_min = float("inf")
execution_max = 0.0
execution_total = 0.0
execution_count = 0

gc.collect()
print_boot_stats()
gc.collect()
test_leds()
time.sleep(0.8)
flash_ok()
time.sleep(0.4)
print("---- INITIALIZATION COMPLETE --------------------")

# MAIN LOOP
# =========================================================================================================
try:                                                            # prepare to catch execution exception
    while True:                                
        read_button_1 = button1.value                           # get the current status of the button

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
        y_scaled = scale_sensor_value(y, SENSOR_MIN_VAL, SENSOR_MAX_VAL)

      
        x_final = int(((255 - x_scaled) ** 2 / (255 ** 2)) * 255) # invert and exponentially scale. Rework to reduce run-time floating-point math.
        y_final = y_scaled / 255 * 360

        color = hue_value_to_rgb(y_final, x_final)
   
        #color = rgb_fade(MAX_RED, x_final)                     # fade based on proximity
       
       
        if read_button_1:                                       # condition to follow if the button is pushed (e.g. read_button = True)
            pixels.fill(MAX_BLUE)
        else:                                                   # otherwise follow this   
            pixels.fill(color)  

        pixels.show()

        #pixels_np = fire(pixels_np, fire_fade_by, PIXEL_COUNT, SPIRAL_DRIFT, SPARK_COUNT)
        #pixels[:] = pixels_np.tolist()
        #pixels.show()

        execution_time = time.monotonic() - current_time

        

        # Track stats
        execution_total += execution_time
        execution_count += 1
        if execution_time < execution_min:
            execution_min = execution_time
        if execution_time > execution_max:
            execution_max = execution_time

        # Every 100 iterations, print stats
        if execution_count % 100 == 0:
            avg = execution_total / execution_count
            print(f" | ExecTime: min={execution_min:.4f}s | max={execution_max:.4f}s | avg={avg:.4f}s", end="")
       
   
except Exception as e:                                          # catch thrown exception
    handle_crash(e)                                             # handle and halt program
