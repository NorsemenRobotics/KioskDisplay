# utils.py

gamma_table = [int((i / 255) ** 2.2 * 255 + 0.5) for i in range(256)] # poplulate a pre-calculated table for gamma correction to avoid run-time floating-point math

def hex_to_rgb(hex_color):
    r = (hex_color >> 16) & 0xFF
    g = (hex_color >> 8) & 0xFF
    b = hex_color & 0xFF
    return (r, g, b)

def rgb_fade(rgb_tuple, fade_factor):
    r, g, b = rgb_tuple
    return (int(r * fade_factor), int(g * fade_factor), int(b * fade_factor))

def gamma_correct(rgb_tuple):
    r, g, b = rgb_tuple
    return (gamma_table[r], gamma_table[g], gamma_table[b])