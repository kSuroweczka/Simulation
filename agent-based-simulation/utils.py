from enum import Enum

class State(Enum):
    ACTIVE = 1
    ESCAPED = 2
    OBSTACLE = 3
    EXIT = 4

Colors = {
    'STUDENT': "#000080",
    'WALL': "#000000",
    'EXIT': "#d62728",
    'BENCH': "#7d420e",
    'TREE': "#108722", 
}

WIDTH = 250
HEIGHT = 120
PIXEL_RATIO = 4
