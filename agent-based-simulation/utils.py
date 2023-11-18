from enum import Enum

class State(Enum):
    ACTIVE = 1
    ESCAPED = 2
    OBSTACLE = 3

Colors = {
    'STUDENT': "#2ca02c",
    'WALL': "#000000"
}

WIDTH = 250
HEIGHT = 120
PIXEL_RATIO = 4