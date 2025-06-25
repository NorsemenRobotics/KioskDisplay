import board
import time

# from rainbowio import colorwheel
import neopixel

import board
import busio
import adafruit_vl6180x
#import adafruit_vl6180x_0x69

import gc #garbage collector

# CONSTANTS
# ==========================================================================================================
PIXEL_PIN = board.A1
PIXEL_COUNT = 250
PIXEL_BRIGHTNESS = 1.0
PIXEL_BYTES = 3
PIXEL_AUTO_WRITE = False
PIXEL_ORDER = neopixel.GRB

SENSOR_MAX_VAL = 180 # sensor appears only to start returning data at ~180 mm or less
SENSOR_MIN_VAL = 1

INTERACTION_TIMEOUT = 600.0
REQUIRED_STABLE_READINGS = 25

MAX_RED = (255, 0, 0)
MAX_BLUE = (0, 0, 255)
MAX_GREEN = (0, 255, 0)
MAX_WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CRASH_RED = (106, 0, 0)
CRASH_YELLOW = (68, 68, 0)

PANTONE_485 = 0xDA291C
TEST_COLOR = 0xFF0000



# INSTANTIATION
# =========================================================================================================
i2c = busio.I2C(board.SCL, board.SDA)
sensorX = adafruit_vl6180x.VL6180X(i2c)
sensorY = adafruit_vl6180x.VL6180X(i2c,0x69)
pixels = neopixel.NeoPixel(PIXEL_PIN, PIXEL_COUNT, bpp=PIXEL_BYTES, brightness=PIXEL_BRIGHTNESS, auto_write=PIXEL_AUTO_WRITE, pixel_order=PIXEL_ORDER)

#watchDog = microcontroller.watchdog

# STATE VARIABLES FOR NO_INTERACTION BUFFERING
stable_count = 0

# FUNCTIONS
# =========================================================================================================

def handle_crash(e):
    print("Unhandled exception occurred:", e)
    for i in range(PIXEL_COUNT):
        if i % 2 == 0:
            pixels[i] = CRASH_RED
        else:
            pixels[i] = CRASH_YELLOW
    pixels.show()
    while True:
        pass

def get_raw_sensor_x():
    return int(sensorX.range)

def get_raw_sensor_y():
    return int(sensorY.range)

def hex_to_rgb(hex_color):
    if not (0x000000 <= hex_color <= 0xFFFFFF):
        raise ValueError("Hex color must be a 24-bit integer between 0x000000 and 0xFFFFFF.")
    r = (hex_color >> 16) & 0xFF
    g = (hex_color >> 8) & 0xFF
    b = hex_color & 0xFF
    return (r, g, b)

def rgb_to_hex(rgb_tuple):
    r, g, b = rgb_tuple
    if any(not (0x00 <= val <= 0xFF) for val in (r, g, b)):
        raise ValueError("Each RGB component must be between 0x00 and 0xFF.")
    return (r << 16) | (g << 8) | b

def rgb_fade(rgb_tuple, fade_factor):
    if not (0 <= fade_factor <= 1):
        raise ValueError("fade_factor out of bounds")
    r, g, b = rgb_tuple
    r = r * fade_factor
    g = g * fade_factor
    b = b * fade_factor
    return (r, g, b)

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
    interaction_timeout_reached = (time.monotonic() - start_time) > elapsed_seconds

    if x == last_x and y == last_y:
        stable_count += 1
    else:
        stable_count = 0

    last_x = x
    last_y = y

    inputs_stable = stable_count >= REQUIRED_STABLE_READINGS
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

def ok():
    for _ in range(2):
        pixels.fill(MAX_GREEN)
        pixels.show()
        time.sleep(0.15)
        pixels.fill(BLACK)
        pixels.show()
        time.sleep(0.15)
    time.sleep(0.25)

def not_ok():
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
start_time = time.monotonic()
x = 0
y = 0
last_x = 0
last_y = 0

# Perform garbage collection to free up any unreferenced objects
gc.collect()

# Get the amount of free memory in bytes
free_memory_bytes = gc.mem_free()

print("\n\n\n\n\n\n\n\n\n\n**** BOOT")
print(f"Free memory: {free_memory_bytes} bytes")

test_leds()
time.sleep(1.25)
ok()
time.sleep(0.67)

# MAIN LOOP
# =========================================================================================================
try:
    while True:
        x = get_raw_sensor_x()
        y = get_raw_sensor_y()
        current_time = time.monotonic()

        print(f"\rX:{x:3}mm | Y:{y:3}mm", end="")

        if no_interaction(INTERACTION_TIMEOUT):
            grab_attention()
            start_time = time.monotonic()

        x_inverted = 255 - x
        x_scaled = scale_sensor_value(x_inverted,SENSOR_MIN_VAL,SENSOR_MAX_VAL) / 255
        x_filtered = x_scaled ** 2

        pixels.fill(rgb_fade(MAX_RED,x_filtered))
        pixels.show()

except Exception as e:
    handle_crash(e)
