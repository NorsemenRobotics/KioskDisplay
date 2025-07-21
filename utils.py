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

def hue_value_to_rgb(h, v):
    """
    Convert a hue angle (0–360) and value (0–255) to an RGB tuple (0–255).
    Saturation is fixed at 100%.
    """
    if not 0 <= h <= 360:
        raise ValueError("Hue must be in range 0–360")
    if not 0 <= v <= 255:
        raise ValueError("Value must be in range 0–255")

    h = h % 360
    s = 1.0
    v = v / 255.0  # Normalize value to 0.0–1.0

    h /= 60.0
    i = int(h)
    f = h - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))

    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q

    return (int(r * 255), int(g * 255), int(b * 255))