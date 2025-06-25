# import time
import board
# from rainbowio import colorwheel
import neopixel

PIXEL_PIN = board.A1
PIXEL_COUNT = 24
PIXEL_BRIGHTNESS = 0.01
PIXEL_BYTES = 3
PIXEL_AUTO_WRITE = True
PIXEL_ORDER = neopixel.GRB

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pixels = neopixel.NeoPixel(PIXEL_PIN, PIXEL_COUNT, bpp=PIXEL_BYTES, brightness=PIXEL_BRIGHTNESS, auto_write=PIXEL_AUTO_WRITE, pixel_order=PIXEL_ORDER)

pixels.fill(GREEN)
pixels.show()

