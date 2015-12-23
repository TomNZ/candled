"""
Models a 2D candle flame.

Recreates part of the algorithm described here:
http://www.nik.no/2006/Gundersen2.pdf
"""

import random

WIDTH = 16
HEIGHT = 32

EDGE = 0

TOTAL_WIDTH = WIDTH + 2 * EDGE
TOTAL_HEIGHT = HEIGHT + 2 * EDGE

CENTER_X = TOTAL_WIDTH / 2

FUEL_SOURCE_MIN = 20.0
FUEL_SOURCE_MAX = 25.0
TEMP_SOURCE = 0.1
FUEL_BURN_RATE = 0.2
FUEL_EXHAUST_RATIO = 1.5
TEMP_RATIO = 10.0


GRAVITY = 0.1
FUEL_MASS = 0.5
EXHAUST_MASS = 1.0

BUOYANCY = 0.1

THRESH_TEMP = 0.8

EXPANSION_AMT = 0.1

FUEL_DISSIPATION = 0.05
EXHAUST_DISSIPATION = 0.1
TEMP_DISSIPATION = 0.2

FUEL_DIFFUSE_RATE = 0.2
EXHAUST_DIFFUSE_RATE = 0.1
TEMP_DIFFUSE_RATE = 0.3


class Velocity(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return '<Vector: %s, %s>' % (self.x, self.y)

class CandLED(object):
    def __init__(self):
        self.fuel_field = self._get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT, default=lambda: 1.0)
        self.temp_field = self._get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT, default=lambda: 1.6)
        self.exhaust_field = self._get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT)
        self.vel_field = self._get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT, default=lambda: Velocity())

    @staticmethod
    def _get_matrix(width, height, default=None):
        if not default:
            default = lambda: 0.0
        return [[default() for _ in range(height)] for _ in range(width)]

    @staticmethod
    def _diffuse(time, field, rate):
        new_field = CandLED._get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT)

        for x in range(TOTAL_WIDTH):
            for y in range(TOTAL_HEIGHT):
                new_val = field[x][y] * (1 - rate * 4)
                new_val += field[max(0, x-1)][y] * rate
                new_val += field[min(TOTAL_WIDTH-1, x+1)][y] * rate
                new_val += field[x][max(0, y)] * rate
                new_val += field[x][min(TOTAL_HEIGHT-1, y+1)] * rate
                new_field[x][y] = new_val

        return new_field

    def _advect(self, time, field):
        new_field = CandLED._get_matrix(TOTAL_WIDTH, TOTAL_HEIGHT)

        for x in range(TOTAL_WIDTH):
            for y in range(TOTAL_HEIGHT):
                curr_amt = field[x][y]
                vel = self.vel_field[x][y]
                target_x = x + vel.x
                target_y = y + vel.y
                for new_x in [int(target_x), int(target_x) + 1]:
                    for new_y in [int(target_y), int(target_y) + 1]:
                        if new_x >= 0 and new_x < TOTAL_WIDTH and new_y >= 0 and new_y < TOTAL_HEIGHT:
                            x_ratio = 1.0 - abs(target_x - new_x)
                            y_ratio = 1.0 - abs(target_y - new_y)
                            new_field[new_x][new_y] += x_ratio * y_ratio * curr_amt

        return new_field

    def tick_frame(self, time):
        for x in range(TOTAL_WIDTH):
            for y in range(TOTAL_HEIGHT):
                fuel_amt = self.fuel_field[x][y]
                exhaust_amt = self.exhaust_field[x][y]
                temp_amt = self.temp_field[x][y]

                gravity = GRAVITY * (fuel_amt * FUEL_MASS + exhaust_amt * EXHAUST_MASS)
                buoyancy = temp_amt * BUOYANCY

                expansion = 0
                if temp_amt > THRESH_TEMP:
                    expansion = (x - CENTER_X) * EXPANSION_AMT

                self.vel_field[x][y].x = float(expansion)
                self.vel_field[x][y].y = float(gravity - buoyancy)

                # Combustion
                fuel_comb = exhaust_comb = temp_comb = 0
                if temp_amt > THRESH_TEMP:
                    combustion = FUEL_BURN_RATE * fuel_amt
                    fuel_comb = -combustion
                    exhaust_comb = combustion * FUEL_EXHAUST_RATIO + combustion
                    temp_comb = combustion * FUEL_EXHAUST_RATIO * TEMP_RATIO

                # Sources
                fuel_source = random.uniform(FUEL_SOURCE_MIN, FUEL_SOURCE_MAX)\
                    if x == CENTER_X and y == TOTAL_HEIGHT - EDGE - 1 else 0
                temp_source = TEMP_SOURCE

                # Update densities
                self.fuel_field[x][y] = fuel_amt - FUEL_DISSIPATION * fuel_amt + fuel_source + fuel_comb
                self.exhaust_field[x][y] = exhaust_amt - EXHAUST_DISSIPATION * exhaust_amt + exhaust_comb
                self.temp_field[x][y] = temp_amt - TEMP_DISSIPATION * temp_amt + temp_source + temp_comb

        # Advect
        self.fuel_field = self._advect(time, self.fuel_field)
        self.exhaust_field = self._advect(time, self.exhaust_field)
        self.temp_field = self._advect(time, self.temp_field)

        # Diffuse
        self.fuel_field = self._diffuse(time, self.fuel_field, FUEL_DIFFUSE_RATE)
        self.exhaust_field = self._diffuse(time, self.exhaust_field, EXHAUST_DIFFUSE_RATE)
        self.temp_field = self._diffuse(time, self.temp_field, TEMP_DIFFUSE_RATE)
