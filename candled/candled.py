"""
Models a 2D candle flame.

Recreates part of the algorithm described here:
http://www.nik.no/2006/Gundersen2.pdf
"""

WIDTH = 8
HEIGHT = 16

EDGE = 2

TOTAL_WIDTH = WIDTH + 2 * EDGE
TOTAL_HEIGHT = HEIGHT + 2 * EDGE

CENTER_X = TOTAL_WIDTH / 2

FUEL_RATE = 1.0
FUEL_BURN_RATE = 0.3
FUEL_EXHAUST_RATIO = 0.5
TEMP_RATIO = 1.0
EXPANSION_RATIO = 0.1
THERMAL_VEL = 1.0

GRAVITY = 0.1
FUEL_MASS = 0.5
EXHAUST_MASS = 1.0

BUOYANCY = 2.0

THRESH_TEMP = 1.0

EXPANSION_AMT = 0.2

class Velocity(object):
    x = 0
    y = 0

def get_matrix(width, height, default=None):
    if not default:
        default = lambda: 0.0
    return [[default() for _ in range(height)] for _ in range(width)]


fuel_field = get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT)
temp_field = get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT)
exhaust_field = get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT)
vel_field = get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT, default=lambda: Velocity())


def tick_frame(time):
    for x in range(TOTAL_WIDTH):
        for y in range(TOTAL_HEIGHT):
            fuel_amt = fuel_field[x][y]
            exhaust_amt = exhaust_field[x][y]
            temp = temp_field[x][y]

            gravity = GRAVITY * (fuel_amt * FUEL_MASS + exhaust_amt * EXHAUST_MASS)
            buoyancy = temp * BUOYANCY

            expansion = 0
            if temp > THRESH_TEMP:
                expansion = abs(x - CENTER_X) * EXPANSION_AMT

            # Combustion

            # Dissipation
