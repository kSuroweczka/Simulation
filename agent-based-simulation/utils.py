from enum import Enum

class State(Enum):
    ACTIVE = 1
    ESCAPED = 2
    OBSTACLE = 3
    EXIT = 4

Colors = {
    'STUDENT': "#2ca02c",
    'WALL': "#000000",
    'EXIT': "#d62728"
}

WIDTH = 250
HEIGHT = 120
PIXEL_RATIO = 4