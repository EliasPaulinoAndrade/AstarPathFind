from enum import Enum

class Direction(Enum):
    TOP = (0, 1)
    BOTTOM = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
